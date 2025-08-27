소프트웨어 테스트에서 **테스트 스텁(Test Stub)**은 테스트 대상 시스템(SUT, System Under Test)이 의존하는 다른 컴포넌트의 실제 구현을 대체하는 간단한 코드 조각입니다. 주로 [[단위 테스트(Unit Test)]]나 [[하향식 통합 테스트]]에서 사용되며, 테스트 환경을 제어하고 예측 가능한 결과를 얻기 위해 활용됩니다.

스텁을 사용하면 아직 개발되지 않았거나, 테스트하기 어렵거나, 느리거나, 예측 불가능한 외부 의존성을 격리하여 테스트 대상 코드에만 집중할 수 있습니다.

---

## 테스트 스텁의 정의 및 목적

### 정의 (Definition)

**테스트 스텁**은 테스트 중에 호출될 때 미리 정해진 (canned) 응답을 반환하도록 프로그래밍된 모의 객체(Test Double)의 한 유형입니다. 실제 의존 객체와 동일한 인터페이스(또는 클래스)를 가지지만, 실제 로직을 수행하는 대신 테스트 케이스가 요구하는 특정 상황을 시뮬레이션하는 단순한 로직만을 포함합니다.

예를 들어, 데이터베이스에서 사용자 정보를 가져오는 모듈을 테스트할 때, 실제 데이터베이스에 접근하는 대신 "항상 '홍길동' 사용자 정보를 반환하는" 스텁을 사용할 수 있습니다.

### 목적 (Purpose)

테스트 스텁은 다음과 같은 다양한 목적을 위해 사용됩니다.

1. 의존성 격리 (Dependency Isolation):
    
    테스트 대상 코드(SUT)를 외부 의존성으로부터 분리합니다. 이를 통해 테스트는 외부 환경의 변화나 불안정성에 영향을 받지 않고 오직 SUT의 로직 정확성만을 검증할 수 있게 되어 테스트의 신뢰성과 예측 가능성을 높입니다.
    
2. 미개발 모듈 대체 (Placeholder for Unimplemented Modules):
    
    [[하향식 통합 테스트]]에서처럼 아직 개발되지 않은 하위 모듈의 역할을 임시로 수행합니다. 이를 통해 상위 모듈의 개발과 테스트를 하위 모듈의 완료 여부와 관계없이 진행할 수 있습니다.
    
3. 특정 조건/경로 시뮬레이션 (Simulating Specific Conditions/Paths):
    
    실제 환경에서 만들기 어렵거나 위험한 특정 상황(예: 네트워크 오류, 디스크 공간 부족, 특정 예외 발생)이나 코드 경로를 스텁을 통해 손쉽게 시뮬레이션할 수 있습니다.
    
4. 테스트 속도 향상 (Improving Test Speed):
    
    실제 데이터베이스 접근, 외부 API 호출 등 시간이 오래 걸리는 작업을 수행하는 의존성을 스텁으로 대체하면 테스트 실행 시간을 크게 단축시킬 수 있습니다. 이는 개발 과정에서 빠른 피드백을 얻는 데 매우 중요합니다.
    
5. 테스트 결정성 확보 (Ensuring Test Determinism):
    
    외부 요인(예: 현재 시간, 랜덤 값, 외부 서비스의 가변적인 응답)에 따라 결과가 달라질 수 있는 부분을 고정된 응답을 반환하는 스텁으로 대체함으로써, 테스트가 항상 동일한 조건에서 실행되고 일관된 결과를 내도록 보장합니다.
    

---

## 테스트 스텁의 주요 특징

테스트 스텁은 일반적으로 다음과 같은 특징을 가집니다.

- **단순함 (Simplicity):** 실제 의존성보다 훨씬 간단한 로직을 가집니다. 복잡한 비즈니스 로직이나 내부 상태 관리를 포함하지 않는 것이 일반적입니다.
- **제어된 응답 (Controlled Responses):** 테스트 케이스의 특정 요구에 따라 미리 정의된, 하드코딩된 값을 반환합니다. 특정 입력에 대해 어떤 출력을 줄지 명확하게 설정됩니다.
- **상태 비저장 또는 최소 상태 (Stateless or Minimal State):** 대부분의 스텁은 호출 간에 상태를 유지하지 않거나, 테스트에 필요한 최소한의 상태 정보만을 가집니다.
- **인터페이스 일치 (Interface Implementation):** 테스트 대상 코드가 실제 의존 객체를 사용하는 방식 그대로 스텁을 사용할 수 있도록, 실제 의존 객체와 동일한 인터페이스를 구현하거나 동일한 메서드 시그니처를 제공합니다.

---

## 테스트 스텁 구현 방법

테스트 스텁은 직접 코드를 작성하여 수동으로 구현하거나, 테스트 프레임워크 및 라이브러리의 도움을 받아 구현할 수 있습니다.

### 1. 수동 구현 (Manual Implementation)

개발자가 직접 의존성의 인터페이스를 구현하는 클래스를 작성하여 스텁을 만듭니다.

**예시 (Java):**

`UserRepository` 인터페이스와 이를 사용하는 `UserService`가 있다고 가정해 보겠습니다.

```java
// UserRepository.java (인터페이스)
public interface UserRepository {
    User findById(String id);
    boolean save(User user);
}

// User.java (데이터 클래스)
public class User {
    private String id;
    private String name;

    public User(String id, String name) {
        this.id = id;
        this.name = name;
    }
    public String getId() { return id; }
    public String getName() { return name; }
    // ... 기타 메서드
}

// UserService.java (테스트 대상)
public class UserService {
    private UserRepository userRepository;

    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public String getUserGreeting(String userId) {
        User user = userRepository.findById(userId);
        if (user != null) {
            return "안녕하세요, " + user.getName() + "님!";
        } else {
            return "사용자를 찾을 수 없습니다.";
        }
    }
}
```

이제 `findById` 메서드가 특정 사용자 정보를 반환하도록 하는 스텁을 수동으로 구현합니다.

```java
// UserFindByIdStub.java (수동으로 작성한 스텁)
public class UserFindByIdStub implements UserRepository {
    private User userToReturn;
    private String expectedId;

    public UserFindByIdStub(String expectedId, User userToReturn) {
        this.expectedId = expectedId;
        this.userToReturn = userToReturn;
    }

    @Override
    public User findById(String id) {
        System.out.println("Stub: findById 호출됨 (id: " + id + ")");
        if (this.expectedId.equals(id)) {
            return this.userToReturn;
        }
        return null; // 예상 ID가 아니면 null 반환
    }

    @Override
    public boolean save(User user) {
        // 이 테스트에서는 save 동작이 중요하지 않으므로 간단히 true 반환
        System.out.println("Stub: save 호출됨 (user: " + user.getName() + "), 항상 true 반환");
        return true;
    }
}

// 테스트 코드 예시
// import org.junit.jupiter.api.Test;
// import static org.junit.jupiter.api.Assertions.assertEquals;
//
// public class UserServiceTest {
//     @Test
//     void testGetUserGreeting_UserExists() {
//         // Given: 특정 ID로 조회 시 반환될 User 객체와 스텁 생성
//         User stubbedUser = new User("test1", "홍길동");
//         UserRepository userRepositoryStub = new UserFindByIdStub("test1", stubbedUser);
//         UserService userService = new UserService(userRepositoryStub);
//
//         // When: 스텁을 사용하는 서비스 메서드 호출
//         String greeting = userService.getUserGreeting("test1");
//
//         // Then: 예상되는 인사말 검증
//         assertEquals("안녕하세요, 홍길동님!", greeting);
//     }
// }
```

- **장점:** 특정 요구사항에 매우 세밀하게 맞춘 스텁을 만들 수 있습니다. 외부 라이브러리 의존성이 없습니다.
- **단점:** 만들어야 할 스텁이 많아지면 반복적인 코드가 늘어나고 유지보수가 어려워질 수 있습니다.

### 2. 테스트 프레임워크/라이브러리 사용 (Using Testing Frameworks/Libraries)

[[Mockito Strict Stubbing]], EasyMock, JMock (Java의 경우)와 같은 목킹(Mocking) 프레임워크를 사용하면 스텁을 훨씬 간결하고 유연하게 생성할 수 있습니다. 이러한 도구들은 런타임에 동적으로 스텁 객체를 생성하고 그 동작을 정의할 수 있게 해줍니다.

**예시 (Java - Mockito 사용):**

Java

```
// UserServiceTestWithMockito.java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.*; // Mockito 임포트

public class UserServiceTestWithMockito {

    @Test
    void testGetUserGreeting_UserExists_WithMockito() {
        // Given: Mockito를 사용하여 UserRepository의 목(스텁 역할) 생성
        UserRepository mockUserRepository = mock(UserRepository.class);
        User predefinedUser = new User("test1", "홍길동");

        // 스텁 설정: mockUserRepository의 findById("test1")가 호출되면 predefinedUser를 반환
        when(mockUserRepository.findById("test1")).thenReturn(predefinedUser);

        UserService userService = new UserService(mockUserRepository);

        // When: 스텁을 사용하는 서비스 메서드 호출
        String greeting = userService.getUserGreeting("test1");

        // Then: 예상되는 인사말 검증
        assertEquals("안녕하세요, 홍길동님!", greeting);

        // (선택적) findById 메서드가 "test1" 인자로 1번 호출되었는지 검증
        verify(mockUserRepository, times(1)).findById("test1");
    }

    @Test
    void testGetUserGreeting_UserNotFound_WithMockito() {
        // Given
        UserRepository mockUserRepository = mock(UserRepository.class);

        // 스텁 설정: findById("unknown")가 호출되면 null을 반환 (Mockito의 기본 동작이기도 함)
        when(mockUserRepository.findById("unknown")).thenReturn(null);

        UserService userService = new UserService(mockUserRepository);

        // When
        String greeting = userService.getUserGreeting("unknown");

        // Then
        assertEquals("사용자를 찾을 수 없습니다.", greeting);
    }
}
```

- **장점:** 필요한 스텁 코드를 직접 작성하는 수고를 덜어줍니다. 다양한 상황에 대한 스텁의 동작을 유연하게 정의할 수 있으며, 테스트 코드의 가독성도 높일 수 있습니다.
- **단점:** 해당 프레임워크의 사용법을 익혀야 합니다.
- 더 자세한 Mockito 사용법은 Mockito로 스텁(Stub) 구현하기 노트를 참고해 주세요.

---

## 테스트 스텁 사용 시 주의사항

- **과도한 스텁 사용 지양 (Avoid Overuse):** 모든 의존성을 스텁으로 대체하면 테스트가 실제 실행 환경과 너무 동떨어질 수 있습니다. 이는 단위 테스트에서는 유용하지만, [[통합 테스트(Integration Test)]]의 목적을 저해할 수 있습니다. 필요한 최소한의 범위에서 스텁을 활용하는 것이 좋습니다.
- **스텁의 정확성 유지 (Maintain Stub Accuracy):** 스텁이 모방하는 실제 컴포넌트의 인터페이스나 기본적인 반환 값의 규칙이 변경되면, 스텁도 이에 맞춰 업데이트해야 합니다. 그렇지 않으면 테스트가 잘못된 가정 하에 수행될 수 있습니다.
- **스텁 로직은 단순하게 (Keep Stub Logic Simple):** 스텁은 가능한 한 단순해야 합니다. 스텁 내부에 복잡한 로직이 들어가면 스텁 자체가 버그의 원인이 되거나 스텁을 위한 테스트가 필요해지는 아이러니한 상황이 발생할 수 있습니다.
- **테스트의 의도 명확화 (Clarify Test Intent):** 스텁이 어떤 특정 상황을 시뮬레이션하고 어떤 값을 반환하도록 설정되었는지 테스트 코드를 통해 명확히 드러나야 합니다. 이는 테스트를 이해하고 유지보수하는 데 중요합니다.

---

## 스텁(Stub) vs 목(Mock) vs 페이크(Fake)

테스트 스텁은 [[테스트 더블(Test Double)]]의 한 종류입니다. 테스트 더블에는 스텁 외에도 목(Mock), 페이크(Fake), 더미(Dummy), 스파이(Spy) 등이 있습니다.

간단히 말해, **스텁**은 주로 테스트 중 호출에 대해 미리 준비된 값을 반환하여 **상태 검증(state verification)**을 돕는 데 중점을 둡니다. 반면, **목**은 호출되었을 때의 행위(예: 특정 메서드가 특정 인자로 몇 번 호출되었는지)를 기록하고 이를 검증하는 **행위 검증(behavior verification)**에 더 중점을 둡니다.

이들의 자세한 차이점은 Mocks, Stubs, Fakes의 차이 문서에서 더 깊이 있게 다루겠습니다.

---

## 결론

테스트 스텁은 의존성을 효과적으로 관리하고, 제어 가능하며 예측 가능한 테스트 환경을 구축하는 데 필수적인 도구입니다. 수동으로 구현하거나 테스트 프레임워크를 활용하여 스텁을 적절히 사용하면, 테스트 대상 코드의 격리 수준을 높이고, 테스트 실행 속도를 개선하며, 다양한 시나리오를 효과적으로 검증할 수 있습니다. 이를 통해 소프트웨어의 품질을 향상시키고 개발 효율성을 높이는 데 크게 기여합니다.

---

## 참고 자료

- Fowler, Martin. (2007). _Mocks Aren't Stubs_. ([https://martinfowler.com/articles/mocksArentStubs.html](https://martinfowler.com/articles/mocksArentStubs.html))
- Mockito Documentation ([https://site.mockito.org/](https://site.mockito.org/))
- JUnit 5 User Guide ([https://junit.org/junit5/docs/current/user-guide/](https://junit.org/junit5/docs/current/user-guide/))
- Meszaros, Gerard. (2007). _xUnit Test Patterns: Refactoring Test Code_. Addison-Wesley. (Chapter on Test Double)