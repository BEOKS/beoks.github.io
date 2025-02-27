### 개요
오라클 데이터베이스의 기본 요소 중에는 [[Oracle Comment | Comment]] 가 있으며, 그 중에는 오라클 데이터베이스 옵티마이저에 별도의 지시를 추가할 수 있는 [[Oracle Hints|Hint]] 기능이 있습니다. 이 힌트 중 `IGNORE_ROW_ON_DUPKEY_INDEX`는 INSERT 쿼리 실행시 인텍스 충돌이 발생하면 로우 레벨 롤백이 발생해 쿼리를 발생시키지 않고 다음 쿼리를 수행합니다.

---

### 사용법

```sql
INSERT /*+ IGNORE_ROW_ON_DUPKEY_INDEX (테이블_이름 인덱스_이름) */
INTO 테이블_이름 (컬럼1, 컬럼2, ...)
VALUES (값1, 값2, ...);
```

```sql
INSERT /*+ IGNORE_ROW_ON_DUPKEY_INDEX (테이블_이름 (컬럼1,컬럼2,...)) */
INTO 테이블_이름 (컬럼1, 컬럼2, ...)
VALUES (값1, 값2, ...);
```

**예시:**

```sql
INSERT /*+ IGNORE_ROW_ON_DUPKEY_INDEX (employees emp_unique_idx) */
INTO employees (employee_id, first_name, last_name)
VALUES (101, 'John', 'Doe');
```


```sql
INSERT /*+ IGNORE_ROW_ON_DUPKEY_INDEX (employees (employee_id, first_name)) */
INTO employees (employee_id, first_name, last_name)
VALUES (101, 'John', 'Doe');
```
위의 예시에서 `emp_unique_idx`는 `employees` 테이블의 고유 인덱스입니다. 만약 `employee_id`가 이미 존재하여 고유 제약 조건에 위배되면 해당 레코드는 무시되고 다음 레코드 처리를 계속합니다.

**주의사항:**
- 딱 하나의 인덱스만 명시할 수 있습니다. 
- 힌트에는 대상 테이블과 해당 테이블의 고유 인덱스 또는 제약 조건 이름을 지정해야 합니다.
- 이 힌트는 중복 키로 인한 오류만 무시하며, 다른 유형의 오류는 여전히 발생합니다.
- 대량의 데이터를 처리하는 경우에도 유용하게 사용할 수 있습니다.

이렇게 하면 고유 제약 조건으로 인한 충돌 발생 시 해당 레코드를 무시하고 다음 INSERT 작업을 계속 수행할 수 있습니다.

**참고자료:**

- [Oracle 공식 문서 - IGNORE_ROW_ON_DUPKEY_INDEX 힌트](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/Comments.html#GUID-A6D8F462-2A50-4C28-AE60-3011A479D512)

---

**요약:** INSERT 문에서 `IGNORE_ROW_ON_DUPKEY_INDEX` 힌트를 사용하여 UNIQUE 제약 조건 위반 시 오류를 무시하고 다음 쿼리를 수행할 수 있습니다.

---

### 참고 자료

1. [Oracle IGNORE_ROW_ON_DUPKEY_INDEX Hint ](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/Comments.html#GUID-20390275-91A7-49DC-AAD1-A1FE943A4F75)
