import mysql.connector
import time
import random
import string

# 0. MySQL 접속 정보
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '' # 패스워드 공백
}
DB_NAME = 'test_rollup_db4'
TABLE_NAME = 'hierarchical_data4'
NUM_ROWS = 3000000 # 데이터 수 변경 가능 (테스트 시에는 더 적은 수로 시작하는 것을 권장)
BATCH_SIZE = 50000 # 한 번에 삽입할 데이터 수

def generate_random_string(length=5):
    """지정된 길이의 무작위 문자열 생성"""
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(length))

def get_connection(config, db_name=None):
    """MySQL 연결 반환"""
    if db_name:
        config['database'] = db_name
    return mysql.connector.connect(**config)

def create_database_and_table():
    """데이터베이스와 테이블 생성"""
    try:
        # 데이터베이스 생성 (없으면)
        cnx_server = get_connection(DB_CONFIG)
        cursor_server = cnx_server.cursor()
        cursor_server.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"데이터베이스 '{DB_NAME}'이(가) 준비되었습니다.")
        cursor_server.close()
        cnx_server.close()

        # 테이블 생성
        cnx_db = get_connection(DB_CONFIG, DB_NAME)
        cursor_db = cnx_db.cursor()

        cursor_db.execute(f"DROP TABLE IF EXISTS {TABLE_NAME}")
        ddl = f"""
        CREATE TABLE {TABLE_NAME} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            cat1 VARCHAR(10),
            cat2 VARCHAR(10),
            cat3 VARCHAR(10),
            cat4 VARCHAR(10),
            cat5 VARCHAR(10),
            cat6 VARCHAR(10),
            value_col INT
        ) ENGINE=InnoDB;
        """
        cursor_db.execute(ddl)
        print(f"테이블 '{TABLE_NAME}'이(가) 생성되었습니다.")
        cnx_db.commit()
        cursor_db.close()
        cnx_db.close()
    except mysql.connector.Error as err:
        print(f"데이터베이스/테이블 생성 중 오류 발생: {err}")
        exit(1)

def insert_fake_data():
    """페이크 데이터 삽입"""
    print(f"{NUM_ROWS}개의 페이크 데이터 삽입을 시작합니다 (배치 크기: {BATCH_SIZE})...")
    cnx_db = get_connection(DB_CONFIG, DB_NAME)
    cursor_db = cnx_db.cursor()

    # 계층형 데이터의 카테고리 풀 정의 (다양성 조절)
    # 각 계층별로 값의 가짓수를 다르게 하여 계층 구조의 의미를 부여
    cat1_options = [f'C1_{i}' for i in range(6)]          # 5개
    cat2_options = [f'C2_{i}' for i in range(12)]         # 10개
    cat3_options = [f'C3_{i}' for i in range(18)]         # 20개
    cat4_options = [f'C4_{i}' for i in range(24)]         # 25개
    cat5_options = [f'C5_{i}' for i in range(30)]         # 30개
    cat6_options = [f'C6_{i}' for i in range(36)]         # 40개

    data_to_insert = []
    start_total_time = time.time()
    for i in range(NUM_ROWS):
        row = (
            random.choice(cat1_options),
            random.choice(cat2_options),
            random.choice(cat3_options),
            random.choice(cat4_options),
            random.choice(cat5_options),
            random.choice(cat6_options),
            random.randint(1, 1000) # 수치 데이터
        )
        data_to_insert.append(row)

        if (i + 1) % BATCH_SIZE == 0 or (i + 1) == NUM_ROWS:
            sql = f"INSERT INTO {TABLE_NAME} (cat1, cat2, cat3, cat4, cat5, cat6, value_col) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor_db.executemany(sql, data_to_insert)
            cnx_db.commit()
            data_to_insert = []
            print(f"{(i + 1)}개의 데이터 삽입 완료...")

    end_total_time = time.time()
    print(f"총 {NUM_ROWS}개 데이터 삽입 완료. 소요 시간: {end_total_time - start_total_time:.2f}초")
    cursor_db.close()
    cnx_db.close()

def run_query_and_measure_time(query_description, index_applied=False):
    """쿼리 실행 및 시간 측정"""
    print(f"\n--- {query_description} (인덱스 {'적용됨' if index_applied else '미적용'}) ---")
    cnx_db = get_connection(DB_CONFIG, DB_NAME)
    cursor_db = cnx_db.cursor()

    query = f"""
    SELECT cat1, cat2, cat3, cat4, cat5, cat6, SUM(value_col)
    FROM {TABLE_NAME}
    GROUP BY cat1, cat2, cat3, cat4, cat5, cat6 WITH ROLLUP;
    """

    # 실제 쿼리 실행 전 캐시 등의 영향 최소화를 위해 한 번 더 실행 (선택 사항)
    # cursor_db.execute(query)
    # results = cursor_db.fetchall() # 결과를 가져와야 실제 실행 완료

    start_time = time.time()
    cursor_db.execute(query)
    results = cursor_db.fetchall() # 결과를 모두 가져와야 정확한 시간 측정이 가능
    end_time = time.time()

    execution_time = end_time - start_time
    print(f"쿼리 실행 시간: {execution_time:.4f}초")
    print(f"결과 행 수 (ROLLUP 포함): {len(results)}")
    # print("샘플 결과 (첫 5행):")
    # for row in results[:5]:
    #     print(row)

    cursor_db.close()
    cnx_db.close()
    return execution_time

def apply_index():
    """계층형 컬럼에 인덱스 적용"""
    print("\n--- 인덱스 적용 시작 ---")
    cnx_db = get_connection(DB_CONFIG, DB_NAME)
    cursor_db = cnx_db.cursor()

    index_name = "idx_hierarchical_cats"
    # 기존 인덱스가 있다면 삭제 (선택 사항, 중복 생성 방지)
    try:
        cursor_db.execute(f"DROP INDEX {index_name} ON {TABLE_NAME}")
        print(f"기존 인덱스 '{index_name}' 삭제 완료.")
    except mysql.connector.Error as err:
        if err.errno == 1091: # Can't DROP '...'; check that column/key exists
             print(f"인덱스 '{index_name}'가 존재하지 않아 삭제를 건너뜁니다.")
        else:
            print(f"기존 인덱스 삭제 중 오류: {err}")


    sql_create_index = f"""
    CREATE INDEX {index_name}
    ON {TABLE_NAME} (cat1, cat2, cat3, cat4, cat5, cat6, value_col);
    """
    start_time = time.time()
    cursor_db.execute(sql_create_index)
    cnx_db.commit() # CREATE INDEX는 DDL이지만, 명시적 커밋
    end_time = time.time()
    print(f"인덱스 '{index_name}' 적용 완료. 소요 시간: {end_time - start_time:.2f}초")

    cursor_db.close()
    cnx_db.close()

def main():
    # 0. 데이터베이스 및 테이블 생성
    create_database_and_table()

    # 1. 페이크 데이터 삽입
    # 주의: NUM_ROWS가 크면 이 단계에서 매우 긴 시간이 소요될 수 있습니다.
    # 테스트 시에는 NUM_ROWS를 10만개 정도로 줄여서 빠르게 확인해보세요.
    insert_fake_data()

    # 2. 인덱스 없이 쿼리 실행 및 시간 측정
    time_without_index = run_query_and_measure_time("ROLLUP 쿼리", index_applied=False)

    # 3. 인덱스 적용
    apply_index()

    # 4. 인덱스 적용 후 쿼리 실행 및 시간 측정
    time_with_index = run_query_and_measure_time("ROLLUP 쿼리", index_applied=True)

    # 5. 결과 비교
    print("\n--- 최종 결과 비교 ---")
    print(f"인덱스 미적용 시 실행 시간: {time_without_index:.4f}초")
    print(f"인덱스 적용 시 실행 시간: {time_with_index:.4f}초")

    if time_without_index > 0 and time_with_index > 0:
        improvement = time_without_index - time_with_index
        percentage_improvement = (improvement / time_without_index) * 100
        print(f"성능 개선 시간: {improvement:.4f}초")
        print(f"성능 개선율: {percentage_improvement:.2f}%")
        if percentage_improvement > 0:
            print(f"인덱스 적용으로 인해 쿼리 실행 속도가 약 {percentage_improvement:.2f}% 빨라졌습니다. 🎉")
        elif percentage_improvement < 0:
            print(f"인덱스 적용 후 쿼리 실행 속도가 약 {-percentage_improvement:.2f}% 느려졌습니다. ⚠️ (데이터 분포나 MySQL 옵티마이저 결정에 따라 발생 가능)")
        else:
            print("인덱스 적용 전후 성능 차이가 거의 없습니다.")
    else:
        print("실행 시간 측정에 오류가 있어 성능 비교를 할 수 없습니다.")

if __name__ == "__main__":
    main()