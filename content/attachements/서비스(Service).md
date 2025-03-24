소프트웨어 설계에서 모든 개념이 객체로 자연스럽게 모델링되는 것은 아닙니다. [[도메인 주도 설계(DDD,Domain Driven Design)]]에서는 [[엔티티(Entity)]]와 [[값 객체(Value Objects)]]가 중요한 역할을 하지만, 이 두 범주에 속하지 않는 중요한 도메인 연산들도 존재합니다.

서비스(Service)는 도메인 모델에서 독립적으로 존재하는 인터페이스로, 상태를 캡슐화하지 않고 수행할 기능만을 정의합니다. 서비스는 주로 활동이나 행위를 나타내며, 동사에 가까운 명칭을 가집니다.

예를 들어, 은행 도메인에서 '계좌 이체'는 두 계좌 간 자금 이동 작업입니다. 이 연산은 특정 계좌에 한정되지 않고 여러 객체(예: 두 계좌, 거래 기록 등)를 조정해야 하므로 '계좌 이체 서비스'를 만드는 것이 적절합니다.

## 좋은 서비스의 특성

1. **도메인 개념 관련성**: 해당 연산이 엔티티나 값 객체의 일부가 아닌 도메인 개념과 관련되어야 합니다.
2. **도메인 모델 기반 인터페이스**: 인터페이스는 도메인 모델의 다른 요소들을 기반으로 정의되어야 합니다.
3. **무상태성**: 연산은 상태를 가지지 않아야 하며, 서비스의 인스턴스 이력과 무관하게 어떤 인스턴스든 사용할 수 있어야 합니다.

서비스는 신중하게 활용해야 하며, 엔티티와 값 객체의 **모든 행동을 대체해서는 안 됩니다**. 그러나 연산이 중요한 도메인 개념일 경우, 서비스는 자연스러운 [[도메인 모델(Domain Model)]] 기반 설계를 지원합니다.

## 계층에 따른 서비스 유형

소프트웨어 아키텍처는 각기 다른 책임과 특성을 지닌 여러 계층의 서비스를 포함할 수 있습니다.

### 도메인 서비스 (Domain Service)

도메인 서비스는 비즈니스 로직을 포함하며 도메인 언어의 일부입니다. 예를 들어, '자금 이체 서비스'는 계좌 간 자금 이동 규칙을 포함하는 도메인 서비스입니다.

```java
public interface FundsTransferService {
    TransferResult transfer(Account sourceAccount, Account targetAccount, Money amount);
}

public class FundsTransferServiceImpl implements FundsTransferService {
    @Override
    public TransferResult transfer(Account sourceAccount, Account targetAccount, Money amount) {
        if (!sourceAccount.canWithdraw(amount)) {
            return TransferResult.insufficientFunds();
        }
        
        sourceAccount.withdraw(amount);
        targetAccount.deposit(amount);
        
        return TransferResult.success(new Transaction(sourceAccount, targetAccount, amount));
    }
}
```

### 애플리케이션 서비스 (Application Service)

애플리케이션 서비스는 사용자 요청을 조정하고, 도메인 객체 및 서비스를 활용하여 작업을 수행합니다. 도메인 계층과 인프라 계층 사이의 중간자 역할을 합니다.

```java
@Service
public class FundsTransferApplicationService {
    private final FundsTransferService fundsTransferService;
    private final AccountRepository accountRepository;
    private final NotificationService notificationService;
    
    public FundsTransferApplicationService(
            FundsTransferService fundsTransferService, 
            AccountRepository accountRepository,
            NotificationService notificationService) {
        this.fundsTransferService = fundsTransferService;
        this.accountRepository = accountRepository;
        this.notificationService = notificationService;
    }
    
    @Transactional
    public TransferResultDTO transferFunds(
            String sourceAccountId, String targetAccountId, BigDecimal amount, String currency) {
        Account sourceAccount = accountRepository.findById(sourceAccountId)
                .orElseThrow(() -> new AccountNotFoundException(sourceAccountId));
        Account targetAccount = accountRepository.findById(targetAccountId)
                .orElseThrow(() -> new AccountNotFoundException(targetAccountId));
        Money transferAmount = new Money(amount, Currency.getInstance(currency));
        
        TransferResult result = fundsTransferService.transfer(sourceAccount, targetAccount, transferAmount);
        
        if (result.isSuccessful()) {
            notificationService.notifyTransfer(result.getTransaction());
        }
        
        return TransferResultDTO.fromDomainResult(result);
    }
}
```

### 인프라 서비스 (Infrastructure Service)

인프라 서비스는 이메일 전송, 파일 시스템 접근, 외부 API 호출처럼 기술적인 기능을 제공합니다.

```java
@Service
public class EmailNotificationService implements NotificationService {
    private final JavaMailSender mailSender;
    private final MessageTemplateRepository templateRepository;
    
    @Override
    public void notifyTransfer(Transaction transaction) {
        String customerEmail = transaction.getSourceAccount().getOwner().getEmail();
        String messageBody = createTransferNotificationMessage(transaction);
        
        SimpleMailMessage message = new SimpleMailMessage();
        message.setTo(customerEmail);
        message.setSubject("자금 이체 알림");
        message.setText(messageBody);
        
        mailSender.send(message);
    }
    
    private String createTransferNotificationMessage(Transaction transaction) {
        MessageTemplate template = templateRepository.findByType(MessageType.TRANSFER_NOTIFICATION);
        return template.apply(transaction);
    }
}
```

## 서비스 설계 시 고려사항

### 세분성(Granularity)

서비스의 세분성은 시스템 설계에 중요한 영향을 미칩니다:

- **중간 수준의 무상태 서비스**: 간단한 인터페이스 뒤에 중요한 기능을 캡슐화하여 재사용을 용이하게 합니다.
- **세밀한 객체 문제**: 비효율적인 메시징을 초래할 수 있으며, 도메인 서비스 도입으로 계층간 경계를 명확히 유지할 수 있습니다.

서비스 패턴은 인터페이스의 단순성을 선호하며, 큰 시스템 또는 분산 시스템의 기능을 패키징하는 데 유용합니다.

### 서비스 접근 방식

분산 시스템 아키텍처(J2EE, CORBA 등)는 서비스를 위한 특별한 메커니즘을 제공하지만, 프로젝트에 항상 적합한 것은 아닙니다. 논리적 관심사 분리가 목표라면 이러한 프레임워크는 지나칠 수 있습니다.

서비스 접근보다 중요한 것은 특정 책임을 분리하는 설계입니다. 서비스 인터페이스의 구현자로 "doer" 객체가 충분할 수 있으며, 간단한 싱글톤 접근 방식도 가능합니다.

## 실제 비즈니스 시나리오 예시

### 도메인 서비스

```java
public interface OrderProcessingService {
    OrderProcessingResult process(Order order, Payment payment);
}

public class OrderProcessingServiceImpl implements OrderProcessingService {
    private final InventoryChecker inventoryChecker;

    @Override
    public OrderProcessingResult process(Order order, Payment payment) {
        if (!inventoryChecker.hasAvailableStock(order.getItems())) {
            return OrderProcessingResult.outOfStock(order.getOutOfStockItems());
        }

        order.markAsProcessed();
        order.getItems().forEach(item -> inventoryChecker.reduceStock(item.getProductId(), item.getQuantity()));

        return OrderProcessingResult.success(order);
    }
}
```

### 애플리케이션 서비스

```java
@Service
public class OrderApplicationService {
    private final OrderRepository orderRepository;
    private final OrderProcessingService orderProcessingService;
    private final PaymentService paymentService;
    private final OrderNotificationService notificationService;
    
    @Transactional
    public OrderResultDTO processOrder(Long orderId, PaymentDTO paymentDetails) {
        Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new OrderNotFoundException(orderId));
        
        Payment payment = paymentService.processPayment(
                paymentDetails.getMethod(),
                paymentDetails.getAmount(),
                paymentDetails.getDetails()
        );
        
        if (!payment.isSuccessful()) {
            return OrderResultDTO.paymentFailed(payment.getFailureReason());
        }
        
        OrderProcessingResult result = orderProcessingService.process(order, payment);
        
        if (result.isSuccessful()) {
            order.linkPayment(payment);
            orderRepository.save(order);
            notificationService.sendOrderConfirmation(order);
        }
        
        return OrderResultDTO.fromDomainResult(result);
    }
}
```

### 인프라 서비스

```java
@Service
public class EmailOrderNotificationService implements OrderNotificationService {
    private final JavaMailSender mailSender;
    private final OrderConfirmationTemplateProvider templateProvider;
    
    @Override
    public void sendOrderConfirmation(Order order) {
        Customer customer = order.getCustomer();
        String emailContent = templateProvider.getOrderConfirmationTemplate(order);
        
        MimeMessage message = mailSender.createMimeMessage();
        MimeMessageHelper helper = new MimeMessageHelper(message, true);
        
        try {
            helper.setTo(customer.getEmail());
            helper.setSubject("주문 확인: " + order.getOrderNumber());
            helper.setText(emailContent, true);
            
            mailSender.send(message);
        } catch (MessagingException e) {
            throw new NotificationFailedException("주문 확인 이메일 전송 실패", e);
        }
    }
}
```

## 서비스 패턴의 장단점

### 장점

1. **책임 분리**: 특정 객체에 적절하지 않은 연산을 처리할 명확한 장소를 제공합니다.
2. **도메인 모델 순도 유지**: 엔티티나 값 객체의 개념적 명확성을 유지합니다.
3. **다중 객체 조정**: 여러 도메인 객체 간 상호 작용이 필요한 연산을 캡슐화합니다.
4. **무상태 연산의 명확한 표현**: 인위적 객체 없이 무상태 연산을 표현할 수 있습니다.

### 단점

1. **과도한 사용 위험**: 서비스에 너무 많은 책임을 부여하면 절차적 프로그래밍으로 퇴행할 수 있습니다.
2. **도메인 객체 빈약화**: 도메인 객체가 행동이 없는 데이터 컨테이너로 전락할 수 있습니다.
3. **복잡성 증가**: 추가 계층이 시스템 복잡성을 초래할 수 있습니다.

## 서비스 패턴 적용 가이드라인

1. **도메인 언어 사용**: 서비스 이름은 유비쿼터스 언어에서 가져오거나 도입합니다.
2. **적절한 계층에 배치**: 각 계층의 책임 경계를 존중합니다.
3. **상태 관리 주의**: 서비스를 상태 없이 설계합니다.
4. **세분성 균형**: 중간 수준의 세분성을 목표로 합니다.
5. **인터페이스 명확성**: 도메인 모델의 다른 요소를 기반으로 서비스 인터페이스를 명확히 정의합니다.

## 결론

서비스 패턴은 도메인 주도 설계에서 중요한 역할을 하며, 엔티티나 값 객체에 속하지 않는 중요한 도메인 연산을 수용할 수 있게 합니다. 서비스는 도메인 모델의 개념적 명확성을 유지하며, 복잡한 비즈니스 로직을 표현하는 강력한 도구입니다. 그러나 적절히 사용해야 하며, 도메인 객체의 책임을 과도하게 빼앗지 않도록 주의해야 합니다. 적절히 적용된 서비스 패턴은 소프트웨어 설계의 표현력을 높이고, 유지 보수를 용이하게 하며, 도메인 모델의 순수성을 보존하는 데 기여합니다.

## 참고 문헌

- Evans, Eric. "Domain-Driven Design: Tackling Complexity in the Heart of Software." Addison-Wesley, 2003.
- Vernon, Vaughn. "Implementing Domain-Driven Design." Addison-Wesley, 2013.