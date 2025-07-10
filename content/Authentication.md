---
title: "인증(Authentication)이란 무엇인가?"
date: 2025-07-08
tags: ["Security", "Authentication", "Spring Security"]
---



인증은 간단해 보이지만, 그 이면에는 다양한 기술과 원칙이 숨어있습니다. 이 글을 통해 인증의 정확한 의미부터 최신 프로토콜, 그리고 Spring Security를 활용한 구현 방법까지 명확하게 이해하실 수 있을 것입니다.

## 인증(Authentication)이란 무엇일까요?

**인증(Authentication)**은 시스템에 접근하려는 사용자가 **"자신이 주장하는 그 사람이 맞는지"**를 확인하는 절차입니다. 가장 대표적인 예는 우리가 매일같이 사용하는 아이디와 비밀번호를 통한 로그인입니다.

많은 분들이 [[Authorization]]와 혼동하시는데, 두 개념은 명확히 다릅니다.

*   **인증(Authentication)**: 당신이 **누구인지** 증명하는 과정 (신분증 제시)
*   **[[인가(Authorization)]]**: 당신이 **무엇을 할 수 있는지** 권한을 부여받는 과정 (권한 확인 후 출입증 발급)

인증 절차가 성공적으로 끝나야만, 시스템은 비로소 해당 사용자에게 적절한 권한을 부여하는 인가 절차를 진행할 수 있습니다.

## 대표적인 인증 방법들

시스템은 사용자의 신원을 확인하기 위해 다양한 방법을 사용합니다. 각 방법은 장단점을 가지고 있어 상황에 맞게 선택해야 합니다.

1.  **지식 기반 인증 (Something you know)**
    *   **예시**: 비밀번호, PIN
    *   **장점**: 구현이 가장 간단하고 보편적입니다.
    *   **단점**: 유출, 추측, 무차별 대입 공격(Brute-force attack)에 취약합니다.

2.  **소유 기반 인증 (Something you have)**
    *   **예시**: OTP 기기, 스마트폰 앱, 공인인증서
    *   **장점**: 물리적인 소유가 필요하므로 보안성이 높습니다.
    *   **단점**: 분실이나 도난의 위험이 있습니다.

3.  **특성 기반 인증 (Something you are)**
    *   **예시**: 지문, 얼굴, 홍채 등 생체 정보
    *   **장점**: 사용이 편리하고 복제하기 매우 어렵습니다.
    *   **단점**: 생체 정보 유출 시 변경이 불가능하여 치명적일 수 있습니다.

이러한 방식들을 두 가지 이상 조합하여 보안을 극대화하는 것을 **[[다중 인증(MFA, Multi-Factor Authentication)]]**이라고 부릅니다.

## 토큰 기반 인증: 현대적인 API를 위한 선택

현대 웹과 모바일 환경에서는 상태를 저장하지 않는(Stateless) RESTful API가 널리 사용됩니다. 이러한 구조에서는 요청마다 사용자를 다시 인증해야 하는 비효율이 발생할 수 있는데, 이를 해결하기 위해 **토큰 기반 인증**이 등장했습니다.

가장 대표적인 기술은 **[[JWT(JSON Web Token)]]**입니다.

```mermaid
sequenceDiagram
    participant Client
    participant Server

    Client->>Server: 아이디/비밀번호로 로그인 요청
    Server->>Server: 사용자 정보 확인
    Server->>Client: 인증 성공 후 JWT 발급
    
    Client->>Server: API 요청 시 JWT를 헤더에 포함
    Server->>Server: JWT 유효성 검증
    Server->>Client: 요청에 대한 응답
```

1.  사용자가 성공적으로 인증되면, 서버는 암호화된 **토큰**을 발급합니다.
2.  클라이언트는 이 토큰을 저장해두고, 서버에 요청을 보낼 때마다 HTTP 헤더에 포함시켜 전송합니다.
3.  서버는 토큰의 유효성을 검증하여 사용자를 신뢰하고 요청을 처리합니다.

이 방식은 서버가 세션을 유지할 필요가 없어 확장성이 뛰어나다는 장점이 있습니다.

## 연합 인증과 SSO: OAuth, OIDC, SAML

여러 서비스가 연동되는 환경에서는 사용자가 각 서비스마다 로그인해야 하는 불편함이 있습니다. 이를 해결하기 위해 등장한 것이 **연합 인증(Federated Authentication)**과 **[[싱글 사인온(SSO, Single Sign-On)]]**입니다.

### [[OAuth 2.0]]

OAuth 2.0은 **인가(Authorization)**를 위한 표준 프로토콜입니다. 사용자가 비밀번호를 직접 노출하지 않고도, 특정 애플리케이션이 다른 애플리케이션의 리소스에 접근할 수 있도록 **권한을 위임**하는 메커니즘을 제공합니다. "Google 계정으로 로그인" 기능이 대표적인 예시입니다.

> **중요**: OAuth 2.0 자체는 인증 프로토콜이 아니라, 인가 프레임워크입니다.

### [[OIDC(OpenID Connect)]]

OIDC는 **OAuth 2.0 위에 구축된 인증 계층**입니다. OAuth 2.0의 인가 흐름을 그대로 활용하면서, **ID 토큰(JWT 형식)**을 추가로 발급하여 사용자의 신원 정보를 표준화된 방식으로 제공합니다. 이를 통해 클라이언트는 사용자가 누구인지 확실하게 인증할 수 있습니다.
> **OIDC = OAuth 2.0 (인가) + 인증**

### SAML(Security Assertion Markup Language)

SAML은 주로 기업 환경에서 SSO를 구현하기 위해 사용되는 XML 기반의 표준입니다. 신원 제공자(IdP)와 서비스 제공자(SP) 간에 인증 정보를 안전하게 교환하여, 한 번의 로그인으로 여러 시스템을 이용할 수 있게 해줍니다.

## Spring Security를 이용한 인증 구현

Spring Security는 스프링 기반 애플리케이션의 보안을 위한 강력한 프레임워크입니다. 복잡한 인증/인가 로직을 직접 구현하는 대신, Spring Security가 제공하는 검증된 모듈을 활용하여 안정성을 높일 수 있습니다.

Spring Security의 핵심 인증 아키텍처는 다음과 같습니다.

```mermaid
graph TD
    A[Client Request] --> B{SecurityFilterChain};
    B --> C{AuthenticationFilter};
    C --> D[AuthenticationManager];
    D --> E[AuthenticationProvider];
    E --> F[UserDetailsService];
    F --> G[DB 등에서 사용자 정보 로드];
    G --> E;
    E --> D;
    D -- 인증 성공 --> H[SecurityContextHolder에 인증 정보 저장];
    H --> I[Controller/Service 실행];
    D -- 인증 실패 --> J[AuthenticationException 발생];
```

*   **`UserDetailsService`**: 사용자 이름(username)으로 데이터베이스 등에서 사용자 정보를 조회합니다.
*   **`AuthenticationProvider`**: `UserDetailsService`가 반환한 정보와 사용자가 입력한 정보를 비교하여 실제 인증을 수행합니다.
*   **`AuthenticationManager`**: `AuthenticationProvider`들을 관리하며 인증 과정을 총괄합니다.

다음은 `UserDetailsService`를 직접 구현하는 예시 코드입니다.

```java
@Service
public class CustomUserDetailsService implements UserDetailsService {

    @Autowired
    private UserRepository userRepository;

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        User user = userRepository.findByUsername(username)
                .orElseThrow(() -> new UsernameNotFoundException("해당 사용자를 찾을 수 없습니다: " + username));

        return new org.springframework.security.core.userdetails.User(
                user.getUsername(),
                user.getPassword(),
                // 사용자 권한 목록 설정
                Collections.singletonList(new SimpleGrantedAuthority("ROLE_USER"))
        );
    }
}
```

이처럼 Spring Security를 활용하면, 개발자는 비즈니스 로직에 더 집중하면서도 견고한 보안 기능을 애플리케이션에 손쉽게 통합할 수 있습니다.

## 결론

인증은 디지털 세계에서 신뢰를 구축하는 첫 단추입니다. 단순한 비밀번호 확인부터 복잡한 연합 인증에 이르기까지, 그 원리와 기술을 정확히 이해하는 것은 안전한 시스템을 만드는 데 필수적입니다.

특히 현대적인 애플리케이션 개발에서는 토큰 기반 인증과 OAuth, OIDC 같은 표준 프로토콜의 중요성이 더욱 커지고 있습니다. Spring Security와 같은 프레임워크를 적극적으로 활용하여, 검증된 방식으로 안전하고 효율적인 인증 시스템을 구축하시길 바랍니다.

## 참고 자료
- Spring Security 공식 문서 (https://spring.io/projects/spring-security)
- OAuth 2.0 공식 사이트 (https://oauth.net/2/)
- OpenID Foundation (https://openid.net/)
- Auth0, Okta 등 인증 솔루션 제공사 기술 블로그
