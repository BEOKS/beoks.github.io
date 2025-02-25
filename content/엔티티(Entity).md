## 서론

데이터 모델링에서 '엔티티(Entity)'는 가장 기본적이면서도 핵심적인 개념입니다. 소프트웨어 개발과 데이터베이스 설계에서 현실 세계의 객체나 개념을 모델링하는 방법을 이해하는 것은 효율적인 시스템 구축의 첫걸음입니다. 이 글에서는 엔티티의 개념부터 실제 구현까지 깊이 있게 살펴보겠습니다.

## 엔티티란 무엇인가?

엔티티는 실세계에 존재하는 **구분 가능한 객체나 개념**을 데이터 모델에서 표현한 것입니다. 더 구체적으로, 엔티티는 다음과 같은 특성을 가집니다:

1. **식별 가능성**: 다른 엔티티와 구별될 수 있는 고유한 식별자를 가집니다.
2. **속성 보유**: 해당 객체나 개념의 특성을 설명하는 속성(Attribute)들을 가집니다.
3. **관계 형성 능력**: 다른 엔티티들과 관계(Relationship)를 맺을 수 있습니다.
4. **비즈니스 의미**: 비즈니스 도메인 내에서 **의미 있는 개념**을 나타냅니다.

예를 들어, 은행 시스템에서 '고객', '계좌', '거래' 등은 모두 엔티티가 될 수 있습니다. 각각은 고유하게 식별 가능하고, 자신만의 속성을 가지며, 서로 관계를 맺고 있습니다.

## 엔티티의 유형

### 1. 물리적 엔티티(Physical Entity)
실제 물리적 세계에 존재하는 객체를 나타냅니다. 
- 예: 고객, 제품, 건물, 장비

### 2. 개념적 엔티티(Conceptual Entity)
물리적으로 존재하지는 않지만 비즈니스 프로세스에서 중요한 개념을 나타냅니다.
- 예: 주문, 계약, 예약, 정책

### 3. 이벤트 엔티티(Event Entity)
특정 시점에 발생하는 이벤트나 트랜잭션을 나타냅니다.
- 예: 판매, 입금, 출금, 배송

### 4. 연관 엔티티(Associative Entity)
다대다(Many-to-Many) 관계를 해소하기 위해 사용되는 엔티티입니다.
- 예: 학생-과목 관계에서의 '수강신청' 엔티티

## 엔티티 모델링 과정

### 1. 엔티티 식별
비즈니스 요구사항을 분석하여 중요한 엔티티들을 식별합니다. 명사형 단어들이 주로 엔티티 후보가 됩니다.

### 2. 속성 정의
각 엔티티가 가지는 속성들을 정의합니다. 속성은 엔티티의 특성을 설명하는 데이터 요소입니다.

```
엔티티: 고객(Customer)
속성:
- 고객ID (CustomerID): 고객을 식별하는 고유 번호
- 이름 (Name): 고객의 이름
- 생년월일 (BirthDate): 고객의 생년월일
- 이메일 (Email): 고객의 이메일 주소
- 전화번호 (Phone): 고객의 전화번호
- 가입일 (RegistrationDate): 고객이 서비스에 가입한 날짜
```

### 3. 식별자 결정
각 엔티티 인스턴스를 고유하게 식별할 수 있는 식별자(Identifier)를 결정합니다. 이는 주키(Primary Key)가 됩니다.

**식별자의 유형**:
- **자연 키(Natural Key)**: 업무적으로 이미 존재하는 속성(예: 주민등록번호)
- **대리 키(Surrogate Key)**: 시스템에서 인위적으로 생성한 키(예: 자동증가 ID)

### 4. [[엔티티 관계(Entity Relationship)|관계 정의]]
엔티티들 간의 관계를 정의합니다. 관계는 다음과 같은 유형으로 분류됩니다:

- **일대일(1:1)**: 한 엔티티의 한 인스턴스가 다른 엔티티의 정확히 한 인스턴스와 관련됨
- **일대다(1:N)**: 한 엔티티의 한 인스턴스가 다른 엔티티의 여러 인스턴스와 관련됨
- **다대다(M:N)**: 한 엔티티의 여러 인스턴스가 다른 엔티티의 여러 인스턴스와 관련됨

### 5. 무결성 규칙 정의
엔티티의 데이터 무결성을 보장하기 위한 규칙들을 정의합니다:

- **개체 무결성(Entity Integrity)**: 모든 엔티티는 고유한 식별자를 가져야 함
- **참조 무결성(Referential Integrity)**: 관계를 맺는 엔티티 간의 데이터 일관성 유지
- **도메인 무결성(Domain Integrity)**: 속성 값이 정의된 도메인 내에 있어야 함

## 엔티티 표현 방법

### ER 다이어그램(Entity-Relationship Diagram)
엔티티와 그들 간의 관계를 시각적으로 표현하는 가장 일반적인 방법입니다.

```
[고객] ---- 1:N ---- [주문]
   |
   |---- 1:N ---- [주소]
```

### UML 클래스 다이어그램
객체지향 설계에서 엔티티를 클래스로 표현합니다.

```
+-------------------+
|     Customer      |
+-------------------+
| - customerID: UUID|
| - name: String    |
| - email: String   |
+-------------------+
| + placeOrder()    |
| + updateProfile() |
+-------------------+
         |
         | 1..*
         v
+-------------------+
|       Order       |
+-------------------+
```

## 엔티티의 실제 구현

### 관계형 데이터베이스에서의 구현

엔티티는 테이블로, 속성은 컬럼으로, 관계는 외래 키로 표현됩니다.

```sql
-- 고객 엔티티 테이블 생성
CREATE TABLE Customer (
    CustomerID UUID PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    BirthDate DATE,
    Email VARCHAR(100) UNIQUE,
    Phone VARCHAR(20),
    RegistrationDate DATE NOT NULL
);

-- 주문 엔티티 테이블 생성
CREATE TABLE Orders (
    OrderID UUID PRIMARY KEY,
    CustomerID UUID NOT NULL,
    OrderDate TIMESTAMP NOT NULL,
    TotalAmount DECIMAL(10,2) NOT NULL,
    Status VARCHAR(20) NOT NULL,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
);
```

### 객체지향 언어에서의 구현

Java 등의 객체지향 언어에서는 엔티티를 클래스로 구현합니다.

```java
@Entity
public class Customer {
    @Id
    @GeneratedValue
    private UUID customerId;
    
    @Column(nullable = false)
    private String name;
    
    private LocalDate birthDate;
    
    @Column(unique = true)
    private String email;
    
    private String phone;
    
    @Column(nullable = false)
    private LocalDate registrationDate;
    
    @OneToMany(mappedBy = "customer")
    private List<Order> orders;
    
    // 생성자, 게터, 세터, 비즈니스 메서드 등
}

@Entity
@Table(name = "Orders") // "Order"는 SQL 예약어라 다른 이름 사용
public class Order {
    @Id
    @GeneratedValue
    private UUID orderId;
    
    @ManyToOne
    @JoinColumn(name = "CustomerID", nullable = false)
    private Customer customer;
    
    @Column(nullable = false)
    private LocalDateTime orderDate;
    
    @Column(nullable = false)
    private BigDecimal totalAmount;
    
    @Column(nullable = false)
    private String status;
    
    // 생성자, 게터, 세터, 비즈니스 메서드 등
}
```

### NoSQL 데이터베이스에서의 구현

MongoDB와 같은 문서 지향 데이터베이스에서는 엔티티를 문서(Document)로 표현합니다.

```javascript
// 고객 엔티티 문서 예시
{
  "_id": ObjectId("507f1f77bcf86cd799439011"),
  "name": "홍길동",
  "birthDate": ISODate("1990-01-15T00:00:00Z"),
  "email": "hong@example.com",
  "phone": "010-1234-5678",
  "registrationDate": ISODate("2023-01-10T00:00:00Z"),
  "addresses": [
    {
      "type": "home",
      "street": "서울시 강남구 테헤란로 123",
      "zipCode": "06134"
    }
  ]
}

// 주문 엔티티 문서 예시
{
  "_id": ObjectId("507f191e810c19729de860ea"),
  "customerId": ObjectId("507f1f77bcf86cd799439011"),
  "orderDate": ISODate("2023-03-15T14:30:00Z"),
  "totalAmount": 50000,
  "status": "delivered",
  "items": [
    {
      "productId": ObjectId("507f191e810c19729de860eb"),
      "name": "스마트폰",
      "quantity": 1,
      "price": 50000
    }
  ]
}
```

## 엔티티 설계 시 고려사항

### 1. 정규화 수준
엔티티 설계 시 정규화 수준을 결정해야 합니다. 높은 정규화는 데이터 중복을 줄이지만, 조회 성능에 영향을 줄 수 있습니다.

### 2. 확장성
비즈니스 요구사항이 변경될 가능성을 고려하여 엔티티를 설계해야 합니다. 너무 경직된 설계는 변경 비용을 증가시킵니다.

### 3. 성능
엔티티 간의 관계와 속성 구성이 시스템 성능에 영향을 미칠 수 있습니다. 특히 자주 접근하는,엔티티나 복잡한 관계를 가진 엔티티는 성능 최적화를 고려해야 합니다.

### 4. 도메인 특성 반영
엔티티 설계는 해당 비즈니스 도메인의 특성을 정확히 반영해야 합니다. 도메인 전문가와의 협업이 중요합니다.

## 도메인 주도 설계(DDD)에서의 엔티티

도메인 주도 설계에서는 엔티티를 단순한 데이터 구조체가 아닌, 식별성과 수명주기를 가진 도메인 객체로 간주합니다.

### DDD 엔티티의 특징

1. **식별자에 의한 구별**: 속성이 변경되어도 동일한 엔티티로 인식됩니다.
2. **비즈니스 로직 포함**: 데이터뿐만 아니라 행위(behavior)도 포함합니다.
3. **불변식(Invariant) 유지**: 엔티티는 자신의 일관성과 유효성을 스스로 책임집니다.

```java
// DDD 스타일의 엔티티 예시
public class Customer {
    private final CustomerId id;
    private Name name;
    private Email email;
    private Set<Address> addresses;
    private CustomerStatus status;
    
    // 생성자
    private Customer(CustomerId id, Name name, Email email) {
        this.id = id;
        this.name = name;
        this.email = email;
        this.addresses = new HashSet<>();
        this.status = CustomerStatus.ACTIVE;
    }
    
    // 팩토리 메서드
    public static Customer create(Name name, Email email) {
        validateNewCustomer(name, email);
        return new Customer(new CustomerId(), name, email);
    }
    
    // 비즈니스 메서드
    public void changeEmail(Email newEmail) {
        // 이메일 변경 전 유효성 검사
        validateEmailChange(newEmail);
        this.email = newEmail;
    }
    
    public void addAddress(Address address) {
        if (addresses.size() >= 3) {
            throw new TooManyAddressesException("최대 3개의 주소만 등록 가능합니다.");
        }
        addresses.add(address);
    }
    
    public void deactivate() {
        if (this.status != CustomerStatus.ACTIVE) {
            throw new IllegalStateException("이미 비활성화된 고객입니다.");
        }
        this.status = CustomerStatus.INACTIVE;
    }
    
    // 유효성 검사 메서드
    private static void validateNewCustomer(Name name, Email email) {
        // 유효성 검사 로직
    }
    
    private void validateEmailChange(Email newEmail) {
        // 이메일 변경 유효성 검사 로직
    }
    
    // 게터 메서드 (필요한 경우에만)
    public CustomerId getId() {
        return id;
    }
    
    public CustomerStatus getStatus() {
        return status;
    }
    
    // 동등성 비교
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Customer customer = (Customer) o;
        return id.equals(customer.id);
    }
    
    @Override
    public int hashCode() {
        return id.hashCode();
    }
}
```

## 마이크로서비스에서의 엔티티 설계

마이크로서비스 아키텍처에서는 서비스 경계에 따라 엔티티가 분리되고 중복될 수 있습니다.

### 서비스별 독립적 엔티티 모델

각 마이크로서비스는 자신의 도메인 컨텍스트 내에서 필요한 엔티티만 정의하고 관리합니다. 이로 인해 동일한 실세계 객체가 서로 다른 서비스에서 다르게 모델링될 수 있습니다.

```java
// 고객 서비스의 고객 엔티티
@Entity
public class Customer {
    @Id
    private UUID id;
    private String name;
    private String email;
    private String phone;
    private boolean marketingConsent;
    private LocalDate registrationDate;
    // 마케팅, CRM 관련 속성들...
}

// 주문 서비스의 고객 엔티티 (축소된 버전)
@Entity
public class Customer {
    @Id
    private UUID id;
    private String name;
    private String deliveryAddress;
    private String billingAddress;
    // 주문 처리에 필요한 속성들만 포함...
}
```

### 서비스 간 엔티티 참조

마이크로서비스 간에는 직접적인 엔티티 참조 대신 식별자를 통한 참조나 이벤트 기반 통신을 사용합니다.

```java
// 주문 서비스의 주문 엔티티
@Entity
public class Order {
    @Id
    private UUID id;
    private UUID customerId;  // 직접 Customer 객체 참조가 아닌 ID만 참조
    private LocalDateTime orderDate;
    private OrderStatus status;
    
    @ElementCollection
    private List<OrderItem> items;
    
    // 메서드들...
}
```

## 결론

엔티티는 데이터 모델링의 기본 구성 요소로, 실세계 객체나 개념을 시스템 내에서 표현하는 방법입니다. 잘 설계된 엔티티는 시스템의 이해도를 높이고, 유지보수성을 개선하며, 비즈니스 요구사항의 변화에 유연하게 대응할 수 있게 합니다.

엔티티 설계는 단순히 데이터 구조를 정의하는 것을 넘어, 비즈니스 도메인에 대한 깊은 이해와 소프트웨어 아키텍처에 대한 고려가 필요한 창의적인 과정입니다. 개발자로서 엔티티 모델링에 시간과 노력을 투자하는 것은 장기적으로 높은 가치를 창출합니다.

## 참고 자료
- Database Design for Mere Mortals - Michael J. Hernandez
- Domain-Driven Design - Eric Evans
- Data Model Patterns - David C. Hay
- Clean Architecture - Robert C. Martin

## 연결 노트
- [[주제영역과 엔티티의 관계]]
- [[정규화와 데이터 모델링]]
- [[JPA와 엔티티 매핑]]
- [[도메인 주도 설계의 핵심 개념]]
- [[마이크로서비스 경계와 엔티티 분리]]