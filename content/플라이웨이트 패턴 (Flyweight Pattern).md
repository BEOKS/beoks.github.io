혹시 게임 개발에서 수천, 수만 그루의 나무로 이루어진 숲을 표현하거나, 워드 프로세서에서 수많은 글자를 화면에 표시해야 하는 상황을 상상해 보신 적 있나요? 각 나무나 글자마다 객체를 하나씩 생성한다면 엄청난 메모리가 소모될 것입니다. 플라이웨이트 패턴은 바로 이런 상황에서 빛을 발합니다. 마치 바둑판 위의 바둑돌처럼, 모든 검은 돌은 모양과 색상이 동일(공유되는 특성)하고 실제 놓이는 위치만 다른(개별적인 특성) 원리를 소프트웨어 객체에 적용하는 것이죠.

## 플라이웨이트 패턴이란 무엇인가요?

**플라이웨이트 패턴 (Flyweight Pattern)** 은 **다수의 유사한 객체들을 효율적으로 지원하기 위해 [[객체 공유(Object Sharing)]]를 통해 사용하는 패턴**입니다. 이 패턴의 핵심은 객체가 가진 상태를 두 가지로 분리하는 것입니다.

- **[[내재적 상태(Intrinsic State)]]**: 객체 내부에 저장되며, 여러 문맥에서 공유될 수 있고 변하지 않는 상태입니다. 플라이웨이트 객체가 생성될 때 초기화됩니다. (예: 바둑돌의 색깔, 글자의 코드값)
- **[[외재적 상태(Extrinsic State)]]**: 객체가 사용되는 특정 문맥에 따라 달라지며, 공유되지 않고 클라이언트에 의해 관리되거나 계산되어 플라이웨이트 객체의 메서드 호출 시 매개변수로 전달되는 상태입니다. (예: 바둑돌의 위치, 글자가 그려질 화면 좌표 및 글꼴)

플라이웨이트 객체는 내재적 상태만을 가지고, 외재적 상태는 필요할 때마다 외부에서 주입받아 사용함으로써 객체의 수를 크게 줄일 수 있습니다.

## 왜 플라이웨이트 패턴을 사용할까요?

플라이웨이트 패턴은 다음과 같은 상황에서 특히 강력한 효과를 발휘합니다:

1. **애플리케이션이 대량의 객체를 사용해야 할 때**: 객체 수가 너무 많아 메모리 부족이나 성능 저하가 우려될 때 가장 먼저 고려해 볼 수 있습니다.
2. **객체의 상태 중 상당 부분이 공유 가능할 때**: 즉, 내재적 상태로 분리할 수 있는 부분이 많을 때 효과적입니다.
3. **객체의 상태 중 일부(외재적 상태)만 문맥에 따라 변할 때**: 이 외재적 상태를 클라이언트가 관리할 수 있다면 패턴 적용이 용이합니다.
4. **공유를 통해 객체의 총 수를 줄여 메모리 사용량을 줄이고 싶을 때**: 이것이 플라이웨이트 패턴의 가장 주된 목적입니다.

## 플라이웨이트 패턴의 구조

플라이웨이트 패턴을 구성하는 주요 참여자는 다음과 같습니다:

- **Flyweight (플라이웨이트)**: 플라이웨이트 객체들이 구현해야 하는 인터페이스를 정의합니다. 이 인터페이스는 클라이언트가 호출할 연산(operation)을 포함하며, 이 연산은 외재적 상태를 매개변수로 받아 처리합니다.
- **ConcreteFlyweight (구체적 플라이웨이트)**: `Flyweight` 인터페이스를 구현하고, 내재적 상태를 저장합니다. 이 객체들이 실제로 공유됩니다. 내재적 상태는 생성자를 통해 주입받으며, 불변(immutable)이어야 안전합니다.
- **UnsharedConcreteFlyweight (비공유 구체적 플라이웨이트, 선택적)**: `Flyweight` 인터페이스를 구현하지만, 어떤 이유로든 공유되지 않는 객체입니다. 모든 상태를 스스로 가질 수 있습니다. (예: 특별한 처리가 필요한 몇몇 객체들)
- **FlyweightFactory (플라이웨이트 팩토리)**: 플라이웨이트 객체의 생성과 관리를 담당합니다. 클라이언트가 특정 내재적 상태를 가진 플라이웨이트를 요청하면, 팩토리는 이미 생성된 객체가 있는지 내부 풀(pool)에서 찾아봅니다. 있으면 기존 객체를 반환하고, 없으면 새로 생성하여 풀에 저장한 후 반환합니다.
- **Client (클라이언트)**: 플라이웨이트 객체를 사용합니다. `FlyweightFactory`로부터 플라이웨이트 객체를 얻고, 필요한 외재적 상태를 계산하거나 저장하여 플라이웨이트 객체의 연산 호출 시 전달합니다.

```mermaid
classDiagram
    Client --> FlyweightFactory
    FlyweightFactory ..> "*" ConcreteFlyweight : creates & manages
    Client ..> Flyweight : uses

    class Flyweight {
        <<interface>>
        +operation(extrinsicState: Object) : void
    }
    class ConcreteFlyweight {
        -intrinsicState: Object // 공유되는 내재적 상태
        +ConcreteFlyweight(intrinsicState: Object)
        +operation(extrinsicState: Object) : void
    }
    class UnsharedConcreteFlyweight {
        -allState: Object // 공유되지 않는 모든 상태
        +operation(extrinsicState: Object) : void
    }
    class FlyweightFactory {
        -flyweights: Map~String, Flyweight~ // 플라이웨이트 풀
        +getFlyweight(keyForIntrinsicState: String) : Flyweight
    }
    class Client {
        +process() : void
    }

    Flyweight <|-- ConcreteFlyweight
    Flyweight <|-- UnsharedConcreteFlyweight

    note for FlyweightFactory "getFlyweight(key) {\n  if (!flyweights.containsKey(key)) {\n    flyweights.put(key, new ConcreteFlyweight(key));\n  }\n  return flyweights.get(key);\n}"
    note for ConcreteFlyweight "내재적 상태는 불변(immutable)이어야 함"
    note for Flyweight "operation은 외재적 상태를 받아 처리"
```

## 플라이웨이트 패턴 예시 (Java 코드)

화면에 여러 종류의 나무를 심는 간단한 시뮬레이션을 예로 들어보겠습니다. 나무의 종류(모양, 색상 등)는 내재적 상태로 공유하고, 나무가 심어질 위치나 크기는 외재적 상태로 처리합니다.

```java
import java.util.HashMap;
import java.util.Map;

// Flyweight 인터페이스
interface Tree {
    void draw(int x, int y, int age); // x, y, age는 외재적 상태
}

// ConcreteFlyweight 클래스
class TreeType implements Tree {
    private String name; // 내재적 상태
    private String color; // 내재적 상태
    private String texture; // 내재적 상태

    public TreeType(String name, String color, String texture) {
        this.name = name;
        this.color = color;
        this.texture = texture;
        System.out.println(name + " TreeType 객체 생성됨 (내재적 상태: " + color + ", " + texture + ")");
    }

    @Override
    public void draw(int x, int y, int age) {
        System.out.println(
            name + " 나무를 (" + x + ", " + y + ") 위치에 " + age + "살 나이로 그림 " +
            "[색상: " + color + ", 질감: " + texture + "]"
        );
    }
}

// FlyweightFactory 클래스
class TreeFactory {
    private static Map<String, TreeType> treeTypes = new HashMap<>();

    public static TreeType getTreeType(String name, String color, String texture) {
        String key = name + "-" + color + "-" + texture;
        TreeType result = treeTypes.get(key);
        if (result == null) {
            result = new TreeType(name, color, texture);
            treeTypes.put(key, result);
        }
        return result;
    }
}

// Client
public class Forest {
    public static void main(String[] args) {
        System.out.println("--- 숲 시뮬레이션 시작 ---");

        // 동일한 TreeType 객체가 공유됨
        TreeType pineType1 = TreeFactory.getTreeType("소나무", "초록색", "거친 질감");
        TreeType oakType1 = TreeFactory.getTreeType("참나무", "연갈색", "부드러운 질감");
        TreeType pineType2 = TreeFactory.getTreeType("소나무", "초록색", "거친 질감"); // 기존 객체 재사용

        System.out.println("\n--- 나무 심기 ---");
        // 각 나무는 동일한 TreeType(플라이웨이트)을 공유하지만, 외재적 상태(위치, 나이)는 다름
        pineType1.draw(10, 20, 5);
        oakType1.draw(30, 50, 10);
        pineType2.draw(100, 80, 7); // pineType1과 동일한 객체
        pineType1.draw(150, 30, 6);

        System.out.println("\n생성된 TreeType 객체 수: " + TreeFactory.treeTypes.size()); // 2개만 생성됨
    }
}
```

위 예시에서 `TreeType`은 내재적 상태(나무 이름, 색상, 질감)를 가지는 `ConcreteFlyweight`입니다. `TreeFactory`는 이러한 `TreeType` 객체들을 관리하며, 동일한 내재적 상태를 요구하면 기존 객체를 반환합니다. 클라이언트(`Forest`)는 `TreeFactory`로부터 `TreeType` 객체를 받아, 나무를 그릴 때마다 외재적 상태(위치 `x`, `y`와 나이 `age`)를 전달합니다. 결과적으로 "소나무" 타입과 "참나무" 타입, 단 두 개의 `TreeType` 객체만 생성되어 여러 나무를 표현하는 데 사용됩니다.

## 플라이웨이트 패턴의 장점

- **메모리 사용량 대폭 감소**: 공유를 통해 동일하거나 유사한 객체의 인스턴스 수를 크게 줄여 메모리 절약 효과가 매우 큽니다.
- **성능 향상**: 객체 생성 및 소멸에 드는 비용이 줄어들고, 가비지 컬렉션의 부담도 완화되어 시스템 전반의 성능이 향상될 수 있습니다.
- **객체 상태 관리의 명확성**: 내재적 상태와 외재적 상태를 명확히 구분함으로써 객체의 상태 관리가 더 체계적으로 이루어질 수 있습니다.

## 플라이웨이트 패턴의 단점

- **코드 복잡성 증가**: 내재적 상태와 외재적 상태를 분리하고, 팩토리를 통해 객체를 관리하는 등 초기 설계 및 구현의 복잡성이 다소 증가할 수 있습니다.
- **외재적 상태 계산/관리 비용**: 클라이언트가 외재적 상태를 매번 계산하거나 찾아서 플라이웨이트 객체에 전달해야 하므로, 이 부분에서 추가적인 로직이나 성능 비용이 발생할 수 있습니다.
- **런타임 상태 조합으로 인한 약간의 시간 비용**: 플라이웨이트 객체가 메서드를 실행할 때마다 외재적 상태를 받아와서 내재적 상태와 조합해야 하므로, 약간의 실행 시간 오버헤드가 있을 수 있습니다. (하지만 이는 메모리 절약으로 얻는 이점에 비해 미미한 경우가 많습니다.)
- **동시성 문제 가능성**: 만약 플라이웨이트 객체의 내재적 상태가 어떤 이유로든 변경 가능(mutable)하다면, 여러 스레드에서 공유 시 동시성 문제가 발생할 수 있습니다. 따라서 **내재적 상태는 반드시 불변(immutable)으로 유지하는 것이 중요합니다.**

## 실생활 및 프레임워크 예시

플라이웨이트 패턴은 의외로 우리 주변에서 많이 활용되고 있습니다:

- **Java의 `String` 리터럴 풀**: `"hello"`와 같은 문자열 리터럴은 JVM 내의 문자열 풀(String Pool)에 저장되어 공유됩니다. 동일한 문자열 리터럴을 여러 번 사용해도 실제로는 하나의 `String` 객체를 참조하게 됩니다.
- **Java의 `Integer.valueOf(int i)`**: 특정 범위 내의 `int` 값에 대해서는 `Integer` 객체를 캐싱하여 재사용합니다. (예: -128 ~ 127)
    
    Java
    
    ```
    // Integer i1 = 100;
    // Integer i2 = 100;
    // System.out.println(i1 == i2); // true (같은 객체 참조)
    ```
    
- **워드 프로세서의 글자 표현**: 문서 내의 수많은 글자들은 각 문자의 코드값(내재적 상태)을 가진 플라이웨이트 객체로 표현되고, 글자의 위치, 스타일(글꼴, 크기, 색상 등은 또 다른 플라이웨이트일 수 있음) 등은 외재적 상태로 처리될 수 있습니다.
- **그래픽 시스템**: 선, 원, 사각형 같은 기본 도형 객체나 특정 색상 객체, 아이콘 등을 플라이웨이트로 만들어 공유함으로써 효율성을 높입니다.
- **데이터베이스 연결 풀**: 엄밀히는 리소스 풀링 기법이지만, 제한된 수의 연결 객체를 여러 클라이언트가 공유하여 사용한다는 점에서 플라이웨이트 패턴의 아이디어와 유사한 측면이 있습니다.

## 결론

플라이웨이트 패턴은 애플리케이션에서 수많은 유사 객체를 다루어야 할 때 발생하는 메모리 문제를 해결하는 매우 효과적인 방법입니다. 객체의 상태를 내재적인 것과 외재적인 것으로 현명하게 분리하고, 공유 가능한 내재적 상태를 가진 객체를 재사용함으로써 시스템 자원을 크게 절약할 수 있습니다.

물론, 패턴 적용으로 인한 약간의 복잡성 증가는 감수해야 하지만, 그로 인해 얻는 메모리 효율성과 성능 향상의 이점은 특히 대규모 시스템에서 매우 클 수 있습니다. 여러분의 시스템에도 "가볍게" 만들 수 있는 부분이 있는지 한번 살펴보시는 건 어떨까요?

오늘도 유익한 시간 되셨기를 바랍니다. 다음 디자인 패턴 이야기로 또 만나요!