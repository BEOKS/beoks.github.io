SOLID는 로버트 C. 마틴(Robert C. Martin, 일명 "Uncle Bob")이 2000년대 초반에 제안한 객체지향 프로그래밍 및 설계의 5가지 기본 원칙의 앞글자를 따서 만든 약어입니다. 이 원칙들은 개발자가 유지보수가 쉽고 확장 가능한 시스템을 만들 수 있도록 도와줍니다.

SOLID의 각 글자는 다음을 의미합니다:

- **S**: 단일 책임 원칙 (Single Responsibility Principle)
- **O**: 개방-폐쇄 원칙 (Open-Closed Principle)
- **L**: 리스코프 치환 원칙 (Liskov Substitution Principle)
- **I**: 인터페이스 분리 원칙 (Interface Segregation Principle)
- **D**: 의존성 역전 원칙 (Dependency Inversion Principle)

이제 각 원칙에 대해 자세히 살펴보겠습니다.

## S - 단일 책임 원칙 (Single Responsibility Principle)

> "클래스는 단 하나의 책임만 가져야 한다."

단일 책임 원칙은 모든 클래스가 단 하나의 책임만을 가져야 한다는 개념입니다. 다르게 표현하면, 클래스를 변경해야 하는 이유는 오직 하나뿐이어야 합니다.

### 위반 사례:

```java
public class User {
    private String name;
    private String email;
    
    // 사용자 데이터 관련 메서드
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    
    // 데이터베이스 관련 메서드
    public void saveToDatabase() {
        // 데이터베이스에 사용자 저장 로직
        System.out.println("Saving user to database");
    }
    
    // 보고서 관련 메서드
    public void generateReport() {
        // 사용자 보고서 생성 로직
        System.out.println("Generating user report");
    }
}
```

이 클래스는 다음과 같은 여러 책임을 가지고 있습니다:

1. 사용자 데이터 관리
2. 데이터베이스 작업
3. 보고서 생성

### 개선된 버전:

```java
// 사용자 데이터만 담당
public class User {
    private String name;
    private String email;
    
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
}

// 데이터베이스 작업 담당
public class UserRepository {
    public void save(User user) {
        // 데이터베이스에 사용자 저장 로직
        System.out.println("Saving user to database");
    }
}

// 보고서 생성 담당
public class UserReportGenerator {
    public void generateReport(User user) {
        // 사용자 보고서 생성 로직
        System.out.println("Generating user report");
    }
}
```

이렇게 분리함으로써:

- 각 클래스는 하나의 책임만 가집니다.
- 코드가 더 모듈화되어 유지보수가 용이해집니다.
- 클래스 간의 결합도가 감소합니다.

## O - 개방-폐쇄 원칙 (Open-Closed Principle)

> "소프트웨어 엔티티(클래스, 모듈, 함수 등)는 확장에는 열려 있어야 하고, 수정에는 닫혀 있어야 한다."

이 원칙은 기존 코드를 변경하지 않고도 시스템의 기능을 확장할 수 있어야 한다는 것을 의미합니다.

### 위반 사례:

```java
public class Rectangle {
    private double width;
    private double height;
    
    // 생성자 및 getter/setter 생략
    public double getWidth() { return width; }
    public void setWidth(double width) { this.width = width; }
    public double getHeight() { return height; }
    public void setHeight(double height) { this.height = height; }
}

public class Circle {
    private double radius;
    
    // 생성자 및 getter/setter 생략
    public double getRadius() { return radius; }
    public void setRadius(double radius) { this.radius = radius; }
}

public class AreaCalculator {
    public double calculateArea(Object shape) {
        if (shape instanceof Rectangle) {
            Rectangle rectangle = (Rectangle) shape;
            return rectangle.getWidth() * rectangle.getHeight();
        } 
        else if (shape instanceof Circle) {
            Circle circle = (Circle) shape;
            return Math.PI * circle.getRadius() * circle.getRadius();
        }
        return 0;
    }
}
```

이 설계의 문제점:

- 새로운 도형(예: 삼각형)을 추가하려면 `AreaCalculator` 클래스를 수정해야 합니다.
- 조건문이 늘어나면서 코드가 복잡해집니다.

### 개선된 버전:

```java
public interface Shape {
    double calculateArea();
}

public class Rectangle implements Shape {
    private double width;
    private double height;
    
    // 생성자 및 getter/setter 생략
    
    @Override
    public double calculateArea() {
        return width * height;
    }
}

public class Circle implements Shape {
    private double radius;
    
    // 생성자 및 getter/setter 생략
    
    @Override
    public double calculateArea() {
        return Math.PI * radius * radius;
    }
}

public class AreaCalculator {
    public double calculateArea(Shape shape) {
        return shape.calculateArea();
    }
}
```

개선된 점:

- 새로운 도형을 추가할 때 `Shape` 인터페이스를 구현하는 새 클래스만 만들면 됩니다.
- `AreaCalculator` 클래스는 수정할 필요가 없습니다.
- [[다형성]]을 통해 설계가 더 유연해졌습니다.

## L - 리스코프 치환 원칙 (Liskov Substitution Principle)

> "프로그램의 객체는 프로그램의 정확성을 깨뜨리지 않으면서 하위 타입의 인스턴스로 바꿀 수 있어야 한다."

바바라 리스코프(Barbara Liskov)가 1987년에 소개한 이 원칙은 상속 관계에서 중요한 개념입니다. 쉽게 말해, 자식 클래스는 부모 클래스의 행동을 완벽하게 대체할 수 있어야 합니다.

### 위반 사례:

```java
public class Rectangle {
    protected double width;
    protected double height;
    
    public void setWidth(double width) {
        this.width = width;
    }
    
    public void setHeight(double height) {
        this.height = height;
    }
    
    public double getArea() {
        return width * height;
    }
}

public class Square extends Rectangle {
    @Override
    public void setWidth(double width) {
        this.width = width;
        this.height = width;  // 정사각형이므로 너비와 높이가 같아야 함
    }
    
    @Override
    public void setHeight(double height) {
        this.height = height;
        this.width = height;  // 정사각형이므로 너비와 높이가 같아야 함
    }
}
```

문제점:

```java
void testRectangle(Rectangle r) {
    r.setWidth(5);
    r.setHeight(4);
    // 직사각형이면 면적은 20이어야 함
    assert r.getArea() == 20;  // 직사각형이면 통과, 정사각형이면 실패
}
```

이 테스트는 `Rectangle` 객체로는 통과하지만 `Square` 객체로는 실패합니다. 이는 리스코프 치환 원칙을 위반합니다.

### 개선된 버전:

```java
public interface Shape {
    double getArea();
}

public class Rectangle implements Shape {
    private double width;
    private double height;
    
    public Rectangle(double width, double height) {
        this.width = width;
        this.height = height;
    }
    
    public double getWidth() {
        return width;
    }
    
    public double getHeight() {
        return height;
    }
    
    @Override
    public double getArea() {
        return width * height;
    }
}

public class Square implements Shape {
    private double side;
    
    public Square(double side) {
        this.side = side;
    }
    
    public double getSide() {
        return side;
    }
    
    @Override
    public double getArea() {
        return side * side;
    }
}
```

개선된 점:

- `Square`가 `Rectangle`을 상속하지 않고, 둘 다 `Shape` 인터페이스를 구현합니다.
- 각 클래스는 자신의 속성에 맞게 동작합니다.
- 어떤 `Shape` 객체를 사용하든 예측 가능한 방식으로 작동합니다.

## I - 인터페이스 분리 원칙 (Interface Segregation Principle)

> "클라이언트는 자신이 사용하지 않는 메서드에 의존하도록 강요받지 않아야 한다."

이 원칙은 큰 인터페이스를 여러 개의 작은 인터페이스로 분리하는 것이 좋다고 말합니다. 클라이언트는 필요한 메서드만 있는 인터페이스만 알고 있으면 됩니다.

### 위반 사례:

```java
public interface Worker {
    void work();
    void eat();
    void sleep();
}

public class Human implements Worker {
    @Override
    public void work() {
        System.out.println("Human is working");
    }
    
    @Override
    public void eat() {
        System.out.println("Human is eating");
    }
    
    @Override
    public void sleep() {
        System.out.println("Human is sleeping");
    }
}

public class Robot implements Worker {
    @Override
    public void work() {
        System.out.println("Robot is working");
    }
    
    @Override
    public void eat() {
        // 로봇은 먹지 않음
        throw new UnsupportedOperationException("Robots don't eat");
    }
    
    @Override
    public void sleep() {
        // 로봇은 자지 않음
        throw new UnsupportedOperationException("Robots don't sleep");
    }
}
```

문제점:

- `Robot` 클래스는 `eat()`와 `sleep()` 메서드를 구현해야 하지만, 실제로는 이러한 동작을 수행할 수 없습니다.
- 클라이언트는 사용하지 않는 메서드에 의존하게 됩니다.

### 개선된 버전:

```java
public interface Workable {
    void work();
}

public interface Eatable {
    void eat();
}

public interface Sleepable {
    void sleep();
}

public class Human implements Workable, Eatable, Sleepable {
    @Override
    public void work() {
        System.out.println("Human is working");
    }
    
    @Override
    public void eat() {
        System.out.println("Human is eating");
    }
    
    @Override
    public void sleep() {
        System.out.println("Human is sleeping");
    }
}

public class Robot implements Workable {
    @Override
    public void work() {
        System.out.println("Robot is working");
    }
}
```

개선된 점:

- 인터페이스가 더 작고 집중된 책임을 가집니다.
- `Robot` 클래스는 필요한 `Workable` 인터페이스만 구현합니다.
- 클라이언트는 필요한 기능만 사용할 수 있습니다.

## D - 의존성 역전 원칙 (Dependency Inversion Principle)

> "고수준 모듈은 저수준 모듈에 의존해서는 안 된다. 둘 다 추상화에 의존해야 한다." "추상화는 세부사항에 의존해서는 안 된다. 세부사항은 추상화에 의존해야 한다."

이 원칙은 소프트웨어 모듈 간의 의존성 방향에 관한 것입니다. 전통적인 의존성 방향을 뒤집어 유연성을 증가시키는 것이 목표입니다.

### 위반 사례:

```java
public class LightBulb {
    public void turnOn() {
        System.out.println("LightBulb turned on");
    }
    
    public void turnOff() {
        System.out.println("LightBulb turned off");
    }
}

public class Switch {
    private LightBulb bulb;
    
    public Switch() {
        this.bulb = new LightBulb();
    }
    
    public void operate() {
        // ... 스위치 상태 로직
        bulb.turnOn();
    }
}
```

문제점:

- `Switch` 클래스가 `LightBulb` 클래스에 직접 의존합니다.
- 다른 종류의 장치(예: 팬, TV)를 제어하려면 `Switch` 클래스를 수정해야 합니다.

### 개선된 버전:

```java
public interface Switchable {
    void turnOn();
    void turnOff();
}

public class LightBulb implements Switchable {
    @Override
    public void turnOn() {
        System.out.println("LightBulb turned on");
    }
    
    @Override
    public void turnOff() {
        System.out.println("LightBulb turned off");
    }
}

public class Fan implements Switchable {
    @Override
    public void turnOn() {
        System.out.println("Fan turned on");
    }
    
    @Override
    public void turnOff() {
        System.out.println("Fan turned off");
    }
}

public class Switch {
    private Switchable device;
    
    public Switch(Switchable device) {
        this.device = device;
    }
    
    public void operate() {
        // ... 스위치 상태 로직
        device.turnOn();
    }
}
```

개선된 점:

- 고수준 모듈(`Switch`)과 저수준 모듈(`LightBulb`, `Fan`)이 모두 추상화(`Switchable` 인터페이스)에 의존합니다.
- `Switch` 클래스는 구체적인 구현이 아닌 추상화에 의존하므로 다양한 장치와 함께 사용할 수 있습니다.
- 새로운 장치를 추가할 때 기존 코드를 수정할 필요가 없습니다.

## SOLID 원칙의 실제 적용: 스프링 프레임워크 예시

스프링 프레임워크는 SOLID 원칙을 잘 구현한 예입니다. 특히 의존성 주입(DI)과 관련하여 의존성 역전 원칙(DIP)을 핵심으로 사용합니다.

### 예시: 간단한 사용자 관리 시스템

```java
// 인터페이스 정의 (추상화)
public interface UserRepository {
    User findById(Long id);
    void save(User user);
}

// 구현체 (세부사항)
@Repository
public class JpaUserRepository implements UserRepository {
    @PersistenceContext
    private EntityManager entityManager;

    @Override
    public User findById(Long id) {
        return entityManager.find(User.class, id);
    }

    @Override
    public void save(User user) {
        entityManager.persist(user);
    }
}

// 서비스 계층 (고수준 모듈)
@Service
public class UserService {
    private final UserRepository userRepository;
    
    // 의존성 주입을 통한 의존성 역전 구현
    @Autowired
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }
    
    public User getUserById(Long id) {
        return userRepository.findById(id);
    }
    
    public void createUser(User user) {
        // 비즈니스 로직
        userRepository.save(user);
    }
}

// 컨트롤러 (클라이언트)
@RestController
@RequestMapping("/users")
public class UserController {
    private final UserService userService;
    
    @Autowired
    public UserController(UserService userService) {
        this.userService = userService;
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<User> getUser(@PathVariable Long id) {
        User user = userService.getUserById(id);
        return ResponseEntity.ok(user);
    }
    
    @PostMapping
    public ResponseEntity<Void> createUser(@RequestBody User user) {
        userService.createUser(user);
        return ResponseEntity.status(HttpStatus.CREATED).build();
    }
}
```

이 예시에서:

- **단일 책임 원칙(SRP)**: 각 클래스는 하나의 책임만 가집니다. `UserRepository`는 데이터 접근, `UserService`는 비즈니스 로직, `UserController`는 HTTP 요청 처리만 담당합니다.
- **개방-폐쇄 원칙(OCP)**: 새로운 저장소 구현(예: `MongoUserRepository`)을 추가할 때 기존 코드를 수정할 필요가 없습니다.
- **리스코프 치환 원칙(LSP)**: `JpaUserRepository`는 `UserRepository` 인터페이스를 완벽하게 구현하므로 언제든지 대체 가능합니다.
- **인터페이스 분리 원칙(ISP)**: `UserRepository` 인터페이스는 필요한 메서드만 정의합니다.
- **의존성 역전 원칙(DIP)**: 고수준 모듈(`UserService`)은 저수준 모듈(`JpaUserRepository`)에 직접 의존하지 않고, 추상화(`UserRepository` 인터페이스)에 의존합니다.

## SOLID 원칙의 이점

SOLID 원칙을 따르면 다음과 같은 이점을 얻을 수 있습니다:

1. **유지보수성 향상**: 코드가 모듈화되어 변경 사항이 격리됩니다.
2. **확장성 개선**: 기존 코드를 수정하지 않고도 새로운 기능을 추가할 수 있습니다.
3. **테스트 용이성**: 각 컴포넌트를 독립적으로 테스트하기 쉽습니다.
4. **코드 재사용성 증가**: 느슨하게 결합된 컴포넌트는 여러 곳에서 재사용하기 쉽습니다.
5. **더 명확한 설계**: 책임이 명확하게 분리되어 코드를 이해하기 쉽습니다.

## SOLID 원칙 적용 시 주의사항

SOLID 원칙을 맹목적으로 따르는 것은 위험할 수 있습니다. 다음 사항을 고려해야 합니다:

1. **과잉 엔지니어링 방지**: 작은 문제에 복잡한 솔루션을 적용하지 마세요.
2. **실용성 유지**: 완벽한 설계보다 실용적인 설계가 더 중요할 수 있습니다.
3. **점진적 적용**: 기존 코드베이스에 점진적으로 SOLID 원칙을 적용하세요.
4. **상황에 맞는 판단**: 모든 상황에 모든 원칙이 적합하지는 않습니다.

## 결론

SOLID 원칙은 객체지향 설계의 핵심 기둥이며, 유지보수가 용이하고 확장 가능한 소프트웨어를 만드는 데 중요한 지침을 제공합니다. 이러한 원칙을 이해하고 적절하게 적용하면 더 나은 코드 구조를 만들고 장기적으로 개발 비용을 절감할 수 있습니다.

그러나 SOLID 원칙은 도그마가 아니라 지침으로 생각해야 합니다. 항상 문제의 복잡성과 프로젝트의 요구 사항을 고려하여 적절한 수준의 추상화와 모듈화를 적용해야 합니다.

여러분의 다음 프로젝트에서 SOLID 원칙을 적용해 보세요. 처음에는 어려울 수 있지만, 시간이 지남에 따라 이러한 원칙이 자연스럽게 여러분의 설계 사고방식에 녹아들 것입니다.

## 관련 노트

- [[다형성]]
- [[객체지향 설계]]
- [[디자인 패턴]]
- [[테스트 주도 개발]]
- [[스프링 프레임워크]]