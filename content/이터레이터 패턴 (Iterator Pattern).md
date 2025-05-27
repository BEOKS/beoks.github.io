안녕하세요! 오늘은 **이터레이터 패턴(Iterator Pattern)**에 대해 깊이 있게 알아보겠습니다. 이터레이터 패턴은 컬렉션의 내부 구조를 노출하지 않으면서 요소들에 순차적으로 접근할 수 있는 방법을 제공하는 아주 유용한 패턴입니다. 🧐

---

### **이터레이터 패턴이란 무엇일까요?**

이 패턴의 핵심 목표는 **컬렉션(Collection) 객체의 내부 표현 방식(예: `List`, `Set`, `Map` 등)을 클라이언트로부터 숨기는 것**입니다. 클라이언트는 컬렉션이 어떻게 구현되었는지 전혀 몰라도, 이터레이터(Iterator)라는 통일된 인터페이스를 통해 컬렉션의 모든 요소에 접근할 수 있습니다.

마치 TV 리모컨과 같습니다. 우리는 리모컨의 '다음 채널' 버튼만 누르면 채널이 바뀌는 것을 알지, TV 내부에서 어떤 복잡한 과정을 거쳐 채널이 변경되는지는 알 필요가 없죠. 여기서 리모컨이 바로 **이터레이터**의 역할을 하는 것입니다.

---

### **이터레이터 패턴의 구조**

이터레이터 패턴은 크게 두 가지 핵심 역할로 구성됩니다.

1. **Iterator (반복자)**: 컬렉션의 요소를 순회하고 접근하는 데 필요한 인터페이스를 정의합니다. 일반적으로 `hasNext()`와 `next()` 같은 메서드를 포함합니다.
2. **Aggregate (집합체)**: 이터레이터 객체를 생성하는 인터페이스를 정의합니다. 이 인터페이스를 구현하는 클래스가 바로 우리가 순회하려는 실제 컬렉션 객체입니다.

```mermaid
classDiagram
    direction RL
    class Aggregate {
        <<interface>>
        +createIterator() Iterator
    }
    class ConcreteAggregate {
        +createIterator() Iterator
    }
    class Iterator {
        <<interface>>
        +hasNext() boolean
        +next() Object
    }
    class ConcreteIterator {
        -aggregate ConcreteAggregate
        -currentIndex int
        +hasNext() boolean
        +next() Object
    }
    class Client

    Client ..> Aggregate
    Client ..> Iterator
    Aggregate <|-- ConcreteAggregate
    Iterator <|-- ConcreteIterator
    ConcreteAggregate --> ConcreteIterator : creates
```

- **Client**: `Aggregate`와 `Iterator` 인터페이스를 모두 사용하여 `ConcreteAggregate`의 요소들을 순회합니다.
- **Aggregate**: `Iterator` 객체를 생성하는 팩토리 메서드(`createIterator()`)를 가집니다.
- **ConcreteAggregate**: `Aggregate`를 구현하며, `ConcreteIterator`의 인스턴스를 생성하여 반환합니다.
- **Iterator**: 순회를 위한 표준 메서드(`hasNext()`, `next()`)를 정의합니다.
- **ConcreteIterator**: `Iterator`를 구현하며, 특정 `ConcreteAggregate`를 순회하는 로직을 가집니다. 현재 순회 위치를 추적합니다.

---

### **왜 이터레이터 패턴을 사용해야 할까요?**

이터레이터 패턴을 사용하면 다음과 같은 장점을 얻을 수 있습니다.

- **캡슐화 강화**: 컬렉션의 내부 구조가 외부에 노출되지 않습니다. 이는 [[캡슐화(Encapsulation)]] 원칙을 지키는 데 도움이 되며, 컬렉션의 구현이 변경되어도 클라이언트 코드는 영향을 받지 않습니다.
- **단일 책임 원칙 (SRP)**: 컬렉션 순회 로직이 컬렉션 객체 자체에서 분리됩니다. 컬렉션은 데이터 저장이라는 본연의 책임에만 집중하고, 순회 책임은 이터레이터에게 위임됩니다. 이는  [[단일 책임 원칙(Single Responsibility Principle)]]을 만족시킵니다.
- **코드 유연성 및 재사용성 증가**: 다양한 종류의 컬렉션에 대해 통일된 방식으로 순회할 수 있습니다. `List`를 순회하던 코드를 `Set`을 순회하도록 변경하는 것이 매우 간단해집니다.
- **다양한 순회 방식 지원**: 하나의 컬렉션에 대해 여러 종류의 이터레이터(예: 정방향 순회 이터레이터, 역방향 순회 이터레이터)를 제공할 수 있습니다.

---

### **Java에서의 이터레이터 패턴 활용**

사실 Java 개발자라면 이미 자신도 모르게 이터레이터 패턴을 매일 사용하고 있을 가능성이 높습니다. Java의 [[컬렉션 프레임워크(Collection Framework)]]가 바로 이터레이터 패턴을 기반으로 설계되었기 때문입니다.

`java.util.Iterator` 인터페이스와 `java.lang.Iterable` 인터페이스가 이 패턴의 핵심입니다.

- **`Iterable`**: `Aggregate` 역할에 해당하며, `iterator()` 메서드를 통해 `Iterator` 객체를 반환합니다. `List`, `Set`, `Map` 등 모든 컬렉션 클래스가 이 인터페이스를 구현합니다.
- **`Iterator`**: `Iterator` 역할에 해당하며, `hasNext()`, `next()`, `remove()` 메서드를 제공합니다.

간단한 Java 예시 코드를 살펴보겠습니다.

```java
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

public class IteratorExample {
    public static void main(String[] args) {
        // ConcreteAggregate 역할
        List<String> fruits = new ArrayList<>();
        fruits.add("Apple");
        fruits.add("Banana");
        fruits.add("Cherry");

        // Aggregate로부터 Iterator를 얻음
        Iterator<String> iterator = fruits.iterator(); // iterator() 메서드 사용

        // Client는 Iterator를 사용하여 요소를 순회
        while (iterator.hasNext()) {
            String fruit = iterator.next();
            System.out.println(fruit);
        }
    }
}
```

위 코드에서 `main` 메서드(Client)는 `ArrayList`의 내부 구조가 어떻게 생겼는지 전혀 알 필요가 없습니다. 단지 `iterator()`를 호출하여 `Iterator`를 얻고, `hasNext()`와 `next()`를 통해 요소를 순회할 뿐입니다. 만약 `ArrayList`를 `LinkedList`나 `HashSet`으로 바꿔도 순회하는 코드는 전혀 변경할 필요가 없습니다. 이것이 이터레이터 패턴의 가장 큰 힘입니다. 

---

### **스프링 프레임워크와 이터레이터 패턴**

스프링 프레임워크(Spring Framework)에서도 이터레이터 패턴의 원리를 찾아볼 수 있습니다. 예를 들어, 스프링 데이터 JPA에서 제공하는 `PagingAndSortingRepository`는 `findAll(Pageable pageable)` 메서드를 통해 `Page<T>` 객체를 반환합니다.

이 `Page<T>` 객체는 `Iterable<T>`를 상속받기 때문에, 현재 페이지의 데이터들을 이터레이터 패턴을 통해 쉽게 순회할 수 있습니다.

```java
// Spring Data Commons의 Page 인터페이스 일부
public interface Page<T> extends Slice<T> {
    
    // ... 다른 메서드들
    
    // Iterable<T>를 상속받아 iterator() 메서드를 제공
    @Override
    Iterator<T> iterator(); 
}
```

클라이언트 코드는 데이터베이스에서 데이터를 어떻게 페이징 처리하여 가져왔는지 상세히 알 필요 없이, 반환된 `Page` 객체의 이터레이터를 사용하여 결과 데이터를 처리하기만 하면 됩니다. 이처럼 스프링은 복잡한 내부 동작을 추상화하고 개발자가 핵심 비즈니스 로직에 집중할 수 있도록 돕는 데 이터레이터와 같은 디자인 패턴을 적극적으로 활용합니다.

---

### **이터레이터 패턴 사용 시 고려사항**

이터레이터 패턴은 매우 유용하지만, 한 가지 주의할 점이 있습니다. 바로 **순회 중 컬렉션 변경** 문제입니다.

이터레이터를 사용하여 컬렉션을 순회하는 도중에 해당 컬렉션의 요소가 추가되거나 삭제되면 `ConcurrentModificationException`이 발생할 수 있습니다. 이는 이터레이터가 순회 시작 시점의 컬렉션 상태를 기준으로 동작하는데, 실제 컬렉션의 상태가 달라지면서 발생하는 문제입니다.

---

### **결론**

이터레이터 패턴은 컬렉션의 내부 구현을 숨기고, 요소에 접근하는 방법을 표준화하여 코드의 **유연성**, **재사용성**, **캡슐화**를 높여주는 강력한 디자인 패턴입니다. 이미 Java와 스프링을 비롯한 많은 프레임워크와 라이브러리에 깊숙이 녹아들어 있으므로, 그 원리를 정확히 이해하고 사용한다면 더욱 견고하고 유지보수하기 좋은 코드를 작성할 수 있을 것입니다.
