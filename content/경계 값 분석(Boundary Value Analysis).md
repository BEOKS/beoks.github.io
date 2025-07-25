경계 값 분석(Boundary Value Analysis, BVA)은 소프트웨어 테스팅, 특히 블랙박스 테스팅에서 널리 사용되는 테스트 케이스 설계 기법입니다. 이 기법의 핵심 아이디어는 대부분의 오류가 입력 값의 경계 또는 그 근처에서 발생한다는 경험적 사실에 기반합니다. 따라서 경계 값 분석은 입력 조건의 최소값, 최대값, 그리고 그 바로 안팎의 값들을 테스트 케이스로 선택하여 오류를 효과적으로 찾아내는 데 중점을 둡니다.

## 왜 경계 값에 주목해야 하는가?

애플리케이션을 개발할 때, 특정 범위 내의 값만 유효하게 처리하도록 로직을 구현하는 경우가 많습니다. 예를 들어, "나이는 0세 이상 120세 이하이어야 한다" 또는 "비밀번호 길이는 8자 이상 16자 이하여야 한다" 와 같은 요구사항이 있을 수 있습니다.

개발자들은 이러한 경계를 처리하기 위해 조건문(예: `if (age >= 0 && age <= 120)`)을 사용하는데, 이 과정에서 부등호(`<`, `<=`, `>`, `>=`)를 잘못 사용하거나, 경계 조건을 정확히 구현하지 못하는 실수가 발생하기 쉽습니다. 예를 들어, `age < 120`으로 코딩해야 할 것을 `age <= 120`으로 하거나 그 반대로 하는 경우입니다. 경계 값 분석은 바로 이러한 종류의 오류를 발견하는 데 매우 효과적입니다.

## 경계 값 분석을 통한 테스트 케이스 도출 방법

경계 값 분석은 주로 [[동등 분할(Equivalence Partitioning)]] 기법으로 유효하거나 유효하지 않은 데이터의 그룹(파티션)을 나눈 후, 각 파티션의 경계에 있는 값들을 테스트 케이스로 선정합니다.

일반적으로 입력 조건이 특정 범위를 가질 때 (예: `[min, max]`), 다음과 같은 값들을 테스트 케이스로 고려합니다:

1. **최소값 (Min)**: 범위의 가장 작은 값
2. **최소값 바로 아래 (Min - 1)**: 유효 범위 바로 바깥의 값 (오류 조건)
3. **최소값 바로 위 (Min + 1)**: 유효 범위 안쪽의 값
4. **일반적인 유효값 (Nominal/Typical Value)**: 범위 내의 임의의 정상 값
5. **최대값 바로 아래 (Max - 1)**: 유효 범위 안쪽의 값
6. **최대값 (Max)**: 범위의 가장 큰 값
7. **최대값 바로 위 (Max + 1)**: 유효 범위 바로 바깥의 값 (오류 조건)

**예시 1: 시험 점수 입력 (0점에서 100점 사이)**

- 입력 범위: `[0, 100]`
- 경계 값 테스트 케이스:
    - `-1` (Min - 1, 유효하지 않음)
    - `0` (Min, 유효함)
    - `1` (Min + 1, 유효함)
    - `50` (Nominal, 유효함)
    - `99` (Max - 1, 유효함)
    - `100` (Max, 유효함)
    - `101` (Max + 1, 유효하지 않음)

**예시 2: 아이템 수량 선택 (1개 이상 5개 이하)**

- 입력 범위: `[1, 5]`
- 경계 값 테스트 케이스:
    - `0` (Min - 1, 유효하지 않음)
    - `1` (Min, 유효함)
    - `2` (Min + 1, 유효함)
    - `3` (Nominal, 유효함)
    - `4` (Max - 1, 유효함)
    - `5` (Max, 유효함)
    - `6` (Max + 1, 유효하지 않음)

## 경계 값 분석의 장점

1. **높은 오류 검출율**: 경험적으로 경계 지점에서 많은 결함이 발견되므로, 이 부분을 집중적으로 테스트하여 오류를 효과적으로 찾아낼 수 있습니다.
2. **테스트 케이스 수 최적화**: 모든 가능한 입력 값을 테스트하는 대신, 오류 발생 가능성이 높은 경계 값에 집중하므로 상대적으로 적은 수의 테스트 케이스로 효율적인 테스트가 가능합니다.
3. **간단하고 적용하기 쉬움**: 기법 자체가 이해하고 적용하기 쉬워 많은 테스터들이 선호합니다.

## 경계 값 분석의 한계 및 고려사항

- **입력 변수 간의 상호작용**: 경계 값 분석은 주로 단일 입력 변수의 경계에 초점을 맞춥니다. 여러 입력 변수 간의 복잡한 상호작용이나 종속성으로 인해 발생하는 오류는 발견하기 어려울 수 있습니다.
- **논리적 오류**: 경계와 무관한 애플리케이션 내부의 논리적 오류는 검출하지 못할 수 있습니다.
- **비기능적 측면**: 성능이나 보안과 같은 비기능적 측면은 고려하지 않습니다.
- **동등 분할과의 연계**: 경계 값 분석은 동등 분할 기법과 함께 사용될 때 더욱 강력한 효과를 발휘합니다. 동등 분할로 데이터 집합을 나눈 후, 각 분할의 경계를 BVA로 테스트하는 것이 일반적입니다.

## API 테스트에서의 활용

앞서 설명된 API 단위 테스트의 "테스트 케이스 설계" 섹션에서 언급된 "예외 케이스" 및 "경계 값 분석"은 API의 요청 파라미터 유효성을 검증하는 데 매우 중요합니다.

예를 들어, API가 다음과 같은 요청 파라미터를 받는다고 가정해 봅시다:

- `age` (정수, 18세 이상 60세 이하 허용)
- `limit` (정수, 한 페이지에 보여줄 아이템 수, 1 이상 100 이하 허용)
- `query` (문자열, 검색어, 길이 1 이상 50 이하 허용)

이러한 파라미터들에 대해 경계 값 분석을 적용하여 다음과 같은 테스트 케이스를 도출할 수 있습니다:

- `age`: 17, 18, 19, 59, 60, 61
- `limit`: 0, 1, 2, 99, 100, 101
- `query` (길이 기준): 0 (빈 문자열), 1, 2, 49, 50, 51

API 테스트 시, 이러한 경계 값을 포함하는 요청을 보내고 API가 예상대로 올바른 응답(성공 또는 정의된 오류 응답)을 반환하는지 확인합니다.

## 결론

경계 값 분석은 테스트할 입력 값의 범위를 효과적으로 좁히고, 오류 발생 가능성이 높은 지점을 집중적으로 공략하여 테스트 효율성과 품질을 높이는 강력한 테스트 설계 기법입니다. 특히 API의 입력 파라미터 유효성 검증, 비즈니스 규칙의 경계 조건 확인 등 다양한 상황에서 유용하게 활용될 수 있습니다. 다른 테스트 설계 기법과 함께 적절히 사용한다면 더욱 견고한 소프트웨어를 만드는 데 크게 기여할 것입니다.