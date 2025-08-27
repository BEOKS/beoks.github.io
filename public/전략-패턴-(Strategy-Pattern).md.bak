전략 패턴은 **알고리즘군을 정의하고, 각 알고리즘을 캡슐화하여, 런타임에 상호 교체할 수 있도록 만드는** 행위 디자인 패턴입니다.

이 패턴을 사용하면 클라이언트(알고리즘을 사용하는 쪽)의 변경 없이, 알고리즘 자체를 유연하게 변경할 수 있습니다. 예를 들어, 목적지까지 가는 방법에는 버스, 지하철, 택시 등 여러 '전략'이 있을 수 있습니다. 어떤 교통수단을 이용하든 '목적지까지 간다'는 최종 목표는 동일합니다. 전략 패턴은 이처럼 다양한 '방법(전략)'들을 독립적인 객체로 만들어, 상황에 맞게 쉽게 교체하여 사용할 수 있도록 합니다.

이 패턴은 [[개방-폐쇄 원칙 (Open-Closed Principle)]]을 가장 잘 따르는 패턴 중 하나입니다. 즉, 기존 코드(Context)의 수정 없이 새로운 기능(전략)을 추가할 수 있습니다.

### 전략 패턴이 해결하고자 하는 문제

쇼핑몰에서 상품 가격을 계산하는 로직을 생각해 보겠습니다. 일반 회원 할인, VIP 회원 할인, 특정 카드사 제휴 할인 등 다양한 할인 '전략'이 있을 수 있습니다. 전략 패턴을 사용하지 않는다면, 가격을 계산하는 메서드 내부에 다음과 같은 코드가 들어갈 가능성이 높습니다.

```java
public class PriceCalculator {
    public double calculate(Item item, Member member) {
        double price = item.getPrice();
        if ("VIP".equals(member.getGrade())) {
            // VIP 할인 로직
            price *= 0.8; 
        } else if ("GOLD".equals(member.getGrade())) {
            // 골드 회원 할인 로직
            price *= 0.9;
        } else {
            // 일반 회원 할인 로직
            price *= 0.95;
        }
        // ... 여기에 새로운 할인 정책이 추가될 때마다 if-else가 계속 늘어난다.
        return price;
    }
}
```

이러한 코드는 새로운 할인 정책이 생길 때마다 `calculate` 메서드를 직접 수정해야 하므로 OCP 원칙에 위배됩니다. 또한, 코드가 점점 복잡해지고 유지보수가 어려워집니다. 전략 패턴은 이러한 `if-else` 또는 `switch` 문을 제거하고, 각 할인 정책을 별도의 '전략' 클래스로 분리하여 문제를 해결합니다.

### 핵심 구성 요소

전략 패턴은 세 가지 주요 역할로 구성됩니다.

- **Context (컨텍스트)**: 전략을 사용하는 클래스입니다. 구체적인 전략의 구현 내용은 알지 못한 채, 오직 `Strategy` 인터페이스에만 의존합니다. `Context`는 `Strategy` 객체를 멤버 변수로 가지며, 필요에 따라 동적으로 교체할 수 있습니다.
- **Strategy (전략 인터페이스)**: 모든 구체적인 전략 클래스들이 구현해야 하는 공통 인터페이스입니다. `Context`가 호출할 메서드를 정의합니다.
- **Concrete Strategy (구체적인 전략)**: `Strategy` 인터페이스를 구현하여 실제 알고리즘을 제공하는 클래스입니다.

```mermaid
classDiagram
    class Context {
        - strategy: Strategy
        + setStrategy(strategy: Strategy)
        + executeStrategy()
    }
    class Strategy {
        <<interface>>
        + doOperation()
    }
    class ConcreteStrategyA {
        + doOperation()
    }
    class ConcreteStrategyB {
        + doOperation()
    }

    Context o-- Strategy : "전략을 가짐(Composition)"
    note for Context "전략을 실행"

    Strategy <|.. ConcreteStrategyA : "구현"
    Strategy <|.. ConcreteStrategyB : "구현"
```

### Java 예시 코드: 결제 시스템

다양한 결제 수단(신용카드, 카카오페이 등)을 처리하는 시스템을 전략 패턴으로 구현해 보겠습니다.

```java
// Strategy 인터페이스
public interface PaymentStrategy {
    void pay(int amount);
}

// ConcreteStrategy 1: 신용카드 결제
public class CreditCardStrategy implements PaymentStrategy {
    private String cardHolderName;
    private String cardNumber;

    public CreditCardStrategy(String cardHolderName, String cardNumber) {
        this.cardHolderName = cardHolderName;
        this.cardNumber = cardNumber;
    }

    @Override
    public void pay(int amount) {
        System.out.println(amount + "원을 신용카드(" + cardNumber + ")로 결제합니다.");
    }
}

// ConcreteStrategy 2: 카카오페이 결제
public class KakaoPayStrategy implements PaymentStrategy {
    private String email;

    public KakaoPayStrategy(String email) {
        this.email = email;
    }

    @Override
    public void pay(int amount) {
        System.out.println(amount + "원을 카카오페이(" + email + ")로 결제합니다.");
    }
}

// Context: 결제 대행
public class ShoppingCart {
    private int totalAmount;
    
    // ... 상품 추가 로직 ...

    public void pay(PaymentStrategy paymentMethod) {
        paymentMethod.pay(totalAmount);
    }
}

// 실행
public class Application {
    public static void main(String[] args) {
        ShoppingCart cart = new ShoppingCart();
        // cart.addItem(...)
        // cart.setTotalAmount(10000);

        // 신용카드로 결제 (전략 1)
        cart.pay(new CreditCardStrategy("홍길동", "1234-5678-9012-3456"));
        
        // 카카오페이로 결제 (전략 2)
        cart.pay(new KakaoPayStrategy("gildong@example.com"));
    }
}
```

`ShoppingCart`(Context)는 어떤 결제 방식(Concrete Strategy)이 들어오는지 신경 쓰지 않고, 단지 `PaymentStrategy` 인터페이스의 `pay` 메서드를 호출할 뿐입니다. 덕분에 나중에 '네이버페이'나 '토스'와 같은 새로운 결제 전략이 추가되더라도 `ShoppingCart` 코드는 전혀 수정할 필요가 없습니다.

### 스프링 프레임워크에서의 활용

스프링 프레임워크는 [[의존성 역전 원칙 (Dependency Inversion Principle)]]을 통해 전략 패턴을 매우 자연스럽게 구현할 수 있도록 지원합니다.

1. PasswordEncoder

Spring Security의 PasswordEncoder는 전략 패턴의 대표적인 예시입니다. PasswordEncoder는 비밀번호를 암호화하는 방법에 대한 '전략' 인터페이스입니다.

```java
// Strategy 인터페이스
public interface PasswordEncoder {
    String encode(CharSequence rawPassword);
    boolean matches(CharSequence rawPassword, String encodedPassword);
}
```

개발자는 `BCryptPasswordEncoder`, `SCryptPasswordEncoder` 등 스프링이 제공하는 다양한 `ConcreteStrategy` 중에서 원하는 암호화 전략을 선택하여 Bean으로 등록하기만 하면 됩니다.

```java
@Configuration
public class SecurityConfig {
    @Bean
    public PasswordEncoder passwordEncoder() {
        // BCrypt 암호화 전략을 사용
        return new BCryptPasswordEncoder(); 
    }
}
```

2. 의존성 주입을 통한 전략 선택

여러 할인 정책(전략)을 Bean으로 등록하고, 필요한 곳에서 특정 전략을 주입받아 사용할 수 있습니다.

```java
// 할인 전략 인터페이스
public interface DiscountStrategy {
    int applyDiscount(int price);
}

@Component("flatDiscount")
public class FlatDiscountStrategy implements DiscountStrategy {
    @Override
    public int applyDiscount(int price) {
        return price - 1000; // 정액 할인
    }
}

@Component("percentDiscount")
public class PercentageDiscountStrategy implements DiscountStrategy {
    @Override
    public int applyDiscount(int price) {
        return (int) (price * 0.9); // 정률 할인
    }
}

// Context
@Service
public class OrderService {
    private final DiscountStrategy discountStrategy;

    // 생성자를 통해 특정 전략을 주입받음
    // @Qualifier("flatDiscount") 또는 @Qualifier("percentDiscount")로 선택
    public OrderService(@Qualifier("percentDiscount") DiscountStrategy discountStrategy) {
        this.discountStrategy = discountStrategy;
    }

    public int calculatePrice(int price) {
        return discountStrategy.applyDiscount(price);
    }
}
```

이처럼 스프링의 DI 컨테이너를 사용하면, 코드 수정 없이 설정(`@Qualifier`의 이름 변경)만으로 `OrderService`가 사용하는 할인 전략을 동적으로 변경할 수 있어 전략 패턴의 장점을 극대화할 수 있습니다.

### [[템플릿 메서드 패턴 (Template Method Pattern)]]과의 비교

전략 패턴은 **합성(Composition)**을, 템플릿 메서드 패턴은 **상속(Inheritance)**을 사용한다는 점에서 가장 큰 차이가 있습니다. 자세한 비교는 [[템플릿 메서드 패턴 (Template Method Pattern)]] 문서의 비교표를 참고해주세요.

- **전략 패턴**: '무엇'을 할지는 Context가 결정하고, '어떻게' 할지는 Strategy 객체에 위임합니다. (런타임에 교체 가능)
- **템플릿 메서드 패턴**: '전체적인 흐름'은 상위 클래스가 결정하고, '세부적인 내용'을 하위 클래스가 채워 넣습니다. (컴파일 타임에 결정)