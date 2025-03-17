# OAuth 2.0: 완벽 가이드
OAuth 2.0은 사용자의 비밀번호를 공유하지 않고도 제3자 애플리케이션이 사용자의 보호된 리소스에 접근할 수 있게 해주는 [[인증(Authentication)]]과 [[인가(Authorization)]] 프레임워크입니다. 2012년 IETF(Internet Engineering Task Force)에 의해 RFC 6749로 표준화되었으며, 현재 웹과 모바일 애플리케이션에서 가장 널리 사용되는 인증 프로토콜 중 하나입니다.

기존 인증 방식에서는 사용자가 제3자 애플리케이션에 자신의 계정 정보(아이디/비밀번호)를 직접 제공해야 했지만, OAuth 2.0을 사용하면 사용자는 ID 제공자(Identity Provider)를 통해 인증한 후, 특정 리소스에 대한 접근 권한만 제3자 애플리케이션에 위임할 수 있습니다. 이러한 방식으로 사용자는 보안을 유지하면서도 다양한 서비스를 연동하여 사용할 수 있습니다.

## OAuth 2.0의 주요 구성요소

OAuth 2.0에는 네 가지 주요 역할이 있습니다:

1. **리소스 소유자(Resource Owner)**: 보호된 리소스에 접근 권한을 부여할 수 있는 개체로, 일반적으로 최종 사용자입니다.
    
2. **리소스 서버(Resource Server)**: 보호된 리소스를 호스팅하고 액세스 토큰을 사용하여 요청을 수락하고 응답하는 서버입니다.
    
3. **클라이언트(Client)**: 리소스 소유자의 보호된 리소스에 접근하려는 애플리케이션입니다. 클라이언트는 웹 애플리케이션, 모바일 앱, 데스크톱 애플리케이션 등 다양한 형태가 될 수 있습니다.
    
4. **인증 서버(Authorization Server)**: 리소스 소유자를 인증하고 권한 부여를 받은 후 클라이언트에게 액세스 토큰을 발급하는 서버입니다.
    

이러한 역할들의 상호작용을 통해 OAuth 2.0은 사용자의 인증 정보를 직접 공유하지 않고도 안전하게 리소스에 접근할 수 있는 방법을 제공합니다.

## 인증 흐름(Grant Type)

OAuth 2.0은 다양한 유형의 클라이언트와 사용 사례를 지원하기 위해 여러 가지 인증 흐름(Grant Type)을 정의합니다. 각 흐름은 특정 시나리오와 보안 요구사항에 맞게 설계되었습니다.

### 권한 부여 코드 흐름(Authorization Code Flow)

가장 일반적으로 사용되는 흐름으로, 웹 애플리케이션에 적합합니다. 이 흐름은 백엔드 서버에서 클라이언트 비밀을 안전하게 보관할 수 있는 환경에 최적화되어 있습니다.

```mermaid
sequenceDiagram
    participant 사용자 as 사용자(리소스 소유자)
    participant 클라이언트 as 클라이언트
    participant 인증서버 as 인증 서버
    participant 리소스서버 as 리소스 서버
    
    사용자->>클라이언트: 1. 서비스 접근
    클라이언트->>사용자: 2. 인증 서버로 리다이렉트
    사용자->>인증서버: 3. 인증 요청
    인증서버->>사용자: 4. 로그인 및 권한 동의 화면
    사용자->>인증서버: 5. 로그인 및 권한 동의
    인증서버->>사용자: 6. 권한 부여 코드와 함께 리다이렉트
    사용자->>클라이언트: 7. 권한 부여 코드 전달
    클라이언트->>인증서버: 8. 권한 부여 코드로 토큰 요청
    Note right of 클라이언트: client_id, client_secret, code, redirect_uri 포함
    인증서버->>클라이언트: 9. 액세스 토큰 및 리프레시 토큰 발급
    클라이언트->>리소스서버: 10. 액세스 토큰으로 리소스 요청
    리소스서버->>클라이언트: 11. 요청한 리소스 반환
```

### 암묵적 흐름(Implicit Flow)

단일 페이지 애플리케이션(SPA)과 같이 클라이언트 측 JavaScript 애플리케이션에 적합한 간소화된 흐름입니다. 권한 부여 코드 없이 바로 액세스 토큰이 발급되지만, 보안상 권한 부여 코드 흐름에 비해 취약점이 있습니다.

```mermaid
sequenceDiagram
    participant 사용자 as 사용자(리소스 소유자)
    participant 클라이언트 as 클라이언트(브라우저)
    participant 인증서버 as 인증 서버
    participant 리소스서버 as 리소스 서버
    
    사용자->>클라이언트: 1. 서비스 접근
    클라이언트->>사용자: 2. 인증 서버로 리다이렉트
    사용자->>인증서버: 3. 인증 요청
    인증서버->>사용자: 4. 로그인 및 권한 동의 화면
    사용자->>인증서버: 5. 로그인 및 권한 동의
    인증서버->>사용자: 6. 액세스 토큰과 함께 리다이렉트(URI Fragment)
    사용자->>클라이언트: 7. 액세스 토큰 전달
    클라이언트->>리소스서버: 8. 액세스 토큰으로 리소스 요청
    리소스서버->>클라이언트: 9. 요청한 리소스 반환
```

> **참고**: 보안상의 이유로 OAuth 2.0 보안 최적화(OAuth 2.0 Security Best Current Practice)에서는 새로운 애플리케이션에서 암묵적 흐름 대신 Authorization Code Flow with PKCE를 사용할 것을 권장하고 있습니다.

### 리소스 소유자 비밀번호 자격 증명 흐름(Resource Owner Password Credentials Flow)

사용자의 이름과 비밀번호를 직접 사용하여 액세스 토큰을 얻는 흐름입니다. 높은 신뢰도를 가진 애플리케이션(자사 애플리케이션)에서만 제한적으로 사용해야 합니다.

```mermaid
sequenceDiagram
    participant 사용자 as 사용자(리소스 소유자)
    participant 클라이언트 as 클라이언트
    participant 인증서버 as 인증 서버
    participant 리소스서버 as 리소스 서버
    
    사용자->>클라이언트: 1. 사용자명/비밀번호 제공
    클라이언트->>인증서버: 2. 사용자 자격 증명으로 토큰 요청
    인증서버->>클라이언트: 3. 액세스 토큰 및 리프레시 토큰 발급
    클라이언트->>리소스서버: 4. 액세스 토큰으로 리소스 요청
    리소스서버->>클라이언트: 5. 요청한 리소스 반환
```

### 클라이언트 자격 증명 흐름(Client Credentials Flow)

사용자 컨텍스트가 없는 서버 간 통신에 사용됩니다. 클라이언트가 자신의 자격 증명을 사용하여 직접 액세스 토큰을 요청합니다.

```mermaid
sequenceDiagram
    participant 클라이언트 as 클라이언트(서버)
    participant 인증서버 as 인증 서버
    participant 리소스서버 as 리소스 서버
    
    클라이언트->>인증서버: 1. 클라이언트 자격 증명으로 토큰 요청
    인증서버->>클라이언트: 2. 액세스 토큰 발급
    클라이언트->>리소스서버: 3. 액세스 토큰으로 리소스 요청
    리소스서버->>클라이언트: 4. 요청한 리소스 반환
```

## 토큰 유형

OAuth 2.0에서 사용되는 주요 토큰 유형에 대해 알아보겠습니다.

### 액세스 토큰(Access Token)

보호된 리소스에 접근하기 위한 자격 증명으로 사용되는 토큰입니다. 액세스 토큰은 일반적으로 짧은 수명(보통 몇 시간 또는 그 이하)을 가지며, 다양한 형식(JWT, 불투명 토큰 등)으로 구현될 수 있습니다.

액세스 토큰은 다음과 같은 방식으로 리소스 서버에 전달됩니다:

```
GET /api/user/profile HTTP/1.1
Host: example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 리프레시 토큰(Refresh Token)

액세스 토큰이 만료된 후 새로운 액세스 토큰을 발급받기 위해 사용하는 토큰입니다. 리프레시 토큰은 액세스 토큰보다 긴 수명을 가지며, 사용자가 매번 재인증하지 않아도 되게 합니다.

```java
// 리프레시 토큰을 사용하여 새로운 액세스 토큰 요청 예시
@Service
public class TokenRefreshService {

    @Autowired
    private RestTemplate restTemplate;
    
    @Value("${oauth2.client.id}")
    private String clientId;
    
    @Value("${oauth2.client.secret}")
    private String clientSecret;
    
    @Value("${oauth2.token.endpoint}")
    private String tokenEndpoint;
    
    public TokenResponse refreshAccessToken(String refreshToken) {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_FORM_URLENCODED);
        
        MultiValueMap<String, String> map = new LinkedMultiValueMap<>();
        map.add("grant_type", "refresh_token");
        map.add("refresh_token", refreshToken);
        map.add("client_id", clientId);
        map.add("client_secret", clientSecret);
        
        HttpEntity<MultiValueMap<String, String>> request = new HttpEntity<>(map, headers);
        
        ResponseEntity<TokenResponse> response = restTemplate.postForEntity(
            tokenEndpoint, request, TokenResponse.class);
        
        return response.getBody();
    }
    
    // 토큰 응답을 위한 DTO 클래스
}
```

### ID 토큰

[[OpenID Connect]]에서 도입된 개념으로, 사용자의 신원 정보를 포함하는 JWT(JSON Web Token) 형식의 토큰입니다. ID 토큰은 인증의 결과로, 사용자의 프로필 정보를 포함합니다.

## 스프링 부트에서 OAuth 2.0 구현하기

스프링 부트는 OAuth 2.0을 쉽게 구현할 수 있는 다양한 라이브러리와 기능을 제공합니다. 여기서는 OAuth 2.0의 각 역할(클라이언트, 리소스 서버, 인증 서버)을 스프링 부트에서 구현하는 방법을 살펴보겠습니다.

### OAuth 2.0 클라이언트 구현

Spring Security OAuth2 Client를 사용하면 OAuth 2.0 클라이언트를 쉽게 구현할 수 있습니다.

```java
// build.gradle
dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-oauth2-client'
    implementation 'org.springframework.boot:spring-boot-starter-web'
}
```

```java
// application.yml
spring:
  security:
    oauth2:
      client:
        registration:
          github:
            client-id: your-client-id
            client-secret: your-client-secret
            scope: read:user
          google:
            client-id: your-google-client-id
            client-secret: your-google-client-secret
            scope: profile,email
```

```java
// SecurityConfig.java
@Configuration
@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {
    
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
            .authorizeRequests(authorize -> authorize
                .antMatchers("/", "/login**", "/error**").permitAll()
                .anyRequest().authenticated()
            )
            .oauth2Login(oauth2 -> oauth2
                .loginPage("/login")
                .defaultSuccessUrl("/home", true)
            );
    }
}
```

### OAuth 2.0 리소스 서버 구현

Spring Security OAuth2 Resource Server를 사용하여 리소스 서버를 구현할 수 있습니다.

```java
// build.gradle
dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-oauth2-resource-server'
    implementation 'org.springframework.boot:spring-boot-starter-web'
}
```

```java
// application.yml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://your-auth-server.com
          jwk-set-uri: https://your-auth-server.com/.well-known/jwks.json
```

```java
// ResourceServerConfig.java
@Configuration
@EnableWebSecurity
public class ResourceServerConfig extends WebSecurityConfigurerAdapter {
    
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
            .authorizeRequests(authorize -> authorize
                .antMatchers("/public/**").permitAll()
                .anyRequest().authenticated()
            )
            .oauth2ResourceServer(oauth2 -> oauth2
                .jwt(jwt -> jwt
                    .jwtAuthenticationConverter(jwtAuthenticationConverter())
                )
            );
    }
    
    private JwtAuthenticationConverter jwtAuthenticationConverter() {
        JwtGrantedAuthoritiesConverter jwtGrantedAuthoritiesConverter = new JwtGrantedAuthoritiesConverter();
        jwtGrantedAuthoritiesConverter.setAuthoritiesClaimName("roles");
        jwtGrantedAuthoritiesConverter.setAuthorityPrefix("ROLE_");
        
        JwtAuthenticationConverter jwtAuthenticationConverter = new JwtAuthenticationConverter();
        jwtAuthenticationConverter.setJwtGrantedAuthoritiesConverter(jwtGrantedAuthoritiesConverter);
        return jwtAuthenticationConverter;
    }
}
```

### OAuth 2.0 인증 서버 구현

Spring Boot 2.0 이후부터 Spring Security OAuth 프로젝트는 더 이상 적극적으로 유지보수되지 않고, Spring Authorization Server 프로젝트가 개발되고 있습니다. 여기서는 Spring Authorization Server를 사용한 구현 예시를 살펴보겠습니다.

```java
// build.gradle
dependencies {
    implementation 'org.springframework.security:spring-security-oauth2-authorization-server:0.3.1'
    implementation 'org.springframework.boot:spring-boot-starter-web'
    implementation 'org.springframework.boot:spring-boot-starter-security'
}
```

```java
// AuthorizationServerConfig.java
@Configuration
@EnableWebSecurity
public class AuthorizationServerConfig {

    @Bean
    @Order(1)
    public SecurityFilterChain authorizationServerSecurityFilterChain(HttpSecurity http) throws Exception {
        OAuth2AuthorizationServerConfiguration.applyDefaultSecurity(http);
        
        return http
            .exceptionHandling(exceptions ->
                exceptions.authenticationEntryPoint(
                    new LoginUrlAuthenticationEntryPoint("/login"))
            )
            .build();
    }

    @Bean
    @Order(2)
    public SecurityFilterChain standardSecurityFilterChain(HttpSecurity http) throws Exception {
        return http
            .formLogin(withDefaults())
            .authorizeHttpRequests(authorize ->
                authorize.anyRequest().authenticated()
            )
            .build();
    }

    @Bean
    public RegisteredClientRepository registeredClientRepository() {
        RegisteredClient client = RegisteredClient.withId(UUID.randomUUID().toString())
            .clientId("client")
            .clientSecret("{noop}secret")
            .clientAuthenticationMethod(ClientAuthenticationMethod.CLIENT_SECRET_BASIC)
            .authorizationGrantType(AuthorizationGrantType.AUTHORIZATION_CODE)
            .authorizationGrantType(AuthorizationGrantType.REFRESH_TOKEN)
            .redirectUri("http://127.0.0.1:8080/login/oauth2/code/client")
            .scope("read")
            .scope("write")
            .build();

        return new InMemoryRegisteredClientRepository(client);
    }

    @Bean
    public JWKSource<SecurityContext> jwkSource() {
        RSAKey rsaKey = generateRsa();
        JWKSet jwkSet = new JWKSet(rsaKey);
        return (jwkSelector, securityContext) -> jwkSelector.select(jwkSet);
    }

    private static RSAKey generateRsa() {
        KeyPair keyPair = generateRsaKey();
        RSAPublicKey publicKey = (RSAPublicKey) keyPair.getPublic();
        RSAPrivateKey privateKey = (RSAPrivateKey) keyPair.getPrivate();
        return new RSAKey.Builder(publicKey)
            .privateKey(privateKey)
            .keyID(UUID.randomUUID().toString())
            .build();
    }

    private static KeyPair generateRsaKey() {
        try {
            KeyPairGenerator keyPairGenerator = KeyPairGenerator.getInstance("RSA");
            keyPairGenerator.initialize(2048);
            return keyPairGenerator.generateKeyPair();
        } catch (Exception ex) {
            throw new IllegalStateException(ex);
        }
    }

    @Bean
    public ProviderSettings providerSettings() {
        return ProviderSettings.builder()
            .issuer("http://auth-server:9000")
            .build();
    }
}
```

## 보안 고려사항

OAuth 2.0을 구현할 때 고려해야 할 몇 가지 중요한 보안 사항이 있습니다:

1. **HTTPS 사용**: 모든 OAuth 2.0 엔드포인트는 HTTPS(TLS)를 통해 보호되어야 합니다.
    
2. **상태 매개변수(state parameter) 사용**: CSRF(Cross-Site Request Forgery) 공격을 방지하기 위해 권한 부여 요청에 상태 매개변수를 포함하고 콜백 시 검증해야 합니다.
    
3. **PKCE(Proof Key for Code Exchange) 사용**: 모바일 애플리케이션이나 단일 페이지 애플리케이션에서는 PKCE를 사용하여 인증 코드 가로채기 공격을 방지해야 합니다.
    
4. **토큰 저장**: 액세스 토큰과 리프레시 토큰은 안전하게 저장해야 합니다. 브라우저 환경에서는 HttpOnly 쿠키를 사용하는 것이 좋습니다.
    
5. **클라이언트 비밀 보호**: 클라이언트 비밀은 노출되지 않도록 서버 측 코드에만 저장해야 합니다.
    
6. **스코프 제한**: 애플리케이션이 요청하는 권한(스코프)은 필요한 최소한으로 제한해야 합니다.
    

## 모범 사례

OAuth 2.0을 구현할 때 다음과 같은 모범 사례를 따르는 것이 좋습니다:

1. **최신 흐름 사용**: 새로운 애플리케이션에서는 가능한 한 권한 부여 코드 흐름(PKCE와 함께)을 사용하세요.
    
2. **짧은 수명의 액세스 토큰**: 액세스 토큰의 수명은 짧게(1시간 이하) 설정하고, 필요한 경우 리프레시 토큰을 사용하여 갱신하세요.
    
3. **토큰 검증**: 리소스 서버는 액세스 토큰의 서명, 발급자, 대상, 만료 시간 등을 철저히 검증해야 합니다.
    
4. **에러 처리**: 자세한 오류 정보는 노출하지 않고, 표준 OAuth 2.0 오류 코드를 사용하세요.
    
5. **로깅과 모니터링**: 인증 및 권한 부여 관련 이벤트를 로깅하고 모니터링하여 이상 징후를 탐지하세요.
    

## 마치며

OAuth 2.0은 강력하고 유연한 인증 및 권한 부여 프레임워크이지만, 올바르게 구현하기 위해서는 여러 보안 고려사항과 모범 사례를 이해하고 따라야 합니다. 이 글에서는 OAuth 2.0의 기본 개념, 주요 구성요소, 다양한 인증 흐름, 그리고 스프링 부트에서의 구현 방법에 대해 살펴보았습니다.

실제 애플리케이션에서 OAuth 2.0을 구현할 때는 사용 사례와 보안 요구사항에 맞는 적절한 흐름을 선택하고, 최신 보안 권장 사항을 따르는 것이 중요합니다. 또한 OAuth 2.0은 계속 발전하고 있으므로, 최신 표준과 모범 사례를 주기적으로 확인하는 것이 좋습니다.

## 참고 자료

- [OAuth 2.0 공식 문서 (RFC 6749)](https://tools.ietf.org/html/rfc6749)
- [OAuth 2.0 위협 모델 및 보안 고려사항 (RFC 6819)](https://tools.ietf.org/html/rfc6819)
- [OAuth 2.0 보안 최적화 (BCP)](https://tools.ietf.org/html/draft-ietf-oauth-security-topics)