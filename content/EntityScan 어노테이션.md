# @EntityScan 어노테이션

`@EntityScan`은 Spring Boot에서 JPA [[엔티티(Entity)]] 클래스들을 스캔할 패키지를 명시적으로 지정하는 어노테이션입니다. Spring Boot의 기본 [[자동 구성(Auto Configuration)]] 메커니즘을 보완하여, 복잡한 프로젝트 구조나 특별한 요구사항이 있는 경우에 엔티티 스캔 경로를 정밀하게 제어할 수 있습니다.

## 기본 엔티티 스캔 메커니즘

Spring Boot는 기본적으로 `@SpringBootApplication`이 선언된 메인 클래스와 동일한 패키지 및 하위 패키지에서 `@Entity` 어노테이션이 붙은 클래스들을 자동으로 스캔합니다. 이는 대부분의 일반적인 프로젝트 구조에서 잘 작동하지만, 복잡한 모듈 구조나 멀티모듈 프로젝트에서는 제한이 있을 수 있습니다.

```java
@SpringBootApplication
public class MyApplication {
    public static void main(String[] args) {
        SpringApplication.run(MyApplication.class, args);
    }
}
```

위와 같은 설정에서는 `MyApplication` 클래스가 위치한 패키지와 그 하위 패키지에서만 엔티티를 스캔합니다.

## @EntityScan의 필요성

다음과 같은 상황에서 `@EntityScan`이 필요합니다:

1. **멀티모듈 프로젝트**: 엔티티 클래스가 별도의 모듈에 정의되어 있는 경우
2. **외부 라이브러리 엔티티**: 서드파티 라이브러리의 엔티티를 사용하는 경우
3. **특별한 패키지 구조**: 엔티티가 메인 애플리케이션 클래스와 다른 패키지 계층에 있는 경우
4. **선택적 엔티티 스캔**: 특정 엔티티만 포함하거나 제외하고 싶은 경우

## 기본 사용법

### 단일 패키지 지정

```java
@SpringBootApplication
@EntityScan("com.example.app.domain")
public class MyApplication {
    public static void main(String[] args) {
        SpringApplication.run(MyApplication.class, args);
    }
}
```

### 여러 패키지 지정

```java
@SpringBootApplication
@EntityScan({"com.example.app.domain", "com.example.shared.entities"})
public class MyApplication {
    public static void main(String[] args) {
        SpringApplication.run(MyApplication.class, args);
    }
}
```

### 베이스 패키지 클래스로 지정

```java
@SpringBootApplication
@EntityScan(basePackageClasses = {User.class, Order.class})
public class MyApplication {
    public static void main(String[] args) {
        SpringApplication.run(MyApplication.class, args);
    }
}
```

## 고급 사용법

### 별도 구성 클래스에서 사용

메인 애플리케이션 클래스를 깔끔하게 유지하기 위해 별도의 구성 클래스에서 `@EntityScan`을 사용할 수 있습니다:

```java
@Configuration
@EntityScan("com.example.app.domain")
public class DatabaseConfiguration {
    // 데이터베이스 관련 추가 구성
}
```

### 엔티티 필터링과 함께 사용

특정 엔티티만 스캔하도록 필터를 적용할 수도 있습니다:

```java
@Configuration
@EntityScan("com.example.app.domain")
public class MyEntityScanConfiguration {
    
    @Bean
    public ManagedClassNameFilter entityFilter() {
        return className -> className.startsWith("com.example.app.customer");
    }
}
```

이 방법은 테스트 환경에서 특정 엔티티만 로드하여 [[테스트 성능(Test Performance)]]을 향상시키거나, 특정 기능별로 엔티티를 분리하여 관리할 때 유용합니다.

## 멀티모듈 프로젝트에서의 활용

멀티모듈 프로젝트에서는 엔티티가 별도의 모듈에 정의되는 경우가 많습니다. 이때 `@EntityScan`을 사용하여 모든 관련 엔티티를 포함할 수 있습니다:

```java
@SpringBootApplication
@EntityScan({
    "com.example.user.domain",
    "com.example.order.domain", 
    "com.example.product.domain"
})
public class ECommerceApplication {
    public static void main(String[] args) {
        SpringApplication.run(ECommerceApplication.class, args);
    }
}
```

이러한 구조는 [[도메인 주도 설계(Domain Driven Design)]]를 적용한 프로젝트에서 각 [[바운디드 컨텍스트(Bounded Context)]]별로 엔티티를 분리할 때 특히 유용합니다.

## NoSQL 데이터베이스와의 사용

`@EntityScan`은 JPA뿐만 아니라 MongoDB, Elasticsearch, Cassandra 등의 NoSQL 데이터베이스에서도 사용할 수 있습니다:

### MongoDB와 함께 사용

```java
@SpringBootApplication
@EntityScan("com.example.app.document")
public class MongoApplication {
    public static void main(String[] args) {
        SpringApplication.run(MongoApplication.class, args);
    }
}
```

MongoDB의 `@Document` 어노테이션이 붙은 클래스들도 `@EntityScan`으로 스캔할 수 있습니다.

### Elasticsearch와 함께 사용

```java
@SpringBootApplication
@EntityScan("com.example.app.search")
public class SearchApplication {
    public static void main(String[] args) {
        SpringApplication.run(SearchApplication.class, args);
    }
}
```

Elasticsearch의 `@Document` 어노테이션이 붙은 클래스들을 스캔할 때도 동일하게 사용됩니다.

## 주의사항과 모범 사례

### 1. 패키지 구조의 일관성

엔티티 클래스들을 일관된 패키지 구조로 관리하는 것이 중요합니다. 일반적으로 다음과 같은 구조를 권장합니다:

```
com.example.app
├── domain/          # 엔티티 클래스
├── repository/      # 리포지토리 인터페이스
├── service/         # 서비스 클래스
└── controller/      # 컨트롤러 클래스
```

### 2. 순환 참조 방지

여러 모듈에서 엔티티를 스캔할 때 [[순환 참조(Circular Reference)]] 문제가 발생하지 않도록 주의해야 합니다.

### 3. 테스트 구성 분리

테스트 환경에서는 별도의 엔티티 스캔 구성을 사용하는 것이 좋습니다:

```java
@TestConfiguration
@EntityScan("com.example.app.test.domain")
public class TestDatabaseConfiguration {
    // 테스트용 엔티티 스캔 구성
}
```

### 4. 성능 고려사항

불필요한 패키지까지 스캔하지 않도록 스캔 범위를 최소화하는 것이 애플리케이션 시작 시간(Application Startup Time)을 단축하는 데 도움이 됩니다.

## 다른 어노테이션과의 관계

`@EntityScan`은 다른 Spring Boot 어노테이션들과 함께 사용되는 경우가 많습니다:

### @EnableJpaRepositories와 함께 사용

```java
@SpringBootApplication
@EntityScan("com.example.app.domain")
@EnableJpaRepositories("com.example.app.repository")
public class MyApplication {
    public static void main(String[] args) {
        SpringApplication.run(MyApplication.class, args);
    }
}
```

엔티티 스캔과 리포지토리 스캔을 각각 다른 패키지에서 수행할 수 있습니다.

### @ComponentScan과의 구분

`@ComponentScan`은 일반적인 Spring 컴포넌트(`@Service`, `@Repository`, `@Controller` 등)를 스캔하는 반면, `@EntityScan`은 오직 엔티티 클래스만을 대상으로 합니다.

## 실제 프로젝트 적용 예시

대규모 전자상거래 애플리케이션에서의 `@EntityScan` 활용 예시입니다:

```java
@SpringBootApplication
@EntityScan({
    "com.example.ecommerce.user.entity",
    "com.example.ecommerce.product.entity",
    "com.example.ecommerce.order.entity",
    "com.example.ecommerce.payment.entity",
    "com.example.shared.audit.entity"
})
@EnableJpaRepositories({
    "com.example.ecommerce.*.repository",
    "com.example.shared.audit.repository"
})
public class ECommerceApplication {
    public static void main(String[] args) {
        SpringApplication.run(ECommerceApplication.class, args);
    }
}
```

이러한 구성을 통해 각 도메인별로 엔티티를 분리하면서도 공통 기능(예: 감사 로깅)을 위한 엔티티는 공유할 수 있습니다.

## 문제 해결

### 엔티티를 찾을 수 없는 경우

만약 `@Entity` 어노테이션이 붙은 클래스가 있음에도 불구하고 JPA가 인식하지 못한다면, 다음을 확인해보세요:

1. **패키지 경로 확인**: `@EntityScan`에 지정된 패키지 경로가 올바른지 확인
2. **클래스패스 포함 여부**: 해당 엔티티 클래스가 클래스패스에 포함되어 있는지 확인
3. **의존성 설정**: 엔티티가 포함된 모듈이 빌드 의존성에 포함되어 있는지 확인

### 중복 엔티티 매핑 오류

같은 엔티티가 여러 번 스캔되어 중복 매핑 오류가 발생하는 경우:

```java
@EntityScan(basePackages = {"com.example.app.domain"}, 
           excludeFilters = @ComponentScan.Filter(type = FilterType.REGEX, 
                                                pattern = ".*\\.test\\..*"))
public class MyApplication {
    // 애플리케이션 구성
}
```

필터를 사용하여 특정 패키지나 클래스를 제외할 수 있습니다.

## 결론

`@EntityScan` 어노테이션은 Spring Boot 애플리케이션에서 엔티티 스캔을 정밀하게 제어할 수 있는 강력한 도구입니다. 기본 자동 구성만으로는 해결하기 어려운 복잡한 프로젝트 구조나 특별한 요구사항을 만족시킬 수 있으며, 멀티모듈 프로젝트나 NoSQL 데이터베이스를 사용하는 프로젝트에서 특히 유용합니다.

올바른 패키지 구조와 함께 `@EntityScan`을 적절히 활용하면 [[유지보수성(Maintainability)]]이 높고 확장 가능한 데이터 접근 계층을 구축할 수 있습니다. 다만 스캔 범위를 최소화하여 성능을 최적화하고, 다른 스캔 관련 어노테이션들과의 관계를 잘 이해하여 사용하는 것이 중요합니다.

## 참고 자료

- Spring Boot 공식 문서: Auto-configuration
- Spring Data JPA 레퍼런스 가이드
- [[JPA 엔티티 매핑 전략]]
- [[Spring Boot 멀티모듈 프로젝트 구성]]
