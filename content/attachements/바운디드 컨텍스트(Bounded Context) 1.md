바운디드 컨텍스트는 도메인 모델이 유효한 경계(boundary)를 가지는 컨텍스트를 말합니다. 각 컨텍스트는 특정한 [[도메인 모델(Domain Model)]]과 [[유비쿼터스 언어(Ubiquitous Language)]]를 가지고 있으며, 이 경계 내에서 해당 모델과 언어의 일관성이 유지됩니다. 즉, 동일한 용어가 다른 컨텍스트에서 다른 의미를 가질 수 있으며, 각 컨텍스트는 이를 독립적으로 관리합니다.

> **예시**: 기업의 인사 관리 시스템에서 "사용자(User)"라는 용어는 HR 컨텍스트에서는 직원(Employee)을 의미하지만, IT 지원 컨텍스트에서는 시스템 접근 권한을 가진 계정(Account)을 의미할 수 있습니다.

## 바운디드 컨텍스트의 중요성

- **복잡성 관리**: 도메인을 작고 **관리하기 쉬운 단위로 분할**하여 시스템 전체의 복잡성을 줄입니다.
- **모델의 일관성 유지**: 각 컨텍스트 내에서 도메인 모델의 일관성과 무결성을 유지할 수 있습니다.
- **팀 간 협업 강화**: 컨텍스트별로 팀을 구성하여 병렬 작업이 가능하며, 각 팀은 자신의 컨텍스트에 집중할 수 있습니다.
- **유비쿼터스 언어의 효과적 적용**: 컨텍스트 내에서 통일된 용어와 개념을 사용하여 의사소통의 효율성을 높입니다.
- **변경 영향 최소화**: 한 컨텍스트의 변경이 다른 컨텍스트에 미치는 영향을 줄여 시스템의 안정성을 높입니다.

## 바운디드 컨텍스트 정의 방법

1. **도메인 분석**: 전체 도메인을 이해하고, 주요 기능과 개념을 식별합니다.
2. **하위 도메인 구분**: 도메인을 논리적으로 분할하여 하위 도메인을 정의합니다.
3. **컨텍스트 경계 설정**: 하위 도메인에 따라 바운디드 컨텍스트의 경계를 설정합니다.
4. **유비쿼터스 언어 수립**: 각 컨텍스트 내에서 사용할 용어와 개념을 정의합니다.
5. **컨텍스트 간 관계 정의**: 컨텍스트 간의 의존성과 통합 방식을 명확히 합니다.

## 바운디드 컨텍스트의 적용 예시

### 예시: 전자상거래 플랫폼

전자상거래 플랫폼에서는 여러 가지 기능을 제공하며, 이를 바운디드 컨텍스트로 분리할 수 있습니다.

#### 1. 상품 관리 컨텍스트(Product Context)

- **기능**:
  - 제품의 등록, 수정, 삭제
  - 재고 관리
- **유비쿼터스 언어**: 상품(Product), 재고(Inventory), 카테고리(Category)
- **도메인 모델 코드 예시**:

```java
// Product.java
public class Product {
    private Long id;
    private String name;
    private Category category;
    private int stockQuantity;

    // 생성자
    public Product(Long id, String name, Category category, int stockQuantity) {
        this.id = id;
        this.name = name;
        this.category = category;
        this.stockQuantity = stockQuantity;
    }

    // 재고 증가
    public void addStock(int quantity) {
        this.stockQuantity += quantity;
    }

    // 재고 감소
    public void removeStock(int quantity) throws IllegalArgumentException {
        int restStock = this.stockQuantity - quantity;
        if (restStock < 0) {
            throw new IllegalArgumentException("재고가 부족합니다.");
        }
        this.stockQuantity = restStock;
    }

    // Getter, Setter 생략
}

// Category.java
public class Category {
    private Long id;
    private String name;

    // 생성자
    public Category(Long id, String name) {
        this.id = id;
        this.name = name;
    }

    // Getter, Setter 생략
}
```

#### 2. 주문 처리 컨텍스트(Order Context)

- **기능**:
  - 주문 생성 및 취소
  - 주문 내역 조회
- **유비쿼터스 언어**: 주문(Order), 주문 항목(OrderItem), 결제 상태(PaymentStatus)
- **도메인 모델 코드 예시**:

```java
// Order.java
public class Order {
    private Long orderId;
    private List<OrderItem> orderItems;
    private LocalDateTime orderDate;
    private OrderStatus status;

    // 생성자
    public Order(Long orderId, List<OrderItem> orderItems) {
        this.orderId = orderId;
        this.orderItems = orderItems;
        this.orderDate = LocalDateTime.now();
        this.status = OrderStatus.ORDERED;
    }

    // 주문 취소
    public void cancelOrder() {
        if (status == OrderStatus.SHIPPED) {
            throw new IllegalStateException("이미 배송된 상품은 취소가 불가능합니다.");
        }
        this.status = OrderStatus.CANCELED;
        for (OrderItem item : orderItems) {
            item.cancel();
        }
    }

    // Getter, Setter 생략
}

// OrderItem.java
public class OrderItem {
    private Long productId;
    private int orderPrice;
    private int count;

    // 생성자
    public OrderItem(Long productId, int orderPrice, int count) {
        this.productId = productId;
        this.orderPrice = orderPrice;
        this.count = count;
    }

    // 주문 항목 취소
    public void cancel() {
        // 상품 재고 수량 원상복구 로직 등
    }

    // Getter, Setter 생략
}
```

#### 3. 배송 관리 컨텍스트(Shipping Context)

- **기능**:
  - 배송 정보 생성 및 수정
  - 배송 상태 추적
- **유비쿼터스 언어**: 배송(Shipment), 배송 상태(ShippingStatus), 운송장 번호(TrackingNumber)
- **도메인 모델 코드 예시**:

```java
// Shipment.java
public class Shipment {
    private Long shipmentId;
    private Long orderId;
    private String trackingNumber;
    private ShippingStatus status;

    // 생성자
    public Shipment(Long shipmentId, Long orderId) {
        this.shipmentId = shipmentId;
        this.orderId = orderId;
        this.status = ShippingStatus.READY;
    }

    // 배송 시작
    public void startShipping(String trackingNumber) {
        this.trackingNumber = trackingNumber;
        this.status = ShippingStatus.SHIPPED;
    }

    // 배송 완료
    public void completeShipping() {
        this.status = ShippingStatus.DELIVERED;
    }

    // Getter, Setter 생략
}
```

### 컨텍스트 간 관계

- **주문 처리 컨텍스트**는 **상품 관리 컨텍스트**의 제품 정보를 읽기 전용으로 사용합니다. 두 컨텍스트는 서로 독립적인 모델을 가지며, 필요한 데이터만 API 호출 등을 통해 가져옵니다.
- **배송 관리 컨텍스트**는 **주문 처리 컨텍스트**에서 발생하는 주문 완료 이벤트를 구독하여 배송을 시작합니다.

#### 컨텍스트 간 통신 예시

**이벤트 발행과 구독을 통한 비동기 통신을 활용하여 컨텍스트 간 결합도를 낮춥니다.**

```java
// OrderService.java (주문 처리 컨텍스트)
public class OrderService {
    private EventPublisher eventPublisher;

    public void placeOrder(Order order) {
        // 주문 저장 로직
        // ...

        // 주문 완료 이벤트 발행
        OrderPlacedEvent event = new OrderPlacedEvent(order.getOrderId());
        eventPublisher.publish(event);
    }
}

// OrderPlacedEvent.java
public class OrderPlacedEvent {
    private Long orderId;

    public OrderPlacedEvent(Long orderId) {
        this.orderId = orderId;
    }

    // Getter
    public Long getOrderId() {
        return orderId;
    }
}
```

```java
// ShipmentService.java (배송 관리 컨텍스트)
public class ShipmentService {
    public void handleOrderPlacedEvent(OrderPlacedEvent event) {
        // 주문 ID로 배송 생성
        Shipment shipment = new Shipment(generateShipmentId(), event.getOrderId());
        shipmentRepository.save(shipment);
    }

    private Long generateShipmentId() {
        // Shipment ID 생성 로직
        return System.currentTimeMillis();
    }
}
```

위의 예시에서는 **이벤트 주도 아키텍처**를 통해 주문 처리 컨텍스트에서 주문이 완료되면 주문 완료 이벤트를 발행하고, 배송 관리 컨텍스트에서 이 이벤트를 구독하여 배송을 처리합니다. 이를 통해 컨텍스트 간의 강한 결합을 피하고, 각 컨텍스트가 독립적으로 동작할 수 있도록 합니다.

## 바운디드 컨텍스트 적용 시 고려 사항

- **명확한 경계 정의**: 컨텍스트의 책임과 범위를 명확히 하여 혼란을 방지합니다.
- **모델의 독립성 유지**: 각 컨텍스트의 도메인 모델은 독립적으로 관리됩니다.
- **통합 전략 수립**: 컨텍스트 간 데이터 교환 및 의존성을 관리하기 위한 전략이 필요합니다.
- **팀 협업 강화**: 컨텍스트 간 의존성이 있는 경우, 팀 간의 원활한 의사소통이 중요합니다.
- **변경 관리**: 한 컨텍스트의 변경이 다른 컨텍스트에 미치는 영향을 최소화하도록 설계합니다.

## 바운디드 컨텍스트와 마이크로서비스

- **연관성**: 바운디드 컨텍스트는 마이크로서비스의 경계를 결정하는 데 유용한 가이드가 됩니다.
- **차이점**: 바운디드 컨텍스트는 도메인 모델링의 개념이고, 마이크로서비스는 시스템 아키텍처에 대한 구현 방식입니다.
- **시너지 효과**: 바운디드 컨텍스트를 기반으로 마이크로서비스를 설계하면 도메인 모델의 일관성을 유지하면서 확장성과 유연성을 확보할 수 있습니다.

## 결론

바운디드 컨텍스트는 복잡한 도메인을 효과적으로 관리하고, 모델의 명확성과 일관성을 유지하는 데 핵심적인 역할을 합니다. Java 코드를 통해 살펴본 예시처럼, 각 컨텍스트는 독립적인 도메인 모델과 로직을 가지며, 필요에 따라 이벤트나 API 등을 통해 컨텍스트 간 통신을 수행합니다. 이를 통해 개발 팀은 도메인의 복잡성을 줄이고, 변화에 유연하게 대응하며, 고품질의 소프트웨어를 개발할 수 있습니다. 바운디드 컨텍스트를 올바르게 적용하기 위해서는 도메인에 대한 깊은 이해와 팀 간의 원활한 협업이 필요합니다.