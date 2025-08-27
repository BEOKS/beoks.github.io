`@ContextConfiguration`은 Spring 테스트 프레임워크에서 ApplicationContext를 구성하기 위한 핵심 어노테이션입니다. 이 어노테이션을 통해 테스트에서 사용할 Spring 설정을 명시적으로 지정할 수 있으며, 다양한 방식으로 애플리케이션 컨텍스트를 로드할 수 있습니다.

## @ContextConfiguration의 역할

`@ContextConfiguration`은 Spring TestContext Framework의 핵심 구성 요소로서 다음과 같은 기능을 제공합니다:

1. **설정 소스 지정**: XML, Java Config, Groovy 스크립트 등 다양한 형태의 설정을 지정할 수 있습니다
2. **컨텍스트 초기화**: ApplicationContextInitializer를 통한 프로그래밍 방식의 컨텍스트 초기화
3. **커스텀 로더**: 특별한 요구사항이 있는 경우 커스텀 ContextLoader 지정 가능
4. **계층 구조**: 복잡한 애플리케이션에서 부모-자식 컨텍스트 계층 구조 지원

## 주요 속성

`@ContextConfiguration`은 다음과 같은 주요 속성들을 제공합니다:

### locations (또는 value)
XML 설정 파일의 위치를 지정합니다:

```java
@ContextConfiguration("/test-config.xml")
class XmlApplicationContextTests {
    // 테스트 내용
}
```

여러 XML 파일을 함께 로드할 수도 있습니다:

```java
@ContextConfiguration({"/app-config.xml", "/test-config.xml"})
class MultipleXmlConfigTests {
    // 테스트 내용
}
```

### classes
Java Configuration 클래스를 지정합니다:

```java
@ContextConfiguration(classes = TestConfig.class)
class ConfigClassApplicationContextTests {
    // 테스트 내용
}
```

여러 설정 클래스를 함께 사용할 수도 있습니다:

```java
@ContextConfiguration(classes = {AppConfig.class, TestConfig.class})
class MultipleConfigClassTests {
    // 테스트 내용
}
```

### initializers
ApplicationContextInitializer를 통한 프로그래밍 방식의 컨텍스트 초기화를 지원합니다:

```java
@ContextConfiguration(initializers = CustomContextInitializer.class)
class ContextInitializerTests {
    // 테스트 내용
}
```

### loader
특별한 요구사항이 있는 경우 커스텀 ContextLoader를 지정할 수 있습니다:

```java
@ContextConfiguration(
    locations = "/test-context.xml", 
    loader = CustomContextLoader.class
)
class CustomLoaderTests {
    // 테스트 내용
}
```

## 기본 사용 패턴

### 1. XML 기반 설정

가장 전통적인 방식으로 XML 파일을 통해 빈을 정의하고 테스트에서 로드합니다:

```java
@ExtendWith(SpringExtension.class)
@ContextConfiguration("/repository-config.xml")
class HibernateTitleRepositoryTests {

    @Autowired
    private HibernateTitleRepository titleRepository;

    @Test
    void findById() {
        Title title = titleRepository.findById(10L);
        assertNotNull(title);
    }
}
```

### 2. Java Configuration 기반 설정

현대적인 Spring 개발에서 선호되는 방식으로, `@Configuration` 클래스를 통해 빈을 정의합니다:

```java
@ExtendWith(SpringExtension.class)
@ContextConfiguration(classes = {AppConfig.class, TestConfig.class})
class MyTest {
    
    @Autowired
    private MyService myService;
    
    @Test
    void testBusinessLogic() {
        // 테스트 로직
    }
}
```

### 3. 중첩 설정 클래스 활용

테스트 클래스 내부에 정적 중첩 클래스로 설정을 정의할 수 있습니다:

```java
@SpringJUnitConfig
class OrderServiceTest {

    @Configuration
    static class Config {
        
        @Bean
        OrderService orderService() {
            OrderService orderService = new OrderServiceImpl();
            // 속성 설정 등
            return orderService;
        }
    }

    @Autowired
    OrderService orderService;

    @Test
    void testOrderService() {
        // orderService 테스트
    }
}
```

## 고급 활용법

### 1. 컨텍스트 초기화자 활용

ApplicationContextInitializer를 통해 컨텍스트 로드 후 추가적인 설정을 수행할 수 있습니다:

```java
@ExtendWith(SpringExtension.class)
@ContextConfiguration(
    classes = TestConfig.class,
    initializers = TestAppCtxInitializer.class
)
class MyTest {
    // 테스트 내용
}
```

이 방식은 다음과 같은 경우에 유용합니다:
- 프로퍼티 소스 추가
- 빈 정의 후처리
- 조건부 설정 적용

### 2. 초기화자만 사용하는 설정

설정 파일이나 클래스 없이 초기화자만으로 컨텍스트를 구성할 수도 있습니다:

```java
@ExtendWith(SpringExtension.class)
@ContextConfiguration(initializers = EntireAppInitializer.class)
class MyTest {
    // 테스트 내용
}
```

### 3. 혼합 설정 방식

XML과 Java Configuration을 함께 사용할 수도 있습니다:

```java
@ExtendWith(SpringExtension.class)
@ContextConfiguration({"/app-config.xml", "/TestConfig.groovy"})
class MixedConfigTest {
    // 테스트 내용
}
```

## 설정 상속과 오버라이드

### 설정 상속

부모 테스트 클래스의 설정을 자식 클래스가 상속받을 수 있습니다:

```java
@ExtendWith(SpringExtension.class)
@ContextConfiguration("/base-config.xml")
class BaseTest {
    // 기본 테스트
}

@ContextConfiguration("/extended-config.xml")
class ExtendedTest extends BaseTest {
    // 확장된 테스트 - base-config.xml과 extended-config.xml 모두 로드됨
}
```

### 설정 오버라이드

`inheritLocations = false` 속성을 사용하여 부모의 설정을 완전히 교체할 수 있습니다:

```java
@ContextConfiguration(
    locations = "/test-specific-config.xml",
    inheritLocations = false
)
class OverrideTest extends BaseTest {
    // 부모의 설정을 무시하고 새로운 설정만 사용
}
```

## 컨텍스트 계층 구조

복잡한 애플리케이션에서는 `@ContextHierarchy`와 함께 사용하여 부모-자식 컨텍스트 구조를 만들 수 있습니다:

```java
@ContextHierarchy({
    @ContextConfiguration("/parent-config.xml"),
    @ContextConfiguration("/child-config.xml")
})
class ContextHierarchyTests {
    // 계층 구조를 가진 컨텍스트 테스트
}
```

이 방식은 다음과 같은 상황에서 유용합니다:
- 웹 애플리케이션의 루트 컨텍스트와 서블릿 컨텍스트 분리
- 모듈별 컨텍스트 구성
- 보안 설정과 비즈니스 로직 분리

## 웹 애플리케이션 컨텍스트

웹 애플리케이션을 테스트할 때는 `@WebAppConfiguration`과 함께 사용합니다:

```java
@ExtendWith(SpringExtension.class)
@WebAppConfiguration
@ContextConfiguration(classes = WebConfig.class)
class WebIntegrationTests {
    
    @Autowired
    private WebApplicationContext wac;
    
    // 웹 애플리케이션 테스트
}
```

## 프로파일 활용

`@ActiveProfiles`와 함께 사용하여 특정 프로파일이 활성화된 상태에서 테스트할 수 있습니다:

```java
@ExtendWith(SpringExtension.class)
@ContextConfiguration("/app-config.xml")
@ActiveProfiles("dev")
class TransferServiceTest {

    @Autowired
    TransferService transferService;

    @Test
    void testTransferService() {
        // dev 프로파일이 활성화된 상태에서 테스트
    }
}
```

이를 통해 다음과 같은 이점을 얻을 수 있습니다:
- 환경별 설정 테스트
- 조건부 빈 활성화
- 특정 기능의 활성화/비활성화 테스트

## 편의 어노테이션과의 조합

### @SpringJUnitConfig

JUnit 5를 사용할 때는 `@SpringJUnitConfig`를 사용하여 더 간결하게 작성할 수 있습니다:

```java
@SpringJUnitConfig(TestConfig.class)
class SimpleTests {
    
    @Test
    void testMethod() {
        // 테스트 로직
    }
}
```

이는 다음과 동일합니다:

```java
@ExtendWith(SpringExtension.class)
@ContextConfiguration(classes = TestConfig.class)
class SimpleTests {
    // 동일한 효과
}
```

### @SpringJUnitWebConfig

웹 애플리케이션 테스트를 위한 편의 어노테이션입니다:

```java
@SpringJUnitWebConfig(TestConfig.class)
class ConfigurationClassJUnitJupiterSpringWebTests {
    // 웹 애플리케이션 테스트
}
```

## 메타 어노테이션 활용

반복되는 설정을 메타 어노테이션으로 추상화할 수 있습니다:

```java
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@ContextConfiguration({"/app-config.xml", "/test-data-access-config.xml"})
@ActiveProfiles("dev")
@Transactional
public @interface TransactionalDevTestConfig { }
```

사용 시:

```java
@TransactionalDevTestConfig
class OrderRepositoryTests { 
    // 메타 어노테이션으로 간단한 설정
}
```

## 동적 프로퍼티 설정

`@DynamicPropertySource`와 함께 사용하여 런타임에 프로퍼티를 설정할 수 있습니다:

```java
@ContextConfiguration
class MyIntegrationTests {

    static MyExternalServer server = // 외부 서버 인스턴스

    @DynamicPropertySource
    static void dynamicProperties(DynamicPropertyRegistry registry) {
        registry.add("server.port", server::getPort);
    }

    // 테스트 내용
}
```

이는 다음과 같은 상황에서 유용합니다:
- 테스트 컨테이너 사용 시 동적 포트 설정
- 외부 시스템 연동 테스트
- 런타임에 결정되는 설정값 처리

## 스프링 부트와의 통합

Spring Boot 애플리케이션에서는 `@SpringBootTest`와 함께 사용하거나, 슬라이스 테스트 어노테이션들과 조합하여 사용할 수 있습니다:

```java
@DataJpaTest
@ContextConfiguration(classes = TestDataConfig.class)
class RepositoryTest {
    // JPA 리포지토리 테스트에 추가 설정 적용
}
```

더 자세한 스프링 부트 테스트 방법은 Spring Boot 테스트 전략을 참고해주세요.

## 성능 최적화

### 컨텍스트 캐싱

Spring TestContext Framework는 동일한 설정의 컨텍스트를 캐시하여 성능을 향상시킵니다. 따라서 가능한 한 공통된 설정을 사용하는 것이 좋습니다.

### 슬라이스 테스트 활용

전체 애플리케이션 컨텍스트 대신 필요한 부분만 로드하는 슬라이스 테스트 패턴을 활용하면 테스트 실행 속도를 크게 향상시킬 수 있습니다.

## 주의사항과 모범 사례

### 테스트 격리

각 테스트는 독립적으로 실행되어야 하므로, 공유 상태를 변경하는 테스트는 적절한 정리 작업이 필요합니다. 테스트 격리 전략을 참고해주세요.

### 설정 복잡도 관리

너무 복잡한 설정은 테스트의 가독성과 유지보수성을 해치므로, 적절한 수준에서 추상화하는 것이 중요합니다.

### 환경별 설정 분리

개발, 테스트, 운영 환경별로 다른 설정이 필요한 경우 프로파일 기반 설정 관리를 통해 체계적으로 관리해야 합니다.

## 트러블슈팅

### 흔한 문제들

1. **설정 파일을 찾을 수 없는 경우**: 클래스패스 확인 및 절대/상대 경로 설정 점검
2. **빈 중복 정의**: 여러 설정에서 동일한 빈을 정의할 때 발생
3. **순환 참조**: 빈 간의 의존성이 순환할 때 발생

자세한 문제 해결 방법은 Spring 테스트 트러블슈팅 가이드를 참고해주세요.

## 결론

`@ContextConfiguration`은 Spring 테스트의 핵심 어노테이션으로, 다양한 방식으로 애플리케이션 컨텍스트를 구성할 수 있는 강력한 기능을 제공합니다. XML, Java Configuration, Groovy 등 다양한 설정 방식을 지원하며, 초기화자를 통한 프로그래밍 방식의 설정도 가능합니다.

효과적인 테스트를 위해서는 테스트의 목적에 맞는 적절한 설정 방식을 선택하고, 성능과 유지보수성을 고려한 설정 구조를 만들어야 합니다. 또한 Spring Boot의 슬라이스 테스트 어노테이션들과 조합하여 사용하면 더욱 효율적인 테스트 환경을 구축할 수 있습니다.

더 자세한 Spring 테스트 기법과 실제 적용 사례는 Spring 테스트 마스터하기와 실전 Spring 테스트 패턴을 참고해주세요. 