이전에 간단한 복합 인덱스를 적용했을 때는 캐시 효과나 인덱스 구조의 한계로 인해 기대만큼의 성능 향상을 보지 못하거나 오히려 미미한 성능 저하를 경험할 수도 있다는 점을 배웠습니다. (이전 실험에서는 약 -1.62%의 성능 변화를 관찰했었죠.)

하지만, 쿼리에 필요한 모든 데이터를 담고 있는 **커버링 인덱스**를 사용하면 어떻게 될까요? 이번 테스트에서는 무려 **약 70%의 성능 향상**을 확인할 수 있었습니다! 지금부터 그 비결을 자세히 파헤쳐 보겠습니다.

---
## [[MySQL WITH ROLLUP]] 다시 살펴보기

잠시 복습하자면, `WITH ROLLUP`은 `GROUP BY` 절과 함께 사용되어, 지정된 컬럼 그룹별 집계는 물론 각 그룹핑 레벨의 소계와 총계까지 한 번의 쿼리로 반환하는 강력한 기능입니다. 복잡한 리포트나 다차원 분석에 매우 유용하죠. (자세한 내용은 [[GROUP BY 절과 WITH ROLLUP 활용법]] 참고)

---
## 성능 테스트: 커버링 인덱스의 압도적인 힘!

이전 테스트와 동일한 환경에서, 인덱스 전략만 **커버링 인덱스**로 변경하여 다시 한번 `WITH ROLLUP` 쿼리의 성능을 측정했습니다.

### 테스트 환경 및 핵심 변경 사항

* **데이터베이스**: 로컬 MySQL 서버
* **테이블**: 6개의 계층형 문자열 컬럼(`cat1` ~ `cat6`)과 1개의 수치형 컬럼(`value_col`)으로 구성.
    ```sql
    CREATE TABLE hierarchical_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        cat1 VARCHAR(10),
        cat2 VARCHAR(10),
        cat3 VARCHAR(10),
        cat4 VARCHAR(10),
        cat5 VARCHAR(10),
        cat6 VARCHAR(10),
        value_col INT
    );
    ```
* **데이터**: 총 **300만 건**의 무작위 계층형 데이터
* **테스트 쿼리**:
    ```sql
    SELECT cat1, cat2, cat3, cat4, cat5, cat6, SUM(value_col)
    FROM hierarchical_data
    GROUP BY cat1, cat2, cat3, cat4, cat5, cat6 WITH ROLLUP;
    ```
* **핵심 변경: 커버링 인덱스 적용**
    이전에는 `GROUP BY` 컬럼들만 포함하는 인덱스를 사용했지만, 이번에는 **쿼리가 필요로 하는 모든 컬럼 (GROUP BY 대상 컬럼 + SUM 집계 대상 컬럼)을 포함하는 커버링 인덱스**를 생성했습니다.
    ```sql
    -- 기존 인덱스가 있다면 삭제 후 진행
    -- DROP INDEX idx_hierarchical_cats ON hierarchical_data;

    CREATE INDEX idx_covering_rollup_all_cats_value
    ON hierarchical_data (cat1, cat2, cat3, cat4, cat5, cat6, value_col);
    ```
    이것이 바로 [[커버링 인덱스(Covering Index)]]입니다.

### 테스트 결과: 놀라운 변화!

| 항목                     | 인덱스 미적용 시 | 커버링 인덱스 적용 시 | 개선 효과          |
| :----------------------- | :-------------: | :-----------------: | :----------------: |
| **쿼리 실행 시간** | **17.3397초** | **5.2211초** | **12.1187초 단축** |
| 인덱스 생성 시간         | \-              | 7.41초              | \-                 |
| 결과 행 수 (ROLLUP 포함) | 3,797,973건     | 3,797,973건         | 동일               |
| **성능 개선율** | \-              | \-                  | **약 69.89%** |

보이시나요? 커버링 인덱스를 적용하자 쿼리 실행 시간이 **17.34초에서 5.22초로 대폭 단축되어, 약 69.89%의 압도적인 성능 향상**을 달성했습니다! 🎉 이전 테스트에서 겪었던 실망감은 온데간데없네요.

---
## 분석: 왜 커버링 인덱스는 이렇게 강력할까요?

커버링 인덱스가 일반적인 복합 인덱스와 어떻게 다르기에 이런 극적인 차이를 만들어낼까요?

1.  **인덱스 미적용 시**: MySQL은 테이블 전체를 훑어보고(`Full Table Scan`), `GROUP BY` 컬럼들을 기준으로 데이터를 정렬하거나 해시 처리한 후 `ROLLUP` 집계를 수행합니다. 데이터가 많을수록 이 과정은 매우 느립니다.

2.  **일반 복합 인덱스 (Non-Covering)의 한계**: `GROUP BY` 컬럼들(`cat1`~`cat6`)만 포함한 인덱스는 그룹핑에는 도움을 줄 수 있지만, `SUM(value_col)`을 계산하려면 결국 실제 테이블로 돌아가 `value_col` 값을 찾아와야 합니다. 이 과정에서 추가적인 디스크 I/O(테이블 랜덤 액세스)가 발생하여 성능 향상 폭이 제한되거나, 심지어 캐시 상황에 따라서는 더 느려질 수도 있습니다.

3.  **커버링 인덱스의 마법**:
    커버링 인덱스 `(cat1, ..., cat6, value_col)`는 **쿼리 실행에 필요한 모든 정보를 자신 안에 담고 있습니다.**
    * MySQL은 `GROUP BY`에 필요한 `cat1`~`cat6` 컬럼과 `SUM()` 집계에 필요한 `value_col`까지 **모두 인덱스에서 직접 읽어옵니다.**
    * 실제 테이블 데이터에 접근할 필요가 전혀 없어집니다. 이는 디스크 I/O, 특히 랜덤 I/O를 획기적으로 줄여줍니다.
    * 인덱스 자체도 `GROUP BY` 순서에 맞게 정렬되어 있으므로, 정렬 작업 부하도 크게 감소합니다.

아래 그림은 이 차이를 명확하게 보여줍니다.

```mermaid
graph TD
    subgraph 인덱스 미적용 시 ROLLUP 처리 흐름
        A[쿼리 요청] --> B{테이블 전체 스캔};
        B --> C{데이터 정렬 또는 해싱};
        C --> D{ROLLUP 연산};
        D --> E[결과 반환];
    end

    subgraph 커버링 인덱스 적용 시 ROLLUP 처리 흐름
        F[쿼리 요청] --> G{커버링 인덱스 스캔};
        G --> H{<center>인덱스 데이터만으로<br/>그룹핑 및 SUM 계산</center>};
        H --> I{ROLLUP 연산};
        I --> J[결과 반환];
    end
````

커버링 인덱스를 사용하면 "테이블 전체 스캔"이나 "테이블 랜덤 액세스" 단계가 사라지고, 모든 작업이 효율적인 인덱스 내에서 완료됩니다.

---

## 결론

이번 테스트는 `WITH ROLLUP`과 같은 집계 쿼리에서 커버링 인덱스가 얼마나 강력한 성능 개선을 가져올 수 있는지 명확히 보여줍니다.

- **집계 쿼리에는 커버링 인덱스를 적극적으로 고려하세요.** `SELECT` 목록, `WHERE` 절, `GROUP BY` 절, `ORDER BY` 절, 그리고 집계 함수에 사용되는 모든 컬럼을 인덱스에 포함시키는 것을 목표로 합니다.
- **`EXPLAIN`을 생활화하세요.** 인덱스를 생성한 후에는 반드시 `EXPLAIN`을 통해 MySQL이 실제로 커버링 인덱스를 사용하고 있는지 (`Extra` 필드에 `Using index` 표시 확인), 불필요한 작업(예: `Using filesort`)은 없는지 확인해야 합니다.
- **트레이드오프를 인지하세요.** 커버링 인덱스는 일반적으로 컬럼 수가 많아져 인덱스 크기가 커지고, `INSERT/UPDATE/DELETE` 시 인덱스 업데이트 비용이 증가할 수 있습니다. 하지만 읽기 성능이 매우 중요한 분석 쿼리에서는 이러한 비용을 감수할 가치가 충분한 경우가 많습니다.

단순히 인덱스를 거는 것에서 한 걸음 더 나아가, 쿼리의 특성을 정확히 이해하고 그에 맞는 '커버링' 전략을 구사하는 것이 MySQL 성능 최적화의 중요한 열쇠입니다. 이번 경험이 여러분의 쿼리 성능 개선 여정에 큰 도움이 되기를 바랍니다!

---

## 참고 자료
- [MySQL 8.0 Reference Manual - 14.19.3 GROUP BY Modifiers (WITH ROLLUP, CUBE)](https://dev.mysql.com/doc/refman/8.0/en/group-by-modifiers.html)
- [MySQL 8.0 Reference Manual - 10.3.1 How MySQL Uses Indexes](https://dev.mysql.com/doc/refman/8.0/en/mysql-indexes.html) 
- [MySQL 8.0 Reference Manual - 10.2.1 Optimizing SELECT Statements](https://www.google.com/search?q=https://dev.mysql.com/doc/refman/8.0/en/optimizing-selects.html)
