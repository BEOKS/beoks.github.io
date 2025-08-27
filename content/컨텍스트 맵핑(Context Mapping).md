## 컨텍스트 맵핑이란?

컨텍스트 맵핑은 여러 [[바운디드 컨텍스트(Bounded Context)]] 간의 **관계를 시각화하고 문서화하는 기술**입니다. 각 바운디드 컨텍스트는 자체적인 모델, 언어, 경계를 가지고 있으며, 이들이 어떻게 상호작용하고 통합되는지 명확하게 표현하는 것이 컨텍스트 맵핑의 목적입니다.

## 컨텍스트 맵핑의 패턴들
[[도메인 주도 설계(DDD,Domain Driven Design)]]에서는 여러 바운디드 컨텍스트 간의 관계를 설명하기 위한 다양한 패턴을 제시합니다. 각 패턴은 팀 간의 협력 방식, 기술적 통합 방식, 그리고 조직적 관계를 반영합니다.

### 1. 공유 커널(Shared Kernel)

두 팀이 도메인 모델의 일부를 공유하기로 합의하는 관계입니다. 공유되는 부분은 양쪽 팀 모두에게 중요하며, 이 부분에 대한 변경은 양팀의 동의가 필요합니다.

```
TeamA <--(Shared Kernel)--> TeamB
```

**장점**:
- 중복 작업 감소
- 통합 간소화

**단점**:
- 변경에 대한 협의 필요로 유연성 감소
- 상호 의존성 증가

**예시**: 주문 시스템과 배송 시스템이 공통으로 사용하는 고객 정보 모델

### 2. 고객-공급자(Customer-Supplier)

한 컨텍스트(공급자)가 다른 컨텍스트(고객)에 서비스를 제공하는 관계입니다. 공급자는 고객의 요구사항을 충족시키기 위해 노력하지만, 최종 결정권은 공급자에게 있습니다.

```
CustomerTeam ---(Downstream)---> SupplierTeam
```

**특징**:
- 명확한 의존성 방향
- 공급자는 고객의 요구를 고려해야 함
- 계획과 일정 조정 필요

**예시**: 결제 시스템(공급자)과 주문 시스템(고객) 간의 관계

### 3. 순응자(Conformist)

한 컨텍스트가 다른 컨텍스트의 모델을 그대로 따르는 경우입니다. 주로 상류 팀이 하류 팀의 요구를 고려할 동기가 없을 때 발생합니다.

```
UpstreamTeam ---(Model)--> ConformistTeam
```

**특징**:
- 상류팀의 모델을 그대로 수용
- 번역 비용 없음
- 하류팀의 자율성 제한

**예시**: 서드파티 API를 그대로 사용하는 경우

### 4. 부패 방지 계층(Anticorruption Layer, ACL)

외부 시스템이나 레거시 시스템과 통합할 때, 자신의 모델을 보호하기 위해 중간에 변환 계층을 두는 패턴입니다.

```
OurSystem ---(ACL)---> LegacySystem
```

**특징**:
- 외부/레거시 시스템의 영향 최소화
- 자체 모델의 순수성 유지
- 추가 개발 비용 발생

**코드 예시**:

```java
// 외부 시스템의 사용자 정보
class ExternalUser {
    private String userId;
    private String name;
    private String addr;
    
    // getters & setters
}

// 우리 시스템의 사용자 모델
class User {
    private UUID id;
    private String fullName;
    private Address address;
    
    // getters & setters
}

// ACL - 번역 담당
class UserTranslator {
    public User translateFromExternal(ExternalUser externalUser) {
        User user = new User();
        user.setId(UUID.fromString(externalUser.getUserId()));
        user.setFullName(externalUser.getName());
        user.setAddress(new Address(externalUser.getAddr()));
        return user;
    }
}
```

### 5. 오픈 호스트 서비스(Open Host Service)와 발행된 언어(Published Language)

서비스를 공개 API 형태로 제공하고, 잘 정의된 프로토콜을 통해 통합을 단순화하는 패턴입니다.

```
Clients ---(Published Language)---> OpenHostService
```

**특징**:
- 공개 API 통해 서비스 제공
- 표준화된 통합 프로토콜
- 다수의 클라이언트 지원

**예시**: REST API, GraphQL 등을 통한 서비스 제공

### 6. 분리된 길(Separate Ways)

통합의 이점보다 분리의 이점이 더 클 때, 컨텍스트 간 통합을 최소화하거나 없애는 패턴입니다.

```
SystemA   SystemB
  |         |
(최소한의 통합 또는 없음)
```

**특징**:
- 컨텍스트 간 결합도 최소화
- 개발 자율성 극대화
- 중복 가능성 있음

**예시**: 독립적으로 운영되는 마케팅 시스템과 인사 시스템

## 컨텍스트 맵 작성하기

컨텍스트 맵은 다양한 방식으로 표현할 수 있으며, 일반적으로 다음과 같은 요소를 포함합니다:

1. **바운디드 컨텍스트**: 각 컨텍스트를 표현하는 도형(보통 원이나 사각형)
2. **관계**: 컨텍스트 간 관계를 나타내는 선이나 화살표
3. **패턴 명시**: 각 관계가 어떤 패턴을 따르는지 표시
4. **팀 정보**: 각 컨텍스트를 담당하는 팀 정보

!Pasted image 20250225222205.png

## 컨텍스트 맵핑의 실제 적용

컨텍스트 맵핑은 단순한 다이어그램 이상의 가치를 제공합니다. 이를 통해 다음과 같은 이점을 얻을 수 있습니다:

### 1. 전략적 설계 도구

컨텍스트 맵핑은 시스템 설계의 전략적 결정을 내리는 데 도움이 됩니다. 어느 부분을 통합하고 어느 부분을 분리할지, 어떤 통합 패턴을 사용할지 결정하는 과정에서 비즈니스와 기술적 고려사항을 균형 있게 반영할 수 있습니다.

### 2. 의사소통 도구

컨텍스트 맵은 개발자, 설계자, 제품 관리자 등 다양한 이해관계자 간의 의사소통을 돕습니다. 전체 시스템의 구조와 각 부분의 관계를 시각적으로 보여줌으로써 복잡한 시스템에 대한 공통된 이해를 형성할 수 있습니다.

### 3. 변경 관리 도구

시스템이 진화함에 따라 컨텍스트 맵도 함께 업데이트되어야 합니다. 이 과정에서 변경의 영향 범위를 파악하고, 필요한 협의와 조정을 계획할 수 있습니다.

## 실전 적용 사례: 이커머스 시스템

실제 이커머스 시스템에서 컨텍스트 맵핑을 적용한 사례를 살펴보겠습니다:

### 바운디드 컨텍스트 식별

- **상품 카탈로그**: 상품 정보, 카테고리, 검색 기능
- **주문 관리**: 장바구니, 주문 처리, 주문 상태 관리
- **결제 처리**: 결제 수단, 거래 처리, 환불
- **배송 관리**: 배송 추적, 배송 상태, 배송 옵션
- **고객 관리**: 고객 정보, 계정 관리, 로그인
- **재고 관리**: 재고 수준, 입고, 출고 관리

### 관계 패턴 결정

1. **상품 카탈로그 ↔ 주문 관리**: 공유 커널
   - 두 컨텍스트 모두 상품 정보를 핵심적으로 다루므로 공유

2. **주문 관리 → 결제 처리**: 고객-공급자
   - 주문 시스템이 결제 시스템의 서비스를 요청

3. **주문 관리 → 배송 관리**: 고객-공급자
   - 주문 완료 후 배송 정보 전달

4. **배송 관리 → 레거시 재고 시스템**: 부패 방지 계층
   - 오래된 재고 시스템과 통합하면서 현대적인 배송 시스템 보호

5. **고객 관리 → 전체 시스템**: 오픈 호스트 서비스
   - 고객 정보를 표준화된 API로 제공

### 컨텍스트 맵 구현 방안

```java
// 주문 관리와 결제 처리 간의 고객-공급자 관계 구현 예시

// 주문 관리 컨텍스트
public class OrderService {
    private final PaymentGateway paymentGateway;
    
    public OrderService(PaymentGateway paymentGateway) {
        this.paymentGateway = paymentGateway;
    }
    
    public Order placeOrder(Cart cart, Customer customer) {
        Order order = createOrderFromCart(cart);
        
        // 결제 서비스 호출 (Customer-Supplier 패턴)
        PaymentResult result = paymentGateway.processPayment(
            order.getId(),
            order.getTotalAmount(),
            customer.getPaymentInfo()
        );
        
        if (result.isSuccessful()) {
            order.markAsPaid();
            // 추가 처리
        }
        
        return order;
    }
}

// 결제 처리 컨텍스트의 인터페이스 (공급자)
public interface PaymentGateway {
    PaymentResult processPayment(String orderId, Money amount, PaymentInfo paymentInfo);
}

// 실제 구현체는 결제 컨텍스트에 존재
```

## 컨텍스트 맵핑 작성 시 고려사항

### 1. 조직 구조 반영

컨텍스트 맵은 기술적 구조뿐만 아니라 조직 구조도 반영해야 합니다. 콘웨이의 법칙(Conway's Law)에 따르면, 시스템 설계는 조직의 의사소통 구조를 반영하게 됩니다. 따라서 팀 구조와 의사소통 방식을 고려하여 컨텍스트 맵을 작성해야 합니다.

### 2. 현실적인 통합 전략

이상적인 설계보다 현실적으로 구현 가능한 통합 전략을 선택하는 것이 중요합니다. 레거시 시스템, 기술적 제약, 리소스 제한 등을 고려하여 실행 가능한 방향을 설정해야 합니다.

### 3. 진화하는 문서로 관리

컨텍스트 맵은 한 번 작성하고 끝나는 것이 아니라, 시스템과 함께 진화하는 살아있는 문서로 관리되어야 합니다. 정기적인 리뷰와 업데이트를 통해 현재 시스템의 상태를 정확히 반영하도록 유지해야 합니다.

## 결론

컨텍스트 맵핑은 DDD의 핵심 도구 중 하나로, 복잡한 시스템의 구조와 통합 지점을 이해하고 관리하는 데 큰 도움이 됩니다. 각 바운디드 컨텍스트의 경계를 명확히 하고, 컨텍스트 간의 관계를 적절한 패턴으로 설계함으로써 복잡성을 관리하고 유연한 시스템을 구축할 수 있습니다.

효과적인 컨텍스트 맵핑을 위해서는 기술적 측면뿐만 아니라 조직적, 전략적 측면도 고려해야 하며, 이를 통해 비즈니스 도메인의 복잡성을 효과적으로 다룰 수 있는 시스템 구조를 설계할 수 있습니다.

## 참고 자료

- Eric Evans, "Domain-Driven Design: Tackling Complexity in the Heart of Software"
- Vaughn Vernon, "Implementing Domain-Driven Design"
- Alberto Brandolini, "Strategic Domain-Driven Design"