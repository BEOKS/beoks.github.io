리스코프 치환 원칙(LSP)은 객체 지향 프로그래밍의 다섯 가지 [[SOLID 원칙]] 중 하나로, 바바라 리스코프(Barbara Liskov)가 1987년에 제안한 개념입니다. 이 원칙은 상속 관계에서 하위 타입(자식 클래스)이 상위 타입(부모 클래스)을 대체할 수 있어야 한다는 것을 의미합니다.

## 리스코프 치환 원칙의 정의

리스코프 치환 원칙은 간단히 말해 "하위 타입은 상위 타입을 대체할 수 있어야 한다"는 것입니다. 좀 더 형식적인 정의는 다음과 같습니다:

> "프로그램의 속성(정확성, 수행하는 작업 등)을 변경하지 않고 하위 타입의 객체를 상위 타입의 객체로 대체할 수 있어야 한다."

즉, 부모 클래스 타입으로 선언된 변수에 자식 클래스의 인스턴스를 할당해도 프로그램이 예상대로 동작해야 합니다.

## 리스코프 치환 원칙의 중요성

리스코프 치환 원칙은 다음과 같은 이유로 객체 지향 설계에서 중요합니다:

1. **코드 재사용성**: 상속 관계가 올바르게 설계되면 부모 클래스의 코드를 재사용할 수 있습니다.
2. **유지보수성**: 상위 타입의 동작을 보장받을 수 있어 예측 가능한 코드를 작성할 수 있습니다.
3. **다형성의 올바른 구현**: 다형성을 안전하게 활용할 수 있게 합니다.
4. **확장성**: 기존 코드를 변경하지 않고도 새로운 하위 타입을 추가할 수 있습니다.

## 리스코프 치환 원칙 준수 방법

리스코프 치환 원칙을 준수하기 위해서는 다음과 같은 규칙을 따라야 합니다:

### 1. 메서드 시그니처 규칙

- **사전조건을 강화하지 않기**: 하위 타입의 메서드는 상위 타입의 메서드보다 더 강한 사전조건(precondition)을 요구해서는 안 됩니다.
- **사후조건을 약화하지 않기**: 하위 타입의 메서드는 상위 타입의 메서드보다 더 약한 사후조건(postcondition)을 보장해서는 안 됩니다.
- **예외 규칙**: 하위 타입의 메서드는 상위 타입의 메서드에서 명시되지 않은 예외를 발생시켜서는 안 됩니다.

### 2. 속성 규칙

- **불변 속성 유지**: 하위 타입은 상위 타입에서 정의한 불변 속성(invariant)을 유지해야 합니다.
- **히스토리 규칙**: 하위 타입은 상위 타입의 행동 방식을 변경해서는 안 됩니다.

## 리스코프 치환 원칙 위반 사례

리스코프 치환 원칙을 위반하는 대표적인 사례를 살펴보겠습니다:

### 1. 직사각형-정사각형 문제

가장 유명한 LSP 위반 사례는 직사각형(Rectangle)과 정사각형(Square) 관계입니다.

```java
// 직사각형 클래스
public class Rectangle {
    protected int width;
    protected int height;
    
    public void setWidth(int width) {
        this.width = width;
    }
    
    public void setHeight(int height) {
        this.height = height;
    }
    
    public int getArea() {
        return width * height;
    }
}

// 정사각형 클래스 (직사각형 상속)
public class Square extends Rectangle {
    // 정사각형은 너비와 높이가 같아야 하므로 메서드를 오버라이드
    @Override
    public void setWidth(int width) {
        this.width = width;
        this.height = width;  // 너비가 변경되면 높이도 같이 변경
    }
    
    @Override
    public void setHeight(int height) {
        this.height = height;
        this.width = height;  // 높이가 변경되면 너비도 같이 변경
    }
}
```

문제점은 다음과 같은 코드에서 발생합니다:

```java
void testRectangle(Rectangle rectangle) {
    rectangle.setWidth(5);
    rectangle.setHeight(4);
    assert rectangle.getArea() == 20;  // 직사각형에서는 통과, 정사각형에서는 실패
}
```

`Rectangle` 타입으로 선언된 변수에 `Square` 객체를 할당하면, `testRectangle` 메서드는 예상대로 동작하지 않습니다. 정사각형에서는 너비를 설정한 후 높이를 설정하면 너비도 같이 변경되기 때문입니다.

이 문제는 `Square`가 `Rectangle`의 행동 방식을 변경하여 리스코프 치환 원칙을 위반한 사례입니다. 이러한 경우, 상속보다는 합성(Composition)을 고려하는 것이 좋습니다.

### 2. 메서드 오버라이딩 문제

하위 클래스에서 메서드를 오버라이딩할 때 기존 동작을 크게 변경하는 경우에도 LSP를 위반할 수 있습니다.

```java
// 은행 계좌 클래스
public class BankAccount {
    protected double balance;
    
    public void withdraw(double amount) {
        if (amount > 0) {
            balance -= amount;
        }
    }
}

// 당좌 계좌 클래스
public class CheckingAccount extends BankAccount {
    private double overdraftLimit;
    
    @Override
    public void withdraw(double amount) {
        if (balance + overdraftLimit >= amount) {
            balance -= amount;
        } else {
            throw new IllegalStateException("한도 초과");  // 예상치 못한 예외
        }
    }
}
```

이 경우, `BankAccount` 타입으로 선언된 변수에 `CheckingAccount` 객체를 할당하면, `withdraw` 메서드를 호출했을 때 예상치 못한 예외가 발생할 수 있습니다. 이는 리스코프 치환 원칙을 위반합니다.

## 리스코프 치환 원칙 준수 예시

다음은 리스코프 치환 원칙을 준수하는 예시입니다:

```java
// 새 인터페이스
public interface Bird {
    void move();
}

// 날 수 있는 새
public class FlyingBird implements Bird {
    @Override
    public void move() {
        System.out.println("날아서 이동합니다.");
    }
}

// 날지 못하는 새
public class NonFlyingBird implements Bird {
    @Override
    public void move() {
        System.out.println("걸어서 이동합니다.");
    }
}
```

이 설계에서는 모든 새가 `move` 메서드를 구현하지만, 각자의 방식으로 이동합니다. `Bird` 타입으로 선언된 변수에 어떤 구현체를 할당하더라도 프로그램은 예상대로 동작합니다.

## 리스코프 치환 원칙과 다른 SOLID 원칙과의 관계

리스코프 치환 원칙은 다른 SOLID 원칙들과 밀접한 관련이 있습니다:

1. **단일 책임 원칙(SRP)**: 클래스가 단일 책임을 가지도록 설계하면 하위 클래스도 같은 책임을 유지하기 쉬워집니다.
2. **개방-폐쇄 원칙(OCP)**: 리스코프 치환 원칙을 준수하면 확장에 열려있고 수정에 닫혀있는 코드를 작성하기 쉬워집니다.
3. **인터페이스 분리 원칙(ISP)**: 작고 구체적인 인터페이스를 사용하면 리스코프 치환 원칙을 준수하기 쉬워집니다.
4. **의존성 역전 원칙(DIP)**: 구체적인 구현보다 추상화에 의존하면 리스코프 치환 원칙을 준수하기 쉬워집니다.

## 스프링 프레임워크에서의 리스코프 치환 원칙

스프링 프레임워크에서는 리스코프 치환 원칙이 다음과 같이 적용됩니다:

1. **의존성 주입(DI)**: 스프링의 의존성 주입은 인터페이스에 의존하므로 리스코프 치환 원칙을 자연스럽게 지원합니다.
2. **템플릿 메서드 패턴**: 스프링의 템플릿 클래스들은 리스코프 치환 원칙을 고려하여 설계되었습니다.
3. **AOP(관점 지향 프로그래밍)**: 스프링 AOP는 프록시를 사용하여 원본 객체를 대체하므로 리스코프 치환 원칙을 따라야 합니다.

예시로, 스프링의 `JdbcTemplate`을 확장할 때 리스코프 치환 원칙을 준수하는 방법을 살펴보겠습니다:

```java
@Service
public class CustomJdbcTemplate extends JdbcTemplate {
    @Override
    public <T> T queryForObject(String sql, Class<T> requiredType) {
        // JdbcTemplate의 동작을 보존하면서 확장
        logger.info("SQL 실행: " + sql);
        return super.queryForObject(sql, requiredType);
    }
}
```

이 예시에서 `CustomJdbcTemplate`은 기존 `JdbcTemplate`의 동작을 변경하지 않고 로깅 기능을 추가하여 리스코프 치환 원칙을 준수합니다.

## 리스코프 치환 원칙을 준수하기 위한 설계 방법

리스코프 치환 원칙을 준수하기 위한 몇 가지 설계 방법을 알아보겠습니다:

1. **계약에 의한 설계(Design by Contract)**: 메서드의 사전조건, 사후조건, 불변 조건을 명확히 정의합니다.
2. **상속보다 합성**: 행동이 완전히 일치하지 않을 경우 상속보다 합성을 사용합니다.
3. **추상화 수준 유지**: 상속 계층 구조에서 추상화 수준을 일관되게 유지합니다.
4. **인터페이스 활용**: 구현보다 인터페이스에 의존합니다.
5. **단위 테스트**: 하위 타입이 상위 타입을 대체할 수 있는지 테스트합니다.

## 리스코프 치환 원칙 위반 시 문제점

리스코프 치환 원칙을 위반하면 다음과 같은 문제가 발생할 수 있습니다:

1. **버그 발생**: 예상치 못한 동작으로 인해 버그가 발생할 수 있습니다.
2. **코드 품질 저하**: 하위 타입을 처리하기 위한 특별한 로직이 필요할 수 있습니다.
3. **유지보수 어려움**: 코드 변경 시 예상치 못한 영향을 미칠 수 있습니다.
4. **다형성 활용 어려움**: 다형성의 이점을 제대로 활용할 수 없습니다.
5. **테스트 복잡성 증가**: 각 하위 타입에 대해 별도의 테스트가 필요할 수 있습니다.

## 실제 개발에서의 적용 방법

실제 개발에서 리스코프 치환 원칙을 적용하는 방법을 알아보겠습니다:

1. **코드 리뷰**: 상속 관계가 리스코프 치환 원칙을 준수하는지 검토합니다.
2. **단위 테스트**: 하위 타입이 상위 타입의 테스트를 통과하는지 확인합니다.
3. **인터페이스 설계**: 행동이 명확히 정의된 인터페이스를 설계합니다.
4. **문서화**: 클래스와 메서드의 계약을 명확히 문서화합니다.
5. **점진적 리팩토링**: 리스코프 치환 원칙을 위반하는 코드를 점진적으로 개선합니다.

자세한 적용 방법은 [[객체 지향 프로그래밍 실전 적용법]]을 참고해주세요.

## 결론

리스코프 치환 원칙은 객체 지향 설계의 핵심 원칙 중 하나로, 상속 관계에서 하위 타입이 상위 타입을 대체할 수 있어야 한다는 것을 의미합니다. 이 원칙을 준수하면 다형성을 안전하게 활용할 수 있고, 코드의 재사용성, 유지보수성, 확장성을 향상시킬 수 있습니다.

하지만 리스코프 치환 원칙을 준수하기 위해서는 상속 관계를 신중하게 설계해야 하며, 때로는 상속보다 합성이나 인터페이스를 활용하는 것이 더 나은 선택일 수 있습니다. 객체 지향 설계에서 리스코프 치환 원칙을 이해하고 적용하는 것은 더 나은 소프트웨어를 개발하기 위한 중요한 단계입니다.

## 참고 자료

- Effective Java, 3rd Edition - Joshua Bloch
- Clean Code - Robert C. Martin
- Design Patterns: Elements of Reusable Object-Oriented Software - Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides
- Object-Oriented Software Construction - Bertrand Meyer