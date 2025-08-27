소프트웨어 테스트, 특히 [[단위 테스트(Unit Test)]]를 작성할 때, 우리는 코드가 의도한 대로 동작했는지 확인하고자 합니다. 이러한 확인 작업은 크게 두 가지 스타일로 나눌 수 있는데, 그중 하나가 바로 **상태 검증(State Verification)**입니다. 상태 검증은 테스트 대상 코드(SUT, System Under Test)를 실행한 후, 관련된 객체나 시스템의 **상태**가 우리가 기대하는 값으로 올바르게 변경되었는지를 직접 확인하는 테스트 방식입니다.

이는 마치 우리가 자판기에 돈을 넣고 버튼을 눌렀을 때, 실제로 원하는 음료수가 나오고 거스름돈이 정확히 반환되었는지 그 "결과물(상태)"을 확인하는 것과 유사합니다. 상태 검증은 테스트의 결과를 명확하게 보여주어 이해하기 쉽고 직관적인 테스트를 작성하는 데 도움을 줍니다.

상태 검증은 종종 [[행위 검증(Behavior Verification)]]과 비교되곤 합니다. 행위 검증이 "올바른 과정을 거쳤는가?"에 초점을 맞춘다면, 상태 검증은 "올바른 결과가 나왔는가?"에 더 집중합니다.

## 상태 검증의 핵심 원리

상태 검증은 다음과 같은 핵심 원리에 기반합니다.

1. **관찰 가능한 상태 (Observable State)**: 검증의 대상이 되는 상태는 테스트 코드에서 접근하여 그 값을 읽을 수 있어야 합니다. 이는 보통 객체의 공개(public) Getter 메서드를 통해 이루어지지만, 경우에 따라서는 패키지 보호(package-private) 필드에 접근하거나, 테스트만을 위한 특정 메서드를 통해 상태를 확인할 수도 있습니다.
2. **사후 조건 (Post-conditions)**: 상태 검증은 특정 작업(SUT의 메서드 호출 등)이 완료된 후, 해당 객체 또는 시스템이 만족해야 하는 조건(기대되는 상태)을 명시하고 이를 확인합니다.
3. **단언 (Assertions)**: `assertEquals()`, `assertTrue()`, `assertNotNull()` 등과 같은 단언 메서드를 사용하여 기대하는 상태와 실제 객체의 상태를 비교합니다. 만약 두 상태가 일치하지 않으면 테스트는 실패합니다.

## 상태 검증의 대상

상태 검증은 다양한 대상의 상태 변화를 확인할 수 있습니다.

- **SUT(System Under Test) 자체의 상태 변화**:
    - 객체의 특정 필드 값이 기대하는 값으로 변경되었는지 (예: `user.getName()`이 "홍길동"인가?)
    - 객체 내부의 컬렉션 크기가 변경되었거나 특정 요소가 추가/삭제되었는지 (예: `cart.getItemCount()`가 1인가?)
- **의존 객체의 상태 변화 (주로 [[테스트 더블(Test Double)]] 중 Fake 객체 사용 시)**:
    - SUT가 Fake 객체와 상호작용한 결과로 Fake 객체 내부의 데이터가 기대한 대로 변경되었는지 (예: `InMemoryUserRepository`에 사용자 정보가 저장되었는지 확인)
- **시스템의 부수 효과(Side Effects)로 인한 상태 변화 (넓은 의미의 상태)**:
    - SUT 실행 결과 특정 파일이 생성되었거나 파일 내용이 기대하는 대로 쓰였는지 확인 (이는 [[통합 테스트(Integration Test)]]의 성격이 강할 수 있습니다)
    - 데이터베이스에 특정 레코드가 삽입/수정/삭제되었는지 확인 (이 또한 주로 통합 테스트에서 다룹니다)

단위 테스트 수준에서는 주로 SUT 자체의 상태나, SUT가 직접 사용하는 Fake 객체의 상태를 검증하는 데 초점을 맞춥니다.

## 상태 검증의 장점

- **이해하기 쉬움**: 테스트 코드가 "어떤 작업을 수행하면(When), 결과적으로 이런 상태가 되어야 한다(Then)"는 명확하고 직관적인 구조를 갖기 때문에 테스트의 의도를 파악하기 쉽습니다.
- **구현 변경에 상대적으로 덜 민감함**: SUT의 내부 로직이나 알고리즘이 변경되더라도, 최종적으로 관찰되는 상태(결과)만 동일하다면 테스트는 여전히 통과할 수 있습니다. 이는 행위 검증에 비해 리팩토링에 대한 테스트의 견고성을 높여줍니다.
- **명확한 실패 원인 파악**: 테스트가 실패했을 때, 기대했던 상태 값과 실제 상태 값이 어떻게 다른지 직접적으로 보여주므로 문제의 원인을 비교적 쉽게 추론할 수 있습니다.

## 상태 검증의 단점 및 고려사항

- **관찰 가능한 상태의 필요성**: 상태를 검증하기 위해서는 해당 상태에 접근할 수 있는 방법(주로 Getter 메서드)이 필요합니다. 때로는 테스트만을 위해 이러한 접근자를 추가해야 할 수도 있으며, 이는 객체의 [[캡슐화(Encapsulation)]]를 다소 약화시킬 수 있다는 비판을 받기도 합니다. (이는 테스트 용이성과 캡슐화 사이의 트레이드오프 문제입니다. 자세한 내용은 [[테스트를 위한 인터페이스 설계]] 문서를 참고하세요.)
- **모든 것을 상태로 검증하기 어려움**: SUT의 메서드가 반환 값이 없거나(`void`), 객체 내부의 상태를 변경하지 않고 오직 다른 객체와의 상호작용(메서드 호출)만 수행하는 경우에는 상태 검증만으로는 테스트하기 어려울 수 있습니다. 이러한 경우 [[행위 검증(Behavior Verification)]]이 보완적으로 사용될 수 있습니다.
- **상태가 복잡한 경우 검증의 어려움**: 검증해야 할 상태가 매우 많거나 그 구조가 복잡한 경우, 모든 상태를 일일이 확인하는 단언문들이 많아져 테스트 코드가 길어지고 유지보수가 어려워질 수 있습니다. 이럴 때는 Custom Assertion이나 Matcher 라이브러리를 활용하여 검증 로직을 추상화하는 것이 도움이 될 수 있습니다.

## 상태 검증과 테스트 더블의 관계

상태 검증은 [[테스트 더블(Test Double)]]과 밀접하게 연관되어 사용됩니다.

- **스텁(Stub)**: 스텁은 SUT의 의존 객체로부터 미리 정해진 값을 반환하도록 하여, SUT가 특정 로직을 실행하고 특정 상태에 도달하도록 유도하는 데 사용됩니다. 이후 SUT의 상태를 검증하여 스텁이 제공한 입력에 따라 SUT가 올바르게 동작했는지 확인합니다.
    - 예: `PaymentService` 스텁이 "결제 성공" 상태를 반환했을 때, `Order` 객체의 상태가 "결제 완료"로 변경되었는지 검증.
- **페이크(Fake)**: 페이크 객체는 실제 구현을 단순화한 버전으로, SUT와의 상호작용을 통해 자신의 내부 상태를 변경할 수 있습니다. 테스트에서는 SUT를 실행한 후, 이 페이크 객체의 상태가 기대하는 대로 변경되었는지 검증할 수 있습니다.
    - 예: `OrderService`가 주문을 처리한 후, `InMemoryOrderRepository`(Fake)에 해당 주문 정보가 올바르게 저장되었는지 `findById` 등으로 확인하여 검증.

## Java 예시 (JUnit 사용)

다음은 Java와 JUnit5를 사용하여 객체의 상태를 검증하는 간단한 예시입니다.

**검증 대상 클래스: `BankAccount`**

```java
// BankAccount.java
class InsufficientFundsException extends RuntimeException {
    public InsufficientFundsException(String message) {
        super(message);
    }
}

public class BankAccount {
    private String accountNumber;
    private double balance;
    private boolean active;

    public BankAccount(String accountNumber, double initialBalance) {
        if (initialBalance < 0) {
            throw new IllegalArgumentException("Initial balance cannot be negative.");
        }
        this.accountNumber = accountNumber;
        this.balance = initialBalance;
        this.active = true;
    }

    public void deposit(double amount) {
        if (!active) {
            throw new IllegalStateException("Account is not active.");
        }
        if (amount <= 0) {
            throw new IllegalArgumentException("Deposit amount must be positive.");
        }
        this.balance += amount;
    }

    public void withdraw(double amount) {
        if (!active) {
            throw new IllegalStateException("Account is not active.");
        }
        if (amount <= 0) {
            throw new IllegalArgumentException("Withdrawal amount must be positive.");
        }
        if (this.balance < amount) {
            throw new InsufficientFundsException("Insufficient funds. Current balance: " + this.balance);
        }
        this.balance -= amount;
    }

    public void deactivateAccount() {
        this.active = false;
    }

    // 상태 검증을 위한 Getter 메서드들
    public String getAccountNumber() { return accountNumber; }
    public double getBalance() { return balance; }
    public boolean isActive() { return active; }
}
```

**테스트 코드: `BankAccountTest`**

```java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import static org.junit.jupiter.api.Assertions.*;

public class BankAccountTest {

    @Test
    @DisplayName("새 계좌 생성 시 초기 잔액과 활성 상태 검증")
    void newAccount_shouldHaveInitialBalanceAndBeActive() {
        // Given (Arrange)
        String accountNumber = "123-456";
        double initialBalance = 100.0;

        // When (Act)
        BankAccount account = new BankAccount(accountNumber, initialBalance);

        // Then (Assert) - 상태 검증
        assertEquals(accountNumber, account.getAccountNumber(), "계좌번호가 일치해야 합니다.");
        assertEquals(initialBalance, account.getBalance(), 0.001, "초기 잔액이 일치해야 합니다.");
        assertTrue(account.isActive(), "계좌는 초기에 활성 상태여야 합니다.");
    }

    @Test
    @DisplayName("활성 계좌에 입금 시 잔액 증가 검증")
    void deposit_shouldIncreaseBalance_whenAccountIsActiveAndAmountIsPositive() {
        // Given
        BankAccount account = new BankAccount("789-012", 200.0);
        double depositAmount = 50.0;

        // When
        account.deposit(depositAmount);

        // Then - 상태 검증
        assertEquals(250.0, account.getBalance(), 0.001, "입금 후 잔액이 정확히 증가해야 합니다.");
    }

    @Test
    @DisplayName("잔액 충분 시 출금하면 잔액 감소 검증")
    void withdraw_shouldDecreaseBalance_whenSufficientFunds() {
        // Given
        BankAccount account = new BankAccount("345-678", 150.0);
        double withdrawalAmount = 70.0;

        // When
        account.withdraw(withdrawalAmount);

        // Then - 상태 검증
        assertEquals(80.0, account.getBalance(), 0.001, "출금 후 잔액이 정확히 감소해야 합니다.");
    }

    @Test
    @DisplayName("계좌 비활성화 시 active 상태 false로 변경 검증")
    void deactivateAccount_shouldSetAccountToInactive() {
        // Given
        BankAccount account = new BankAccount("678-901", 50.0);

        // When
        account.deactivateAccount();

        // Then - 상태 검증
        assertFalse(account.isActive(), "계좌가 비활성화 상태여야 합니다.");
        // 비활성화 후 잔액은 그대로 유지되는지도 확인 (의도된 동작이라면)
        assertEquals(50.0, account.getBalance(), 0.001, "비활성화 후에도 잔액은 유지되어야 합니다.");
    }

    @Test
    @DisplayName("잔액 부족 시 출금하면 예외 발생 및 잔액 불변 검증")
    void withdraw_shouldThrowExceptionAndBalanceUnchanged_whenInsufficientFunds() {
        // Given
        BankAccount account = new BankAccount("012-345", 30.0);
        double withdrawalAmount = 100.0;
        double initialBalance = account.getBalance(); // 예외 발생 전 잔액 기록

        // When & Then - 예외 발생 검증 및 상태 검증
        assertThrows(InsufficientFundsException.class, () -> {
            account.withdraw(withdrawalAmount);
        }, "잔액 부족 시 InsufficientFundsException이 발생해야 합니다.");

        // 예외 발생 후 잔액이 변하지 않았는지 추가적인 상태 검증
        assertEquals(initialBalance, account.getBalance(), 0.001, "출금 실패 시 잔액은 변하지 않아야 합니다.");
    }
}
```

위 예시에서 `assertEquals`, `assertTrue`, `assertFalse`와 같은 JUnit의 단언 메서드들이 `BankAccount` 객체의 `balance`나 `active` 필드 값을 직접 확인하여 상태를 검증하고 있습니다.

## 결론

상태 검증은 단위 테스트에서 SUT의 동작 결과를 가장 직접적이고 명확하게 확인할 수 있는 기본적인 접근 방식입니다. 이는 테스트의 의도를 쉽게 이해하도록 돕고, SUT가 올바른 최종 결과를 만들어내는지에 대한 신뢰를 줍니다.

모든 경우에 상태 검증만이 정답은 아니지만, 대부분의 경우 상태 검증을 우선적으로 고려하고, 필요한 경우 [[행위 검증(Behavior Verification)]]과 같은 다른 테스트 스타일과 상호 보완적으로 사용하여 테스트 스위트의 완성도를 높이는 것이 바람직합니다. 견고한 테스트는 결국 더 안정적이고 품질 높은 소프트웨어로 이어지기 때문입니다.

## 참고 자료

- "xUnit Test Patterns: Refactoring Test Code" 
- Martin Fowler - "StateVerification" (블로그 등 관련 아티클)
- JUnit 5 User Guide ([https://junit.org/junit5/docs/current/user-guide/](https://junit.org/junit5/docs/current/user-guide/))
- AssertJ Documentation ([https://assertj.github.io/doc/](https://assertj.github.io/doc/)) - 더 풍부한 Fluent API를 제공하는 Assertion 라이브러리