상태 패턴은 **객체의 내부 상태가 변경됨에 따라 객체의 행위를 변경할 수 있게 하는** 행위 디자인 패턴입니다. 이 패턴을 사용하면, 상태에 따라 달라지는 복잡한 `if-else` 나 `switch` 문을 사용하는 대신, **마치 객체의 클래스가 바뀌는 것처럼** 보이게 하여 코드를 훨씬 깔끔하고 직관적으로 만들 수 있습니다.

가장 대표적인 예시는 자판기입니다. 자판기는 '동전 없음', '동전 있음', '상품 품절' 등 여러 상태를 가집니다.

- **동전 없음 상태**: 동전을 넣을 수만 있습니다. 상품 선택 버튼을 눌러도 반응이 없습니다.
- **동전 있음 상태**: 상품을 선택할 수 있습니다. 동전을 더 넣거나 반환받을 수도 있습니다.
- **상품 품절 상태**: 어떤 행동을 해도 "품절"이라는 메시지만 보여줍니다.

이처럼 자판기(객체)의 현재 상태가 무엇이냐에 따라, 사용자의 행동에 대한 반응(메서드 결과)이 완전히 달라집니다. 상태 패턴은 이러한 각 '상태'를 별도의 클래스로 캡슐화하여 관리하는 방법입니다.

### 상태 패턴이 해결하고자 하는 문제

상태 패턴이 없다면, 우리는 자판기의 모든 동작 메서드 안에 현재 상태를 확인하는 조건문을 넣어야 합니다.

```java
public class VendingMachine {
    private State state = State.NO_COIN; // NO_COIN, HAS_COIN, SOLD_OUT

    public void insertCoin() {
        if (state == State.HAS_COIN) {
            System.out.println("이미 동전이 있습니다.");
        } else if (state == State.NO_COIN) {
            System.out.println("동전을 넣었습니다.");
            this.state = State.HAS_COIN;
        } else if (state == State.SOLD_OUT) {
            System.out.println("품절입니다. 동전이 반환됩니다.");
        }
    }

    public void selectItem() {
        if (state == State.HAS_COIN) {
            System.out.println("상품이 나왔습니다.");
            this.state = State.NO_COIN;
        } else if (state == State.NO_COIN) {
            System.out.println("동전을 먼저 넣어주세요.");
        } else if (state == State.SOLD_OUT) {
            System.out.println("품절입니다.");
        }
    }
    // ... 다른 모든 메서드에도 이런 조건문이 반복됨
}
```

이런 코드는 새로운 상태('예열 중' 등)가 추가될 때마다 모든 메서드의 조건문을 수정해야 하므로 [[개방-폐쇄 원칙 (Open-Closed Principle)]]에 위배되며, 코드가 복잡해지고 버그가 발생하기 쉽습니다.

### 핵심 구성 요소

상태 패턴은 이 문제를 해결하기 위해 상태와 행위를 다음과 같이 분리합니다.

- **Context (컨텍스트)**: 상태를 가지는 객체입니다. 현재 상태를 나타내는 `State` 객체의 인스턴스를 가지고 있으며, 상태에 따른 실제 행동은 현재의 `State` 객체에게 위임합니다. 또한, `State` 객체가 컨텍스트의 상태를 변경할 수 있도록 자신의 인스턴스를 `State` 객체에게 전달합니다.
- **State (상태 인터페이스)**: 컨텍스트가 가질 수 있는 모든 상태들의 공통 인터페이스입니다. 각 상태에서 수행될 수 있는 모든 행동에 대한 메서드를 정의합니다.
- **ConcreteState (구체적인 상태)**: `State` 인터페이스를 구현한 클래스입니다. 특정 상태에서 수행될 행동을 구체적으로 구현합니다. 또한, 특정 행동이 수행된 후 **다음 상태로 전환하는 책임**을 가집니다.

```mermaid
stateDiagram-v2
    direction LR
    [*] --> Draft

    Draft --> InReview : review()
    InReview --> Published : publish()
    Published --> [*]
```

위 다이어그램은 문서(Document)의 상태 변화를 보여줍니다. 문서의 상태는 `Draft` -> `InReview` -> `Published`로 전환될 수 있습니다. 상태 패턴은 `Draft`, `InReview`, `Published`를 각각 별도의 `State` 클래스로 만드는 것입니다.

### Java 예시 코드: 온라인 문서의 상태 관리

온라인 문서가 '초안(Draft)', '검토 중(In Review)', '발행됨(Published)' 상태를 가지는 시스템을 구현해 보겠습니다.

```java
// Context 클래스
public class Document {
    private State currentState;
    private String content;

    public Document() {
        // 초기 상태는 '초안'
        this.currentState = new DraftState(); 
    }

    // 상태를 변경하는 메서드
    public void changeState(State newState) {
        this.currentState = newState;
    }

    // 행동을 현재 상태 객체에 위임
    public void review() {
        currentState.review(this);
    }

    public void publish() {
        currentState.publish(this);
    }
    // Getter, Setter...
}


// State 인터페이스
public interface State {
    void review(Document document);
    void publish(Document document);
}


// ConcreteState 1: 초안 상태
public class DraftState implements State {
    @Override
    public void review(Document document) {
        System.out.println("문서를 '검토 중' 상태로 변경합니다.");
        document.changeState(new InReviewState()); // 상태 전환
    }

    @Override
    public void publish(Document document) {
        System.out.println("초안 상태에서는 발행할 수 없습니다.");
    }
}

// ConcreteState 2: 검토 중 상태
public class InReviewState implements State {
    @Override
    public void review(Document document) {
        System.out.println("이미 검토 중인 문서입니다.");
    }

    @Override
    public void publish(Document document) {
        System.out.println("문서를 '발행'합니다.");
        document.changeState(new PublishedState()); // 상태 전환
    }
}

// ConcreteState 3: 발행됨 상태
public class PublishedState implements State {
    @Override
    public void review(Document document) {
        System.out.println("이미 발행된 문서는 검토할 수 없습니다.");
    }

    @Override
    public void publish(Document document) {
        System.out.println("이미 발행된 문서입니다.");
    }
}
```

`Document`(Context) 클래스에는 더 이상 복잡한 `if-else` 문이 없습니다. 모든 로직은 각 `ConcreteState` 클래스 내부로 캡슐화되었습니다. `document.review()`를 호출하면, `Document`는 어떤 로직을 수행할지 고민하지 않고 현재 상태 객체(`currentState`)에게 "네가 알아서 처리해"라고 위임합니다. 상태 전환의 책임도 `State` 객체 자신이 가지게 되어 각 객체의 책임이 명확해집니다.

### [[전략 패턴 (Strategy Pattern)]]과의 비교

상태 패턴은 클래스 다이어그램 구조가 [[전략 패턴 (Strategy Pattern)]]과 거의 동일하여 혼동하기 쉽지만, **의도**가 완전히 다릅니다.

|   |   |   |
|---|---|---|
|**구분**|**상태 패턴 (State Pattern)**|**전략 패턴 (Strategy Pattern)**|
|**의도**|객체의 **상태**에 따라 행위를 변경|클라이언트가 선택한 **알고리즘**을 동적으로 교체|
|**상태 변경 주체**|**상태 객체 자신** 또는 **컨텍스트**가 내부적으로 결정|**클라이언트(외부)**가 명시적으로 전략을 선택하여 변경|
|**관심사**|"지금 어떤 상태인가?"에 따른 행동의 변화|"어떤 알고리즘을 사용할 것인가?"에 대한 선택|
|**상태 객체 간의 관계**|각 상태 객체는 다음 상태 객체를 알고 있음 (상태 전환을 위해)|각 전략 객체는 서로를 알지 못하며, 독립적임|
|**예시**|자판기, 문서 라이프사이클, 신호등|결제 방법, 정렬 알고리즘, 압축 방식|

간단히 말해, **상태 패턴은 내부 상태에 따라 행동이 '자동으로' 바뀌는 것**에 초점을 맞추고, **전략 패턴은 클라이언트가 필요에 따라 행동을 '선택하여' 바꾸는 것**에 초점을 맞춥니다.

### 스프링 프레임워크에서의 활용: Spring Statemachine

복잡한 상태 관리가 필요한 애플리케이션을 위해, 스프링은 **[[Spring Statemachine]]**이라는 별도의 프로젝트를 제공합니다. 이 프로젝트는 상태 패턴을 기반으로 상태, 전이(transition), 액션(action) 등을 어노테이션과 빌더를 통해 매우 선언적으로 구성할 수 있게 해줍니다.

Spring Statemachine을 사용하면 상태 머신의 구성, 이벤트에 따른 상태 전이, 특정 상태 진입/이탈 시의 액션 등을 스프링의 DI 컨테이너와 통합하여 체계적으로 관리할 수 있습니다. 수십 개의 상태와 복잡한 전이 규칙을 가진 시스템을 개발해야 한다면, 직접 상태 패턴을 구현하기보다는 Spring Statemachine 사용을 적극적으로 고려하는 것이 좋습니다.