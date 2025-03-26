싱글톤 패턴은 클래스의 인스턴스가 오직 하나만 생성되도록 보장하고, 그 인스턴스에 대한 전역적인 접근점을 제공하는 디자인 패턴입니다. 이 패턴은 소프트웨어 디자인에서 가장 많이 사용되는 패턴 중 하나로, [[객체 지향 프로그래밍(OOP)]]의 원칙과 함께 시스템 전체에서 상태를 공유해야 할 때 유용합니다.

## 싱글톤 패턴의 목적

싱글톤 패턴은 다음과 같은 목적을 위해 사용됩니다:

1. **인스턴스 제한**: 특정 클래스의 인스턴스가 오직 하나만 존재하도록 보장합니다.
2. **전역 접근점**: 해당 인스턴스에 대한 전역적인 접근 지점을 제공합니다.
3. **리소스 공유**: 데이터베이스 연결, 파일 시스템, 설정 정보 등의 공유 리소스를 관리합니다.
4. **메모리 효율성**: 동일한 객체를 여러 번 생성하지 않음으로써 메모리 사용을 최적화합니다.

## 싱글톤 패턴의 구현 방법

Java에서 싱글톤 패턴을 구현하는 방법은 여러 가지가 있습니다. 각각의 방법은 특정 상황이나 요구사항에 따라 장단점이 있습니다.

### 1. 기본 싱글톤 패턴

```java
public class BasicSingleton {
    // private 정적 변수로 유일한 인스턴스 보관
    private static BasicSingleton instance;
    
    // private 생성자로 외부에서 인스턴스 생성 방지
    private BasicSingleton() {
        // 초기화 코드
    }
    
    // 인스턴스에 접근하기 위한 public 정적 메소드
    public static BasicSingleton getInstance() {
        if (instance == null) {
            instance = new BasicSingleton();
        }
        return instance;
    }
    
    // 싱글톤 객체의 기능을 제공하는 메소드
    public void doSomething() {
        System.out.println("싱글톤 객체가 작업을 수행합니다.");
    }
}
```

이 기본적인 구현은 단일 스레드 환경에서는 잘 작동하지만, 멀티스레드 환경에서는 [[경쟁 상태(Race Condition)]]가 발생할 수 있습니다. 두 개 이상의 스레드가 동시에 `getInstance()`를 호출하면 둘 다 `instance`가 `null`임을 확인하고 각각 새 인스턴스를 생성할 수 있습니다.

### 2. 스레드 안전한 싱글톤 패턴 구현

#### 2.1. synchronized 키워드를 사용한 방법

```java
public class ThreadSafeSingleton {
    private static ThreadSafeSingleton instance;
    
    private ThreadSafeSingleton() {
        // 초기화 코드
    }
    
    // synchronized 키워드를 사용하여 멀티스레드 환경에서 안전하게 구현
    public static synchronized ThreadSafeSingleton getInstance() {
        if (instance == null) {
            instance = new ThreadSafeSingleton();
        }
        return instance;
    }
}
```

이 방법은 스레드 안전성을 보장하지만, `synchronized` 키워드로 인해 성능 저하가 발생할 수 있습니다. 모든 스레드가 `getInstance()` 메소드에 접근할 때마다 동기화가 발생하기 때문입니다.

#### 2.2. 이른 초기화(Eager Initialization)

```java
public class EagerSingleton {
    // 클래스 로딩 시점에 인스턴스 생성
    private static final EagerSingleton INSTANCE = new EagerSingleton();
    
    private EagerSingleton() {
        // 초기화 코드
    }
    
    public static EagerSingleton getInstance() {
        return INSTANCE;
    }
}
```

이 방법은 클래스가 로드될 때 인스턴스가 생성되므로 스레드 안전성이 보장됩니다. 그러나 싱글톤 객체가 무거운 리소스를 사용하는 경우, 실제로 사용되지 않더라도 메모리를 차지하게 됩니다.

#### 2.3. 이중 검사 잠금(Double-Checked Locking)

```java
public class DCLSingleton {
    private static volatile DCLSingleton instance;
    
    private DCLSingleton() {
        // 초기화 코드
    }
    
    public static DCLSingleton getInstance() {
        if (instance == null) {
            synchronized (DCLSingleton.class) {
                if (instance == null) {
                    instance = new DCLSingleton();
                }
            }
        }
        return instance;
    }
}
```

이 방법은 `instance`가 `null`인 경우에만 동기화 블록을 실행하므로 성능이 향상됩니다. Java 5 이상에서는 `volatile` 키워드를 사용하여 [[메모리 가시성(Memory Visibility)]] 문제를 해결해야 합니다.

#### 2.4. 정적 내부 클래스(권장 방법)

```java
public class HolderSingleton {
    private HolderSingleton() {
        // 초기화 코드
    }
    
    // 정적 내부 클래스를 사용한 지연 초기화
    private static class SingletonHolder {
        private static final HolderSingleton INSTANCE = new HolderSingleton();
    }
    
    public static HolderSingleton getInstance() {
        return SingletonHolder.INSTANCE;
    }
}
```

이 방법은 지연 초기화와 스레드 안전성을 모두 제공합니다. `SingletonHolder` 클래스는 `getInstance()` 메소드가 호출될 때만 로드되며, JVM은 클래스 로딩의 스레드 안전성을 보장합니다. 이 방법은 가장 많이 권장되는 싱글톤 구현 방법입니다.

#### 2.5. 열거형(Enum)을 사용한 방법

```java
public enum EnumSingleton {
    INSTANCE;
    
    // 싱글톤 객체의 기능을 제공하는 메소드
    public void doSomething() {
        System.out.println("열거형 싱글톤 객체가 작업을 수행합니다.");
    }
}
```

이 방법은 Joshua Bloch의 "Effective Java"에서 권장하는 방법으로, 간결하고 직렬화 문제를 자동으로 처리합니다. 또한 리플렉션을 통한 공격에도 안전합니다. 그러나 열거형은 상속이 불가능하고, 초기화를 지연시킬 수 없다는 제약이 있습니다.

## 싱글톤 패턴의 문제점과 해결 방법

### 1. 리플렉션을 통한 공격

Java의 리플렉션 API를 사용하면 private 생성자에 접근하여 여러 인스턴스를 생성할 수 있습니다.

```java
// 리플렉션을 통한 싱글톤 무력화 예시
Constructor<BasicSingleton> constructor = BasicSingleton.class.getDeclaredConstructor();
constructor.setAccessible(true);
BasicSingleton instance1 = constructor.newInstance();
BasicSingleton instance2 = constructor.newInstance();
// instance1 != instance2, 싱글톤 패턴이 깨짐
```

**해결 방법**: 생성자에서 이미 인스턴스가 생성되었는지 확인하거나, 열거형을 사용하여 싱글톤을 구현합니다.

### 2. 직렬화/역직렬화 문제

직렬화된 싱글톤 객체가 역직렬화될 때 새로운 인스턴스가 생성될 수 있습니다.

**해결 방법**: `readResolve()` 메소드를 구현하여 역직렬화 과정에서 싱글톤 인스턴스를 반환하도록 합니다.

```java
public class SerializableSingleton implements Serializable {
    private static final long serialVersionUID = 1L;
    private static SerializableSingleton instance = new SerializableSingleton();
    
    private SerializableSingleton() {}
    
    public static SerializableSingleton getInstance() {
        return instance;
    }
    
    // 역직렬화 시 호출되어 싱글톤 인스턴스를 반환
    protected Object readResolve() {
        return getInstance();
    }
}
```

### 3. 클래스 로더 문제

여러 클래스 로더가 사용되는 환경에서는 각 클래스 로더마다 싱글톤 클래스의 인스턴스가 생성될 수 있습니다.

**해결 방법**: JNDI와 같은 글로벌 레지스트리를 사용하거나, 클래스 로더 아키텍처를 적절히 설계합니다.

## 스프링 프레임워크에서의 싱글톤 패턴

스프링 프레임워크는 기본적으로 모든 빈(Bean)을 싱글톤으로 관리합니다. 이는 스프링의 IoC(Inversion of Control) 컨테이너가 빈의 생명주기를 관리하고, 필요한 곳에 동일한 인스턴스를 주입함으로써 구현됩니다.

```java
@Service
public class UserService {
    // 이 클래스의 인스턴스는 스프링에 의해 자동으로 싱글톤으로 관리됩니다.
    
    @Autowired
    private UserRepository userRepository;
    
    public User findById(Long id) {
        return userRepository.findById(id).orElse(null);
    }
}
```

스프링에서는 빈의 스코프를 `@Scope` 어노테이션을 통해 변경할 수 있습니다:

```java
@Service
@Scope("prototype") // 요청마다 새 인스턴스 생성
public class NonSingletonService {
    // ...
}
```

스프링의 싱글톤 관리 방식은 다음과 같은 이점이 있습니다:

1. 개발자가 직접 싱글톤을 구현할 필요가 없습니다.
2. 스레드 안전성, 직렬화 등의 문제를 프레임워크 차원에서 처리합니다.
3. 테스트가 용이합니다(의존성 주입을 통한 모의 객체 사용).

스프링의 빈 관리에 대한 자세한 내용은 [[스프링 빈 스코프]]를 참고해주세요.

## 싱글톤 패턴의 사용 사례

싱글톤 패턴은 다양한 상황에서 유용하게 사용됩니다:

1. **데이터베이스 연결 관리**: 데이터베이스 커넥션 풀은 비용이 많이 드는 자원이므로 싱글톤으로 관리됩니다.
2. **로깅 시스템**: 로그 파일에 동시에 여러 인스턴스가 기록하는 것을 방지합니다.
3. **설정 관리**: 애플리케이션 설정 정보를 중앙에서 관리합니다.
4. **캐시 관리**: 애플리케이션 전체에서 동일한 캐시 인스턴스를 공유합니다.
5. **스레드 풀**: 제한된 개수의 스레드를 관리하는 스레드 풀은 싱글톤으로 구현됩니다.
6. **디바이스 관리자**: 프린터, 스캐너 등의 디바이스를 관리하는 클래스는 싱글톤으로 구현됩니다.

## 싱글톤 패턴의 장단점

### 장점

1. **메모리 효율성**: 한 번만 객체를 생성하므로 메모리를 절약할 수 있습니다.
2. **전역 접근성**: 애플리케이션 어디서나 동일한 인스턴스에 접근할 수 있습니다.
3. **객체 공유**: 상태와 행동을 공유할 수 있습니다.
4. **리소스 제한**: 특정 자원에 대한 접근을 제한할 수 있습니다.

### 단점

1. **결합도 증가**: 싱글톤을 사용하는 클래스들은 싱글톤 클래스와 강하게 결합됩니다.
2. **테스트 어려움**: 전역 상태로 인해 단위 테스트가 어려워질 수 있습니다.
3. **동시성 문제**: 여러 스레드가 싱글톤 객체를 동시에 수정할 때 적절한 동기화가 필요합니다.
4. **책임 과중**: 싱글톤 클래스가 너무 많은 책임을 가지게 될 수 있습니다.
5. **[[단일 책임 원칙(SRP)]]** 위반: 싱글톤 패턴은 객체의 생성과 비즈니스 로직을 동시에 관리합니다.

## 싱글톤 패턴 사용 시 모범 사례

1. **적절한 사용**: 싱글톤이 정말 필요한 상황에서만 사용합니다(공유 자원, 중앙 관리 등).
2. **지연 초기화**: 필요할 때만 인스턴스를 생성하여 리소스를 절약합니다.
3. **스레드 안전성 보장**: 멀티스레드 환경을 고려하여 구현합니다.
4. **인터페이스 사용**: 싱글톤 클래스가 인터페이스를 구현하도록 하여 결합도를 낮춥니다.
5. **의존성 주입 고려**: 가능하다면 스프링과 같은 프레임워크의 IoC 컨테이너를 활용합니다.
6. **상태 관리**: 싱글톤 객체의 상태가 변경 가능한 경우, 동기화 메커니즘을 적용합니다.

## 유틸리티 클래스와의 차이

유틸리티 클래스와의 차이는 [[싱글톤 패턴 vs 유틸리티 클래스]]를 참고해주세요
## 결론

싱글톤 패턴은 클래스의 인스턴스가 하나만 존재하도록 보장하는 강력한 디자인 패턴입니다. 공유 자원 관리, 중앙 집중식 서비스 제공 등 다양한 상황에서 유용하게 활용됩니다. 그러나 전역 상태 관리로 인한 테스트 어려움, 강한 결합도 등의 단점도 있으므로 신중하게 사용해야 합니다.

현대적인 개발 환경에서는 스프링과 같은 프레임워크가 제공하는 IoC 컨테이너를 통해 싱글톤 패턴의 장점을 활용하면서 단점을 최소화할 수 있습니다. 이러한 방식으로 응용 프로그램 내에서 객체의 생명주기와 의존성을 효과적으로 관리할 수 있습니다.

## 참고 자료

- Effective Java, 3rd Edition - Joshua Bloch
- Design Patterns: Elements of Reusable Object-Oriented Software - Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides (Gang of Four)
- Head First Design Patterns - Eric Freeman, Elisabeth Robson
- Spring Framework Documentation(https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#beans-factory-scopes)
- Java Concurrency in Practice - Brian Goetz