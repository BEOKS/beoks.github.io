import mysql.connector
import time
import random
import string

# 0. MySQL 접속 정보
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': ''  # 패스워드 공백
}
DB_NAME = 'test_rollup_db'  # 기존 데이터베이스 재활용 또는 새 이름 지정
TABLE_NAME_NO_INDEX = 'insert_test_no_index'
TABLE_NAME_WITH_INDEX = 'insert_test_with_index'

NUM_ROWS_FOR_INSERT_TEST = 3000000  # 삽입 테스트용 데이터 수 (조절 가능)
BATCH_SIZE = 10000                 # 한 번에 삽입할 데이터 수

INDEX_COLUMNS = ['cat1', 'cat2', 'cat3', 'cat4', 'cat5', 'cat6']
INDEX_NAME = 'idx_perf_test_cats'

def get_connection(config, db_name=None):
    """MySQL 연결 반환"""
    if db_name:
        config['database'] = db_name
    return mysql.connector.connect(**config)

def generate_fake_data_for_insert(num_rows):
    """삽입 테스트용 페이크 데이터 생성 (메모리에 미리 생성)"""
    data_batch = []
    cat_options_list = [
        [f'C1_{i}' for i in range(5)],
        [f'C2_{i}' for i in range(10)],
        [f'C3_{i}' for i in range(20)],
        [f'C4_{i}' for i in range(25)],
        [f'C5_{i}' for i in range(30)],
        [f'C6_{i}' for i in range(40)]
    ]
    for _ in range(num_rows):
        row = (
            random.choice(cat_options_list[0]),
            random.choice(cat_options_list[1]),
            random.choice(cat_options_list[2]),
            random.choice(cat_options_list[3]),
            random.choice(cat_options_list[4]),
            random.choice(cat_options_list[5]),
            random.randint(1, 1000)  # 수치 데이터
        )
        data_batch.append(row)
    return data_batch

def create_table_generic(cursor, table_name, include_index=False):
    """테이블 생성 (인덱스 포함/미포함 옵션)"""
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    ddl = f"""
    CREATE TABLE {table_name} (
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
    cursor.execute(ddl)
    # print(f"테이블 '{table_name}'이(가) 생성되었습니다.")

    if include_index:
        index_cols_str = ", ".join(INDEX_COLUMNS)
        sql_create_index = f"CREATE INDEX {INDEX_NAME} ON {table_name} ({index_cols_str});"
        cursor.execute(sql_create_index)
        # print(f"테이블 '{table_name}'에 인덱스 '{INDEX_NAME}'이(가) 적용되었습니다.")


def measure_insert_time(table_name, data_to_insert, has_index=False):
    """데이터 삽입 시간 측정"""
    print(f"\n--- '{table_name}' 테이블에 데이터 삽입 테스트 (인덱스: {'있음' if has_index else '없음'}) ---")

    cnx_db = None
    try:
        cnx_db = get_connection(DB_CONFIG, DB_NAME)
        cursor = cnx_db.cursor()

        # 테이블 생성
        create_table_generic(cursor, table_name, include_index=has_index)
        cnx_db.commit() # DDL 후 커밋

        total_inserted_rows = 0
        insert_start_time = time.time()

        for i in range(0, len(data_to_insert), BATCH_SIZE):
            batch = data_to_insert[i:i + BATCH_SIZE]
            if not batch:
                continue

            sql = f"""INSERT INTO {table_name}
                      (cat1, cat2, cat3, cat4, cat5, cat6, value_col)
                      VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            cursor.executemany(sql, batch)
            cnx_db.commit() # 각 배치 후 커밋
            total_inserted_rows += len(batch)
            # print(f"{total_inserted_rows} / {len(data_to_insert)} 행 삽입됨...")

        insert_end_time = time.time()
        execution_time = insert_end_time - insert_start_time
        print(f"총 {total_inserted_rows}개 데이터 삽입 완료. 소요 시간: {execution_time:.4f}초")
        return execution_time

    except mysql.connector.Error as err:
        print(f"오류 발생: {err}")
        if cnx_db and cnx_db.is_connected():
             # 롤백은 DML에 주로 사용되지만, 에러 핸들링의 일부로 추가
            cnx_db.rollback()
        return float('inf') # 오류 시 매우 큰 값 반환
    finally:
        if cnx_db and cnx_db.is_connected():
            cursor.close()
            cnx_db.close()


def main():
    # 데이터베이스 생성 (없으면)
    try:
        cnx_server = get_connection(DB_CONFIG)
        cursor_server = cnx_server.cursor()
        cursor_server.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"데이터베이스 '{DB_NAME}'이(가) 준비되었습니다.")
        cursor_server.close()
        cnx_server.close()
    except mysql.connector.Error as err:
        print(f"데이터베이스 준비 중 오류: {err}")
        exit(1)

    # 테스트용 데이터 미리 생성 (동일한 데이터로 비교하기 위함)
    print(f"{NUM_ROWS_FOR_INSERT_TEST}개의 테스트 데이터 생성 중...")
    all_data = generate_fake_data_for_insert(NUM_ROWS_FOR_INSERT_TEST)
    print("테스트 데이터 생성 완료.")

    # 1. 인덱스 없이 삽입 시간 측정
    time_no_index = measure_insert_time(TABLE_NAME_NO_INDEX, all_data, has_index=False)

    # 2. 인덱스 적용 후 삽입 시간 측정
    time_with_index = measure_insert_time(TABLE_NAME_WITH_INDEX, all_data, has_index=True)

    # 3. 결과 비교
    print("\n\n--- 최종 삽입 시간 비교 ---")
    if time_no_index == float('inf') or time_with_index == float('inf'):
        print("오류로 인해 일부 테스트가 완료되지 않아 비교할 수 없습니다.")
        return

    print(f"인덱스 없을 시 삽입 시간  : {time_no_index:.4f}초")
    print(f"인덱스 있을 시 삽입 시간  : {time_with_index:.4f}초")

    if time_no_index > 0: # 0으로 나누기 방지
        difference = time_with_index - time_no_index
        percentage_increase = (difference / time_no_index) * 100
        print(f"인덱스로 인한 삽입 시간 증가: {difference:.4f}초")
        print(f"인덱스로 인한 삽입 시간 증가율: {percentage_increase:.2f}%")
        if percentage_increase > 0:
            print(f"예상대로, 인덱스가 있을 때 삽입 시간이 약 {percentage_increase:.2f}% 더 오래 걸렸습니다.")
        elif percentage_increase < 0:
            print(f"예상과 달리, 인덱스가 있을 때 삽입 시간이 약 {-percentage_increase:.2f}% 더 빨랐습니다. (시스템 환경 또는 매우 특수한 경우)")
        else:
            print("인덱스 유무에 따른 삽입 시간 차이가 거의 없습니다.")
    else:
        print("인덱스 없는 경우의 삽입 시간이 0으로 측정되어 비율을 계산할 수 없습니다.")

if __name__ == "__main__":
    main()