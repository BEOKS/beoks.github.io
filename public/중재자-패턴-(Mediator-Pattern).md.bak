### **중재자 패턴이란 무엇일까요?**

**중재자 패턴**은 여러 객체(Colleague)들이 서로 직접 통신하지 않고, **중재자(Mediator)**라는 하나의 객체를 통해서만 소통하도록 만드는 디자인 패턴입니다. 객체들은 더 이상 서로를 알 필요가 없으며, 오직 중재자에게만 메시지를 보내고 받습니다.

마치 항공 관제탑과 같습니다. 수많은 비행기들이 서로 직접 통신하며 이착륙 순서를 정한다면 큰 혼란이 발생하고 충돌 위험도 높아질 것입니다. 대신 모든 비행기는 관제탑과만 통신하고, 관제탑이 각 비행기의 이착륙을 조율하고 지시합니다. 여기서 **관제탑이 중재자**, **각 비행기가 동료 객체(Colleague)** 역할을 하는 것입니다.

이 패턴은 객체 간의 관계가 복잡한 그물망(many-to-many) 구조일 때, 이를 중앙 집중적인 스타(star) 구조로 단순화하여 시스템의 [[결합도(Coupling)]]를 획기적으로 낮춥니다.

---

### **중재자 패턴의 구조**

중재자 패턴은 다음의 주요 역할들로 구성됩니다.

1. **Mediator (중재자)**: Colleague 객체들과 통신하는 인터페이스를 정의합니다.
2. **ConcreteMediator (구체적인 중재자)**: `Mediator` 인터페이스를 구현하며, Colleague 객체 간의 통신을 실제로 조정합니다. 모든 Colleague를 알고 있어야 하며, 이들의 상태를 관리하고 복잡한 상호작용 로직을 처리합니다.
3. **Colleague (동료)**: 다른 Colleague와 통신해야 하는 객체들의 인터페이스를 정의합니다. `Mediator` 객체를 참조합니다.
4. **ConcreteColleague (구체적인 동료)**: `Colleague` 인터페이스를 구현하며, 자신의 `Mediator`를 통해 다른 Colleague와 통신합니다.

```mermaid
classDiagram
    class Mediator {
        <<interface>>
        +mediate(colleague: Colleague)
    }
    class ConcreteMediator {
        -colleagueA: ConcreteColleagueA
        -colleagueB: ConcreteColleagueB
        +setColleagueA(colleagueA)
        +setColleagueB(colleagueB)
        +mediate(colleague: Colleague)
    }
    class Colleague {
        <<abstract>>
        #mediator: Mediator
        +Colleague(mediator)
    }
    class ConcreteColleagueA {
        +doSomething()
    }
    class ConcreteColleagueB {
        +doSomethingElse()
    }

    Mediator <|-- ConcreteMediator
    Colleague <|-- ConcreteColleagueA
    Colleague <|-- ConcreteColleagueB
    ConcreteMediator --> Colleague : knows
    Colleague --> Mediator : communicates via
    Client --> ConcreteMediator : creates
    Client --> ConcreteColleagueA : creates
    Client --> ConcreteColleagueB : creates
```

- **Client**: `ConcreteMediator`와 `ConcreteColleague` 객체들을 생성하고 연결합니다.
- **ConcreteColleague**: 어떤 이벤트가 발생하면 `Mediator`에게 알립니다 (`mediate()` 호출).
- **ConcreteMediator**: 한 `Colleague`로부터 메시지를 받으면, 그에 따른 로직을 수행하고 필요한 다른 `Colleague`들에게 행동을 지시합니다.

---

### **왜 중재자 패턴을 사용해야 할까요?**

중재자 패턴을 도입하면 얻을 수 있는 이점은 명확합니다.

- **결합도 감소**: Colleague 객체들은 서로 직접 알 필요가 없으며, 오직 `Mediator`만 알면 됩니다. 이는 객체 간의 의존성을 크게 줄여줍니다.
- **재사용성 증가**: 각 Colleague 객체는 다른 Colleague들과 직접적인 연결이 없으므로, 다른 시스템에서 재사용하기가 더 쉬워집니다.
- **중앙 집중 제어**: 객체 간의 복잡한 상호작용 로직이 `Mediator` 한 곳에 집중됩니다. 이로 인해 시스템의 동작을 이해하고 관리하기가 수월해집니다.
- **유지보수 용이성**: 상호작용 로직을 변경해야 할 때, 여러 Colleague 클래스를 수정할 필요 없이 `Mediator` 클래스만 수정하면 됩니다.

하지만 단점도 존재합니다. 모든 로직이 `Mediator`에 집중되면서 **`Mediator` 자체가 비대해지고 복잡해질 수 있습니다 (God Object)**. 이는 오히려 유지보수를 더 어렵게 만들 수 있으므로, 패턴을 적용할 때 신중한 설계가 필요합니다.

---

### **Java에서의 중재자 패턴 활용**

간단한 채팅방 예제를 통해 중재자 패턴을 이해해 보겠습니다. 여러 명의 사용자가 채팅방(중재자)을 통해 메시지를 주고받는 상황입니다.

```java
import java.util.ArrayList;
import java.util.List;

// Mediator Interface
interface ChatMediator {
    void sendMessage(String msg, User user);
    void addUser(User user);
}

// Colleague (Abstract)
abstract class User {
    protected ChatMediator mediator;
    protected String name;

    public User(ChatMediator mediator, String name) {
        this.mediator = mediator;
        this.name = name;
    }

    public abstract void send(String msg);
    public abstract void receive(String msg);
}

// ConcreteMediator
class ChatRoom implements ChatMediator {
    private List<User> users;

    public ChatRoom() {
        this.users = new ArrayList<>();
    }

    @Override
    public void addUser(User user) {
        this.users.add(user);
    }

    @Override
    public void sendMessage(String msg, User user) {
        // 메시지를 보낸 사용자를 제외한 모든 사용자에게 메시지 전송
        for (User u : this.users) {
            if (u != user) {
                u.receive(msg);
            }
        }
    }
}

// ConcreteColleague
class ChatUser extends User {
    public ChatUser(ChatMediator mediator, String name) {
        super(mediator, name);
    }

    @Override
    public void send(String msg) {
        System.out.println(this.name + " sends: " + msg);
        mediator.sendMessage(msg, this);
    }

    @Override
    public void receive(String msg) {
        System.out.println(this.name + " receives: " + msg);
    }
}

// Client
public class MediatorPatternDemo {
    public static void main(String[] args) {
        ChatMediator chatRoom = new ChatRoom();

        User user1 = new ChatUser(chatRoom, "Alice");
        User user2 = new ChatUser(chatRoom, "Bob");
        User user3 = new ChatUser(chatRoom, "Charlie");

        chatRoom.addUser(user1);
        chatRoom.addUser(user2);
        chatRoom.addUser(user3);

        user1.send("Hi everyone!");
    }
}
```

이 예제에서 `ChatUser` 객체들은 서로의 존재를 모릅니다. 메시지를 보낼 때 오직 `ChatRoom`(중재자)에게 전달할 뿐입니다. 그러면 `ChatRoom`이 알아서 다른 모든 사용자에게 메시지를 전달해 줍니다. 새로운 사용자가 추가되거나 기존 사용자가 나가더라도 `ChatUser` 코드는 전혀 변경할 필요가 없습니다.

---

### **스프링 프레임워크와 중재자 패턴**

[[스프링 프레임워크(Spring Framework)]]의 핵심 컴포넌트 중 하나인 **`DispatcherServlet`**은 중재자 패턴의 좋은 예시입니다.

웹 애플리케이션에서 클라이언트의 요청이 들어오면, `DispatcherServlet`이 가장 먼저 요청을 받습니다. 그 후, 이 `DispatcherServlet`이 중재자 역할을 수행하며 요청을 처리할 적절한 핸들러(`@Controller`)를 찾고(`HandlerMapping`), 핸들러를 실행하며(`HandlerAdapter`), 결과를 뷰(`ViewResolver`, `View`)로 전달하여 최종 응답을 생성하는 모든 과정을 조율합니다.

`Controller`, `HandlerMapping`, `ViewResolver` 등의 컴포넌트들은 서로 직접 통신하지 않고, 오직 `DispatcherServlet`을 통해서만 상호작용합니다. 이 구조 덕분에 각 컴포넌트는 자신의 책임에만 집중할 수 있으며, 전체 웹 요청 처리 흐름은 `DispatcherServlet`에 의해 중앙에서 관리됩니다.

---

### **결론**

중재자 패턴은 여러 객체가 얽혀있는 복잡한 관계를 단순하고 명확한 구조로 재구성하는 강력한 도구입니다. 객체 간의 결합도를 낮춰 시스템 전체의 유연성과 확장성, 유지보수성을 향상시킵니다.

물론 중재자 객체가 너무 많은 책임을 떠안아 복잡해질 위험도 있지만, 객체 간의 상호작용이 명확히 정의되고 통제되어야 하는 상황이라면 중재자 패턴은 훌륭한 해결책이 될 수 있습니다. 여러분의 코드에 얽히고설킨 스파게티 코드가 보인다면, 중재자 패턴 도입을 고려해 보시는 건 어떨까요? 😉