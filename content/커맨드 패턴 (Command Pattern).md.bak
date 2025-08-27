**커맨드 패턴**은 요청을 객체의 형태로 캡슐화하여, 요청하는 객체(Invoker)와 요청을 처리하는 객체(Receiver)를 분리하는 행동 디자인 패턴입니다. 📝 이 패턴을 사용하면 요청에 필요한 모든 정보(메서드 이름, 매개변수 등)를 커맨드 객체에 저장하여, 요청을 큐에 쌓거나, 로그로 기록하거나, 작업 취소(Undo) 및 재실행(Redo) 기능을 구현할 수 있습니다.

---

### 커맨드 패턴의 주요 구성 요소

커맨드 패턴은 주로 네 가지 주요 역할로 구성됩니다.

- **Command (커맨드)**: 실행될 기능에 대한 인터페이스입니다. 모든 구체적인 커맨드 클래스들은 이 인터페이스를 구현해야 하며, 보통 `execute()`라는 단일 메서드를 가집니다.
- **ConcreteCommand (구체적인 커맨드)**: `Command` 인터페이스를 구현하며, 실제 요청을 처리하는 `Receiver` 객체에 대한 참조를 가집니다. `execute()` 메서드가 호출되면 `Receiver`의 특정 메서드를 호출하여 작업을 수행합니다.
- **Invoker (호출자)**: `Command` 객체를 저장하고, 특정 시점에 해당 `Command`의 `execute()` 메서드를 호출하여 요청을 실행합니다. `Invoker`는 `ConcreteCommand`가 어떻게 동작하는지 알 필요 없이 오직 `Command` 인터페이스에만 의존합니다.
- **Receiver (수신자)**: 요청을 실제로 처리하는 객체입니다. `ConcreteCommand`에 의해 호출되는 비즈니스 로직을 포함하고 있습니다.
- **Client (클라이언트)**: `Receiver` 객체를 생성하고, `ConcreteCommand` 객체를 생성하여 `Receiver`와 연결한 뒤, 이 `ConcreteCommand`를 `Invoker`에 설정합니다.

---

### 커맨드 패턴의 장점

- **요청자와 수신자의 분리**: 요청을 보내는 객체와 실제 기능을 수행하는 객체 사이의 결합도를 낮출 수 있습니다. 이를 통해 코드의 유연성과 확장성이 향상됩니다.
- **작업 취소 및 재실행 기능**: 커맨드 객체에 실행 취소(`undo()`) 메서드를 추가하여, 수행된 작업을 되돌리거나 다시 실행하는 기능을 비교적 쉽게 구현할 수 있습니다.
- **요청의 큐잉 및 로깅**: 커맨드 객체 자체를 큐에 저장하여 순차적으로 처리하거나, 실행된 커맨드를 로그로 남겨 시스템의 상태를 추적하고 복구하는 데 사용할 수 있습니다.
- **다양한 요청의 매개변수화**: 새로운 기능을 추가하고 싶을 때, 새로운 `ConcreteCommand` 클래스를 만들기만 하면 되므로 기존 코드를 수정할 필요가 없습니다 (개방-폐쇄 원칙, OCP).

---

### 간단한 예시: 리모컨

가장 흔한 예시 중 하나는 다양한 가전제품을 제어하는 리모컨입니다.

- **Client**: 리모컨 버튼에 기능을 설정하는 사용자입니다.
- **Invoker**: 리모컨(`SimpleRemoteControl`) 객체입니다. `Command` 객체를 저장할 슬롯(버튼)이 있습니다.
- **Command**: `Command` 인터페이스입니다. `execute()` 메서드를 가집니다.
- **ConcreteCommand**:
    - `LightOnCommand`: 전등을 켜는 명령.
    - `GarageDoorOpenCommand`: 차고 문을 여는 명령.
- **Receiver**:
    - `Light`: 전등 객체. `on()`, `off()` 메서드를 가집니다.
    - `GarageDoor`: 차고 문 객체. `open()`, `close()` 메서드를 가집니다.

**자바(Java) 코드 예시:**
```java
// Command 인터페이스
public interface Command {
    public void execute();
}

// Receiver: 전등
public class Light {
    public void on() {
        System.out.println("전등이 켜졌습니다.");
    }
}

// ConcreteCommand: 전등 켜기 커맨드
public class LightOnCommand implements Command {
    Light light;

    public LightOnCommand(Light light) {
        this.light = light;
    }

    public void execute() {
        light.on();
    }
}

// Invoker: 리모컨
public class SimpleRemoteControl {
    Command slot;

    public void setCommand(Command command) {
        slot = command;
    }

    public void buttonWasPressed() {
        slot.execute();
    }
}

// Client
public class RemoteControlTest {
    public static void main(String[] args) {
        SimpleRemoteControl remote = new SimpleRemoteControl();
        Light light = new Light();
        LightOnCommand lightOn = new LightOnCommand(light);

        remote.setCommand(lightOn);
        remote.buttonWasPressed(); // "전등이 켜졌습니다." 출력
    }
}
```

이 예시에서 `SimpleRemoteControl`(Invoker)은 자신이 실행하는 것이 `LightOnCommand`인지 전혀 알지 못합니다. 그저 `execute()` 메서드를 가진 `Command` 객체를 실행할 뿐입니다. 이로 인해 리모컨 코드의 변경 없이도 다른 `Command`(예: `GarageDoorOpenCommand`)를 할당하여 다양한 기능을 수행할 수 있습니다.