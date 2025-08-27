옵서버 패턴은 **한 객체의 상태가 변경되면 그 객체에 의존하는 다른 객체들에게 자동으로 알려주고 업데이트하는** 일대다(one-to-many) 의존성을 정의하는 행위 디자인 패턴입니다.

이 패턴은 흔히 **발행-구독(Publish-Subscribe)** 모델로도 알려져 있습니다. 가장 직관적인 예시는 유튜브 채널 구독입니다.

- **유튜버 (Subject, 발행자)**: 새로운 영상을 올리며 상태를 변경합니다.
- **구독자 (Observer, 구독자)**: 유튜버를 구독하고 있으며, 새 영상이 올라오면 알림을 받습니다.

여기서 중요한 점은 유튜버가 자신의 구독자가 누구인지, 몇 명인지 일일이 알 필요가 없다는 것입니다. 유튜버는 그저 "내 채널을 구독하는 모든 사람에게 알려줘"라는 신호만 보내면, 시스템이 알아서 모든 구독자에게 알림을 전달합니다. 이처럼 발행자와 구독자 간의 **느슨한 결합(Loose Coupling)**이 옵서버 패턴의 핵심입니다.

### 핵심 구성 요소

옵서버 패턴은 주로 두 개의 주체와 그 구현체로 구성됩니다.

- **Subject (주체, 발행자)**: 관찰 대상이 되는 객체입니다. 내부에 Observer들의 목록을 가지고 있으며, Observer를 등록(`register`/`attach`)하거나 제거(`unregister`/`detach`)하는 메서드를 제공합니다. 상태가 변경되었을 때, 등록된 모든 Observer에게 알리는(`notify`) 역할을 합니다.
- **Observer (관찰자, 구독자)**: Subject의 상태 변화를 통지받는 객체입니다. 보통 `update()`와 같은 메서드를 가지며, Subject로부터 알림이 오면 이 메서드가 호출됩니다.
- **ConcreteSubject**: Subject 인터페이스의 실제 구현체입니다. 상태를 가지고 있으며, 상태가 변경될 때 `notify()` 메서드를 호출하여 Observer들에게 알립니다.
- **ConcreteObserver**: Observer 인터페이스의 실제 구현체입니다. `update()` 메서드가 호출되었을 때 수행할 구체적인 동작을 정의합니다.

### Java 예시 코드: 주식 가격 알림 시스템

주식 중개소(Subject)의 특정 주식 가격이 변동될 때마다, 해당 주식에 관심 있는 투자자(Observer)들에게 알림을 보내는 시스템을 구현해 보겠습니다.

```java
import java.util.ArrayList;
import java.util.List;

// Observer 인터페이스
public interface Investor {
    void update(String stockName, float price);
}

// Subject 인터페이스
public interface StockBroker {
    void registerInvestor(Investor investor);
    void unregisterInvestor(Investor investor);
    void notifyInvestors();
}

// ConcreteSubject: 실제 주식 중개소
public class ConcreteStockBroker implements StockBroker {
    private String stockName;
    private float price;
    private List<Investor> investors = new ArrayList<>();

    public ConcreteStockBroker(String stockName) {
        this.stockName = stockName;
    }

    @Override
    public void registerInvestor(Investor investor) {
        investors.add(investor);
    }

    @Override
    public void unregisterInvestor(Investor investor) {
        investors.remove(investor);
    }

    @Override
    public void notifyInvestors() {
        for (Investor investor : investors) {
            // Push 방식: 변경된 정보를 직접 전달
            investor.update(stockName, price);
        }
    }

    public void setPrice(float price) {
        this.price = price;
        System.out.println(stockName + "의 가격이 " + price + "로 변경되었습니다.");
        notifyInvestors(); // 가격이 변경되면 모든 투자자에게 알림
    }
}

// ConcreteObserver: 실제 투자자
public class ConcreteInvestor implements Investor {
    private String name;

    public ConcreteInvestor(String name) {
        this.name = name;
    }

    @Override
    public void update(String stockName, float price) {
        System.out.println("[" + name + "] 알림: " + stockName + "의 가격이 " + price + "가 되었습니다!");
    }
}

// 실행
public class Application {
    public static void main(String[] args) {
        ConcreteStockBroker samsungBroker = new ConcreteStockBroker("삼성전자");
        
        Investor investorA = new ConcreteInvestor("개미 투자자 A");
        Investor investorB = new ConcreteInvestor("기관 투자자 B");

        samsungBroker.registerInvestor(investorA);
        samsungBroker.registerInvestor(investorB);

        samsungBroker.setPrice(80000);
        // 출력:
        // 삼성전자의 가격이 80000.0로 변경되었습니다.
        // [개미 투자자 A] 알림: 삼성전자의 가격이 80000.0가 되었습니다!
        // [기관 투자자 B] 알림: 삼성전자의 가격이 80000.0가 되었습니다!

        samsungBroker.unregisterInvestor(investorB);
        samsungBroker.setPrice(85000);
        // 출력:
        // 삼성전자의 가격이 85000.0로 변경되었습니다.
        // [개미 투자자 A] 알림: 삼성전자의 가격이 85000.0가 되었습니다!
    }
}
```

### 스프링 프레임워크에서의 활용: `ApplicationEventPublisher`

스프링 프레임워크는 옵서버 패턴을 내장하여 **[[이벤트 기반 아키텍처(Event-Driven Architecture)]]**를 손쉽게 구현할 수 있도록 지원합니다. 개발자는 복잡한 Observer, Subject 클래스들을 직접 만들 필요 없이 스프링이 제공하는 메커니즘을 사용하면 됩니다.

- **`ApplicationEvent` (메시지)**: Subject가 발행하는 이벤트(상태 변화) 정보입니다. 개발자는 `ApplicationEvent`를 상속받아 원하는 데이터를 담는 커스텀 이벤트를 만듭니다.
- **`ApplicationEventPublisher` (발행자)**: 이벤트를 발행하는 역할을 합니다. 서비스 클래스에 주입받아 `publishEvent()` 메서드를 호출하기만 하면 됩니다.
- **`@EventListener` (구독자)**: 이벤트를 수신하여 처리하는 메서드에 이 어노테이션을 붙입니다. 스프링이 알아서 해당 이벤트를 구독하는 Observer로 등록해 줍니다.

#### 예시: 주문 완료 시 이메일 발송 및 재고 감소

`OrderService`에서 주문이 완료되면 `OrderCompletedEvent`를 발행하고, `EmailService`와 `InventoryService`가 이 이벤트를 구독하여 각각 이메일 발송과 재고 감소 처리를 하는 예시입니다.

```java
// 1. 이벤트 정의 (메시지)
public class OrderCompletedEvent extends ApplicationEvent {
    private final Order order;

    public OrderCompletedEvent(Object source, Order order) {
        super(source);
        this.order = order;
    }
    // Getter
}


// 2. 이벤트 발행 (Publisher)
@Service
public class OrderService {
    private final ApplicationEventPublisher eventPublisher;

    public OrderService(ApplicationEventPublisher eventPublisher) {
        this.eventPublisher = eventPublisher;
    }

    public void completeOrder(Order order) {
        // ... 주문 처리 로직 ...
        System.out.println(order.getId() + "번 주문 처리가 완료되었습니다.");
        
        // 이벤트 발행
        eventPublisher.publishEvent(new OrderCompletedEvent(this, order));
    }
}


// 3. 이벤트 구독 (Observer/Listener)
@Component
public class EmailService {
    @EventListener
    public void sendConfirmationEmail(OrderCompletedEvent event) {
        System.out.println(event.getOrder().getCustomerEmail() + " 주소로 주문 완료 이메일을 발송합니다.");
    }
}

@Component
public class InventoryService {
    @EventListener
    @Async // 이메일 발송과 재고 감소를 비동기적으로 처리할 수도 있습니다.
    public void decreaseStock(OrderCompletedEvent event) {
        System.out.println(event.getOrder().getProductId() + " 상품의 재고를 감소시킵니다.");
    }
}
```

이 구조의 가장 큰 장점은 **`OrderService`가 `EmailService`나 `InventoryService`의 존재를 전혀 알지 못한다는 것**입니다. `OrderService`는 그저 "주문이 완료되었다"는 사실만 외칠 뿐입니다. 나중에 문자 메시지 발송, 배송 시스템 연동 등 새로운 기능이 추가되더라도, 새로운 `@EventListener`를 구현하기만 하면 되므로 기존 코드를 수정할 필요가 없이 시스템을 확장할 수 있습니다. 이는 서비스 간의 결합도를 획기적으로 낮춰 유지보수성이 높은 마이크로서비스 아키텍처의 기반이 됩니다.