## 행위 검증 (Behavior Verification) 마스터하기: 객체 간의 올바른 소통 확인

소프트웨어 테스트에서 우리가 검증하고자 하는 것은 단순히 최종 결과 값만이 아닙니다. 때로는 시스템의 특정 부분이 다른 부분과 "올바르게 소통"했는지, 즉 올바른 작업을 올바른 순서와 방식으로 요청했는지를 확인하는 것이 중요할 때가 있습니다. 이러한 종류의 테스트를 **행위 검증(Behavior Verification)** 또는 상호작용 테스트(Interaction Testing)라고 부릅니다.

행위 검증은 테스트 대상 코드(SUT, System Under Test)가 자신의 의존 객체(DOC, Depended-On Component)와 기대하는 방식으로 상호작용했는지를 중점적으로 확인하는 테스트 스타일입니다. 이는 SUT가 의존 객체의 메서드를 올바른 인자로, 올바른 횟수만큼, 그리고 때로는 올바른 순서로 호출했는지 등을 검증하는 것을 포함합니다.

[[상태 검증(State Verification)]]이 "작업 후 시스템의 상태가 올바른가?"에 초점을 맞춘다면, 행위 검증은 "작업 중 올바른 협력(호출)이 이루어졌는가?"에 주목합니다.

## 왜 행위 검증이 필요한가?

[[상태 검증(State Verification)]]만으로는 테스트하기 어렵거나 불충분한 경우가 있습니다. 이럴 때 행위 검증이 유용하게 사용됩니다.

1. **직접 관찰하기 어려운 부수 효과(Side Effects) 검증**: SUT가 실행된 결과로 외부 시스템에 메시지를 보내거나(예: 이메일 발송, SMS 전송, 로깅 시스템에 로그 기록), 데이터베이스에 특정 작업을 수행하라고 명령하는 경우, 이러한 외부 시스템의 실제 상태 변화를 단위 테스트에서 직접 확인하기는 어렵거나 바람직하지 않습니다. 이때 SUT가 해당 외부 시스템의 인터페이스(의존 객체)를 올바르게 호출했는지 검증하는 것이 현실적인 대안입니다.
2. **반환 값이 없는(void) 메서드 테스트**: SUT의 메서드가 값을 반환하지 않고 내부 상태를 변경하지도 않으면서, 오직 다른 객체의 메서드를 호출하는 역할만 수행할 때, 호출된 메서드가 올바르게 호출되었는지 행위 검증을 통해 확인할 수 있습니다.
3. **의존 객체의 상태를 직접 알 수 없을 때**: 의존 객체가 자신의 상태를 외부로 노출하지 않거나(강한 [[캡슐화(Encapsulation)]]), 상태 자체가 매우 복잡하여 검증하기 어려운 경우, SUT가 해당 의존 객체와 올바른 방식으로 "대화"했는지 확인하는 것으로 테스트의 목적을 달성할 수 있습니다.

## 행위 검증의 핵심 원리

행위 검증은 다음과 같은 원리에 기반하여 동작합니다.

- **간접적인 입력/출력 (Indirect Inputs/Outputs) 검증**: SUT가 의존 객체의 메서드를 호출할 때 전달하는 값들을 "간접적인 출력(SUT 입장에서)"으로 간주하고, 이 값들이 올바른지 검증합니다. 반대로 의존 객체가 SUT에게 값을 반환하면 이는 "간접적인 입력(SUT 입장에서)"이 됩니다. (행위 검증은 주로 간접적인 출력, 즉 호출에 집중합니다.)
- **상호작용(Interaction)에 초점**: 객체 지향 시스템에서 객체들은 서로 메시지를 주고받으며(메서드 호출) 협력합니다. 행위 검증은 이러한 객체 간의 상호작용 프로토콜이 올바르게 지켜졌는지 확인합니다.
- **테스트 더블의 적극적인 활용**: [[테스트 더블(Test Double)]], 특히 [[Mock Object|목 객체(Mock Object)]]와 [[Spy|스파이(Spy)]]가 핵심적인 역할을 합니다. 목 객체는 SUT로부터의 호출을 기록하고, 테스트 종료 후 이 기록을 바탕으로 기대했던 상호작용이 실제로 발생했는지 검증합니다.

## 행위 검증의 대상

행위 검증을 통해 확인할 수 있는 주요 상호작용의 측면은 다음과 같습니다.

- **메서드 호출 여부**: 의존 객체의 특정 메서드가 최소 한 번 이상 호출되었는지, 또는 전혀 호출되지 않았는지 (`never()`) 검증합니다.
- **메서드 호출 횟수**: 특정 메서드가 정확히 N번 호출되었는지 (`times(N)`), 또는 최소 N번 (`atLeast(N)`), 최대 N번 (`atMost(N)`) 호출되었는지 검증합니다.
- **메서드 호출 시 전달된 인자**: 의존 객체의 메서드가 호출될 때, 우리가 기대하는 값(또는 특정 조건을 만족하는 값)이 인자로 전달되었는지 검증합니다. [[ArgumentCaptor]] 등을 사용하여 실제 전달된 인자를 포착하여 상세히 검증할 수도 있습니다.
- **메서드 호출 순서**: 여러 의존 객체의 메서드들이나 한 의존 객체의 여러 메서드들이 특정 순서대로 호출되었는지 검증합니다. (주의: 과도한 순서 검증은 테스트를 매우 취약하게 만들 수 있으므로 신중하게 사용해야 합니다.)

## 행위 검증의 장점

- **관찰 불가능한 로직 테스트**: 외부 API 호출, 로깅, 알림 발송 등 직접적인 결과 상태를 확인하기 어려운 로직의 실행 여부를 검증할 수 있습니다.
- **`void` 메서드 테스트 용이**: 반환 값이 없는 메서드라도, 해당 메서드가 올바른 협력 객체와 올바르게 상호작용했는지 확인할 수 있습니다.
- **설계 개선 유도**: (특히 [[테스트 주도 개발(TDD)]]과 함께 사용될 때) 객체 간의 책임과 협력을 명확히 정의하도록 유도하여, 보다 잘 설계된 시스템을 만드는 데 도움을 줄 수 있습니다. SUT와 DOC 간의 인터페이스에 대해 더 깊이 고민하게 만듭니다.

## 행위 검증의 단점 및 고려사항

- **구현과의 강한 결합 (Tight Coupling to Implementation)**: 행위 검증은 SUT가 "어떻게" 동작하는지, 즉 내부적으로 어떤 의존 객체의 어떤 메서드를 호출하는지에 깊이 관여합니다. 이로 인해 SUT의 최종 결과는 동일하더라도 내부 구현 방식(호출하는 메서드나 순서 등)이 변경되면 테스트가 실패할 수 있습니다. 이는 리팩토링을 어렵게 만들고 테스트를 "취약하게(brittle)" 만듭니다.
- **과도한 명세 (Overspecification) 위험**: SUT와 의존 객체 간의 모든 세세한 상호작용을 검증하려고 하면 테스트 코드가 매우 장황해지고 이해하기 어려워집니다. 또한, 사소한 내부 변경에도 테스트가 깨지기 쉬워집니다.
- **테스트의 의도 파악 어려움**: 때로는 "왜 이 호출을 검증하는 것이 중요한가?"라는 질문에 답하기 어려울 수 있습니다. 상태 검증이 "결과가 올바르다"라는 명확한 메시지를 주는 반면, 행위 검증은 "호출이 올바르다"라는 메시지를 주는데, 이것이 비즈니스 가치와 직접적으로 연결되지 않는 것처럼 보일 수 있습니다.
- **Mock 객체 설정의 복잡성**: 의존성이 많거나 상호작용이 복잡한 경우, Mock 객체를 설정하고 검증하는 코드가 상당히 복잡해질 수 있습니다.

이러한 단점 때문에 행위 검증은 신중하게, 꼭 필요한 경우에만 사용하는 것이 권장됩니다.

## 행위 검증과 테스트 더블의 관계

- **[[Mock Object|목 객체(Mock Object)]]**: 행위 검증을 위해 특별히 설계된 테스트 더블입니다. 목 객체는 테스트 전에 "기대하는 호출"을 설정하고(선택 사항), SUT 실행 후 실제로 해당 호출이 발생했는지 `verify()`를 통해 검증합니다. Mockito와 같은 프레임워크에서 `mock()`으로 생성된 객체를 `verify()`와 함께 사용할 때 목 객체의 역할을 수행합니다.
- **[[Spy|스파이(Spy)]]**: 실제 객체를 감싸서 만들어지며, 실제 객체의 로직을 대부분 그대로 사용하면서 특정 메서드의 호출을 추적하거나 일부 메서드만 스텁(stub)할 수 있습니다. 스파이 객체 또한 `verify()`를 사용하여 메서드 호출 행위를 검증할 수 있습니다.

## Java 예시 (Mockito 활용)

다음은 [[Mockito]] 프레임워크를 사용하여 행위 검증을 수행하는 Java 예시입니다.

**검증 대상 시스템 로직:**

```java
// User.java (이전 예시 재사용)
public class User {
    private String id;
    private String email;
    private boolean prefersEmailNotifications;
    public User(String id, String email, boolean prefersEmailNotifications) { /* ... */ }
    public String getId() { return id; }
    public String getEmail() { return email; }
    public boolean isPrefersEmailNotifications() { return prefersEmailNotifications; }
}

// NotificationService.java (인터페이스)
public interface NotificationService {
    void sendNotification(String userId, String message);
    boolean sendAdminNotification(String subject, String body); // 반환값이 있는 예시 추가
}

// EmailService.java (인터페이스)
public interface EmailService {
    void sendEmail(String toAddress, String subject, String body);
}

// UserNotifier.java
import java.util.List;

public class UserNotifier {
    private NotificationService notificationService;
    private EmailService emailService;

    public UserNotifier(NotificationService notificationService, EmailService emailService) {
        this.notificationService = notificationService;
        this.emailService = emailService;
    }

    public void notifyUser(User user, String message) {
        if (user.isPrefersEmailNotifications()) {
            emailService.sendEmail(user.getEmail(), "Notification", message);
        } else {
            notificationService.sendNotification(user.getId(), message);
        }
    }

    public boolean notifyAdminsWithMessage(String message) {
        // 관리자에게 중요한 메시지를 보내고 성공 여부를 반환한다고 가정
        return notificationService.sendAdminNotification("Urgent Admin Alert", message);
    }

    public void sendPromotionalEmailToUsers(List<User> users, String promoCode) {
        for (User user : users) {
            if (user.isPrefersEmailNotifications()) {
                String personalizedMessage = "Dear " + user.getId() + ", here is your promo code: " + promoCode;
                emailService.sendEmail(user.getEmail(), "Special Promotion!", personalizedMessage);
            }
        }
        // 프로모션 발송 후 관리자에게 요약 알림
        notificationService.sendNotification("admin_promo_log", users.size() + " users targeted for promo " + promoCode);
    }
}
```

**테스트 코드: `UserNotifierTest`**

```java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import org.mockito.ArgumentCaptor;
import org.mockito.InOrder;

import java.util.Arrays;
import java.util.List;

import static org.mockito.Mockito.*; // Mockito의 static 메서드들을 import
import static org.junit.jupiter.api.Assertions.*;

public class UserNotifierTest {

    @Test
    @DisplayName("사용자가 이메일 수신을 선호하면 이메일 발송")
    void notifyUser_shouldSendEmail_whenUserPrefersEmail() {
        // Given (Arrange)
        NotificationService mockNotificationService = mock(NotificationService.class); // 목 객체 생성
        EmailService mockEmailService = mock(EmailService.class);               // 목 객체 생성
        UserNotifier userNotifier = new UserNotifier(mockNotificationService, mockEmailService);

        User user = new User("user001", "user001@example.com", true);
        String message = "Important update for you!";

        // When (Act)
        userNotifier.notifyUser(user, message);

        // Then (Assert) - 행위 검증
        // mockEmailService의 sendEmail 메서드가 특정 인자들로 호출되었는지 검증
        verify(mockEmailService).sendEmail("user001@example.com", "Notification", "Important update for you!");
        // mockNotificationService의 sendNotification 메서드는 호출되지 않았는지 검증
        verify(mockNotificationService, never()).sendNotification(anyString(), anyString());
    }

    @Test
    @DisplayName("사용자가 이메일 수신을 선호하지 않으면 푸시 알림 발송")
    void notifyUser_shouldSendPushNotification_whenUserDoesNotPreferEmail() {
        // Given
        NotificationService mockNotificationService = mock(NotificationService.class);
        EmailService mockEmailService = mock(EmailService.class);
        UserNotifier userNotifier = new UserNotifier(mockNotificationService, mockEmailService);

        User user = new User("user002", "user002@example.com", false);
        String message = "Quick reminder!";

        // When
        userNotifier.notifyUser(user, message);

        // Then - 행위 검증
        verify(mockNotificationService).sendNotification("user002", "Quick reminder!");
        verify(mockEmailService, never()).sendEmail(anyString(), anyString(), anyString());
    }

    @Test
    @DisplayName("관리자 알림 시 반환값 스텁 및 호출 검증")
    void notifyAdminsWithMessage_shouldCallAdminNotificationAndReturnItsResult() {
        // Given
        NotificationService mockNotificationService = mock(NotificationService.class);
        EmailService mockEmailService = mock(EmailService.class); // 이 테스트에서는 사용되지 않지만 생성자 주입을 위해 필요
        UserNotifier userNotifier = new UserNotifier(mockNotificationService, mockEmailService);
        String adminMessage = "System critical alert!";

        // 목 객체의 특정 메서드가 호출될 때 반환할 값을 미리 설정 (스텁 역할)
        when(mockNotificationService.sendAdminNotification("Urgent Admin Alert", adminMessage)).thenReturn(true);

        // When
        boolean result = userNotifier.notifyAdminsWithMessage(adminMessage);

        // Then - 상태 검증 (반환값) 및 행위 검증
        assertTrue(result, "관리자 알림 결과는 스텁된 값(true)이어야 합니다.");
        // sendAdminNotification 메서드가 정확한 인자들로 호출되었는지 검증
        verify(mockNotificationService).sendAdminNotification("Urgent Admin Alert", adminMessage);
    }

    @Test
    @DisplayName("프로모션 이메일 발송 시 인자 캡처 및 호출 횟수/순서 검증")
    void sendPromotionalEmailToUsers_shouldSendCorrectEmailsAndLogSummary() {
        // Given
        NotificationService mockNotificationService = mock(NotificationService.class);
        EmailService mockEmailService = mock(EmailService.class);
        UserNotifier userNotifier = new UserNotifier(mockNotificationService, mockEmailService);

        User user1 = new User("Alice", "alice@example.com", true);
        User user2 = new User("Bob", "bob@example.com", false); // 이메일 비선호
        User user3 = new User("Charlie", "charlie@example.com", true);
        List<User> users = Arrays.asList(user1, user2, user3);
        String promoCode = "SUMMER25";

        // When
        userNotifier.sendPromotionalEmailToUsers(users, promoCode);

        // Then - 행위 검증 (호출 횟수)
        verify(mockEmailService, times(1)).sendEmail(eq("alice@example.com"), eq("Special Promotion!"), contains("SUMMER25"));
        verify(mockEmailService, times(1)).sendEmail(eq("charlie@example.com"), eq("Special Promotion!"), contains("SUMMER25"));
        verify(mockEmailService, never()).sendEmail(eq("bob@example.com"), anyString(), anyString()); // Bob에게는 보내지 않음

        // ArgumentCaptor를 사용하여 관리자 알림 메시지 검증
        ArgumentCaptor<String> userIdCaptor = ArgumentCaptor.forClass(String.class);
        ArgumentCaptor<String> messageCaptor = ArgumentCaptor.forClass(String.class);
        verify(mockNotificationService).sendNotification(userIdCaptor.capture(), messageCaptor.capture());

        assertEquals("admin_promo_log", userIdCaptor.getValue());
        assertTrue(messageCaptor.getValue().startsWith("2 users targeted for promo SUMMER25")); // Alice, Charlie 2명

        // 호출 순서 검증 (신중하게 사용!)
        // 예: Charlie에게 이메일 발송 후, 관리자 요약 알림이 발생하는지
        InOrder inOrder = inOrder(mockEmailService, mockNotificationService);
        inOrder.verify(mockEmailService).sendEmail(eq("charlie@example.com"), anyString(), anyString());
        inOrder.verify(mockNotificationService).sendNotification(eq("admin_promo_log"), anyString());
    }
}
```

위 예시에서 `verify()`, `never()`, `times()`, `when().thenReturn()`, `ArgumentCaptor`, `InOrder` 등 Mockito의 다양한 기능을 사용하여 SUT와 의존 객체 간의 상호작용을 상세하게 검증하고 있습니다. 더 자세한 Mockito 사용법은 [[Mockito 사용 가이드]]에서 확인할 수 있습니다.

## 상태 검증과의 균형: 언제 무엇을 사용할까?

행위 검증과 상태 검증은 서로 경쟁하는 관계라기보다는 상호 보완적인 관계입니다. 어떤 검증 방식을 사용할지는 테스트의 목적과 상황에 따라 결정해야 합니다.

- **"시카고 학파 (Chicago School)" 또는 "고전적 TDD (Classicist TDD)"**: 상태 검증을 선호합니다. 객체의 최종 상태가 올바르면 내부적으로 어떤 일이 일어났는지는 크게 중요하지 않다고 봅니다. 구현의 유연성을 높이고 테스트의 취약성을 줄이는 데 도움이 됩니다.
- **"런던 학파 (London School)" 또는 "목 객체주의자 (Mockist TDD)"**: 행위 검증을 적극적으로 활용합니다. 객체 간의 협력과 메시지 전달을 중요하게 여기며, 이를 통해 객체의 역할을 명확히 하고 설계를 개선해 나간다고 봅니다.

일반적으로 다음과 같은 가이드라인을 따를 수 있습니다.

- **SUT의 실행 결과를 직접 관찰하고 검증할 수 있는 명확한 상태가 있다면, [[상태 검증(State Verification)]]을 우선적으로 사용하세요.** 이것이 테스트를 더 직관적이고 구현 변화에 덜 민감하게 만듭니다.
- **SUT의 실행 결과가 반환 값이나 명확한 상태 변화로 나타나지 않고, 주로 다른 객체와의 상호작용(메서드 호출)으로 나타난다면, 행위 검증을 고려하세요.** (예: 로거 호출, 외부 서비스 API 호출, 알림 발송 등)
- **행위 검증을 사용할 때는 최소한의 필요한 상호작용만 검증하도록 노력하세요.** 과도한 행위 검증은 테스트를 취약하게 만듭니다. "이 호출이 정말로 비즈니스적으로 중요한가?"를 자문해 보세요.

## 결론

행위 검증은 객체 지향 시스템에서 객체들이 서로 올바르게 "소통"하고 협력하는지를 확인하는 강력한 테스트 기법입니다. 특히 외부 시스템과의 연동이나 직접적인 상태 변화를 확인하기 어려운 경우에 유용합니다.

하지만 행위 검증은 SUT의 내부 구현에 대한 의존성을 높여 테스트를 취약하게 만들 수 있는 단점도 가지고 있습니다. 따라서 상태 검증과 적절히 조화롭게 사용하며, 꼭 필요한 핵심적인 상호작용을 검증하는 데 신중하게 활용하는 것이 중요합니다. 올바른 사용은 시스템 설계를 개선하고, 눈에 보이지 않는 중요한 로직들을 효과적으로 테스트하는 데 큰 도움을 줄 것입니다.

## 참고 자료

- "Growing Object-Oriented Software, Guided by Tests" - Steve Freeman, Nat Pryce (런던 학파 TDD의 대표적인 저서)
- Martin Fowler - "Mocks Aren't Stubs" ([https://martinfowler.com/articles/mocksArentStubs.html](https://martinfowler.com/articles/mocksArentStubs.html))
- Martin Fowler - "ChicagoVsLondon" ([https://martinfowler.com/articles/ChicagoVsLondon.html](https://www.google.com/search?q=https://martinfowler.com/articles/ChicagoVsLondon.html))
- Mockito 공식 문서 ([https://site.mockito.org/](https://site.mockito.org/)) - 특히 `verify()`, `ArgumentCaptor`, `InOrder` API 문서