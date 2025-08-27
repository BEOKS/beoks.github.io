책임 연쇄 패턴은 **요청을 보내는 쪽(Sender)과 요청을 처리하는 쪽(Receiver)을 분리(decoupling)하고, 여러 객체에게 요청을 처리할 기회를 주는** 행위 디자인 패턴입니다.

이 패턴은 객체들을 마치 사슬처럼 연결하여, 요청이 해결될 때까지 사슬을 따라 차례대로 전달되게 합니다. 가장 직관적인 예시는 회사의 경비 승인 절차입니다.

1. 직원이 경비 지출 요청서를 제출합니다.
2. **팀장**이 요청을 받고, 자신의 승인 한도(예: 50만 원 미만) 내에 있는지 확인합니다. 한도 내라면 승인하고 절차를 종료합니다.
3. 한도를 초과하면, 팀장은 요청을 **부서장**에게 넘깁니다.
4. **부서장** 역시 자신의 한도(예: 300만 원 미만)를 확인하고, 처리할 수 없으면 **본부장**에게 넘깁니다.

이 과정에서 요청을 제출한 직원은 최종적으로 누가 이 요청을 승인하게 될지 알 필요가 없습니다. 그저 첫 번째 책임자인 팀장에게 요청을 보낼 뿐입니다. 이처럼 요청을 보내는 쪽과 처리하는 쪽의 결합을 끊고, 처리 객체들을 유연하게 연결하는 것이 이 패턴의 핵심입니다.

### 핵심 구성 요소

- **Handler (핸들러 인터페이스)**: 요청을 처리하는 모든 객체들의 공통 인터페이스입니다. 요청을 처리하는 메서드(예: `handleRequest`)와, 다음 핸들러를 설정하는 메서드(`setNext`)를 정의합니다.
- **ConcreteHandler (구체적인 핸들러)**: `Handler` 인터페이스를 구현한 클래스입니다. 자신이 요청을 처리할 수 있는지 확인하고, 처리할 수 있다면 요청을 처리합니다. 처리할 수 없다면, 자신이 연결하고 있는 다음 핸들러에게 요청을 그대로 전달합니다.
- **Client (클라이언트)**: `ConcreteHandler`들을 생성하고, 이들을 체인으로 엮습니다. 그리고 첫 번째 핸들러에게 요청을 보냄으로써 전체 프로세스를 시작합니다.

```mermaid
graph TD
    Client --> HandlerA;
    subgraph Chain
        direction LR
        HandlerA -- "처리 못하면 전달" --> HandlerB;
        HandlerB -- "처리 못하면 전달" --> HandlerC;
        HandlerC -- "처리 못하면 전달" --> End;
    end
```

### Java 예시 코드: 경비 승인 시스템

앞서 설명한 경비 승인 시스템을 코드로 구현해 보겠습니다.

```java
// 요청 정보를 담는 클래스
class ExpenseReport {
    private final double amount;
    public ExpenseReport(double amount) { this.amount = amount; }
    public double getAmount() { return amount; }
}

// Handler 추상 클래스
abstract class Approver {
    protected Approver nextApprover; // 다음 승인자 (체인의 다음 링크)

    public void setNext(Approver approver) {
        this.nextApprover = approver;
    }

    // 요청을 처리하는 템플릿
    public abstract void processRequest(ExpenseReport report);
}

// ConcreteHandler 1: 팀장
class TeamLead extends Approver {
    private final double approvalLimit = 500_000;

    @Override
    public void processRequest(ExpenseReport report) {
        if (report.getAmount() < approvalLimit) {
            System.out.println("팀장이 승인했습니다. (금액: " + report.getAmount() + ")");
        } else if (nextApprover != null) {
            System.out.println("팀장 승인 불가. 부서장에게 요청을 전달합니다.");
            nextApprover.processRequest(report);
        }
    }
}

// ConcreteHandler 2: 부서장
class DepartmentManager extends Approver {
    private final double approvalLimit = 3_000_000;

    @Override
    public void processRequest(ExpenseReport report) {
        if (report.getAmount() < approvalLimit) {
            System.out.println("부서장이 승인했습니다. (금액: " + report.getAmount() + ")");
        } else if (nextApprover != null) {
            System.out.println("부서장 승인 불가. 본부장에게 요청을 전달합니다.");
            nextApprover.processRequest(report);
        } else {
            System.out.println("아무도 승인할 수 없는 금액입니다.");
        }
    }
}
// ... 본부장 클래스도 유사하게 구현 가능

// Client
public class Application {
    public static void main(String[] args) {
        // 1. 핸들러(승인자) 생성
        Approver teamLead = new TeamLead();
        Approver manager = new DepartmentManager();
        // ...

        // 2. 체인으로 연결
        teamLead.setNext(manager);

        // 3. 요청 시작
        teamLead.processRequest(new ExpenseReport(300_000));  // 팀장이 처리
        System.out.println("---");
        teamLead.processRequest(new ExpenseReport(1_500_000)); // 부서장이 처리
        System.out.println("---");
        teamLead.processRequest(new ExpenseReport(5_000_000)); // 아무도 처리 못함
    }
}
```

### 스프링 프레임워크에서의 활용: 서블릿 필터(Servlet Filter)와 Spring Security

책임 연쇄 패턴의 가장 대표적이고 강력한 실제 사용 사례는 Java 웹 애플리케이션의 **서블릿 필터 체인**과 **Spring Security**입니다.

클라이언트로부터 들어온 HTTP 요청은 실제 컨트롤러의 메서드에 도달하기 전에 여러 개의 필터로 구성된 체인을 통과합니다.

1. **`CharacterEncodingFilter`**: 요청의 인코딩을 UTF-8로 설정합니다. 작업을 마친 후, 다음 필터로 요청을 넘깁니다.
2. **`CorsFilter`**: CORS(Cross-Origin Resource Sharing) 관련 헤더를 검사하고 처리합니다. 작업을 마친 후, 다음 필터로 요청을 넘깁니다.
3. **`UsernamePasswordAuthenticationFilter` (Spring Security)**: `/login`과 같은 특정 URL의 요청을 가로채 사용자 인증을 시도합니다. 인증에 성공하면 다음 필터로, 실패하면 요청을 중단하고 에러 응답을 보냅니다.
4. **`AuthorizationFilter` (Spring Security)**: 인증된 사용자가 해당 요청에 접근할 권한이 있는지 확인합니다. 권한이 없으면 요청을 중단합니다.
5. ... (기타 여러 필터)
6. **`DispatcherServlet`**: 모든 필터를 통과한 후에야 비로소 요청이 최종 목적지인 스프링의 `DispatcherServlet`에 도달합니다.

각 필터는 `javax.servlet.Filter` 인터페이스의 `doFilter` 메서드를 구현합니다.

```java
public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) 
        throws IOException, ServletException {
    
    // 1. 요청에 대한 선처리 (예: 인코딩 설정)
    System.out.println("필터 A: 선처리 작업");

    // 2. 체인의 다음 필터 호출
    chain.doFilter(request, response);

    // 3. 응답에 대한 후처리 (모든 체인이 끝난 후 실행됨)
    System.out.println("필터 A: 후처리 작업");
}
```

`chain.doFilter(request, response)`를 호출하는 부분이 바로 **"다음 핸들러에게 요청을 전달하는"** 책임 연쇄 패턴의 핵심입니다. 만약 특정 필터가 이 호출을 생략하면, 그 뒤의 모든 필터와 컨트롤러는 실행될 기회조차 얻지 못하고 요청 처리가 중단됩니다. 이 구조 덕분에 인증, 인가, 로깅, CORS 등 웹 애플리케이션의 다양한 횡단 관심사(cross-cutting concerns)를 각각의 필터라는 독립적인 모듈로 분리하여 체계적으로 관리할 수 있습니다.

### 장점과 단점

#### 장점

- **결합도 감소**: 요청자와 수신자 간의 결합도를 낮춥니다. 요청자는 체인의 구조나 누가 요청을 처리하는지 알 필요가 없습니다.
- **유연성 및 단일 책임 원칙**: 각 핸들러는 자신의 책임에만 집중합니다. 또한, 런타임에 체인의 순서를 바꾸거나 새로운 핸들러를 추가/삭제하는 것이 용이합니다.

#### 단점

- **처리 보장 불가**: 체인의 끝까지 도달했음에도 불구하고 요청이 처리되지 않을 가능성이 존재합니다.
- **디버깅의 어려움**: 요청이 여러 핸들러를 거치면서 처리되므로, 로직의 흐름을 추적하기가 다소 복잡할 수 있습니다.
- **성능 저하 가능성**: 체인이 길어질 경우, 요청이 처리되기까지 여러 객체를 거치면서 약간의 성능 저하가 발생할 수 있습니다.