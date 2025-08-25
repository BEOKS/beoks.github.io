Spring Statemachine은 스프링 애플리케이션 내에서 **상태 머신(State Machine) 개념을 쉽게 사용할 수 있도록 지원하는 프레임워크**입니다. 이 프레임워크는 앞서 살펴본 [[상태 패턴 (State Pattern)]]을 훨씬 더 체계적이고, 강력하며, 선언적인 방식으로 구현할 수 있게 해주는 사실상의 표준 솔루션입니다.

단순히 `if-else` 문을 제거하는 수준을 넘어, 복잡한 상태 전이 로직, 동시성 제어, 계층적 상태 관리 등 엔터프라이즈급 애플리케이션에서 요구되는 다양한 기능들을 제공합니다.

### 왜 직접 구현하지 않고 Spring Statemachine을 사용할까요?

[[상태 패턴 (State Pattern)]] 예제처럼 직접 상태를 관리하는 코드를 작성할 수도 있지만, 비즈니스 로직이 복잡해질수록 다음과 같은 문제에 직면하게 됩니다.

1. **보일러플레이트 코드 증가**: 상태와 전이가 많아질수록 `State` 인터페이스를 구현하는 클래스가 무수히 많아지고, 이를 관리하는 코드가 복잡해집니다.
2. **전이 로직의 복잡성**: 특정 조건이 만족될 때만 상태를 전이시키거나(Guard), 상태가 바뀔 때 특정 액션을 수행(Action)하는 로직을 직접 구현하는 것은 번거롭습니다.
3. **동시성 문제**: 멀티스레드 환경(예: 웹 서버)에서 여러 스레드가 동시에 상태를 변경하려고 할 때, 상태가 일관성 없게 변경될 수 있습니다. 이를 막기 위한 동시성 제어는 매우 어렵습니다.
4. **가시성 부족**: 코드를 일일이 분석하지 않으면 전체 상태가 어떻게 흐르는지 파악하기 어렵습니다.

Spring Statemachine은 이러한 문제들을 **설정 기반의 선언적 방식**으로 해결하여, 개발자가 비즈니스 로직에만 집중할 수 있도록 돕습니다.

### 핵심 개념

Spring Statemachine을 사용하기 위해 알아야 할 핵심 용어는 다음과 같습니다.

- **State (상태)**: 시스템이 머무를 수 있는 특정 상태. (예: `DRAFT`, `IN_REVIEW`, `PUBLISHED`)
- **Event (이벤트)**: 상태를 변경시키는 트리거. (예: `REVIEW_REQUESTED`, `APPROVED`, `REJECTED`)
- **Transition (전이)**: 특정 **이벤트**가 발생했을 때, 한 **상태**에서 다른 **상태**로 변경되는 과정.
- **Action (액션)**: 상태가 **전이**될 때 실행되는 코드. (예: 데이터베이스에 로그 남기기, 이메일 발송)
- **Guard (가드)**: **전이**가 일어나기 위해 반드시 만족해야 하는 조건. `Guard`의 평가 결과가 `true`일 때만 전이가 실행됩니다. (예: 문서를 발행(publish)하려면, 작성자가 관리자 권한을 가지고 있어야 한다.)

```mermaid
graph TD
    A[Source State] -- "Event [Guard] / Action" --> B(Target State)
```

### Spring Boot 시작하기 예제

앞서 다룬 문서 상태 관리 시스템을 Spring Statemachine으로 구현해 보겠습니다.

#### 1. 의존성 추가 (`pom.xml`)

```xml
<dependency>
    <groupId>org.springframework.statemachine</groupId>
    <artifactId>spring-statemachine-core</artifactId>
    <version>4.0.0</version> </dependency>
</dependency>
```

#### 2. 상태(States)와 이벤트(Events) 정의

`enum`을 사용하여 상태와 이벤트를 명확하게 정의하는 것이 일반적입니다.

```java
public enum DocumentStates {
    DRAFT, IN_REVIEW, PUBLISHED
}

public enum DocumentEvents {
    REVIEW, PUBLISH, REJECT
}
```

#### 3. 상태 머신 설정 (`StateMachineConfig.java`)

`@EnableStateMachine` 어노테이션을 사용하여 상태 머신을 활성화하고, `StateMachineConfigurerAdapter`를 상속받아 상태, 전이, 리스너 등을 설정합니다.

```java
import org.springframework.context.annotation.Configuration;
import org.springframework.statemachine.config.EnableStateMachine;
import org.springframework.statemachine.config.EnumStateMachineConfigurerAdapter;
import org.springframework.statemachine.config.builders.StateMachineStateConfigurer;
import org.springframework.statemachine.config.builders.StateMachineTransitionConfigurer;

import java.util.EnumSet;

@Configuration
@EnableStateMachine
public class StateMachineConfig extends EnumStateMachineConfigurerAdapter<DocumentStates, DocumentEvents> {

    // 1. 상태 구성
    @Override
    public void configure(StateMachineStateConfigurer<DocumentStates, DocumentEvents> states) throws Exception {
        states
            .withStates()
                .initial(DocumentStates.DRAFT) // 초기 상태를 DRAFT로 설정
                .states(EnumSet.allOf(DocumentStates.class)); // 모든 enum을 상태로 등록
    }

    // 2. 전이 구성
    @Override
    public void configure(StateMachineTransitionConfigurer<DocumentStates, DocumentEvents> transitions) throws Exception {
        transitions
            // DRAFT 상태에서 REVIEW 이벤트를 받으면 IN_REVIEW 상태로 전이
            .withExternal()
                .source(DocumentStates.DRAFT).target(DocumentStates.IN_REVIEW)
                .event(DocumentEvents.REVIEW)
                .and()
            // IN_REVIEW 상태에서 PUBLISH 이벤트를 받으면 PUBLISHED 상태로 전이
            .withExternal()
                .source(DocumentStates.IN_REVIEW).target(DocumentStates.PUBLISHED)
                .event(DocumentEvents.PUBLISH)
                .action(publishAction()) // 전이 시 액션 실행
                .and()
            // IN_REVIEW 상태에서 REJECT 이벤트를 받으면 DRAFT 상태로 전이
            .withExternal()
                .source(DocumentStates.IN_REVIEW).target(DocumentStates.DRAFT)
                .event(DocumentEvents.REJECT)
                .guard(rejectGuard()); // 특정 가드 조건을 만족해야만 전이
    }
    
    // 3. 액션(Action) 정의
    public Action<DocumentStates, DocumentEvents> publishAction() {
        return context -> System.out.println("발행 액션: 발행 로그를 데이터베이스에 저장합니다.");
    }
    
    // 4. 가드(Guard) 정의
    public Guard<DocumentStates, DocumentEvents> rejectGuard() {
        return context -> {
            // 예시: 요청 헤더에 'isManager' 플래그가 true일 때만 반려 가능
            // Object isManager = context.getMessageHeader("isManager");
            // return isManager != null && (Boolean) isManager;
            System.out.println("가드 평가: 반려 조건을 확인합니다.");
            return true; // 여기서는 간단히 true 반환
        };
    }
}
```

#### 4. 상태 머신 사용하기

서비스 클래스에 `StateMachine`을 주입받아 `sendEvent()` 메서드로 이벤트를 발생시켜 상태를 변경합니다.

```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.statemachine.StateMachine;
import org.springframework.stereotype.Service;

@Service
public class DocumentService {

    private final StateMachine<DocumentStates, DocumentEvents> stateMachine;

    @Autowired
    public DocumentService(StateMachine<DocumentStates, DocumentEvents> stateMachine) {
        this.stateMachine = stateMachine;
    }

    public void reviewDocument() {
        // 상태 머신 시작 (필요한 경우)
        stateMachine.start(); 
        
        // REVIEW 이벤트 전송
        boolean success = stateMachine.sendEvent(DocumentEvents.REVIEW);
        
        System.out.println("REVIEW 이벤트 전송 결과: " + success);
        System.out.println("현재 상태: " + stateMachine.getState().getId());
        
        stateMachine.stop();
    }
}
```

이처럼 Spring Statemachine을 사용하면, 상태 전이에 대한 복잡한 로직이 서비스 코드에서 완전히 분리되고, 설정 클래스에 선언적으로 명시되어 전체 흐름을 이해하고 관리하기가 매우 쉬워집니다.

### 실제 사용 사례

Spring Statemachine은 다음과 같이 명확한 라이프사이클을 가진 객체를 관리하는 데 매우 유용합니다.

- **주문/결제 시스템**: `ORDER_CREATED` -> `PAYMENT_PENDING` -> `PAID` -> `SHIPPED` -> `DELIVERED` / `CANCELLED`
- **작업 흐름 (Workflow) 및 BPM**: `APPROVAL_PENDING` -> `APPROVED` / `REJECTED` -> `CLOSED`
- **사용자 온보딩/인증 절차**: `REGISTERED` -> `EMAIL_VERIFICATION_PENDING` -> `ACTIVE`
- **IoT 장비 제어**: `IDLE` -> `RUNNING` -> `SUSPENDED` -> `SHUTDOWN`

결론적으로, 다수의 상태와 복잡한 전이 규칙을 가진 시스템을 개발한다면, 직접 [[상태 패턴 (State Pattern)]]을 구현하는 것보다 Spring Statemachine을 도입하여 안정성과 유지보수성을 크게 향상시키는 것이 현명한 선택입니다.