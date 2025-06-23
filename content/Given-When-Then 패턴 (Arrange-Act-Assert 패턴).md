테스트 코드를 작성하는 것은 이제 선택이 아닌 필수인 시대입니다. 하지만 단순히 코드를 커버하는 것을 넘어, **읽기 쉽고 이해하기 쉬우며 유지보수가 용이한 테스트 코드**를 작성하는 것은 또 다른 차원의 이야기입니다. 바로 이때, Given-When-Then (또는 Arrange-Act-Assert) 패턴이 빛을 발합니다. 이 패턴은 테스트 코드의 구조를 명확하게 만들어, 마치 잘 쓰인 한 편의 시나리오처럼 테스트의 의도를 명확히 전달해 줍니다.

이 글을 통해 Given-When-Then 패턴이 무엇인지, 각 단계가 어떤 의미를 가지는지, 그리고 이 패턴을 사용함으로써 얻을 수 있는 이점은 무엇인지 명확하게 이해하실 수 있을 것입니다. 더 나아가, 실제 Java와 Spring 환경에서 어떻게 적용할 수 있는지 간단한 예시를 통해 살펴보겠습니다.

---

## Given-When-Then 패턴이란?

**Given-When-Then 패턴**은 테스트 코드의 구조를 세 부분으로 나누어 작성하는 방식입니다. 이 패턴은 [[행위 주도 개발(BDD)]]에서 유래되었으며, 테스트의 목적과 흐름을 명확하게 표현하는 데 도움을 줍니다. 많은 개발자들이 이 패턴을 **Arrange-Act-Assert (AAA) 패턴**이라고도 부르는데, 사실상 동일한 개념을 지칭합니다.

각 단계는 다음과 같은 의미를 가집니다:

- **Given (준비, Arrange)**: 테스트를 실행하기 위한 **사전 조건**을 설정하는 단계입니다. 테스트 대상 시스템이나 객체가 특정 상태에 있도록 만들거나, 필요한 데이터를 준비하고, 의존성을 설정하는 작업을 포함합니다.
- **When (실행, Act)**: 실제로 **테스트하려는 동작**을 수행하는 단계입니다. 일반적으로 테스트 대상 객체의 메서드를 호출하거나, 특정 기능을 실행시키는 코드가 위치합니다.
- **Then (검증, Assert)**: When 단계에서 실행한 동작의 **결과를 확인하고 검증**하는 단계입니다. 예상한 결과값과 실제 결과값을 비교하거나, 시스템의 상태 변화가 올바르게 이루어졌는지, 혹은 특정 예외가 발생했는지 등을 확인합니다.

이 패턴을 사용하면 테스트의 의도가 명확해지고, 어떤 부분을 테스트하는지, 어떤 결과를 기대하는지를 쉽게 파악할 수 있습니다. 이는 테스트 코드의 가독성을 높여줄 뿐만 아니라, 유지보수와 팀원 간의 협업에도 큰 도움을 줍니다.

---

## 각 단계별 상세 설명

Given-When-Then 패턴의 각 단계를 좀 더 자세히 살펴보겠습니다.

### 1. Given (준비 / Arrange)

이 단계의 핵심 목표는 **테스트 시나리오를 실행하는 데 필요한 모든 환경과 조건을 설정**하는 것입니다. 마치 연극의 막이 오르기 전에 무대를 준비하는 것과 같습니다.

- **무엇을 준비해야 할까요?**
    - 테스트 대상 객체 생성 및 초기화
    - 테스트에 필요한 입력 데이터 생성 (예: 특정 값을 가진 변수, 객체)
    - 외부 의존성 설정 (예: [[Mocking|모킹(Mocking)]]을 이용한 가짜 객체 주입)
    - 테스트 시작 전 시스템이 특정 상태에 있도록 설정 (예: 데이터베이스에 특정 데이터 삽입)

이 단계에서는 테스트의 **맥락(Context)**을 명확히 정의하는 것이 중요합니다. "어떤 상황에서" 테스트가 진행되는지를 설명하는 부분이기 때문입니다.

### 2. When (실행 / Act)

Given 단계에서 모든 준비가 끝났다면, 이제 **실제로 테스트하고자 하는 행동**을 수행할 차례입니다. 이 단계는 테스트 시나리오의 주인공이 등장하여 특정 행동을 하는 장면과 같습니다.

- **무엇을 실행해야 할까요?**
    - 주로 테스트 대상 클래스의 특정 메서드를 호출합니다.
    - 하나의 특정 동작(Action)에 집중하는 것이 좋습니다. 여러 동작을 한 번에 테스트하려고 하면 테스트의 의도가 불분명해지고 실패 시 원인 파악이 어려워질 수 있습니다.

When 단계는 "무엇을 할 때"에 해당하는 부분으로, 테스트의 핵심 로직을 실행하는 부분입니다.

### 3. Then (검증 / Assert)

When 단계에서 특정 행동을 수행했다면, 그 결과가 **우리가 예상한 대로인지 확인**하는 단계입니다. 연극의 결말에서 관객이 기대했던 메시지나 감동을 얻는 것과 비슷합니다.

- **무엇을 검증해야 할까요?**
    - 메서드의 반환 값이 예상과 일치하는지 확인합니다.
    - 객체의 상태가 기대한 대로 변경되었는지 확인합니다.
    - 특정 메서드가 예상한 횟수만큼 호출되었는지 확인합니다 (Mockito의 `verify` 등).
    - 예상된 예외가 올바르게 발생하는지 확인합니다.
    - [[Assertion Library|단언 라이브러리(Assertion Library)]] (예: JUnit의 Assertions, AssertJ 등)를 사용하여 검증 로직을 명확하고 간결하게 작성하는 것이 좋습니다.

Then 단계는 "어떤 결과가 나와야 하는가"를 명확히 기술하며, 테스트의 성공 또는 실패를 판정하는 기준이 됩니다.

---

## Given-When-Then 패턴의 장점 ✨

이 패턴을 꾸준히 사용하면 다음과 같은 다양한 이점을 얻을 수 있습니다.

- **명확성 및 가독성 향상**: 테스트 코드의 각 부분이 무엇을 하는지 명확하게 구분되어, 코드를 처음 보는 사람도 테스트의 의도와 흐름을 쉽게 이해할 수 있습니다. 이는 마치 잘 정리된 설명서를 읽는 것과 같습니다.
- **유지보수 용이성**: 테스트의 구조가 명확하기 때문에 요구사항 변경이나 코드 수정 시 테스트 코드를 수정하거나 디버깅하기가 훨씬 수월해집니다. 문제가 발생했을 때 어느 부분(준비, 실행, 검증)에서 문제가 생겼는지 파악하기도 용이합니다.
- **협업 강화**: 팀원 모두가 일관된 구조로 테스트 코드를 작성하게 되므로, 코드 리뷰가 용이해지고 테스트에 대한 팀 전체의 이해도가 높아집니다. 이는 마치 공통된 언어로 소통하는 것과 같습니다.
- **행위 주도 개발(BDD)과의 자연스러운 연결**: 이 패턴은 [[행위 주도 개발(BDD)]]의 시나리오 작성 스타일과 매우 유사하여, BDD를 도입하거나 실천하는 데 자연스럽게 활용될 수 있습니다. 테스트 자체가 시스템의 행위에 대한 명세서 역할을 할 수 있습니다.
- **더 나은 설계 유도**: 테스트를 Given-When-Then 구조로 생각하다 보면, 자연스럽게 테스트 가능한 코드를 작성하도록 유도됩니다. 이는 각 컴포넌트의 책임을 명확히 하고 [[결합도(Coupling)]]를 낮추는 데 기여할 수 있습니다.

---

## Java 및 Spring 환경에서의 예시 ☕

백문이 불여일견입니다. 간단한 Java 코드와 [[JUnit]] 및 [[Mockito Strict Stubbing]]를 사용하여 Given-When-Then 패턴을 적용한 테스트 예시를 살펴보겠습니다. 사용자를 관리하는 `UserService`가 있고, `getUserById`라는 메서드를 테스트한다고 가정해 봅시다.

```java
// 테스트 대상 클래스 (간략화된 예시)
// public class UserService {
//     private UserRepository userRepository;
//     public UserService(UserRepository userRepository) { this.userRepository = userRepository; }
//     public UserDto getUserById(Long id) { /* ... 로직 ... */ }
// }
// public interface UserRepository { User findById(Long id); }
// public class User { /* ... 필드 및 메서드 ... */ }
// public class UserDto { /* ... 필드 및 메서드 ... */ }
// public class UserNotFoundException extends RuntimeException { /* ... */ }

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class UserServiceTest {

    @Test
    @DisplayName("존재하는 사용자 ID로 조회 시 사용자 정보 DTO 반환")
    void getUserById_whenUserExists_shouldReturnUserDto() {
        // Given (준비)
        UserRepository mockUserRepository = mock(UserRepository.class); // UserRepository의 Mock 객체 생성
        UserService userService = new UserService(mockUserRepository); // 테스트 대상 객체에 Mock 객체 주입
        Long userId = 1L;
        User expectedUser = new User(userId, "테스트 유저", "test@example.com"); // 예상되는 User 객체
        UserDto expectedUserDto = new UserDto("테스트 유저", "test@example.com"); // 예상되는 UserDto 객체

        // mockUserRepository.findById(userId)가 호출되면 expectedUser를 반환하도록 설정
        when(mockUserRepository.findById(userId)).thenReturn(expectedUser);

        // When (실행)
        UserDto actualUserDto = userService.getUserById(userId); // 실제 테스트할 메서드 호출

        // Then (검증)
        assertNotNull(actualUserDto);
        assertEquals(expectedUserDto.getName(), actualUserDto.getName(), "사용자 이름이 일치해야 합니다.");
        assertEquals(expectedUserDto.getEmail(), actualUserDto.getEmail(), "사용자 이메일이 일치해야 합니다.");

        // mockUserRepository.findById 메서드가 userId 인자로 정확히 1번 호출되었는지 검증
        verify(mockUserRepository, times(1)).findById(userId);
    }

    @Test
    @DisplayName("존재하지 않는 사용자 ID로 조회 시 UserNotFoundException 발생")
    void getUserById_whenUserNotExists_shouldThrowUserNotFoundException() {
        // Given (준비)
        UserRepository mockUserRepository = mock(UserRepository.class);
        UserService userService = new UserService(mockUserRepository);
        Long nonExistentUserId = 99L;

        // mockUserRepository.findById(nonExistentUserId)가 호출되면 null을 반환하도록 설정 (사용자가 없음을 의미)
        when(mockUserRepository.findById(nonExistentUserId)).thenReturn(null);

        // When & Then (실행 및 검증)
        // userService.getUserById(nonExistentUserId) 실행 시 UserNotFoundException이 발생하는지 검증
        UserNotFoundException exception = assertThrows(UserNotFoundException.class, () -> {
            userService.getUserById(nonExistentUserId);
        });

        // 발생한 예외 메시지가 예상과 일치하는지 확인
        assertEquals("User not found with id: " + nonExistentUserId, exception.getMessage());

        // mockUserRepository.findById 메서드가 nonExistentUserId 인자로 정확히 1번 호출되었는지 검증
        verify(mockUserRepository, times(1)).findById(nonExistentUserId);
    }
}
```

위 예시 코드에서 각 테스트 메서드는 명확하게 Given, When, Then (또는 Arrange, Act, Assert) 주석으로 구분되어 있습니다. 이를 통해 각 부분이 어떤 역할을 하는지 한눈에 파악할 수 있습니다. 또한 `@DisplayName` 어노테이션을 사용하여 테스트의 목적을 자연어로 설명함으로써 가독성을 더욱 높였습니다.

Spring Boot 환경에서 테스트를 작성할 때도 `@SpringBootTest`, `@MockBean` 등의 어노테이션과 함께 이 패턴을 동일하게 적용할 수 있습니다. 자세한 내용은 [[Spring Boot 테스트 전략]] 문서를 참고해주세요.

---

## Given-When-Then 패턴 작성 시 고려사항 🧐

이 패턴을 효과적으로 사용하기 위해 몇 가지 고려할 점들이 있습니다.

- **하나의 테스트는 하나의 시나리오만**: 각 테스트 메서드는 명확하게 하나의 특정 시나리오, 즉 하나의 "Given-When-Then" 흐름만을 검증해야 합니다. 이를 통해 테스트가 실패했을 때 원인을 빠르게 파악하고 수정할 수 있습니다. 이는 [[단위 테스트(Unit Test)]]의 기본 원칙과도 맞닿아 있습니다.
- **독립적인 테스트**: 각 테스트는 다른 테스트의 결과에 영향을 받거나 의존해서는 안 됩니다. 항상 독립적으로 실행될 수 있어야 일관된 결과를 보장합니다.
- **Given, When, Then 단계의 명확한 분리**: 각 단계의 책임이 명확해야 합니다. 예를 들어, Given 단계에서 검증 로직을 넣거나 When 단계에서 너무 많은 준비 코드를 넣는 것은 피해야 합니다.
- **간결하고 명료한 설명**: 각 단계의 코드는 가능한 간결하게 작성하고, 필요하다면 주석이나 `@DisplayName` 같은 기능을 활용하여 테스트의 의도를 명확히 전달해야 합니다.
- **Then 단계의 구체적인 검증**: 막연하게 "성공했다"가 아니라, "어떤 값이 무엇이어야 한다" 또는 "어떤 상태가 어떻게 변경되어야 한다" 와 같이 구체적으로 검증해야 합니다.

---

## 결론 🚀

Given-When-Then (또는 Arrange-Act-Assert) 패턴은 단순히 테스트 코드를 "작성"하는 것을 넘어, "잘 작성된" 테스트 코드를 만드는 데 매우 유용한 프레임워크입니다. 이 패턴을 통해 우리는 테스트의 의도를 명확히 하고, 가독성과 유지보수성을 높이며, 팀원들과 효과적으로 소통할 수 있습니다.

처음에는 각 단계를 나누어 생각하는 것이 다소 어색할 수 있지만, 꾸준히 연습하고 적용하다 보면 자연스럽게 체화될 것입니다. 명확하고 견고한 테스트 코드는 결국 더 안정적이고 품질 높은 소프트웨어를 만드는 데 핵심적인 역할을 한다는 점을 기억하시길 바랍니다.

지금 바로 여러분의 테스트 코드에 Given-When-Then 패턴을 적용해 보세요!

---

## 참고 자료

- Martin Fowler - GivenWhenThen: [https://martinfowler.com/bliki/GivenWhenThen.html](https://martinfowler.com/bliki/GivenWhenThen.html)
- BDD (Behavior-Driven Development) - Cucumber: [https://cucumber.io/docs/bdd/](https://cucumber.io/docs/bdd/)
- JUnit 5 User Guide: [https://junit.org/junit5/docs/current/user-guide/](https://junit.org/junit5/docs/current/user-guide/)
- Mockito Documentation: [https://site.mockito.org/](https://site.mockito.org/)