# @DataJpaTest 어노테이션

`@DataJpaTest`는 Spring Boot에서 제공하는 테스트 슬라이스 어노테이션으로, JPA 관련 컴포넌트만을 테스트 컨텍스트에 로드하여 효율적인 데이터 계층 테스트를 가능하게 합니다. 이 어노테이션은 JPA 리포지토리와 엔티티의 동작을 검증하는 데 특화되어 있으며, 전체 애플리케이션 컨텍스트를 로드하지 않아 빠른 테스트 실행이 가능합니다.

## @DataJpaTest의 역할

`@DataJpaTest`는 다음과 같은 특징을 가지고 있습니다:

1. **선택적 컴포넌트 로딩**: JPA 관련 빈만을 로드하여 테스트 실행 속도를 향상시킵니다
2. **자동 설정**: 테스트에 필요한 JPA 인프라를 자동으로 구성합니다
3. **트랜잭션 롤백**: 각 테스트 메서드가 끝날 때마다 자동으로 롤백됩니다
4. **인메모리 데이터베이스**: 기본적으로 H2와 같은 임베디드 데이터베이스를 사용합니다

## 자동 구성되는 컴포넌트

`@DataJpaTest`를 사용하면 다음 컴포넌트들이 자동으로 구성됩니다:

- **JPA EntityManager**: JPA의 핵심 인터페이스
- **Spring Data JPA Repositories**: 리포지토리 빈들
- **TestEntityManager**: 테스트 전용 EntityManager
- **DataSource**: 데이터베이스 연결
- **JdbcTemplate**: JDBC 접근을 위한 템플릿
- **임베디드 데이터베이스**: H2, Derby, HSQLDB 등

반면 다음과 같은 일반적인 Spring 컴포넌트들은 로드되지 않습니다:

- `@Component`, `@Service`, `@Controller` 빈들
- `@ConfigurationProperties` 빈들

## 기본 사용법

가장 기본적인 `@DataJpaTest` 사용 예시입니다:

```java
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.orm.jpa.TestEntityManager;

@DataJpaTest
class UserRepositoryTest {

    @Autowired
    private TestEntityManager entityManager;

    @Autowired
    private UserRepository userRepository;

    @Test
    void findByEmail_사용자가_존재할때_반환() {
        // given
        User user = new User("test@example.com", "테스트사용자");
        entityManager.persistAndFlush(user);

        // when
        User foundUser = userRepository.findByEmail("test@example.com");

        // then
        assertThat(foundUser).isNotNull();
        assertThat(foundUser.getEmail()).isEqualTo("test@example.com");
    }
}
```

## TestEntityManager 활용

`TestEntityManager`는 테스트에서 엔티티를 관리하기 위한 전용 도구입니다. 일반적인 `EntityManager`보다 테스트에 특화된 메서드들을 제공합니다:

```java
@DataJpaTest
class ProductRepositoryTest {

    @Autowired
    private TestEntityManager entityManager;

    @Autowired
    private ProductRepository productRepository;

    @Test
    void findByCategory_카테고리별_상품조회() {
        // given
        Product product1 = new Product("노트북", "전자제품");
        Product product2 = new Product("스마트폰", "전자제품");
        Product product3 = new Product("책상", "가구");
        
        entityManager.persist(product1);
        entityManager.persist(product2);
        entityManager.persist(product3);
        entityManager.flush();

        // when
        List<Product> electronics = productRepository.findByCategory("전자제품");

        // then
        assertThat(electronics).hasSize(2);
        assertThat(electronics).extracting(Product::getName)
                               .containsExactly("노트북", "스마트폰");
    }
}
```

## 데이터베이스 설정 커스터마이징

기본적으로 `@DataJpaTest`는 인메모리 데이터베이스를 사용하지만, 실제 데이터베이스를 사용하고 싶다면 `@AutoConfigureTestDatabase` 어노테이션으로 설정을 변경할 수 있습니다:

```java
@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class OrderRepositoryIntegrationTest {
    
    @Autowired
    private OrderRepository orderRepository;
    
    @Test
    void findRecentOrders_최근주문조회() {
        // 실제 데이터베이스를 사용한 테스트
    }
}
```

## 추가 컴포넌트 포함하기

`@DataJpaTest`는 기본적으로 JPA 관련 빈만 로드하지만, 때로는 추가적인 컴포넌트가 필요할 수 있습니다. 이런 경우 `@Import` 어노테이션을 사용할 수 있습니다:

```java
@DataJpaTest
@Import(AuditorAware.class)
class AuditableEntityTest {
    
    @Autowired
    private TestEntityManager entityManager;
    
    @Test
    void save_엔티티저장시_감사정보_자동설정() {
        // AuditorAware 빈이 필요한 테스트
    }
}
```

## JSON 테스트와의 결합

JPA 엔티티의 JSON 직렬화/역직렬화를 함께 테스트하려면 `@JsonComponent`를 추가로 포함할 수 있습니다:

```java
@DataJpaTest
class UserEntityJsonTest {
    
    @Autowired
    private TestEntityManager entityManager;
    
    @Autowired
    private JacksonTester<User> json;
    
    @Test
    void serialize_사용자엔티티_JSON변환() throws Exception {
        User user = new User("test@example.com", "테스트사용자");
        
        JsonContent<User> result = json.write(user);
        
        assertThat(result).extractingJsonPathStringValue("$.email")
                         .isEqualTo("test@example.com");
    }
}
```

## 트랜잭션 동작 이해

`@DataJpaTest`로 생성된 테스트는 기본적으로 트랜잭션 내에서 실행되며, 각 테스트 메서드가 완료되면 자동으로 롤백됩니다. 이는 테스트 간의 데이터 격리를 보장합니다:

```java
@DataJpaTest
class TransactionRollbackTest {
    
    @Autowired
    private UserRepository userRepository;
    
    @Test
    void test1_사용자생성() {
        userRepository.save(new User("user1@test.com", "사용자1"));
        assertThat(userRepository.count()).isEqualTo(1);
    }
    
    @Test
    void test2_이전테스트데이터없음() {
        // 이전 테스트의 데이터는 롤백되어 존재하지 않음
        assertThat(userRepository.count()).isEqualTo(0);
    }
}
```

## 슬라이스 테스트의 장점

`@DataJpaTest`와 같은 슬라이스 테스트는 다음과 같은 장점을 제공합니다:

### 빠른 실행 속도
전체 애플리케이션 컨텍스트를 로드하지 않아 테스트 실행 시간이 현저히 단축됩니다. 이는 [[테스트 피드백 루프]]를 빠르게 만들어 개발 생산성을 향상시킵니다.

### 격리된 테스트 환경
데이터 계층만을 대상으로 하는 테스트이므로 다른 계층의 복잡성에 영향받지 않습니다. 이를 통해 [[단위 테스트의 원칙]]을 준수할 수 있습니다.

### 명확한 테스트 범위
JPA 관련 기능만을 테스트하므로 테스트의 의도와 범위가 명확해집니다.

## 실제 프로젝트 적용 사례

실제 스프링 부트 프로젝트에서 `@DataJpaTest`는 다음과 같은 상황에서 활용됩니다:

### 1. 커스텀 쿼리 메서드 검증

```java
@DataJpaTest
class OrderRepositoryTest {
    
    @Autowired
    private OrderRepository orderRepository;
    
    @Test
    void findByStatusAndDateRange_상태와기간으로_주문조회() {
        // 복잡한 쿼리 메서드의 동작 검증
    }
}
```

### 2. JPA 어노테이션 동작 확인

```java
@DataJpaTest
class EntityMappingTest {
    
    @Test
    void cascade_연관관계_캐스케이드_동작확인() {
        // @OneToMany, @CascadeType 등의 동작 검증
    }
}
```

### 3. 데이터베이스 제약조건 테스트

```java
@DataJpaTest
class ValidationTest {
    
    @Test
    void save_필수값누락시_예외발생() {
        // @NotNull, @Column(unique=true) 등의 제약조건 검증
    }
}
```

## 주의사항

`@DataJpaTest` 사용 시 다음 사항들을 주의해야 합니다:

### Configuration 클래스 분리
JPA Auditing과 같은 설정이 메인 애플리케이션 클래스에 포함되어 있으면 슬라이스 테스트에서 문제가 될 수 있습니다. 이런 경우 별도의 [[설정 클래스 분리 패턴]]을 적용해야 합니다.

### 테스트 데이터 관리
인메모리 데이터베이스의 특성을 고려하여 테스트 데이터를 적절히 관리해야 합니다. [[테스트 데이터 관리 전략]]을 참고하여 일관된 접근 방식을 유지하는 것이 중요합니다.

### 실제 환경과의 차이
인메모리 데이터베이스와 실제 운영 데이터베이스 간의 SQL 방언 차이를 고려해야 합니다. 중요한 쿼리의 경우 [[통합 테스트]]를 통해 실제 데이터베이스에서도 검증하는 것이 좋습니다.

## 결론

`@DataJpaTest`는 Spring Boot에서 제공하는 강력한 테스트 도구로, JPA 기반의 데이터 계층을 효율적으로 테스트할 수 있게 해줍니다. 빠른 실행 속도와 격리된 테스트 환경을 제공하여 개발자가 데이터 계층의 로직에 집중할 수 있도록 도와줍니다.

적절한 테스트 전략과 함께 사용한다면, 안정적이고 신뢰할 수 있는 데이터 계층 구현이 가능합니다. 다만 슬라이스 테스트의 한계를 이해하고, 필요에 따라 통합 테스트와 병행하여 사용하는 것이 중요합니다.

더 자세한 테스트 전략과 실제 구현 방법은 [[Spring Boot 테스트 완벽 가이드]]와 [[JPA 테스트 베스트 프랙티스]]를 참고해주세요.
