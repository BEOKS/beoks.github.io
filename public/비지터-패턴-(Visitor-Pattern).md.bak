### **비지터 패턴이란 무엇일까요?**

비지터 패턴의 핵심 아이디어는 **데이터 구조와 해당 데이터를 처리하는 알고리즘을 분리**하는 것입니다. 즉, 데이터(Element)는 자신의 구조만 잘 유지하고, 실제 처리 로직(Visitor)은 외부의 "방문자"에게 맡기는 방식입니다.

예를 들어, 쇼핑 카트에 여러 종류의 상품(책, 전자제품, 식료품 등)이 담겨 있다고 상상해봅시다. 각 상품의 '가격을 계산하는' 기능과 '배송 무게를 계산하는' 기능이 필요하다면, 보통 각 상품 클래스 안에 `getPrice()`, `getWeight()` 같은 메서드를 추가할 것입니다. 하지만 여기에 '할인 가격 계산', '포장 비용 계산' 등 새로운 기능이 계속 추가된다면 어떻게 될까요? 상품 클래스들은 점점 비대해지고, 새로운 기능을 추가할 때마다 모든 상품 클래스를 수정해야 하는 번거로움이 생깁니다.

비지터 패턴은 바로 이 문제를 해결합니다. '가격 계산 Visitor', '무게 계산 Visitor'와 같은 방문자를 만들어, 이들이 쇼핑 카트를 "방문"하면서 각 상품에 맞는 계산을 수행하도록 하는 것입니다. 이렇게 하면 **기존 상품 클래스(데이터 구조)는 전혀 수정하지 않고도 새로운 기능을 무한히 추가**할 수 있습니다.

---

### **비지터 패턴의 구조와 더블 디스패치**

비지터 패턴은 다소 복잡한 구조를 가지며, 그 중심에는 **더블 디스패치(Double Dispatch)**라는 기술이 있습니다.

1. **Visitor (방문자)**: 데이터 구조의 각 `ConcreteElement`를 "방문"하는 `visit()` 메서드를 선언합니다. `visit()` 메서드는 처리할 요소의 타입별로 오버로딩됩니다.
2. **ConcreteVisitor (구체적인 방문자)**: `Visitor` 인터페이스를 구현하며, 각 `visit()` 메서드 안에 실제 처리 알고리즘을 담습니다.
3. **Element (요소)**: "방문"을 받아들일 `accept(Visitor v)` 메서드를 선언합니다.
4. **ConcreteElement (구체적인 요소)**: `Element` 인터페이스를 구현하며, `accept(Visitor v)` 메서드 안에서 `visitor.visit(this)`를 호출합니다.
5. **ObjectStructure (객체 구조)**: `Element`들을 관리하는 컨테이너 역할을 하며, 모든 요소가 `Visitor`를 순차적으로 받아들일 수 있는 인터페이스를 제공합니다.

이 복잡한 상호작용을 `Mermaid`로 표현하면 다음과 같습니다.

```mermaid
sequenceDiagram
    participant Client
    participant ObjectStructure
    participant ConcreteElementA
    participant ConcreteVisitor

    Client->>ObjectStructure: executeOperation(visitor)
    ObjectStructure->>ConcreteElementA: accept(visitor)
    Note right of ConcreteElementA: 첫 번째 디스패치: <br/>어떤 Element의 accept()가 <br/>호출될지 결정됩니다.
    ConcreteElementA->>ConcreteVisitor: visit(this)
    Note right of ConcreteVisitor: 두 번째 디스패치: <br/>Element의 실제 타입에 맞는 <br/>어떤 Visitor의 visit() 메서드가 <br/>호출될지 결정됩니다.
    ConcreteVisitor-->>Client: 결과 반환
```

여기서 핵심은 **더블 디스패치**입니다.

1. 첫 번째 디스패치: 클라이언트는 `ConcreteElement`의 `accept(visitor)`를 호출합니다. 어떤 `accept()` 메서드가 호출될지는 `ConcreteElement`의 실제 타입에 따라 결정됩니다. (`ConcreteElementA` 인가, `ConcreteElementB` 인가?)
2. 두 번째 디스패치: `accept()` 메서드 내부에서는 다시 `visitor.visit(this)`를 호출합니다. 이때 `this`는 `ConcreteElement`의 실제 인스턴스입니다. 컴파일러는 `this`의 타입을 정확히 알고 있으므로, `Visitor`에 정의된 여러 `visit()` 메서드 중에서 **정확한 타입의 `ConcreteElement`를 파라미터로 받는 메서드를 호출**할 수 있습니다.

이 과정을 통해 실행 시점에 객체의 타입과 수행할 연산의 종류, 이 두 가지를 모두 동적으로 선택할 수 있게 됩니다.

---

### **왜 비지터 패턴을 사용해야 할까요?**

비지터 패턴을 사용하면 다음과 같은 장점을 얻을 수 있습니다.

- **[[개방-폐쇄 원칙 (Open-Closed Principle)]] 준수**: 기존의 `Element` 클래스들을 전혀 수정하지 않고도 새로운 연산(`Visitor`)을 추가할 수 있습니다.
- **관심사의 분리**: 데이터 구조와 그 위에서 동작하는 알고리즘을 명확하게 분리할 수 있습니다.
- **코드 정리**: 관련 연산들을 하나의 `ConcreteVisitor` 클래스에 모아둘 수 있어 코드 구조가 깔끔해집니다.

하지만 명확한 단점도 존재합니다.

- **새로운 Element 추가의 어려움**: 새로운 `ConcreteElement` 클래스를 추가하려면 모든 `Visitor` 인터페이스와 `ConcreteVisitor` 클래스에 해당 요소를 처리하는 `visit()` 메서드를 추가해야 합니다. 이는 OCP를 위반하는 결과를 낳습니다.

따라서 비지터 패턴은 **데이터 구조는 비교적 안정적으로 유지되면서, 그 구조에 대한 새로운 연산이 자주 추가될 가능성이 높은 경우**에 가장 적합합니다.

---

### **Java에서의 비지터 패턴 활용**

컴퓨터 부품(CPU, RAM)으로 구성된 컴퓨터를 예로 들어, 각 부품의 정보를 출력하는 `Visitor`를 구현해 보겠습니다.


```java
// Element Interface
interface ComputerPart {
    void accept(ComputerPartVisitor visitor);
}

// Visitor Interface
interface ComputerPartVisitor {
    void visit(Computer computer);
    void visit(Cpu cpu);
    void visit(Ram ram);
}

// ConcreteElements
class Cpu implements ComputerPart {
    @Override
    public void accept(ComputerPartVisitor visitor) {
        visitor.visit(this);
    }
}

class Ram implements ComputerPart {
    @Override
    public void accept(ComputerPartVisitor visitor) {
        visitor.visit(this);
    }
}

// ObjectStructure
class Computer implements ComputerPart {
    ComputerPart[] parts;

    public Computer() {
        parts = new ComputerPart[] {new Cpu(), new Ram()};
    }

    @Override
    public void accept(ComputerPartVisitor visitor) {
        for (ComputerPart part : parts) {
            part.accept(visitor);
        }
        visitor.visit(this);
    }
}

// ConcreteVisitor
class PartDisplayVisitor implements ComputerPartVisitor {
    @Override
    public void visit(Computer computer) {
        System.out.println("Displaying Computer.");
    }

    @Override
    public void visit(Cpu cpu) {
        System.out.println("Displaying CPU.");
    }

    @Override
    public void visit(Ram ram) {
        System.out.println("Displaying RAM.");
    }
}

// Client
public class VisitorPatternDemo {
    public static void main(String[] args) {
        ComputerPart computer = new Computer();
        computer.accept(new PartDisplayVisitor());
    }
}
```

이제 만약 '가격 계산' 기능을 추가하고 싶다면, `Computer`, `Cpu`, `Ram` 클래스는 전혀 건드리지 않고, `PriceCalculatorVisitor`라는 새로운 Visitor만 만들어서 `accept()` 메서드에 넘겨주기만 하면 됩니다.

---

### **스프링 프레임워크와 비지터 패턴**

[[스프링 프레임워크(Spring Framework)]] 내부에서도 비지터 패턴의 원리를 찾아볼 수 있습니다. 대표적인 예는 `BeanDefinitionVisitor` 입니다.

스프링 컨테이너는 애플리케이션의 빈(Bean) 설정 메타데이터(`BeanDefinition`)를 관리합니다. `BeanDefinitionVisitor`는 이 `BeanDefinition` 구조를 순회하면서 특정 작업을 수행하는 데 사용됩니다. 예를 들어, `BeanDefinition`에 정의된 프로퍼티 값(예: `${...}`)을 실제 값으로 교체하는 `PropertyPlaceholderConfigurer`의 내부 동작은 `BeanDefinitionVisitor`를 사용하여 구현됩니다.

이를 통해 스프링은 `BeanDefinition`이라는 핵심 데이터 구조는 변경하지 않으면서, 플레이스홀더 치환, 속성 오버라이딩 등 다양한 부가 기능을 `Visitor`를 통해 유연하게 처리합니다. 자세한 내용은 [[스프링 BeanDefinition 처리 과정]]을 참고해주세요.

---

### **결론**

비지터 패턴은 처음 접하면 더블 디스패치 개념 때문에 다소 어렵게 느껴질 수 있습니다. 하지만 그 원리를 이해하고 나면, **데이터 구조의 안정성을 유지하면서 기능 확장을 우아하게 처리**할 수 있는 매우 강력한 도구임을 알게 됩니다.

객체 구조는 거의 변하지 않지만, 수행해야 할 작업이 자주 바뀌거나 추가되는 시나리오를 마주한다면, 비지터 패턴이 여러분의 코드를 한 단계 더 높은 수준으로 끌어올려 줄 훌륭한 해결책이 될 것입니다.