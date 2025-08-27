단위 테스트를 작성하다 보면, 테스트 대상 코드(SUT, System Under Test)가 외부 의존성을 가지고 있어 테스트하기 어려운 상황에 직면하곤 합니다. 예를 들어, 데이터베이스, 외부 API, 파일 시스템 등은 테스트 환경을 복잡하게 만들고, 테스트 실행 속도를 저하하며, 결과의 일관성을 해칠 수 있습니다. 이때 등장하는 것이 바로 **테스트 더블(Test Double)**입니다.

테스트 더블은 테스트 과정에서 실제 의존 객체 대신 사용되는 모든 종류의 가짜 객체를 총칭하는 용어로, Gerard Meszaros가 그의 저서 "xUnit Test Patterns"에서 처음 소개했습니다. 영화 촬영에서 위험한 장면을 스턴트 더블(Stunt Double)이 대신하는 것처럼, 테스트 더블은 실제 객체를 대신하여 테스트가 원활하게 진행될 수 있도록 돕습니다.

이 글에서는 테스트 더블의 개념과 종류, 그리고 언제 어떤 테스트 더블을 사용해야 하는지에 대해 자세히 알아보겠습니다.

## 왜 테스트 더블이 필요한가?

테스트 더블을 사용하는 주된 이유는 다음과 같습니다.

1. **의존성 격리 (Isolating Dependencies)**: 테스트 대상 코드(SUT)를 외부 의존성으로부터 격리하여, 오직 SUT의 로직만을 정확하게 검증할 수 있게 합니다. 외부 시스템의 상태나 오류에 테스트가 영향을 받지 않도록 합니다.
2. **테스트 결정성 확보 (Ensuring Deterministic Tests)**: 외부 요인(예: 네트워크 상태, 외부 API의 응답 변화)에 관계없이 테스트가 항상 동일한 결과를 반환하도록 보장합니다.
3. **테스트 속도 향상 (Speeding Up Tests)**: 실제 데이터베이스 접근이나 네트워크 통신과 같이 시간이 오래 걸리는 작업을 가짜 객체로 대체하여 테스트 실행 속도를 크게 향상시킵니다. 이는 개발자가 더 자주 테스트를 실행하고 빠른 피드백을 받는 데 중요합니다.
4. **특정 상황 재현 용이 (Simulating Specific Scenarios)**: 실제 환경에서는 재현하기 어려운 예외 상황(예: 네트워크 오류, 디스크 꽉 참)이나 특정 반환 값을 테스트 더블을 통해 손쉽게 시뮬레이션할 수 있습니다.
5. **개발 중 의존성 미완성 시 테스트 가능 (Testing Before Dependencies are Ready)**: 협업 환경에서 아직 개발되지 않았거나 사용할 수 없는 의존 컴포넌트 대신 테스트 더블을 사용하여 SUT 개발 및 테스트를 병행할 수 있습니다.

## 테스트 더블의 종류

Gerard Meszaros는 테스트 더블을 다음과 같이 다섯 가지 유형으로 분류했습니다. 각 유형은 사용 목적과 동작 방식에 차이가 있습니다.


```mermaid
graph TD
    A["테스트 더블 (Test Double)"] --> B(Dummy Object)
    A --> C(Fake Object)
    A --> D(Stub)
    A --> E(Spy)
    A --> F(Mock Object)

    subgraph "단순 대체/자리 채움"
        B
        C
    end

    subgraph "상태 검증 지원 (State Verification)"
        D
    end

    subgraph "행위 검증 지원 (Behavior Verification)"
        E
        F
    end
```

### 1. 더미 객체 (Dummy Object)

- **정의**: 가장 단순한 형태의 테스트 더블로, 실제로는 사용되지 않지만 단지 인스턴스화되어 전달되는 객체입니다. 주로 메서드 시그니처를 만족시키기 위해 인자로 전달되며, 더미 객체의 메서드가 호출될 것으로 예상하지 않습니다.
    
- **특징**: 내부에 로직이 거의 없거나 아예 없습니다. `null` 대신 사용되어 [[NullPointerException]]을 방지하는 용도로 쓰이기도 합니다.
    
- **사용 시나리오**:
    
    - 메서드 호출 시 여러 개의 인자가 필요하지만, 그중 일부는 테스트 로직과 무관할 때.
    - 로그 객체 등을 전달해야 하지만, 해당 테스트에서는 로그 내용을 확인하지 않을 때.
- **Java 예시 (Mockito 활용)**: Mockito는 `mock()` 메서드로 더미 객체를 쉽게 만들 수 있습니다. 만약 해당 객체의 어떤 메서드도 호출되지 않을 것이라면, 별도의 행동 설정 없이 전달만 하면 됩니다.
    ```java
    // Logger 인터페이스가 있다고 가정
    public interface Logger {
        void log(String message);
    }
    
    // 테스트 대상 클래스
    public class SystemManager {
        private final Logger logger;
        public SystemManager(Logger logger) {
            this.logger = logger;
        }
        public String performOperation() {
            // logger.log("Operation performed"); // 이 테스트에서는 로그가 중요하지 않음
            return "Operation Successful";
        }
    }
    
    // 테스트 코드
    @Test
    void performOperation_shouldReturnSuccess_withDummyLogger() {
        Logger dummyLogger = Mockito.mock(Logger.class); // 더미 로거
        SystemManager manager = new SystemManager(dummyLogger);
    
        String result = manager.performOperation();
    
        assertEquals("Operation Successful", result);
        // dummyLogger의 어떤 메서드도 호출되었는지 검증하지 않음
    }
    ```
    

### 2. 페이크 객체 (Fake Object)

- **정의**: 실제 구현을 단순화된 버전으로 대체하는 객체입니다. 실제 작동하는 구현을 가지고 있지만, 프로덕션 환경에서 사용하기에는 부족한 점이 있습니다(예: 인메모리 데이터베이스는 실제 DB의 트랜잭션 처리나 성능 특성을 완벽히 모방하지 못함).
    
- **특징**: 상태를 가질 수 있고, 호출에 따라 다른 결과를 반환할 수 있습니다. 복잡한 로직을 가질 수 있지만, 실제 구현보다는 가볍고 빠릅니다.
    
- **사용 시나리오**:
    
    - 실제 데이터베이스 대신 [[인메모리 데이터베이스(In-Memory Database)]](예: H2)를 사용하는 경우.
    - 실제 외부 서비스 API를 호출하는 대신, 하드코딩된 데이터를 반환하는 가짜 서비스 객체를 사용하는 경우.
- **Java 예시**:
    
    ```java
    // 사용자 정보를 저장하는 인터페이스
    public interface UserRepository {
        User save(User user);
        User findById(Long id);
    }
    
    // 페이크 UserRepository 구현 (In-Memory)
    public class InMemoryUserRepository implements UserRepository {
        private final Map<Long, User> users = new HashMap<>();
        private long nextId = 1L;
    
        @Override
        public User save(User user) {
            if (user.getId() == null) {
                user.setId(nextId++);
            }
            users.put(user.getId(), user);
            return user;
        }
    
        @Override
        public User findById(Long id) {
            return users.get(id);
        }
    }
    
    // 테스트 코드
    @Test
    void userService_createUser_shouldStoreUserInFakeRepository() {
        UserRepository fakeRepository = new InMemoryUserRepository();
        UserService userService = new UserServiceImpl(fakeRepository); // UserServiceImpl은 UserRepository에 의존
    
        User newUser = new User("Test User");
        User createdUser = userService.createUser(newUser); // createUser는 내부적으로 repository.save() 호출
    
        assertNotNull(createdUser.getId());
        assertEquals("Test User", fakeRepository.findById(createdUser.getId()).getName());
    }
    ```
    

### 3. 스텁 (Stub)

- **정의**: 테스트 중에 만들어진 호출에 대해 미리 준비된 응답(canned answer)을 제공하는 객체입니다. SUT(System Under Test)가 의존 객체의 특정 메서드를 호출했을 때, 미리 정해진 값을 반환하도록 설정합니다. "상태 검증(State Verification)"에 주로 사용됩니다.
    
- **특징**: 테스트 케이스에 맞게 특정 입력에 대한 특정 출력을 하도록 프로그래밍됩니다. SUT의 특정 실행 경로를 테스트하기 위해 사용됩니다.
    
- **사용 시나리오**:
    
    - 외부 API 호출 시 특정 JSON 응답을 반환하도록 설정.
    - 데이터베이스 조회 시 특정 객체나 `null`을 반환하도록 설정.
    - 설정 파일에서 특정 설정 값을 읽어오도록 설정.
- **Java 예시 (Mockito 활용)**: Mockito의 `when(...).thenReturn(...)` 구문을 사용하여 스텁을 만듭니다.
    
    ```java
    public interface ExchangeRateService {
        double getRate(String fromCurrency, String toCurrency);
    }
    
    public class PriceCalculator {
        private final ExchangeRateService exchangeRateService;
        public PriceCalculator(ExchangeRateService exchangeRateService) {
            this.exchangeRateService = exchangeRateService;
        }
        public double calculatePriceInKRW(double priceInUSD) {
            double rate = exchangeRateService.getRate("USD", "KRW");
            if (rate <= 0) {
                throw new IllegalArgumentException("Invalid exchange rate");
            }
            return priceInUSD * rate;
        }
    }
    
    // 테스트 코드
    @Test
    void calculatePriceInKRW_shouldUseRateFromStub() {
        ExchangeRateService stubExchangeRateService = Mockito.mock(ExchangeRateService.class);
        // "USD"에서 "KRW"로 환율 조회 시 1300.0 반환하도록 스텁 설정
        Mockito.when(stubExchangeRateService.getRate("USD", "KRW")).thenReturn(1300.0);
    
        PriceCalculator calculator = new PriceCalculator(stubExchangeRateService);
        double priceInKRW = calculator.calculatePriceInKRW(10.0); // 내부적으로 stubExchangeRateService.getRate() 호출
    
        assertEquals(13000.0, priceInKRW, 0.001);
    }
    
    @Test
    void calculatePriceInKRW_shouldThrowException_whenRateIsInvalid() {
        ExchangeRateService stubExchangeRateService = Mockito.mock(ExchangeRateService.class);
        Mockito.when(stubExchangeRateService.getRate("USD", "KRW")).thenReturn(0.0); // 유효하지 않은 환율 반환 스텁
    
        PriceCalculator calculator = new PriceCalculator(stubExchangeRateService);
    
        assertThrows(IllegalArgumentException.class, () -> {
            calculator.calculatePriceInKRW(10.0);
        });
    }
    ```
    

### 4. 스파이 (Spy)

- **정의**: 스텁의 일종이지만, 실제 객체를 부분적으로 사용하면서 특정 메서드만 스텁으로 대체하거나, 호출되었을 때 어떤 방식으로 호출되었는지(예: 호출 횟수, 전달된 인자)를 기록하고 이를 검증할 수 있게 하는 객체입니다. "행위 검증(Behavior Verification)"에 사용되기도 합니다.
    
- **특징**: 실제 객체의 로직을 사용하면서 특정 부분만 제어하고 싶을 때 유용합니다. 호출 정보를 기록하여 간접적인 출력(indirect output)을 검증하는 데 사용됩니다.
    
- **주의**: 실제 객체를 감싸기 때문에, 스파이의 특정 메서드를 스텁 처리하지 않으면 실제 객체의 메서드가 호출됩니다. 이는 예기치 않은 부작용을 일으킬 수 있으므로 사용에 주의가 필요합니다.
    
- **사용 시나리오**:
    
    - 실제 클래스의 대부분의 메서드는 그대로 사용하고, 한두 개의 메서드만 특정 값을 반환하도록 하고 싶을 때.
    - 메서드가 정확한 인자로 호출되었는지, 또는 특정 횟수만큼 호출되었는지 확인하고 싶을 때 (Mockito에서는 Mock 객체로도 가능).
- **Java 예시 (Mockito 활용)**: Mockito의 `spy()` 메서드로 실제 객체를 감싸 스파이를 만듭니다. 특정 메서드를 스텁 처리할 때는 `doReturn(...).when(spy).methodToStub(...)` 형식을 사용합니다.
    

    ```java
    public class EmailService {
        public void sendEmail(String to, String subject, String body) {
            // 실제 이메일 발송 로직 (테스트에서는 실행시키고 싶지 않음)
            System.out.println("Email sent to " + to);
        }
        public String formatEmail(String name) {
            // 이 메서드는 실제 로직을 테스트하고 싶음
            return "Hello, " + name + "!";
        }
    }
    
    public class NotificationManager {
        private final EmailService emailService;
        public NotificationManager(EmailService emailService) {
            this.emailService = emailService;
        }
        public void notifyUser(String name, String emailAddress) {
            String emailBody = emailService.formatEmail(name); // 실제 메서드 호출 원함
            emailService.sendEmail(emailAddress, "Notification", emailBody); // 이 메서드 호출 여부 검증 원함
        }
    }
    
    // 테스트 코드
    @Test
    void notifyUser_shouldFormatAndSendEmail_withSpy() {
        EmailService realEmailService = new EmailService();
        EmailService spyEmailService = Mockito.spy(realEmailService);
    
        // spyEmailService.sendEmail() 메서드가 호출될 때 아무것도 하지 않도록 스텁 처리 (실제 이메일 발송 방지)
        // 주의: spy 객체의 메서드를 스텁할 때는 doReturn/doNothing.when(spy).method() 구문 사용 권장
        Mockito.doNothing().when(spyEmailService).sendEmail(Mockito.anyString(), Mockito.anyString(), Mockito.anyString());
    
        NotificationManager notificationManager = new NotificationManager(spyEmailService);
        notificationManager.notifyUser("John Doe", "john.doe@example.com");
    
        // formatEmail은 실제 메서드가 호출되었는지 (spy이므로) 내용 검증 가능
        // (실제로는 formatEmail 자체를 별도 단위테스트 하는 것이 더 좋음)
    
        // sendEmail 메서드가 특정 인자들로 호출되었는지 검증
        Mockito.verify(spyEmailService).sendEmail("john.doe@example.com", "Notification", "Hello, John Doe!");
    }
    ```
    
    Mockito에서는 Mock 객체도 `verify()`를 통해 호출 여부 및 인자 검증이 가능하므로, Spy의 주요 용도는 **실제 객체의 일부 로직을 실행하면서 특정 부분만 제어하거나 검증**하고 싶을 때입니다.
    

### 5. 목 객체 (Mock Object)

- **정의**: 호출에 대한 기대를 명세(expectation)하고, 해당 기대에 따라 동작하며, 테스트 종료 후 기대대로 호출되었는지 검증하는 객체입니다. 주로 SUT와 의존 객체 간의 상호작용, 즉 "행위 검증(Behavior Verification)"에 초점을 맞춥니다.
    
- **특징**:
    
    - 테스트 시작 전에 Mock 객체에 대한 기대 행위(예: 어떤 메서드가 몇 번 호출되어야 하는지, 어떤 인자를 받아야 하는지)를 설정합니다.
    - SUT가 실행된 후, Mock 객체가 기대한 대로 사용되었는지 `verify()`를 통해 검증합니다.
    - 테스트 실패 시 어떤 상호작용이 잘못되었는지 명확히 알려줍니다.
    - Mockito, EasyMock, JMock과 같은 [[Mocking 프레임워크]]를 통해 쉽게 생성하고 관리할 수 있습니다.
- **사용 시나리오**:
    
    - SUT가 의존 객체의 메서드를 올바른 순서로, 올바른 횟수만큼, 올바른 인자를 사용하여 호출하는지 검증하고 싶을 때.
    - 의존 객체의 반환 값에는 관심이 없거나, 반환 값이 `void`인 메서드의 호출 여부를 검증해야 할 때.
- **Java 예시 (Mockito 활용)**: Mockito의 `mock()`으로 목 객체를 생성하고, `verify()`를 통해 행위를 검증합니다.
    
    ```java
    public interface PaymentGateway {
        PaymentResult processPayment(Order order, CreditCardDetails creditCard);
    }
    // PaymentResult, Order, CreditCardDetails 클래스가 있다고 가정
    
    public class OrderService {
        private final PaymentGateway paymentGateway;
        private final AuditLogService auditLogService; // 또 다른 의존성
    
        public OrderService(PaymentGateway paymentGateway, AuditLogService auditLogService) {
            this.paymentGateway = paymentGateway;
            this.auditLogService = auditLogService;
        }
    
        public boolean placeOrder(Order order, CreditCardDetails creditCard) {
            // ... 주문 처리 로직 ...
            PaymentResult result = paymentGateway.processPayment(order, creditCard); // 핵심 상호작용
            if (result.isSuccess()) {
                auditLogService.logOrderPlaced(order.getId(), "SUCCESS"); // 또 다른 상호작용
                return true;
            } else {
                auditLogService.logOrderPlaced(order.getId(), "FAILED: " + result.getErrorMessage());
                return false;
            }
        }
    }
    // AuditLogService 인터페이스가 있다고 가정
    public interface AuditLogService {
        void logOrderPlaced(String orderId, String status);
    }
    
    
    // 테스트 코드
    @Test
    void placeOrder_shouldCallPaymentGatewayAndLog_whenPaymentSuccessful() {
        PaymentGateway mockPaymentGateway = Mockito.mock(PaymentGateway.class);
        AuditLogService mockAuditLogService = Mockito.mock(AuditLogService.class); // AuditLogService도 Mock으로
    
        Order order = new Order("testOrder123", 100.0);
        CreditCardDetails creditCard = new CreditCardDetails("1234-5678-9012-3456");
        PaymentResult successfulPaymentResult = new PaymentResult(true, null);
    
        // Mock 객체(PaymentGateway)의 기대 행위 설정 (Stub 역할도 겸함)
        Mockito.when(mockPaymentGateway.processPayment(order, creditCard)).thenReturn(successfulPaymentResult);
    
        OrderService orderService = new OrderService(mockPaymentGateway, mockAuditLogService);
        boolean orderPlaced = orderService.placeOrder(order, creditCard);
    
        assertTrue(orderPlaced);
    
        // Mock 객체(PaymentGateway)가 정확히 1번 processPayment 메서드를 order와 creditCard 인자로 호출했는지 검증
        Mockito.verify(mockPaymentGateway, Mockito.times(1)).processPayment(order, creditCard);
        // Mock 객체(AuditLogService)가 정확히 1번 logOrderPlaced 메서드를 특정 인자들로 호출했는지 검증
        Mockito.verify(mockAuditLogService, Mockito.times(1)).logOrderPlaced("testOrder123", "SUCCESS");
    }
    ```
    
    이 예시에서 `mockPaymentGateway`는 `processPayment` 메서드가 호출되면 `successfulPaymentResult`를 반환하도록 설정되어 스텁의 역할도 수행하지만, 테스트 마지막에 `verify()`를 통해 **호출 여부와 횟수, 인자까지 검증**하므로 목 객체의 핵심적인 특징인 행위 검증을 보여줍니다.
    

더 자세한 Mockito 사용법은 [[Mockito 사용 가이드]]를 참고해주세요.

## 테스트 더블 선택 가이드: 상태 검증 vs 행위 검증

어떤 테스트 더블을 선택할지는 테스트의 목적과 SUT와 의존 객체 간의 상호작용 방식에 따라 달라집니다. 핵심적인 구분 기준 중 하나는 [[상태 검증(State Verification)]]과 [[행위 검증(Behavior Verification)]]입니다.

- **상태 검증 (State Verification)**: SUT의 메서드를 호출한 후, SUT나 의존 객체의 상태가 예상대로 변경되었는지 확인하는 방식입니다. 주로 **스텁(Stub)**이나 **페이크(Fake)**를 사용하여 SUT가 특정 상태에 도달하도록 유도하고, 그 결과를 단언(assert)합니다.
- **행위 검증 (Behavior Verification)**: SUT가 의존 객체의 메서드를 올바르게 호출했는지(예: 호출 순서, 횟수, 전달된 인자) 확인하는 방식입니다. 주로 **목(Mock)**이나 **스파이(Spy)**를 사용하여 SUT와 의존 객체 간의 상호작용 자체를 검증합니다.

일반적으로는 상태 검증을 우선적으로 고려하는 것이 좋습니다. 행위 검증은 SUT의 내부 구현에 더 강하게 결합될 수 있어, 리팩토링 시 테스트가 깨지기 쉬운 단점이 있기 때문입니다. 하지만 의존 객체의 상태를 직접 확인할 수 없거나, 부수 효과(side effect)를 일으키는 메서드 호출(예: 이메일 발송, 로깅)을 검증해야 할 때는 행위 검증이 유용합니다.

상황에 따른 선택 가이드:

- 단순히 값을 반환받아 SUT의 로직을 진행해야 한다면: **Stub**
- 실제 구현과 유사하지만 가벼운 버전이 필요하다면: **Fake**
- SUT가 의존 객체와 올바르게 상호작용하는지 검증하고 싶다면 (주로 void 메서드 호출 검증 등): **Mock**
- 실제 객체의 일부 기능은 사용하면서 특정 호출을 검증하거나 일부 메서드만 스텁하고 싶다면: **Spy**
- 단순히 파라미터 자리를 채우는 용도라면: **Dummy**

## 테스트 더블 사용 시 주의사항

- **과도한 Mocking 주의**: 너무 많은 것을 Mocking하면 테스트가 SUT의 구현 세부 사항에 지나치게 의존하게 되어, 작은 리팩토링에도 테스트가 쉽게 깨질 수 있습니다. 테스트는 구현이 아닌 **동작(behavior)**을 검증해야 합니다.
- **Mock 객체의 복잡한 설정**: Mock 객체의 `when-thenReturn` 설정이 매우 복잡해진다면, SUT의 설계가 너무 많은 책임을 지고 있거나 [[단일 책임 원칙(Single Responsibility Principle)]]을 위반했을 가능성을 의심해봐야 합니다.
- **테스트 더블 자체의 로직 최소화**: 테스트 더블, 특히 Fake 객체의 로직이 너무 복잡해지면 테스트 더블 자체를 테스트해야 하는 상황이 올 수 있습니다. 가능한 단순하게 유지해야 합니다.
- **"Mock은 타입이지 역할이 아니다"**: Mockito와 같은 프레임워크를 사용하면 `mock()` 메서드로 생성된 객체는 기술적으로는 "Mock"이지만, 스텁처럼 사용될 수도 있고 스파이처럼 사용될 수도 있습니다. 중요한 것은 테스트에서 해당 객체가 어떤 **역할(stub, spy, mock)**을 수행하도록 의도했는지 명확히 하는 것입니다.

## 결론

테스트 더블은 [[단위 테스트(Unit Test)]]의 품질을 높이고, 테스트 가능하고 유지보수하기 쉬운 코드를 작성하는 데 필수적인 도구입니다. Dummy, Fake, Stub, Spy, Mock 각각의 특징과 사용 목적을 정확히 이해하고, 테스트하려는 상황과 SUT의 상호작용 방식에 따라 가장 적절한 테스트 더블을 선택하는 것이 중요합니다.

효과적인 테스트 더블의 활용은 개발자가 자신의 코드를 더 깊이 이해하고, 더 견고하며 신뢰할 수 있는 소프트웨어를 만드는 데 크게 기여할 것입니다.

## 참고 자료

- "xUnit Test Patterns: Refactoring Test Code" - Gerard Meszaros
- Martin Fowler - "Mocks Aren't Stubs" ([https://martinfowler.com/articles/mocksArentStubs.html](https://martinfowler.com/articles/mocksArentStubs.html))
- Martin Fowler - "TestDouble" ([https://martinfowler.com/bliki/TestDouble.html](https://martinfowler.com/bliki/TestDouble.html))
- Mockito 공식 문서 ([https://site.mockito.org/](https://site.mockito.org/))