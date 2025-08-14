---
title: "인가(Authorization)란 무엇일까?"
date: 2025-07-08
tags: ["Security", "Authorization", "Authentication", "RBAC", "ABAC", "Spring Security"]
---

소프트웨어 시스템에서 **인가(Authorization)**는 사용자가 특정 리소스나 기능에 접근할 수 있는 권한을 부여하고 제어하는 과정을 의미합니다. 많은 사람들이 [[Authentication]]과 인가를 혼동하지만, 이 둘은 명확히 구분되는 개념입니다.

## [[Authentication]]과 인가(Authorization)의 차이

자세한 내용은 [[Authentication]] 문서의 '인증(Authentication)이란 무엇일까요?' 섹션을 참고해주세요.

쉽게 비유하자면, 공항에서 신분증으로 본인임을 확인하는 것이 '인증'이고, 탑승권을 보여주고 비행기에 탑승할 권한을 얻는 것이 '인가'입니다. 시스템 보안의 첫걸음은 이 두 개념을 명확히 이해하는 것에서 시작하며, **항상 인증이 인가보다 먼저 수행되어야 합니다.**

## 접근 제어 모델

인가는 **접근 제어 모델**을 기반으로 구현됩니다. 접근 제어 모델은 누가 무엇을 할 수 있는지를 결정하는 규칙의 구조를 정의합니다. 대표적인 모델로는 역할 기반 접근 제어(RBAC), 속성 기반 접근 제어(ABAC) 등이 있습니다.

-   **역할 기반 접근 제어(RBAC)**: 사용자에게 역할을 할당하고, 역할에 권한을 부여하는 방식입니다. 대규모 조직에서 효율적인 권한 관리가 가능합니다. 자세한 내용은 [[역할 기반 접근 제어(RBAC)]] 문서를 참고해주세요.
-   **속성 기반 접근 제어(ABAC)**: 사용자, 리소스, 환경 등 다양한 속성을 기반으로 동적인 접근 제어를 수행합니다. 매우 세분화된 제어가 필요할 때 유용합니다.

자세한 내용은 [[접근 제어 모델]] 문서를 참고해주세요.

## 스프링 시큐리티에서의 인가 처리

Java, 특히 스프링 프레임워크에서는 Spring Security를 통해 강력한 인가 기능을 구현할 수 있습니다.

### URL 기반 인가

가장 일반적인 방법으로, 특정 URL 패턴에 따라 접근 권한을 제어합니다.

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(authorize -> authorize
                .requestMatchers("/admin/**").hasRole("ADMIN") // /admin/** 경로는 ADMIN 역할만 접근 가능
                .requestMatchers("/user/**").hasAnyRole("USER", "ADMIN") // /user/** 경로는 USER 또는 ADMIN 역할 접근 가능
                .anyRequest().authenticated() // 나머지 요청은 인증된 사용자만 접근 가능
            )
            .formLogin(withDefaults());
        return http.build();
    }
}
```

### 메서드 수준 인가

서비스 계층의 특정 메서드에 어노테이션을 사용하여 더 세밀한 인가 제어를 할 수 있습니다.

```java
@Service
public class ProductService {

    @PreAuthorize("hasRole('ADMIN')") // ADMIN 역할만 이 메서드를 실행할 수 있음
    public void deleteProduct(Long productId) {
        // 상품 삭제 로직
    }
}
```

`@PreAuthorize` 어노테이션은 메서드 실행 전에, `@PostAuthorize`는 실행 후에 권한을 검사합니다. 이를 사용하기 위해서는 설정에 `@EnableMethodSecurity`를 추가해야 합니다.

자세한 내용은 Spring Security 인가 설정 방법을 참고해주세요.

## 최소 권한 원칙

최소 권한 원칙은 보안의 핵심 원칙 중 하나로, 사용자나 시스템이 **자신의 업무를 수행하는 데 필요한 최소한의 권한만** 가져야 한다는 개념입니다. 

자세한 내용은 [[최소 권한 원칙]] 문서를 참고해주세요.

## 결론

인가는 시스템의 자원을 안전하게 보호하기 위한 필수적인 보안 메커니즘입니다. 인증을 통해 신원을 확인한 후, RBAC이나 ABAC 같은 적절한 접근 제어 모델을 선택하고 최소 권한 원칙을 준수하여 인가 정책을 구현해야 합니다. 특히 스프링 시큐리티와 같은 프레임워크를 활용하면 복잡한 인가 요구사항을 보다 체계적이고 안전하게 관리할 수 있습니다.

## 참고 자료
- [IBM - Authentication vs. authorization](https://www.ibm.com/topics/authentication-vs-authorization)
- [NIST - Access Control](https://csrc.nist.gov/glossary/term/access_control)
- [Spring Security Documentation](https://spring.io/projects/spring-security)
