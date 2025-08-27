# Spring @TestConfiguration 어노테이션

`@TestConfiguration`은 Spring Boot에서 테스트 환경에 특화된 설정을 정의하기 위한 어노테이션입니다. 이 어노테이션을 사용하면 운영 환경과는 별도로 테스트에만 사용할 빈을 정의하거나 기존 빈을 테스트용으로 대체할 수 있으며, 테스트의 독립성과 안정성을 보장하는 데 핵심적인 역할을 합니다.

## @TestConfiguration의 역할

`@TestConfiguration`은 다음과 같은 중요한 특징들을 가지고 있습니다:

1. **테스트 전용 빈 정의**: 테스트에서만 사용할 특별한 빈을 정의할 수 있습니다
2. **빈 오버라이드**: 운영 환경의 빈을 테스트용 구현체로 대체할 수 있습니다
3. **격리된 테스트 환경**: 외부 의존성을 제거하여 독립적인 테스트 환경을 구성할 수 있습니다
4. **선택적 적용**: 필요한 테스트에서만 명시적으로 import하여 사용할 수 있습니다

## @Configuration과의 차이점

`@TestConfiguration`과 일반적인 `@Configuration`의 가장 중요한 차이점은 컴포넌트 스캔 동작입니다:

### @Configuration
- Spring의 기본 컴포넌트 스캔에 의해 자동으로 감지됩니다
- 모든 테스트에서 자동으로 적용됩니다
- 운영 애플리케이션에서도 로드될 수 있습니다

### @TestConfiguration
- 컴포넌트 스캔에서 **제외**됩니다
- 테스트에서 명시적으로 import해야만 적용됩니다
- 테스트 전용으로만 사용됩니다

```java
// 일반 Configuration - 자동으로 스캔됨
@Configuration
public class ApplicationConfig {
    @Bean
    public MyService myService() {
        return new MyServiceImpl();
    }
}

// TestConfiguration - 명시적 import 필요
@TestConfiguration
public class TestConfig {
    @Bean
    public MyService myService() {
        return new MockMyService(); // 테스트용 구현체
    }
}
```

## 빈 오버라이딩 활성화

Spring Boot 2.1부터 빈 오버라이딩이 기본적으로 비활성화되어 있습니다. `@TestConfiguration`으로 기존 빈을 오버라이드하려면 다음 설정을 추가해야 합니다:

```properties
# application-test.properties
spring.main.allow-bean-definition-overriding=true
```

이 설정은 테스트 환경에서만 활성화하는 것이 중요합니다.

## 사용 방법

`@TestConfiguration`을 사용하는 방법은 크게 두 가지가 있습니다:

### 1. 별도 클래스로 정의하여 Import

가장 일반적이고 권장되는 방법입니다:

```java
@TestConfiguration
public class EmailTestConfiguration {
    
    @Bean
    @Primary
    public EmailService emailService() {
        return new MockEmailService(); // 실제 이메일 전송 대신 Mock 사용
    }
    
    @Bean
    public EmailTemplate emailTemplate() {
        return new TestEmailTemplate(); // 테스트용 템플릿
    }
}
```

테스트 클래스에서 사용:

```java
@SpringBootTest
@Import(EmailTestConfiguration.class)
class UserServiceTest {
    
    @Autowired
    private UserService userService;
    
    @Autowired
    private EmailService emailService; // Mock 구현체가 주입됨
    
    @Test
    void 사용자가_회원가입하면_환영메일이_발송된다() {
        // given
        User newUser = new User("test@example.com", "테스트사용자");
        
        // when
        userService.registerUser(newUser);
        
        // then
        MockEmailService mockService = (MockEmailService) emailService;
        assertThat(mockService.getSentEmails()).hasSize(1);
        assertThat(mockService.getSentEmails().get(0).getTo())
            .isEqualTo("test@example.com");
    }
}
```

### 2. 정적 중첩 클래스로 정의

테스트 클래스 내부에 정적 중첩 클래스로 정의하는 방법입니다:

```java
@SpringBootTest
class PaymentServiceTest {
    
    @TestConfiguration
    static class PaymentTestConfiguration {
        
        @Bean
        @Primary
        public PaymentGateway paymentGateway() {
            return new MockPaymentGateway(); // 실제 결제 대신 Mock 사용
        }
        
        @Bean
        public PaymentValidator paymentValidator() {
            PaymentValidator validator = Mockito.mock(PaymentValidator.class);
            // 테스트에 필요한 기본 설정
            when(validator.isValid(any())).thenReturn(true);
            return validator;
        }
    }
    
    @Autowired
    private PaymentService paymentService;
    
    @Test
    void 결제가_성공하면_주문이_완료된다() {
        // 테스트 로직
    }
}
```

정적 중첩 클래스로 정의하면 Spring Boot가 자동으로 감지하므로 별도의 `@Import`가 필요하지 않습니다.

## 실전 활용 사례

### 1. 외부 API 연동 테스트

외부 API 호출을 Mock으로 대체하여 안정적인 테스트 환경을 구성합니다:

```java
@TestConfiguration
public class ExternalApiTestConfiguration {
    
    @Bean
    @Primary
    public WeatherApiClient weatherApiClient() {
        WeatherApiClient mockClient = Mockito.mock(WeatherApiClient.class);
        
        // 테스트용 기본 응답 설정
        when(mockClient.getCurrentWeather(anyString()))
            .thenReturn(new WeatherInfo("맑음", 25.0));
            
        return mockClient;
    }
    
    @Bean
    @Primary
    public GeocodeApiClient geocodeApiClient() {
        return new MockGeocodeApiClient(); // 커스텀 Mock 구현체
    }
}
```

### 2. 데이터베이스 테스트 설정

테스트용 데이터베이스 설정이나 초기 데이터를 구성합니다:

```java
@TestConfiguration
public class DatabaseTestConfiguration {
    
    @Bean
    @Primary
    public DataInitializer testDataInitializer() {
        return new TestDataInitializer(); // 테스트용 초기 데이터 로더
    }
    
    @Bean
    public TestDatabaseCleaner databaseCleaner() {
        return new TestDatabaseCleaner(); // 테스트 후 데이터 정리
    }
}
```

### 3. 보안 설정 테스트

테스트 환경에서 보안 설정을 우회하거나 단순화합니다:

```java
@TestConfiguration
public class SecurityTestConfiguration {
    
    @Bean
    @Primary
    public AuthenticationManager authenticationManager() {
        // 테스트용 간단한 인증 관리자
        return new TestAuthenticationManager();
    }
    
    @Bean
    public UserDetailsService userDetailsService() {
        // 고정된 테스트 사용자 제공
        return new InMemoryUserDetailsManager(
            User.withUsername("testuser")
                .password("{noop}password")
                .authorities("ROLE_USER")
                .build()
        );
    }
}
```

## 슬라이스 테스트와의 조합

`@TestConfiguration`은 Spring Boot의 슬라이스 테스트 어노테이션들과 함께 사용할 수 있습니다:

### @WebMvcTest와 함께 사용

```java
@WebMvcTest(ProductController.class)
@Import(ProductTestConfiguration.class)
class ProductControllerTest {
    
    @Autowired
    private MockMvc mockMvc;
    
    @MockBean
    private ProductService productService; // @MockBean으로 서비스 계층 Mock
    
    @Test
    void 상품목록을_조회할수있다() throws Exception {
        // given
        List<Product> products = Arrays.asList(
            new Product("노트북", 1000000),
            new Product("마우스", 50000)
        );
        when(productService.getAllProducts()).thenReturn(products);
        
        // when & then
        mockMvc.perform(get("/api/products"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$", hasSize(2)))
            .andExpect(jsonPath("$[0].name", is("노트북")));
    }
}

@TestConfiguration
public class ProductTestConfiguration {
    
    @Bean
    public ProductValidator productValidator() {
        // 테스트용 검증 로직
        return new LenientProductValidator();
    }
}
```

### @DataJpaTest와 함께 사용

```java
@DataJpaTest
@Import(JpaTestConfiguration.class)
class UserRepositoryTest {
    
    @Autowired
    private TestEntityManager entityManager;
    
    @Autowired
    private UserRepository userRepository;
    
    @Test
    void 이메일로_사용자를_조회할수있다() {
        // given
        User user = new User("test@example.com", "테스트사용자");
        entityManager.persistAndFlush(user);
        
        // when
        Optional<User> foundUser = userRepository.findByEmail("test@example.com");
        
        // then
        assertThat(foundUser).isPresent();
        assertThat(foundUser.get().getEmail()).isEqualTo("test@example.com");
    }
}

@TestConfiguration
public class JpaTestConfiguration {
    
    @Bean
    public AuditorAware<String> auditorProvider() {
        // 테스트용 Auditor 제공
        return () -> Optional.of("test-user");
    }
}
```

## 환경별 테스트 설정

프로파일을 활용하여 환경별로 다른 테스트 설정을 적용할 수 있습니다:

```java
@TestConfiguration
@Profile("integration-test")
public class IntegrationTestConfiguration {
    
    @Bean
    @Primary
    public EmailService emailService() {
        return new RealEmailService(); // 실제 이메일 서비스 사용
    }
}

@TestConfiguration
@Profile("unit-test")
public class UnitTestConfiguration {
    
    @Bean
    @Primary
    public EmailService emailService() {
        return new MockEmailService(); // Mock 이메일 서비스 사용
    }
}
```

테스트에서 프로파일 활성화:

```java
@SpringBootTest
@ActiveProfiles("unit-test")
@Import(UnitTestConfiguration.class)
class UserServiceUnitTest {
    // 단위 테스트 로직
}

@SpringBootTest
@ActiveProfiles("integration-test")
@Import(IntegrationTestConfiguration.class)
class UserServiceIntegrationTest {
    // 통합 테스트 로직
}
```

## 메타 어노테이션 활용

반복되는 테스트 설정을 메타 어노테이션으로 추상화할 수 있습니다:

```java
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@SpringBootTest
@Import({
    EmailTestConfiguration.class,
    PaymentTestConfiguration.class,
    SecurityTestConfiguration.class
})
@ActiveProfiles("test")
public @interface ServiceLayerTest {
}
```

사용 시:

```java
@ServiceLayerTest
class OrderServiceTest {
    // 모든 테스트 설정이 자동으로 적용됨
    
    @Autowired
    private OrderService orderService;
    
    @Test
    void 주문을_생성할수있다() {
        // 테스트 로직
    }
}
```

## 테스트 데이터 관리

`@TestConfiguration`을 활용하여 테스트 데이터를 체계적으로 관리할 수 있습니다:

```java
@TestConfiguration
public class TestDataConfiguration {
    
    @Bean
    public TestDataFactory testDataFactory() {
        return new TestDataFactory();
    }
    
    @Bean
    public UserTestData userTestData() {
        return new UserTestData();
    }
    
    @Bean
    public ProductTestData productTestData() {
        return new ProductTestData();
    }
}

// 테스트 데이터 팩토리
public class TestDataFactory {
    
    public User createTestUser(String suffix) {
        return User.builder()
            .email("test" + suffix + "@example.com")
            .name("테스트사용자" + suffix)
            .build();
    }
    
    public Product createTestProduct(String name, int price) {
        return Product.builder()
            .name(name)
            .price(price)
            .build();
    }
}
```

## Mock과 Spy 조합

`@TestConfiguration`에서 Mockito의 Mock과 Spy를 효과적으로 활용할 수 있습니다:

```java
@TestConfiguration
public class MockConfiguration {
    
    @Bean
    @Primary
    public NotificationService notificationService() {
        NotificationService spy = Mockito.spy(new NotificationServiceImpl());
        
        // 특정 메서드만 Mock 처리
        doNothing().when(spy).sendPushNotification(any());
        
        return spy;
    }
    
    @Bean
    public AuditService auditService() {
        AuditService mock = Mockito.mock(AuditService.class);
        
        // 기본 동작 설정
        when(mock.recordEvent(any())).thenReturn(true);
        
        return mock;
    }
}
```

## 성능 고려사항

### 컨텍스트 캐싱 활용

동일한 `@TestConfiguration`을 사용하는 테스트들은 Spring의 컨텍스트 캐싱 메커니즘을 활용할 수 있습니다:

```java
// 동일한 설정을 사용하는 테스트들
@SpringBootTest
@Import(CommonTestConfiguration.class)
class UserServiceTest { /* 테스트 내용 */ }

@SpringBootTest
@Import(CommonTestConfiguration.class)
class OrderServiceTest { /* 테스트 내용 */ }

// 위 두 테스트는 동일한 애플리케이션 컨텍스트를 공유
```

### 최소한의 빈만 정의

성능 향상을 위해 테스트에 필요한 최소한의 빈만 정의하는 것이 좋습니다:

```java
@TestConfiguration
public class MinimalTestConfiguration {
    
    // 꼭 필요한 빈만 정의
    @Bean
    @Primary
    public PaymentGateway paymentGateway() {
        return new MockPaymentGateway();
    }
    
    // 불필요한 빈은 정의하지 않음
}
```

## 모범 사례

### 1. 명확한 네이밍

테스트 설정 클래스의 이름을 명확하게 지정합니다:

```java
// 좋은 예
@TestConfiguration
public class PaymentServiceTestConfiguration { }

@TestConfiguration
public class EmailIntegrationTestConfiguration { }

// 피해야 할 예
@TestConfiguration
public class TestConfig { }

@TestConfiguration
public class Config { }
```

### 2. 패키지 구조 정리

테스트 설정을 체계적으로 관리합니다:

```
src/test/java/
├── config/
│   ├── CommonTestConfiguration.java
│   ├── SecurityTestConfiguration.java
│   └── DatabaseTestConfiguration.java
├── service/
│   ├── UserServiceTest.java
│   └── PaymentServiceTest.java
└── controller/
    ├── UserControllerTest.java
    └── PaymentControllerTest.java
```

### 3. 문서화

복잡한 테스트 설정에는 충분한 문서화를 제공합니다:

```java
/**
 * 결제 서비스 테스트를 위한 설정
 * 
 * 이 설정은 다음과 같은 테스트 환경을 제공합니다:
 * - Mock 결제 게이트웨이 (실제 결제 없이 테스트 가능)
 * - 테스트용 결제 검증기 (모든 결제를 유효한 것으로 처리)
 * - 인메모리 결제 이력 저장소
 */
@TestConfiguration
public class PaymentServiceTestConfiguration {
    
    /**
     * Mock 결제 게이트웨이
     * 실제 PG사 연동 없이 결제 성공/실패 시나리오를 테스트할 수 있습니다.
     */
    @Bean
    @Primary
    public PaymentGateway paymentGateway() {
        return new MockPaymentGateway();
    }
}
```

## 주의사항

### 1. 운영 환경과의 차이

테스트 환경과 운영 환경의 차이로 인한 문제를 방지하기 위해 중요한 비즈니스 로직은 별도의 [[빅뱅 통합 테스트]]로도 검증해야 합니다.

### 2. 과도한 Mock 사용 지양

너무 많은 Mock을 사용하면 테스트의 신뢰성이 떨어질 수 있으므로, 꼭 필요한 부분만 Mock으로 대체하는 것이 좋습니다.

### 3. 테스트 간 격리

테스트 설정이 다른 테스트에 영향을 주지 않도록 주의해야 합니다. 테스트 격리 전략을 참고해주세요.

## 다른 테스트 어노테이션과의 비교

Spring Boot는 다양한 테스트 어노테이션을 제공합니다:

- **@TestConfiguration**: 테스트 전용 빈 설정 정의
- **@MockBean**: 스프링 컨텍스트의 빈을 Mock으로 대체
- **@SpyBean**: 스프링 컨텍스트의 빈을 Spy로 래핑
- **@TestPropertySource**: 테스트용 프로퍼티 설정

각각의 역할과 사용법에 대한 자세한 내용은 Spring Boot 테스트 어노테이션 완벽 가이드를 참고해주세요.

## 결론

`@TestConfiguration`은 Spring Boot에서 효과적인 테스트 환경을 구축하기 위한 핵심 도구입니다. 이 어노테이션을 활용하면 다음과 같은 이점을 얻을 수 있습니다:

1. **독립적인 테스트 환경**: 외부 의존성을 제거하여 안정적인 테스트 실행
2. **유연한 설정 관리**: 테스트 목적에 맞는 맞춤형 빈 설정
3. **개발 생산성 향상**: 빠르고 안정적인 테스트 실행으로 개발 피드백 루프 단축
4. **코드 품질 향상**: 체계적인 테스트 환경으로 높은 품질의 코드 작성

적절한 `@TestConfiguration` 활용을 통해 견고하고 유지보수가 용이한 테스트 코드를 작성할 수 있으며, 이는 전체적인 애플리케이션의 품질 향상으로 이어집니다.

더 자세한 Spring Boot 테스트 기법과 실제 적용 사례는 Spring Boot 테스트 마스터하기와 실전 테스트 주도 개발을 참고해주세요. 