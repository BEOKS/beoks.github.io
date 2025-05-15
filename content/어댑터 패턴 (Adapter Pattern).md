일상생활에서 해외여행을 갈 때, 우리나라에서 쓰던 전자제품을 외국에서 사용하려면 "돼지코"라고 불리는 여행용 어댑터가 필요한 경우가 있죠? 전압이나 플러그 모양이 달라서 바로 사용할 수 없기 때문인데요. 어댑터 패턴은 소프트웨어 세계에서 바로 이 "돼지코"와 같은 역할을 합니다.

## 어댑터 패턴이란 무엇인가요?

**어댑터 패턴 (Adapter Pattern)** 은 호환되지 않는 인터페이스를 가진 클래스들을 함께 동작할 수 있도록 변환해주는 패턴입니다. 즉, 특정 [[인터페이스]]를 기대하는 클라이언트 코드를 변경하지 않고, 기존에 만들어진 클래스(Adaptee)를 재사용하고 싶을 때 중간에서 둘 사이의 인터페이스 불일치를 해소하는 역할을 합니다.

```mermaid
graph LR
    Client -->|Target 인터페이스 호출| Adapter
    Adapter -->|Adaptee 메서드 호출| Adaptee((Adaptee))

    subgraph 클라이언트 영역
        Client
    end
    subgraph 어댑터 영역
        Adapter
    end
    subgraph 기존 시스템 영역
        Adaptee
    end

    style Client fill:#dae8fc,stroke:#333,stroke-width:2px
    style Adapter fill:#f8cecc,stroke:#333,stroke-width:2px
    style Adaptee fill:#d5e8d4,stroke:#333,stroke-width:2px
```

위 그림처럼 클라이언트는 자신이 기대하는 `Target` 인터페이스만을 바라보고 작업을 요청하지만, 어댑터는 내부적으로 `Adaptee`의 기능을 활용하여 클라이언트의 요청을 처리합니다.

## 왜 어댑터 패턴을 사용할까요?

어댑터 패턴은 다음과 같은 상황에서 유용하게 사용될 수 있습니다:

1. **기존 코드의 재사용**: 이미 잘 만들어져 있고 검증된 클래스(Adaptee)가 있지만, 현재 시스템에서 요구하는 인터페이스와 달라서 바로 사용할 수 없을 때, 어댑터를 통해 재사용할 수 있습니다.
2. **외부 라이브러리 또는 레거시 시스템 통합**: 우리가 직접 수정할 수 없는 외부 라이브러리나 오래된 시스템의 기능을 현재 시스템에 통합해야 할 때, 인터페이스 불일치 문제를 해결할 수 있습니다.
3. **클라이언트 코드 변경 최소화**: 클라이언트는 일관된 인터페이스(`Target`)를 사용하므로, Adaptee가 변경되거나 다른 Adaptee로 교체되더라도 클라이언트 코드의 변경을 최소화할 수 있습니다.

## 어댑터 패턴의 구조

어댑터 패턴을 구성하는 주요 참여자는 다음과 같습니다:

- **Target**: 클라이언트가 사용하고자 하는 인터페이스입니다. 클라이언트는 이 인터페이스를 통해 기능을 요청합니다.
- **Adaptee**: 기존에 존재하며 재사용하고자 하는, 하지만 호환되지 않는 인터페이스를 가진 클래스입니다. "적응 대상"이라고 생각할 수 있습니다.
- **Adapter**: `Target` 인터페이스를 구현하고, 내부적으로 `Adaptee` 객체의 메서드를 호출하여 `Target`의 요청을 `Adaptee`가 이해할 수 있는 형태로 변환합니다. `Target`과 `Adaptee` 사이의 통역사 역할을 합니다.
- **Client**: `Target` 인터페이스를 통해 `Adapter` 객체를 사용하는 코드입니다. 클라이언트는 `Adapter`가 내부적으로 `Adaptee`를 사용한다는 사실을 알 필요가 없습니다.

이들의 관계를 다이어그램으로 표현하면 다음과 같습니다.

```mermaid
classDiagram
    Client --> Target
    Target <|.. Adapter
    Adapter ..> Adaptee : uses

    class Client {
        + request(target: Target)
    }
    class Target {
        <<interface>>
        + operation() : void
    }
    class Adaptee {
        + specificOperation() : void
    }
    class Adapter {
        - adaptee: Adaptee
        + Adapter(adaptee: Adaptee)
        + operation() : void
    }

    note for Adapter "adaptee.specificOperation() 호출"
```

## 어댑터 패턴 구현 방법

어댑터 패턴은 주로 두 가지 형태로 구현됩니다: **클래스 어댑터 패턴**과 **객체 어댑터 패턴**입니다.

### 1. 클래스 어댑터 패턴 (Class Adapter Pattern)

클래스 어댑터 패턴은 [[클래스 상속]]을 사용하여 어댑터를 구현합니다. 어댑터 클래스가 `Target` 인터페이스를 구현(implements)하고, 동시에 `Adaptee` 클래스를 상속(extends)받는 방식입니다. (Java와 같은 단일 상속만 지원하는 언어에서는 `Target`이 인터페이스이고 `Adaptee`가 클래스여야 가능합니다.)

**장점:**

- `Adaptee` 자체를 상속받으므로, `Adaptee`의 protected 멤버에도 접근 가능하며, `Adaptee`의 행동을 오버라이드(override)하기 용이합니다.

**단점:**

- `Adaptee`의 모든 서브클래스에 대해 어댑터를 만들 수 없습니다. 즉, `Adaptee`의 특정 서브클래스만 어댑팅할 수 있습니다.
- Java와 같이 클래스 다중 상속을 지원하지 않는 언어에서는 활용에 제약이 있습니다. (보통 `Target`은 인터페이스, `Adaptee`는 구체 클래스 형태가 됩니다.)

**Java 예시 코드 (클래스 어댑터):**

Java

```
// Target 인터페이스
interface EuropeanSocket {
    void giveElectricity();
}

// Adaptee 클래스 (한국형 플러그)
class KoreanPlug {
    public void powerOn() {
        System.out.println("한국형 플러그에서 전원이 공급됩니다.");
    }
}

// Adapter 클래스
class SocketAdapter extends KoreanPlug implements EuropeanSocket {
    @Override
    public void giveElectricity() {
        // Adaptee의 메서드를 호출 (상속받았으므로 직접 호출 가능)
        powerOn();
    }
}

// Client
public class Main {
    public static void main(String[] args) {
        EuropeanSocket socket = new SocketAdapter();
        socket.giveElectricity(); // 출력: 한국형 플러그에서 전원이 공급됩니다.
    }
}
```

### 2. 객체 어댑터 패턴 (Object Adapter Pattern)

객체 어댑터 패턴은 [[객체 구성 (Composition)]]을 사용하여 어댑터를 구현합니다. 어댑터 클래스가 `Target` 인터페이스를 구현하고, 내부에 `Adaptee` 객체의 인스턴스를 멤버 변수로 가집니다. 클라이언트의 요청이 들어오면, 어댑터는 자신이 가지고 있는 `Adaptee` 객체에게 실제 작업을 위임합니다.

**장점:**

- `Adaptee` 뿐만 아니라 `Adaptee`의 모든 서브클래스에 대해서도 어댑터를 만들 수 있습니다. (어댑터가 `Adaptee` 타입의 인스턴스를 받으므로)
- 클래스 어댑터보다 유연하며, 일반적으로 더 선호되는 방식입니다. (상속보다는 구성을 사용하라는 객체지향 원칙과도 부합)

**단점:**

- `Adaptee`의 내부 동작을 오버라이드하기가 클래스 어댑터보다 조금 더 번거로울 수 있습니다. (직접 상속받지 않았기 때문)

**Java 예시 코드 (객체 어댑터):**

Java

```
// Target 인터페이스
interface UsbPort {
    void connectWithUsbCable();
}

// Adaptee 클래스 (기존의 PS/2 키보드)
class Ps2Keyboard {
    public void connectWithPs2() {
        System.out.println("PS/2 포트에 키보드가 연결되었습니다.");
    }
    public void typeKey() {
        System.out.println("키가 입력됩니다 (PS/2).");
    }
}

// Adapter 클래스
class Ps2ToUsbAdapter implements UsbPort {
    private Ps2Keyboard adaptee; // Adaptee 객체를 멤버로 가짐

    public Ps2ToUsbAdapter(Ps2Keyboard keyboard) {
        this.adaptee = keyboard;
    }

    @Override
    public void connectWithUsbCable() {
        adaptee.connectWithPs2(); // Adaptee의 메서드 호출
        System.out.println("USB 포트를 통해 PS/2 키보드 사용 가능!");
    }

    // 필요하다면 Adaptee의 다른 메서드도 호출하도록 추가 인터페이스 정의 가능
    public void typing() {
        adaptee.typeKey();
    }
}

// Client
public class Computer {
    public static void main(String[] args) {
        Ps2Keyboard oldKeyboard = new Ps2Keyboard();
        UsbPort usbPort = new Ps2ToUsbAdapter(oldKeyboard);

        usbPort.connectWithUsbCable();
        // usbPort.typing(); // UsbPort 인터페이스에는 typing이 없으므로 직접 호출 불가
        // 만약 typing 기능을 사용하고 싶다면, Adapter에 추가 메서드를 만들거나,
        // Target 인터페이스를 더 포괄적으로 설계해야 합니다.
        // 혹은 Adapter 타입을 직접 사용할 수 있지만, 이는 Target 인터페이스를 사용하는 이점을 일부 해칩니다.
        ((Ps2ToUsbAdapter) usbPort).typing(); // 형변환 후 사용 가능 (권장되지는 않음)
    }
}
```

일반적으로 **객체 어댑터 패턴이 클래스 어댑터 패턴보다 더 유연하고 재사용성이 높아 많이 선호**됩니다.

## 어댑터 패턴의 장점

- **재사용성 증가**: 기존 코드를 수정하지 않고 새로운 인터페이스에 맞게 재사용할 수 있습니다.
- **유연성 향상**: 클라이언트와 Adaptee 사이의 의존성을 낮춥니다. 클라이언트는 `Target` 인터페이스에만 의존하므로, Adaptee가 변경되어도 클라이언트 코드는 영향을 받지 않습니다.
- **확장성**: 새로운 Adaptee가 등장하더라도, 새로운 어댑터만 추가하면 기존 클라이언트 코드와 함께 사용할 수 있습니다.

## 어댑터 패턴의 단점

- **클래스/객체 수 증가**: 어댑터를 만들기 위해 추가적인 클래스나 객체가 필요하므로, 시스템의 전반적인 복잡도가 약간 증가할 수 있습니다.
- **양방향 어댑터의 복잡성**: 때로는 `Target`과 `Adaptee` 양쪽 인터페이스를 모두 만족시켜야 하는 양방향 어댑터가 필요할 수 있는데, 이는 구현이 더 복잡해질 수 있습니다. (하지만 일반적인 경우는 단방향입니다)

## 실생활 및 프레임워크 예시

어댑터 패턴은 우리 주변에서도 쉽게 찾아볼 수 있습니다.

- **Java I/O 클래스**:
    - `java.io.InputStreamReader`: `InputStream` (바이트 스트림)을 `Reader` (문자 스트림)로 변환해주는 어댑터 역할을 합니다.
    - `java.io.OutputStreamWriter`: `OutputStream` (바이트 스트림)을 `Writer` (문자 스트림)로 변환해주는 어댑터 역할을 합니다.
- **[[스프링 프레임워크 (Spring Framework)]]의 `HandlerAdapter`**:
    - 스프링 MVC에서 `DispatcherServlet`은 다양한 타입의 핸들러(컨트롤러)를 실행해야 합니다. `HandlerAdapter`는 이 다양한 핸들러들을 `DispatcherServlet`이 일관된 방식으로 호출할 수 있도록 중간에서 어댑터 역할을 수행합니다. 자세한 내용은 [[스프링 HandlerAdapter 동작 방식]]에서 확인하실 수 있습니다.
- **각종 라이브러리 래퍼(Wrapper) 클래스**: 특정 라이브러리의 API를 사용하기 쉽게 감싸거나, 다른 인터페이스로 변환하여 제공하는 래퍼 클래스들이 어댑터 패턴의 한 예로 볼 수 있습니다.

## 결론

어댑터 패턴은 서로 다른 인터페이스를 가진 코드들을 조화롭게 연결하여 시스템의 유연성과 재사용성을 높이는 강력한 도구입니다. "호환성 문제? 어댑터에게 맡겨!" 라는 말이 나올 정도로, 실무에서 다양한 형태로 응용되어 사용됩니다.

새로운 시스템을 설계할 때뿐만 아니라, 기존 시스템을 유지보수하거나 확장할 때도 어댑터 패턴을 잘 활용한다면 많은 이점을 얻을 수 있을 것입니다. 중요한 것은 패턴의 구조를 암기하는 것보다, 어떤 문제를 해결하기 위해 이 패턴이 등장했고, 어떤 상황에 적용하는 것이 적절한지 이해하는 것입니다.

다음번에는 또 다른 유용한 디자인 패턴 이야기로 찾아뵙겠습니다. 읽어주셔서 감사합니다!