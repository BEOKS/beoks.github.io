템플릿 메서드 패턴은 **알고리즘의 골격(뼈대)을 상위 클래스에 정의하고, 알고리즘의 일부 단계를 하위 클래스에서 구현하도록 하는** 행위 디자인 패턴입니다.

이 패턴은 마치 요리 레시피와 같습니다. 레시피에는 "1. 재료 손질하기", "2. 재료 볶기", "3. 소스 넣고 끓이기"와 같은 전체적인 요리 과정(알고리즘의 골격)이 정해져 있습니다. 하지만 "재료"나 "소스"가 무엇인지에 따라 요리의 종류(세부 구현)가 달라집니다. 템플릿 메서드 패턴은 바로 이 레시피처럼, 전체적인 구조는 고정하되 세부적인 내용을 유연하게 변경할 수 있도록 해줍니다.

이 패턴은 [[상속(Inheritance)]]을 통해 기능을 확장하는 대표적인 방법 중 하나입니다.

### 핵심 구성 요소

템플릿 메서드 패턴은 두 가지 주요 부분으로 구성됩니다.

- **추상 클래스 (Abstract Class)**: 템플릿 메서드를 정의하는 클래스입니다. 알고리즘의 골격이 되는 **템플릿 메서드**와, 하위 클래스에서 구현해야 할 **추상 메서드(primitive operations)**, 그리고 선택적으로 재정의할 수 있는 **훅(Hook) 메서드**를 포함합니다.
- **구체 클래스 (Concrete Class)**: 추상 클래스를 상속받아, 구현되지 않았던 추상 메서드나 훅 메서드를 실제로 구현하는 클래스입니다.
- **templateMethod()**: 알고리즘의 뼈대입니다. 이 메서드 안에서 여러 추상 메서드나 훅 메서드를 일정한 순서로 호출합니다. 이 메서드는 일반적으로 상위 클래스에서 `final`로 선언하여 하위 클래스가 수정할 수 없도록 강제합니다.
- **primitiveOperation()**: 하위 클래스에서 반드시 구현해야 하는 단계를 나타내는 추상 메서드입니다.
- **hook()**: 하위 클래스에서 선택적으로 재정의할 수 있는 메서드입니다. 기본 구현을 가지거나, 아무 내용이 없을 수도 있습니다. 알고리즘의 특정 지점에서 하위 클래스에게 추가적인 확장 포인트를 제공하는 역할을 합니다.

### Java 예시 코드: 데이터 처리기

다양한 종류의 파일(CSV, JSON 등)을 읽어와서 데이터를 처리하고 저장하는 공통적인 프로세스가 있다고 가정해 보겠습니다. 파일의 종류에 따라 데이터를 파싱하는 방식만 다를 뿐, 전체적인 흐름(파일 열기 -> 데이터 처리 -> 파일 닫기)은 동일합니다.

```java
// AbstractClass: 데이터 처리의 템플릿을 제공
public abstract class AbstractDataProcessor {

    // 템플릿 메서드: final로 선언하여 하위 클래스에서 재정의하는 것을 방지
    public final void process(String filePath) {
        openFile(filePath);
        String data = parseData(); // 이 부분만 하위 클래스에 따라 달라짐
        processData(data);
        closeFile();
        
        // 훅 메서드 사용
        if (isLoggingRequired()) {
            log();
        }
    }

    // 공통 기능은 상위 클래스에서 구현
    private void openFile(String filePath) {
        System.out.println(filePath + " 파일을 엽니다.");
    }

    private void processData(String data) {
        System.out.println("공통 로직으로 데이터를 처리합니다: " + data);
    }

    private void closeFile() {
        System.out.println("파일을 닫습니다.");
    }
    
    private void log() {
        System.out.println("작업 내용을 로깅합니다.");
    }

    // 하위 클래스에서 반드시 구현해야 하는 부분 (추상 메서드)
    protected abstract String parseData();
    
    // 하위 클래스에서 선택적으로 재정의할 수 있는 부분 (훅 메서드)
    protected boolean isLoggingRequired() {
        return true; // 기본적으로는 로깅을 하도록 설정
    }
}

// ConcreteClass 1: CSV 데이터 처리
public class CsvDataProcessor extends AbstractDataProcessor {
    @Override
    protected String parseData() {
        System.out.println("CSV 형식에 맞게 데이터를 파싱합니다.");
        return "CSV Data";
    }
}

// ConcreteClass 2: JSON 데이터 처리 (로깅은 하지 않도록 재정의)
public class JsonDataProcessor extends AbstractDataProcessor {
    @Override
    protected String parseData() {
        System.out.println("JSON 형식에 맞게 데이터를 파싱합니다.");
        return "JSON Data";
    }

    @Override
    protected boolean isLoggingRequired() {
        return false; // JSON 처리기는 로깅을 하지 않음
    }
}
```

이 구조를 통해 `process()`라는 전체적인 흐름은 `AbstractDataProcessor`가 제어하면서도, `parseData()`라는 핵심적인 가변 로직은 각 `ConcreteClass`가 책임지도록 역할을 분담할 수 있습니다. 이것이 바로 [[제어의 역전 (Inversion of Control)]] 원칙의 한 예이며, "Don't call us, we'll call you(우리를 호출하지 마세요. 우리가 당신을 호출할 겁니다)"라는 **할리우드 원칙**으로도 설명됩니다.

### 스프링 프레임워크에서의 활용: `JdbcTemplate`

스프링 프레임워크의 JdbcTemplate은 템플릿 메서드 패턴의 매우 훌륭한 실제 사용 사례입니다.

과거 JDBC 프로그래밍에서는 개발자가 매번 다음과 같은 반복적인 코드를 작성해야 했습니다.

1. 데이터베이스 커넥션 획득
2. `PreparedStatement` 생성 및 파라미터 바인딩
3. 쿼리 실행
4. `ResultSet` 처리
5. **`try-catch-finally`를 사용한 자원(Connection, PreparedStatement, ResultSet) 해제**
6. 예외 처리 및 전환

이 중에서 1, 5, 6번은 거의 모든 JDBC 작업에서 동일하게 반복되는 상용구 코드(Boilerplate Code)입니다. `JdbcTemplate`은 이 반복적인 부분을 자신의 템플릿 메서드(`query()`, `update()` 등) 안에 숨겨두고, 개발자는 변하는 부분인 2, 3, 4번(실행할 SQL, 파라미터, 결과 처리 방식)만 [[콜백 (Callback)]] 형태로 제공하면 되도록 설계되었습니다.

```java
// 개발자는 RowMapper라는 콜백 인터페이스 구현만 제공하면 된다.
public class MemberRowMapper implements RowMapper<Member> {
    @Override
    public Member mapRow(ResultSet rs, int rowNum) throws SQLException {
        // ResultSet 처리 로직
        return new Member(rs.getLong("id"), rs.getString("name"));
    }
}

// JdbcTemplate 사용
JdbcTemplate jdbcTemplate = new JdbcTemplate(dataSource);
String sql = "SELECT id, name FROM member WHERE id = ?";
Member member = jdbcTemplate.queryForObject(sql, new MemberRowMapper(), 1L);
```

여기서 `jdbcTemplate.queryForObject()`가 바로 템플릿 메서드 역할을 합니다. 이 메서드 내부에서는 커넥션을 얻고, `PreparedStatement`를 만들고, 쿼리를 실행하고, `finally` 블록에서 모든 자원을 안전하게 닫아주는 전체적인 '골격'을 수행합니다. 그리고 `ResultSet`을 실제 `Member` 객체로 어떻게 매핑할 것인지에 대한 세부 로직은 개발자가 `MemberRowMapper`라는 '구체적인 부분'을 구현하여 주입하는 것입니다.

### [[전략 패턴 (Strategy Pattern)]]과의 비교

템플릿 메서드 패턴은 종종 [[전략 패턴 (Strategy Pattern)]]과 비교됩니다. 두 패턴 모두 알고리즘의 일부를 교체할 수 있게 하지만, 그 방법에서 결정적인 차이가 있습니다.

|   |   |   |
|---|---|---|
|**구분**|**템플릿 메서드 패턴 (Template Method Pattern)**|**전략 패턴 (Strategy Pattern)**|
|**목적**|알고리즘의 구조를 정의하고, 일부 단계를 하위 클래스에 위임|알고리즘군(群)을 정의하고, 각 알고리즘을 캡슐화하여 상호 교체 가능하게 함|
|**방법**|**상속 (Inheritance)** 을 사용|**합성 (Composition)** 또는 위임을 사용|
|**변경 시점**|컴파일 타임에 결정 (어떤 하위 클래스를 사용할지)|런타임에 동적으로 변경 가능|
|**유연성**|상대적으로 낮음 (상속 구조에 종속)|상대적으로 높음 (객체를 주입하여 쉽게 변경)|

간단히 말해, **템플릿 메서드 패턴은 "전체적인 흐름은 내가 정할 테니, 너는 비어있는 세부 내용만 채워 넣어"** 라는 방식이고, **전략 패턴은 "이 일을 할 수 있는 여러 방법(전략)이 있는데, 어떤 것을 사용할지는 네가 정해서 나에게 알려줘"** 라는 방식입니다.