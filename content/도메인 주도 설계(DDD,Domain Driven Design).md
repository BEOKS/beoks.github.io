## 소개

**도메인 주도 설계(Domain-Driven Design, DDD)** 는 애플리케이션의 핵심 도메인에 주요 초점을 맞추는 소프트웨어 개발 접근 방식입니다. 2003년 에릭 에반스(Eric Evans)가 "도메인 주도 설계: 소프트웨어의 복잡성을 해결하기"라는 책에서 소개한 DDD는 핵심 비즈니스 개념의 진화하는 **모델과 구현을 연결함**으로써 복잡한 도메인을 다루기 위한 프레임워크를 제공합니다.

이 가이드에서는 DDD가 특별한 이유, 언제 사용해야 하는지, 그리고 프로젝트에서 핵심 패턴과 원칙을 어떻게 구현할 수 있는지 알아보겠습니다.

## 도메인 주도 설계란 무엇인가?

도메인 주도 설계의 핵심은 기술 전문가와 도메인 전문가 사이에 **공유된 이해를 만들어 복잡한 문제를 해결**하는 것입니다. 데이터베이스 테이블, UI 컴포넌트, 시스템 통합에 먼저 집중하는 대신, DDD는 팀이 **비즈니스 도메인과 규칙, 프로세스, 로직을 모델링**하도록 권장합니다.

"도메인"은 소프트웨어가 해결하고자 하는 [[주제영역(Subject Area)]]을 의미합니다. 전자상거래 애플리케이션의 경우, 도메인은 쇼핑 카트, 제품 카탈로그, 주문 처리와 같은 개념을 포함할 수 있습니다. 의료 시스템의 경우, 환자 기록, 치료 계획, 청구 프로세스를 포함할 수 있습니다.

## DDD의 핵심 개념

### 유비쿼터스 언어(Ubiquitous Language)

DDD에서 가장 강력한 개념 중 하나는 유비쿼터스 언어입니다. 이는 개발자, 도메인 전문가, 이해관계자 등 모든 팀원이 공유하는 공통 어휘입니다. 이 언어는 토론, 문서, 심지어 코드 자체에서도 사용됩니다.

예를 들어, 도메인 전문가가 도서관 책에 "보류(hold) 걸기"에 대해 이야기한다면, 코드는 "상태 플래그" 또는 "예약 마커"와 같은 개발자 중심 용어 대신 "보류(holds)"라는 이름의 클래스와 메서드로 이를 반영해야 합니다.

### 경계 지어진 컨텍스트(Bounded Contexts)

실제 도메인은 단일하고 일관된 시스템으로 모델링하기에는 너무 크고 복잡한 경우가 많습니다. DDD는 도메인을 경계 지어진 컨텍스트로 나누어 이 문제를 해결합니다. 이는 특정 모델이 적용되는 명시적 경계입니다.

각 경계 지어진 컨텍스트는 자체 유비쿼터스 언어를 가지며, 동일한 실세계 엔티티를 다르게 표현할 수 있습니다. 예를 들어, 판매 컨텍스트의 "고객(Customer)"은 지원 컨텍스트의 "고객(Customer)"과 다른 속성을 가질 수 있습니다.

### 컨텍스트 맵(Context Maps)

컨텍스트 맵은 서로 다른 경계 지어진 컨텍스트 간의 관계를 정의합니다. 이는 팀이 컨텍스트가 어떻게 상호작용하고 통신하는지 이해하는 데 도움이 되며, 서로 다른 모델 간의 번역이나 팀 책임과 같은 문제를 해결합니다.

### 구성 요소(Building Blocks)

DDD는 도메인 모델을 구현하기 위한 여러 전술적 패턴을 제공합니다:

1. **엔티티(Entities)**: 시간이 지남에 따라 속성이 변할 수 있는, 정체성으로 정의되는 객체입니다(예: 고유 ID를 가진 고객).

2. **값 객체(Value Objects)**: 정체성 없이 속성으로 정의되는, 불변의 객체입니다(예: 돈, 주소).

3. **애그리게이트(Aggregates)**: 단일 단위로 취급되는 관련 엔티티와 값 객체의 클러스터로, 진입점 역할을 하는 지정된 루트 엔티티가 있습니다(예: 주문라인이 있는 주문).

4. **리포지토리(Repositories)**: 애그리게이트를 검색하고 저장하는 메커니즘입니다.

5. **도메인 서비스(Domain Services)**: 특정 엔티티나 값 객체에 자연스럽게 속하지 않지만 도메인의 일부인 작업입니다(예: 결제 처리 서비스).

6. **도메인 이벤트(Domain Events)**: 도메인 전문가가 관심을 갖는 이벤트입니다(예: 주문 완료, 결제 수신).

## 전략적 vs 전술적 DDD

DDD는 종종 두 가지 측면으로 나뉩니다:

**전략적 DDD**는 큰 그림에 초점을 맞춥니다: 경계 지어진 컨텍스트 정의, 유비쿼터스 언어 확립, 컨텍스트 맵 생성 등입니다. 이는 대규모 시스템과 팀을 조직하는 데 도움이 되어, 올바른 방식으로 올바른 문제를 해결하도록 보장합니다.

**전술적 DDD**는 위에서 언급한 구현 패턴을 다룹니다: 엔티티, 값 객체, 애그리게이트 등입니다. 이는 코드에서 도메인 모델을 표현하는 구체적인 방법을 제공합니다.

## DDD 구현: 실용적인 예시

온라인 서점 애플리케이션을 구축한다고 상상해 봅시다. DDD를 어떻게 적용할 수 있는지 알아보겠습니다:

### 1. 유비쿼터스 언어 확립

도메인 전문가(서점 매니저, 직원)와 함께 작업하며 다음과 같은 용어를 개발합니다:
- 카탈로그(Catalog): 이용 가능한 모든 책의 컬렉션
- 재고(Inventory): 보유 중인 실제 책
- 예약(Reservation): 고객을 위해 책을 따로 보관하는 것
- 백오더(Backorder): 재고가 없는 책에 대한 고객 주문

### 2. 경계 지어진 컨텍스트 식별

우리의 서점에는 여러 경계 지어진 컨텍스트가a 있을 수 있습니다:
- 카탈로그 컨텍스트(Catalog Context): 책 정보 관리
- 재고 컨텍스트(Inventory Context): 실제 책 추적
- 주문 컨텍스트(Ordering Context): 고객 주문 처리
- 고객 컨텍스트(Customer Context): 고객 계정 관리

### 3. 컨텍스트 맵 생성

컨텍스트 간의 관계를 정의합니다. 예를 들어:
- 주문 컨텍스트는 카탈로그 컨텍스트의 정보를 소비합니다
- 재고 컨텍스트는 재고가 변경될 때 카탈로그 컨텍스트를 업데이트합니다
- 고객 컨텍스트는 주문 컨텍스트에서 고객 정보를 위해 사용됩니다

### 4. 구성 요소를 사용한 구현

주문 컨텍스트에서는 다음과 같이 만들 수 있습니다:

```csharp
// 엔티티(Entity)
public class Order
{
    public Guid Id { get; private set; }
    private List<OrderLine> _orderLines = new List<OrderLine>();
    public CustomerId CustomerId { get; private set; }
    public OrderStatus Status { get; private set; }
    
    // 도메인 동작
    public void AddBook(BookId bookId, int quantity)
    {
        // 도메인 로직
    }
    
    public void PlaceOrder()
    {
        // 도메인 로직, 잠재적으로 이벤트 발생
        Status = OrderStatus.Placed;
        DomainEvents.Raise(new OrderPlacedEvent(Id));
    }
}

// 값 객체(Value Object)
public class Money
{
    public decimal Amount { get; }
    public string Currency { get; }
    
    public Money(decimal amount, string currency)
    {
        Amount = amount;
        Currency = currency;
    }
    
    public Money Add(Money other)
    {
        if (Currency != other.Currency)
            throw new InvalidOperationException("다른 통화는 더할 수 없습니다");
            
        return new Money(Amount + other.Amount, Currency);
    }
}

// 리포지토리(Repository)
public interface IOrderRepository
{
    Order GetById(Guid id);
    void Save(Order order);
}

// 도메인 서비스(Domain Service)
public class OrderProcessingService
{
    private readonly IOrderRepository _orderRepository;
    private readonly IPaymentService _paymentService;
    private readonly IInventoryService _inventoryService;
    
    public void ProcessOrder(Guid orderId)
    {
        var order = _orderRepository.GetById(orderId);
        
        // Order 엔티티에 속하지 않는 도메인 로직
        var paymentResult = _paymentService.ProcessPayment(order);
        var inventoryResult = _inventoryService.ReserveItems(order);
        
        // 결과로 주문 업데이트
    }
}
```

## DDD를 언제 사용해야 하는가?

도메인 주도 설계는 특정 시나리오에서 빛을 발하지만, 다른 경우에는 과도할 수 있습니다:

**DDD 사용을 고려해야 할 때:**
- 도메인이 많은 비즈니스 규칙을 가진 복잡한 경우
- 기술 전문가와 도메인 전문가 간의 긴밀한 협업이 필요한 경우
- 프로젝트가 장기간에 걸쳐 진화할 예정인 경우
- 비즈니스 로직이 기술적 우려보다 더 중요한 경우

**DDD가 최선의 선택이 아닐 수 있는 경우:**
- 도메인이 단순하고 직관적인 경우
- 애플리케이션이 주로 CRUD 기반인 경우
- 단기 또는 개념 증명용 애플리케이션을 구축하는 경우
- 기술적 우려(성능이나 통합 같은)가 비즈니스 로직보다 중요한 경우

## 흔한 도전과 함정

### 1. 단순한 도메인의 과도한 엔지니어링

모든 애플리케이션이 복잡한 도메인 모델을 필요로 하는 것은 아닙니다. 실용적이 되어 특정 상황에 가치를 더하는 DDD 패턴만 적용하세요.

### 2. 유비쿼터스 언어 무시

많은 팀이 기술적 패턴에 집중하지만 도메인 전문가와 공유 언어를 개발하고 유지하는 것의 중요성을 잊곤 합니다.

### 3. 경계 지어진 컨텍스트 잘못 식별

컨텍스트 경계를 너무 넓게 또는 너무 좁게 그리면 비즈니스 현실과 일치하지 않는 모델이 생길 수 있습니다.

### 4. 기술적 우려가 모델을 주도하도록 허용

흔한 실수는 필수적인 비즈니스 개념을 포착하는 대신, 데이터베이스 스키마나 UI 요구사항이 도메인 모델을 지시하도록 허용하는 것입니다.

## DDD와 현대 아키텍처

도메인 주도 설계는 현대 아키텍처 접근 방식과 잘 맞습니다:

### 마이크로서비스(Microservices)

경계 지어진 컨텍스트는 잠재적 마이크로서비스 경계를 식별하는 자연스러운 방법을 제공합니다. 각 마이크로서비스는 통신을 위한 잘 정의된 인터페이스와 함께 특정 경계 지어진 컨텍스트를 구현할 수 있습니다.

### 이벤트 소싱(Event Sourcing)

도메인 이벤트는 애플리케이션의 상태가 일련의 이벤트에 의해 결정되는 이벤트 소싱과 자연스럽게 어울립니다.

### CQRS(Command Query Responsibility Segregation)

DDD의 명확한 경계와 관심사 분리에 대한 초점은 읽기 및 쓰기 작업을 분리하는 CQRS와 잘 일치합니다.

## DDD를 위한 도구 및 자원

### 모델링 도구
- 이벤트 스토밍(Event Storming) 워크숍
- 컨텍스트 매핑 기법
- 아키텍처 시각화를 위한 C4 모델

### 테스팅 접근 방식
- 행동 주도 개발(Behavior-Driven Development, BDD)
- 도메인 특화 테스팅 프레임워크

### 책과 자원
- "도메인 주도 설계" - 에릭 에반스
- "도메인 주도 설계 구현하기" - 본 버논
- "도메인 주도 설계 핵심" - 본 버논

## 결론

도메인 주도 설계는 단순한 기술적 패턴 모음이 아니라, 비즈니스 도메인을 중심에 두는 소프트웨어 개발에 대한 사고 방식입니다. 기술 전문가와 도메인 전문가 간의 공유된 이해를 만들어냄으로써, DDD는 팀이 실제 비즈니스 문제를 정확하게 반영하고 해결하는 소프트웨어를 구축하도록 도와줍니다.

학습과 협업에 투자가 필요하지만, 비즈니스 가치를 제공하는 유지 관리 가능하고 진화하는 소프트웨어 측면에서의 보상은 DDD를 복잡한 도메인을 다루는 강력한 접근 방식으로 만듭니다.

DDD는 전부 아니면 전무의 명제가 아님을 기억하세요. 유비쿼터스 언어 개발이나 경계 지어진 컨텍스트 식별과 같은 일부 원칙만 적용하더라도 소프트웨어 개발 프로세스에 상당한 이점을 가져올 수 있습니다.