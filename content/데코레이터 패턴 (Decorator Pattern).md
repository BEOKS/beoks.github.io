우리가 카페에서 커피를 주문할 때를 생각해 볼까요? 아메리카노(기본 커피)에 우유를 추가해서 라떼를 만들 수도 있고, 거기에 휘핑크림을 얹거나 시럽을 더할 수도 있습니다. 이때 기본 커피의 본질은 변하지 않으면서 다양한 '토핑'을 통해 새로운 맛과 형태의 커피가 만들어지죠. 데코레이터 패턴은 이처럼 기존 객체(기본 커피)는 그대로 둔 채, 마치 포장지(데코레이터)를 여러 겹 씌우거나 토핑을 추가하듯 기능을 덧씌워 나가는 방식입니다.

## 데코레이터 패턴이란 무엇인가요?

**데코레이터 패턴 (Decorator Pattern)** 은 **주어진 객체에 동적으로 새로운 책임(기능)을 추가하는 패턴**입니다. [[상속 (Inheritance)]]을 통해 기능을 확장하는 방식도 있지만, 데코레이터 패턴은 [[합성 (Composition)]]을 사용하여 더 유연하게 기능을 확장할 수 있는 대안을 제공합니다.

이 패턴의 핵심은 장식될 객체(ConcreteComponent)와 장식하는 객체(Decorator)가 동일한 인터페이스(Component)를 따른다는 점입니다. 이로 인해 클라이언트는 원본 객체든, 여러 번 장식된 객체든 동일한 방식으로 사용할 수 있습니다.


```mermaid
graph LR
    %% Tip: Ensure all indentation is done with regular spaces, not non-breaking spaces.

    Client --> Component_Interface

    subgraph "데코레이션_구조" ["객체 감싸기 구조"]
        Component_Interface
        ConcreteComponent["원본 객체"] --|구현|--> Component_Interface
        Decorator["데코레이터"] --|구현|--> Component_Interface
        %% For the link below, Component_Interface_Ref is defined as a node here.
        Decorator --|포함 (감싸기)|--> Component_Interface_Ref["원본 또는 다른 데코레이터"]

        ConcreteDecoratorA["구체적 데코레이터 A"] --|상속|--> Decorator
        ConcreteDecoratorB["구체적 데코레이터 B"] --|상속|--> Decorator
    end

    style Client fill:#dae8fc,stroke:#333,stroke-width:2px
    style Component_Interface fill:#e1d5e7,stroke:#333,stroke-width:2px
    style Component_Interface_Ref fill:#e1d5e7,stroke:#333,stroke-width:2px,stroke-dasharray: 5 5
    style ConcreteComponent fill:#d5e8d4,stroke:#333,stroke-width:2px
    style Decorator fill:#f8cecc,stroke:#333,stroke-width:2px
    style ConcreteDecoratorA fill:#fff2cc,stroke:#333,stroke-width:2px
    style ConcreteDecoratorB fill:#fff2cc,stroke:#333,stroke-width:2px

    %% The 'note' syntax below is not standard for general notes in LR/TD graphs.
    %% To add a note, you typically associate it with a node, e.g.:
    %% note right of Client : 클라이언트는 원본이든...
    %% For now, I've commented out your original note:
    %% note "클라이언트는 원본이든 장식된 객체든 Component_Interface로 동일하게 사용"
```

마치 양파 껍질처럼, 핵심 객체를 여러 데코레이터가 겹겹이 감싸면서 각 데코레이터가 고유한 기능을 추가하는 형태입니다.

## 왜 데코레이터 패턴을 사용할까요?

데코레이터 패턴은 다음과 같은 상황에서 매우 유용합니다:

1. **[[개방-폐쇄 원칙 (OCP)]] 준수**: 기존 객체의 코드를 수정하지 않고 새로운 기능을 추가하거나 확장하고 싶을 때 사용합니다. 새로운 기능은 새로운 데코레이터 클래스로 구현하면 됩니다.
2. **상속으로 인한 클래스 폭발 방지**: 다양한 기능의 조합이 필요한 경우, 상속을 사용하면 기능 조합마다 서브클래스를 만들어야 해서 클래스 수가 기하급수적으로 늘어날 수 있습니다. 데코레이터 패턴은 필요한 데코레이터들을 조합하여 이 문제를 해결합니다. (예: 커피 + 우유, 커피 + 설탕, 커피 + 우유 + 설탕, 커피 + 휘핑...)
3. **동적인 기능 추가/제거의 유연성**: 런타임에 객체에 기능을 동적으로 추가할 수 있습니다. (엄밀히 말해 패턴 자체는 기능 '제거'를 직접 지원하진 않지만, 데코레이터를 선택적으로 적용함으로써 유사한 효과를 낼 수 있습니다.)
4. **객체의 특정 부분에만 기능 확장**: 모든 객체가 아닌 특정 객체 인스턴스에만 기능을 추가하고 싶을 때 유용합니다.

## 데코레이터 패턴의 구조

데코레이터 패턴을 구성하는 주요 참여자는 다음과 같습니다:

- **Component (컴포넌트)**: 모든 객체(원본 객체와 데코레이터)가 공유하는 공통 인터페이스입니다. 클라이언트가 사용할 핵심 연산(operation)을 정의합니다.
- **ConcreteComponent (구체적 컴포넌트)**: `Component` 인터페이스를 구현하는 원본 객체입니다. 이 객체가 바로 장식될 대상입니다.
- **Decorator (데코레이터)**: `Component` 인터페이스를 구현(또는 상속)하면서, 내부에 다른 `Component` 객체(자신이 감싸고 있는 객체, 즉 `wrappedComponent`)를 참조(HAS-A 관계)합니다. 이 참조를 통해 원본 객체의 `operation`을 호출하고, 그 호출 전후에 추가적인 작업을 수행하여 새로운 기능을 덧붙입니다. 보통 추상 클래스로 정의됩니다.
- **ConcreteDecorator (구체적 데코레이터)**: `Decorator`의 서브클래스로, 실제로 추가할 특정 기능을 구현합니다. 여러 종류의 `ConcreteDecorator`가 존재할 수 있으며, 각각 다른 책임을 가집니다.


```mermaid
classDiagram
    Client --> Component
    Component <|-- ConcreteComponent
    Component <|-- Decorator
    Decorator o-- Component : wrappedComponent
    Decorator <|-- ConcreteDecoratorA
    Decorator <|-- ConcreteDecoratorB

    class Component {
        <<interface>>
        +operation() : String
    }
    class ConcreteComponent {
        +name: String
        +ConcreteComponent(name: String)
        +operation() : String
    }
    class Decorator {
        #wrappedComponent: Component
        +Decorator(c: Component)
        +operation() : String
    }
    class ConcreteDecoratorA {
        +ConcreteDecoratorA(c: Component)
        +operation() : String
        -addedBehaviorA() : String
    }
    class ConcreteDecoratorB {
        +ConcreteDecoratorB(c: Component)
        +operation() : String
        -addedBehaviorB() : String
    }
    class Client {
        // Component 사용
    }
    note for Decorator "return wrappedComponent.operation()"
    note for ConcreteDecoratorA "operation() { return wrappedComponent.operation() + addedBehaviorA(); }"
    note for ConcreteDecoratorB "operation() { return addedBehaviorB() + wrappedComponent.operation(); }"
```

## 데코레이터 패턴 예시 (Java 코드)

카페에서 커피를 주문하고 다양한 토핑을 추가하는 시나리오를 Java 코드로 구현해 보겠습니다.

```java
// Component 인터페이스
interface Coffee {
    String getDescription();
    double cost();
}

// ConcreteComponent 클래스: 기본 커피
class SimpleCoffee implements Coffee {
    @Override
    public String getDescription() {
        return "심플 커피";
    }

    @Override
    public double cost() {
        return 2.0;
    }
}

// Decorator 추상 클래스
abstract class CoffeeDecorator implements Coffee {
    protected Coffee decoratedCoffee; // 감싸고 있는 커피 객체

    public CoffeeDecorator(Coffee coffee) {
        this.decoratedCoffee = coffee;
    }

    @Override
    public String getDescription() {
        return decoratedCoffee.getDescription(); // 위임
    }

    @Override
    public double cost() {
        return decoratedCoffee.cost(); // 위임
    }
}

// ConcreteDecorator 클래스들: 토핑
class MilkDecorator extends CoffeeDecorator {
    public MilkDecorator(Coffee coffee) {
        super(coffee);
    }

    @Override
    public String getDescription() {
        return super.getDescription() + ", 우유 추가";
    }

    @Override
    public double cost() {
        return super.cost() + 0.5;
    }
}

class SugarDecorator extends CoffeeDecorator {
    public SugarDecorator(Coffee coffee) {
        super(coffee);
    }

    @Override
    public String getDescription() {
        return super.getDescription() + ", 설탕 추가";
    }

    @Override
    public double cost() {
        return super.cost() + 0.2;
    }
}

class WhipDecorator extends CoffeeDecorator {
    public WhipDecorator(Coffee coffee) {
        super(coffee);
    }

    @Override
    public String getDescription() {
        return super.getDescription() + ", 휘핑크림 추가";
    }

    @Override
    public double cost() {
        return super.cost() + 0.7;
    }
}

// Client
public class CoffeeShop {
    public static void main(String[] args) {
        Coffee myCoffee = new SimpleCoffee();
        System.out.println(myCoffee.getDescription() + " : $" + myCoffee.cost());

        // 우유 추가
        myCoffee = new MilkDecorator(myCoffee);
        System.out.println(myCoffee.getDescription() + " : $" + myCoffee.cost());

        // 설탕 추가
        myCoffee = new SugarDecorator(myCoffee);
        System.out.println(myCoffee.getDescription() + " : $" + myCoffee.cost());

        // 휘핑크림 추가
        myCoffee = new WhipDecorator(myCoffee);
        System.out.println(myCoffee.getDescription() + " : $" + myCoffee.cost());

        System.out.println("\n--- 다른 커피 주문 ---");
        Coffee anotherCoffee = new WhipDecorator(new MilkDecorator(new SimpleCoffee()));
        System.out.println(anotherCoffee.getDescription() + " : $" + anotherCoffee.cost());
    }
}
```

위 코드에서 `Coffee`가 `Component`, `SimpleCoffee`가 `ConcreteComponent`, `CoffeeDecorator`가 `Decorator`, 그리고 `MilkDecorator`, `SugarDecorator`, `WhipDecorator`가 `ConcreteDecorator` 역할을 합니다. 각 데코레이터는 자신이 감싸고 있는 커피 객체의 메서드를 호출한 후 자신의 기능을 덧붙입니다.

## 데코레이터 패턴의 장점

- **유연성**: 필요한 기능을 객체에 동적으로, 그리고 선택적으로 조합하여 추가할 수 있습니다.
- **[[개방-폐쇄 원칙 (OCP)]] 만족**: 기존 코드를 변경하지 않고 새로운 기능을 추가하는 것이 가능합니다. 새로운 데코레이터 클래스만 만들면 됩니다.
- **상속보다 더 나은 대안**: 기능 확장을 위해 상속을 사용하면 클래스 계층이 복잡해지고, 모든 서브클래스가 부모의 모든 기능을 물려받아야 하는 경직성이 생깁니다. 데코레이터는 필요한 기능만 골라 붙일 수 있어 더 유연합니다.
- **[[단일 책임 원칙]] 준수**: 각 데코레이터 클래스는 하나의 추가적인 책임(기능)에만 집중합니다.

## 데코레이터 패턴의 단점

- **작은 객체들이 많이 생성됨**: 많은 데코레이터를 중첩해서 사용하면, 시스템 내에 작은 객체들이 많이 생겨날 수 있습니다. 이는 전체 구조를 파악하거나 디버깅할 때 다소 혼란스러울 수 있습니다.
- **객체의 정체성(Identity) 혼란**: 데코레이팅된 객체의 실제 타입은 가장 바깥쪽 데코레이터의 타입이 됩니다. 내부의 원본 `ConcreteComponent`나 특정 데코레이터 타입을 확인하기 위해 `instanceof`를 연쇄적으로 사용해야 할 수도 있어 번거롭습니다.
- **설정 코드의 복잡성**: 원하는 기능 조합을 만들기 위해 여러 데코레이터 객체를 순서대로 생성하고 연결하는 코드가 다소 장황해질 수 있습니다. (이는 [[빌더 패턴 (Builder Pattern)]] 등을 사용하여 완화할 수 있습니다.)
- **모든 인터페이스를 동일하게 만들기 어려움**: `Component` 인터페이스에 정의되지 않은 메서드를 `ConcreteComponent`가 가지고 있을 경우, 데코레이터는 해당 메서드를 직접적으로 노출할 수 없습니다.

## 실생활 및 프레임워크 예시

데코레이터 패턴은 다양한 곳에서 활용됩니다:

- **Java I/O 클래스**: `java.io` 패키지는 데코레이터 패턴의 고전적인 예시입니다. 예를 들어, `FileInputStream` (ConcreteComponent) 객체를 `BufferedInputStream` (ConcreteDecorator)으로 감싸서 버퍼링 기능을 추가하거나, `DataInputStream` (ConcreteDecorator)으로 감싸서 기본 자료형을 읽는 기능을 추가할 수 있습니다.
    
    Java
    
    ```
    // 예시: Java I/O
    // InputStream in = new BufferedInputStream(new FileInputStream("myFile.txt"));
    ```
    
- **Java Servlet API**: `HttpServletRequestWrapper`와 `HttpServletResponseWrapper` 클래스는 서블릿 요청 및 응답 객체를 감싸서 기능을 추가하거나 수정하는 데 사용될 수 있습니다.
- **GUI 컴포넌트**: 그래픽 사용자 인터페이스(GUI) 라이브러리에서 텍스트 필드에 스크롤바를 추가하거나, 창에 테두리를 그리는 등의 기능을 데코레이터 패턴으로 구현할 수 있습니다.
- **[[스프링 프레임워크 (Spring Framework)]]**: 스프링에서도 프록시 기반의 AOP(관점 지향 프로그래밍)를 구현할 때 데코레이터 패턴과 유사한 개념이 활용되기도 하며, 특정 서비스 객체에 트랜잭션이나 보안 같은 부가 기능을 동적으로 추가하는 데 사용될 수 있습니다.

## 결론

데코레이터 패턴은 객체의 코드를 변경하지 않으면서도 객체에 새로운 책임을 유연하게 추가할 수 있는 강력한 방법입니다. 특히 다양한 기능의 조합이 필요하거나, [[개방-폐쇄 원칙]]을 지키며 시스템을 확장하고 싶을 때 훌륭한 선택이 될 수 있습니다.

물론, 작은 객체가 많아지거나 설정이 복잡해질 수 있다는 단점도 있지만, 패턴이 제공하는 유연성과 확장성은 이러한 단점을 충분히 상쇄하고도 남습니다. 프로젝트의 특성과 요구사항을 잘 고려하여 데코레이터 패턴을 적재적소에 활용한다면 더욱 견고하고 유연한 시스템을 구축할 수 있을 것입니다.

다음 디자인 패턴 이야기도 기대해주세요! 읽어주셔서 감사합니다.