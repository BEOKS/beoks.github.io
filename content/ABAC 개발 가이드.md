---
title: "ABAC 개발 가이드 (Attribute-Based Access Control Development Guide)"
---

[[속성 기반 접근 제어]]는 사용자, 리소스, 환경 등 접근 요청과 관련된 다양한 **속성(Attribute)**들을 기반으로 정책을 수립하고, 이 정책에 따라 접근 권한을 동적으로 결정하는 접근 제어 모델입니다. RBAC가 역할에 기반한 정적인 권한 관리에 강점이 있다면, ABAC는 매우 세분화되고 동적인 접근 제어가 필요한 복잡한 환경에 적합합니다.

## 1. ABAC 구현의 핵심 개념

ABAC는 다음과 같은 핵심 개념을 기반으로 작동합니다.

-   **주체 속성 (Subject Attributes)**: 접근을 요청하는 사용자(주체)의 속성입니다. (예: 사용자 ID, 역할, 부서, 직책, 보안 등급, 접속 시간, 위치)
-   **객체 속성 (Object/Resource Attributes)**: 접근 대상이 되는 리소스(객체)의 속성입니다. (예: 파일명, 데이터 민감도, 소유자, 생성일, 프로젝트)
-   **환경 속성 (Environment Attributes)**: 접근이 발생하는 환경에 대한 속성입니다. (예: 현재 시간, 요일, 접속 IP 주소, 접속 기기 유형, 네트워크 보안 수준)
-   **액션 속성 (Action Attributes)**: 주체가 객체에 대해 수행하려는 작업의 속성입니다. (예: 읽기, 쓰기, 삭제, 실행, 수정)
-   **정책 (Policy)**: 속성들을 조합하여 '누가(주체 속성) 무엇을(객체 속성) 언제/어디서(환경 속성) 어떻게(액션 속성) 할 수 있는가'를 정의하는 규칙의 집합입니다. 정책은 일반적으로 "IF [조건] THEN [허용/거부]" 형태로 표현됩니다.

## 2. ABAC 구현의 핵심 단계

ABAC를 시스템에 성공적으로 구현하기 위한 단계는 다음과 같습니다.

### 2.1. 속성 정의 및 수집

시스템 내에서 접근 제어에 활용할 모든 속성을 식별하고, 해당 속성들을 어떻게 수집하고 관리할지 결정합니다.

-   **속성 식별**: 비즈니스 요구사항을 분석하여 접근 제어에 필요한 주체, 객체, 환경, 액션 속성을 정의합니다.
-   **속성 소스**: 속성 정보가 어디에 저장되어 있는지 파악합니다. (예: 사용자 DB, LDAP/AD, 리소스 메타데이터, 시스템 시간, 요청 헤더)
-   **속성 수집 메커니즘**: 런타임에 필요한 속성 정보를 효율적으로 가져올 수 있는 방법을 설계합니다.

### 2.2. 정책 설계 및 작성

정의된 속성들을 기반으로 접근 제어 정책을 설계하고 작성합니다. 정책은 명확하고 구체적이며, 비즈니스 규칙을 정확히 반영해야 합니다.

**정책 예시:**
-   "`finance` 부서의 `manager` 역할인 사용자는 `confidential` 등급의 `financial_report`를 `업무 시간`에만 `읽을` 수 있다."
-   "`개발자` 역할의 사용자는 자신이 `소유`한 `코드 파일`을 `수정`할 수 있다."

정책은 XML (XACML), JSON, YAML 등 다양한 형식으로 표현될 수 있으며, 복잡한 정책을 관리하기 위한 정책 관리 시스템(Policy Administration Point, PAP)을 고려할 수 있습니다.

### 2.3. 정책 결정 엔진 (Policy Decision Point, PDP) 구현

사용자의 접근 요청이 들어왔을 때, 수집된 속성 정보와 정의된 정책을 기반으로 접근 허용 여부를 결정하는 핵심 로직입니다. PDP는 다음과 같은 과정을 거칩니다.

1.  **정책 정보 포인트 (Policy Information Point, PIP)**: 접근 요청에 필요한 속성 정보를 다양한 소스에서 수집합니다.
2.  **정책 실행 포인트 (Policy Enforcement Point, PEP)**: 애플리케이션의 특정 지점(예: API 게이트웨이, 컨트롤러, 서비스 메서드)에서 접근 요청을 가로채고, PDP에 결정을 요청합니다.
3.  **정책 결정 (Decision)**: PDP는 PIP로부터 받은 속성들과 정의된 정책을 비교하여 접근을 허용할지, 거부할지 결정합니다.

```mermaid
graph TD
    A[사용자 요청] --> B{PEP (정책 실행 포인트)};
    B --> C[PDP (정책 결정 엔진)];
    C --> D[PIP (정책 정보 포인트)];
    D --> E[속성 소스 (DB, LDAP, 환경 등)];
    C --> F[PAP (정책 관리 시스템)];
    F --> G[정책 저장소];
    C -- 결정 (허용/거부) --> B;
    B -- 결과 --> A;
```

### 2.4. 정책 실행 포인트 (PEP) 통합

애플리케이션 코드에 PEP를 통합하여 접근 요청을 가로채고 PDP의 결정을 적용합니다. 이는 프레임워크의 보안 기능을 활용하거나, AOP(Aspect-Oriented Programming) 등을 통해 구현할 수 있습니다.

## 3. Spring Security를 활용한 ABAC 구현 (Java 예시)

Spring Security는 기본적으로 RBAC에 강하지만, SpEL(Spring Expression Language)과 커스텀 `PermissionEvaluator`를 활용하여 ABAC와 유사한 세분화된 접근 제어를 구현할 수 있습니다.

### 3.1. `@PreAuthorize`와 SpEL 활용

가장 간단한 ABAC 구현 방법은 `@PreAuthorize` 어노테이션 내에서 SpEL을 사용하여 속성 기반 조건을 직접 명시하는 것입니다.

```java
@Service
public class DocumentService {

    // 문서 소유자이거나 ADMIN 역할인 경우에만 수정 허용
    @PreAuthorize("hasRole('ADMIN') or #document.ownerId == authentication.principal.id")
    public Document updateDocument(Document document) {
        // 문서 수정 로직
        return document;
    }

    // 특정 부서의 사용자만 해당 부서 문서를 읽을 수 있도록 허용
    @PreAuthorize("hasAuthority('DOCUMENT:READ') and #document.department == authentication.principal.department")
    public Document getDocument(Long documentId) {
        // 문서 조회 로직
        // 실제로는 documentId로 문서를 조회한 후 속성 비교
        Document document = findDocumentById(documentId);
        if (document == null) {
            throw new DocumentNotFoundException("Document not found");
        }
        // SpEL에서 #document를 사용하려면 메서드 인자로 Document 객체가 직접 전달되거나,
        // @PostAuthorize를 사용하여 반환된 객체를 평가해야 합니다.
        // 또는 CustomPermissionEvaluator를 사용하는 것이 더 유연합니다.
        return document;
    }
}
```

**주의사항:**
-   SpEL 표현식이 복잡해지면 가독성과 유지보수성이 저하될 수 있습니다.
-   메서드 인자로 전달되는 객체의 속성만 직접 참조할 수 있습니다. 메서드 내부에서 조회되는 객체의 속성을 평가하려면 `CustomPermissionEvaluator`가 더 적합합니다.

### 3.2. CustomPermissionEvaluator 구현

더 복잡하고 재사용 가능한 ABAC 정책을 구현하려면 Spring Security의 `PermissionEvaluator` 인터페이스를 구현하는 것이 좋습니다. 이를 통해 `hasPermission()` SpEL 함수를 사용할 수 있습니다.

```java
// CustomPermissionEvaluator.java
@Component
public class CustomPermissionEvaluator implements PermissionEvaluator {

    @Override
    public boolean hasPermission(Authentication authentication, Object targetDomainObject, Object permission) {
        if ((authentication == null) || (targetDomainObject == null) || !(permission instanceof String)) {
            return false;
        }
        // 예: targetDomainObject가 Document 객체이고, permission이 "read"일 때
        if (targetDomainObject instanceof Document) {
            Document document = (Document) targetDomainObject;
            String perm = (String) permission;

            // 현재 사용자 (authentication.getPrincipal()에서 UserDetails 구현체)의 속성
            MyUserDetails currentUser = (MyUserDetails) authentication.getPrincipal();

            if ("read".equals(perm)) {
                // 문서가 공개(public)이거나, 사용자가 소유자이거나, 같은 부서인 경우 허용
                return document.isPublic() ||
                       document.getOwnerId().equals(currentUser.getId()) ||
                       document.getDepartment().equals(currentUser.getDepartment());
            }
            // 다른 권한(write, delete 등)에 대한 로직 추가
        }
        return false;
    }

    @Override
    public boolean hasPermission(Authentication authentication, Serializable targetId, String targetType, Object permission) {
        // targetId와 targetType을 사용하여 객체를 조회한 후 hasPermission(authentication, Object, Object) 호출
        // 예: targetType이 "Document"이고 targetId로 문서를 조회하여 평가
        if ((authentication == null) || !(permission instanceof String)) {
            return false;
        }
        if ("Document".equals(targetType)) {
            // DB에서 documentId로 Document 객체를 조회하는 로직
            Document document = findDocumentById((Long) targetId);
            return hasPermission(authentication, document, permission);
        }
        return false;
    }

    // 실제 Document 객체를 조회하는 서비스 메서드 (예시)
    private Document findDocumentById(Long id) {
        // 실제 DB 조회 로직
        // 예시: return documentRepository.findById(id).orElse(null);
        return new Document(id, 1L, "Finance", false); // 예시 데이터
    }
}

// SecurityConfig에 CustomPermissionEvaluator 등록
@Configuration
@EnableMethodSecurity // 메서드 수준 보안 활성화
public class SecurityConfig {

    // ... (기존 설정)

    @Bean
    public MethodSecurityExpressionHandler methodSecurityExpressionHandler(CustomPermissionEvaluator permissionEvaluator) {
        DefaultMethodSecurityExpressionHandler expressionHandler = new DefaultMethodSecurityExpressionHandler();
        expressionHandler.setPermissionEvaluator(permissionEvaluator);
        return expressionHandler;
    }
}
```

**사용 예시:**

```java
@Service
public class DocumentService {

    @PreAuthorize("hasPermission(#documentId, 'Document', 'read')")
    public Document getDocument(Long documentId) {
        // 문서 조회 로직
        return findDocumentById(documentId);
    }

    @PreAuthorize("hasPermission(#document, 'write')")
    public Document updateDocument(Document document) {
        // 문서 수정 로직
        return document;
    }
}
```

## 4. ABAC 구현 시 고려사항

-   **복잡성 관리**: ABAC는 매우 유연하지만, 정책이 복잡해질수록 관리와 디버깅이 어려워집니다. 정책을 모듈화하고 명확하게 문서화하는 것이 중요합니다.
-   **성능**: 모든 접근 요청마다 속성을 수집하고 정책을 평가해야 하므로 성능 오버헤드가 발생할 수 있습니다. 속성 캐싱, 정책 최적화, 효율적인 PDP 구현이 필요합니다.
-   **속성 관리**: 속성 정보의 정확성과 최신성을 유지하는 것이 중요합니다. 속성 변경 시 정책 평가에 미치는 영향을 고려해야 합니다.
-   **정책 충돌 해결**: 여러 정책이 동시에 적용될 때 충돌이 발생할 수 있습니다. 명시적인 정책 우선순위 규칙(예: Deny-overrides, Permit-overrides)을 정의해야 합니다.
-   **테스트**: ABAC 정책은 복잡하므로 철저한 테스트가 필수적입니다. 다양한 속성 조합과 엣지 케이스에 대한 테스트 시나리오를 작성해야 합니다.
-   **하이브리드 접근**: 모든 접근 제어를 ABAC로만 구현하기보다, [[역할 기반 접근 제어(RBAC)]]로 기본적인 틀을 잡고 ABAC로 세분화된 동적 제어를 보완하는 하이브리드 방식이 더 실용적일 수 있습니다.

## 결론

ABAC는 현대의 복잡하고 동적인 시스템에서 매우 세분화된 접근 제어를 구현하기 위한 강력한 모델입니다. 속성 정의, 정책 설계, 그리고 정책 결정 엔진 구현이 핵심 단계입니다. Spring Security의 SpEL과 `PermissionEvaluator`를 활용하면 Java 애플리케이션에서 ABAC의 유연성을 효과적으로 활용할 수 있습니다. 하지만 높은 유연성만큼 복잡성도 증가하므로, 신중한 설계와 구현, 그리고 철저한 테스트가 동반되어야 합니다.

## 참고 자료

-   [[속성 기반 접근 제어]]
-   [[역할 기반 접근 제어(RBAC)]]
-   [[RBAC 개발 가이드]]
-   [[최소 권한 원칙]]
-   [[접근 제어 모델]]
-   Spring Security Documentation: [https://docs.spring.io/spring-security/reference/](https://docs.spring.io/spring-security/reference/)
-   NIST Special Publication 800-162, Role-Based Access Control (RBAC)
-   NIST Special Publication 800-166, Attribute-Based Access Control (ABAC) for Next-Generation Access Control Systems
