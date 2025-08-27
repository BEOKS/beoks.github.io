[[MCP Server]]에서 **프롬프트(Prompt)**는 단순히 AI에게 전달하는 요청 문장을 넘어, 재사용 가능하고 동적으로 구성할 수 있는 **'대화의 틀' 또는 '작업 지시서'** 역할을 합니다. MCP는 프롬프트를 일회성 텍스트가 아닌, 명확한 명세를 가진 하나의 독립된 개체로 취급하며, 이를 통해 프롬프트의 체계적인 관리와 재사용을 가능하게 합니다.

이 문서는 MCP 서버 환경에서 프롬프트를 정의하고, 동적 로직을 담은 제공자(Provider)를 구현하며, 이를 서버에 등록하여 관리하는 방법을 설명합니다.

---

## 1. 프롬프트(Prompt)의 구성 요소

MCP에서 프롬프트는 클라이언트가 그 용도와 사용법을 명확히 알 수 있도록 구조화된 정보를 가집니다.

1. **이름 (Name)**
    
    - 프롬프트를 고유하게 식별하는 ID입니다. (예: `summarize-text`, `translate-to-english`)
    - 클라이언트는 이 이름을 사용해 특정 프롬프트 템플릿을 서버에 요청합니다.
2. **설명 (Description)**
    
    - 해당 프롬프트가 어떤 목적을 가지고 있으며, 어떤 결과물을 생성하는지에 대한 설명입니다.
    - 개발자가 프롬프트의 용도를 쉽게 파악하고 선택하는 데 도움을 줍니다.
    - 예시: "주어진 텍스트를 세 개의 핵심 문장으로 요약합니다."
3. **인자 (Arguments)**
    
    - 프롬프트 템플릿을 동적으로 완성하기 위해 필요한 변수들의 명세입니다. 각 인자는 `이름`, `설명`, `필수 여부`를 가집니다.
    - 이 인자 덕분에 하나의 프롬프트 템플릿을 다양한 상황에 맞춰 재사용할 수 있습니다.
    - **예시**: `summarize-text` 프롬프트는 '요약할 원본 텍스트'를 전달받기 위해 `originalText`라는 인자를 가질 수 있습니다.

---

## 2. Spring Boot로 프롬프트 제공자(Provider) 구현하기

**프롬프트 제공자(Provider)** 는 프롬프트의 실제 내용을 생성하는 로직을 담은 함수 또는 메서드입니다. 클라이언트가 특정 프롬프트의 생성을 요청(`GetPromptRequest`)하면, 제공자는 요청에 포함된 인자(Arguments)를 사용하여 최종적인 대화 메시지 목록(`PromptMessage`)을 만들어 반환(`GetPromptResult`)합니다.

다음은 '버그 리포트'를 입력받아 '요약 및 분석'을 지시하는 프롬프트를 생성하는 제공자를 Spring Boot로 구현한 예시입니다.

```java
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.ArrayList;
import java.util.Map;

// 프롬프트 제공 로직을 담당하는 서비스
@Service
public class PromptProviderService {

    /**
     * 'bug-report-analysis' 프롬프트 제공자입니다.
     * @param arguments 클라이언트가 보낸 인자 (예: {"reportContent": "앱이 자꾸 멈춰요..."})
     * @return 생성된 프롬프트 메시지가 담긴 결과 객체
     */
    public GetPromptResult getBugReportAnalysisPrompt(Map<String, String> arguments) {
        String reportContent = arguments.get("reportContent");

        // 필수 인자가 없는 경우 에러 처리 (실제로는 MCP 오류 응답을 생성해야 함)
        if (reportContent == null || reportContent.isBlank()) {
            throw new IllegalArgumentException("인자 'reportContent'가 비어있습니다.");
        }

        // 1. 프롬프트 메시지 목록을 생성합니다.
        List<PromptMessage> messages = new ArrayList<>();

        // 2. 시스템(또는 어시스턴트) 역할을 통해 AI에게 기본 지시사항을 전달합니다.
        messages.add(new PromptMessage(
            "system",
            "당신은 버그 리포트 분석 전문가입니다. 다음 사용자 버그 리포트를 읽고, 문제 원인을 추정하고 해결 방안을 제시해주세요."
        ));

        // 3. 사용자 역할을 통해 실제 버그 리포트 내용을 전달합니다.
        messages.add(new PromptMessage(
            "user",
            reportContent
        ));

        // 4. 완성된 메시지 목록을 GetPromptResult에 담아 반환합니다.
        return new GetPromptResult(
            "버그 리포트 분석 및 해결 방안 제시 프롬프트",
            messages
        );
    }

    // --- MCP SDK의 데이터 클래스를 가상으로 구현한 Helper 클래스들 ---

    public static class PromptMessage {
        private final String role;
        private final String content;
        public PromptMessage(String role, String content) {
            this.role = role;
            this.content = content;
        }
        // Getters...
    }

    public static class GetPromptResult {
        private final String description;
        private final List<PromptMessage> messages;
        public GetPromptResult(String description, List<PromptMessage> messages) {
            this.description = description;
            this.messages = messages;
        }
        // Getters...
    }
}
```

이처럼 프롬프트 제공자는 단순한 텍스트 반환을 넘어, AI의 역할(Role)을 지정하고 여러 차례의 대화(Multi-turn) 형식을 미리 구성하는 등 정교한 상호작용을 설계할 수 있게 해줍니다.

---

## 3. 서버에 프롬프트 등록 및 관리

구현된 프롬프트 제공자는 [[MCP 서버 도구 등록 및 관리|도구와 마찬가지로]] 서버의 레지스트리에 등록되어야 클라이언트가 사용할 수 있습니다.

다음은 프롬프트를 관리하는 `McpPromptManager`의 개념적인 예시입니다.

```java
import org.springframework.stereotype.Component;
import javax.annotation.PostConstruct;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.function.Function;

@Component
public class McpPromptManager {

    // 프롬프트 이름과 제공자(Provider) 함수를 매핑하는 저장소
    private final Map<String, Function<Map<String, String>, PromptProviderService.GetPromptResult>> promptRegistry = new ConcurrentHashMap<>();
    
    private final PromptProviderService promptProviderService;
    private final McpNotificationService mcpNotificationService;

    public McpPromptManager(PromptProviderService promptProviderService, McpNotificationService mcpNotificationService) {
        this.promptProviderService = promptProviderService;
        this.mcpNotificationService = mcpNotificationService;
    }

    // 서버 시작 시, 프롬프트들을 자동으로 등록합니다.
    @PostConstruct
    public void initializePrompts() {
        addPrompt("bug-report-analysis", promptProviderService::getBugReportAnalysisPrompt);
        // ... 다른 프롬프트들 등록 ...
    }

    /**
     * 서버에 새로운 프롬프트를 등록합니다.
     * @param name 프롬프트 이름
     * @param provider 프롬프트 제공자 로직
     */
    public void addPrompt(String name, Function<Map<String, String>, PromptProviderService.GetPromptResult> provider) {
        promptRegistry.put(name, provider);
        System.out.println("프롬프트 등록됨: " + name);
        
        // 프롬프트 목록 변경을 클라이언트에게 알립니다.
        mcpNotificationService.sendPromptListChanged();
    }

    /**
     * 등록된 프롬프트를 제거합니다.
     * @param name 제거할 프롬프트 이름
     */
    public void removePrompt(String name) {
        if (promptRegistry.remove(name) != null) {
            System.out.println("프롬프트 제거됨: " + name);
            mcpNotificationService.sendPromptListChanged();
        }
    }

    public Function<Map<String, String>, PromptProviderService.GetPromptResult> getPromptProvider(String name) {
        return promptRegistry.get(name);
    }
}
```

---

## 4. 동적 프롬프트 관리와 클라이언트 알림

운영 중인 서비스에서 새로운 기능이 추가되거나 마케팅 캠페인이 시작될 때, 그에 맞는 새로운 프롬프트가 필요할 수 있습니다. MCP 서버는 **`PromptListChangedNotification`** 알림을 통해 이러한 변경사항을 실시간으로 클라이언트에게 전파할 수 있습니다.

예를 들어, 관리자가 '여름 휴가 계획 추천 프롬프트'를 시스템에 새로 추가하면, 서버는 즉시 이 알림을 모든 클라이언트에게 보냅니다. 클라이언트는 이 알림을 받고 서버로부터 최신 프롬프트 목록을 가져와 사용자에게 새로운 기능을 제공할 수 있습니다. 이처럼 서버 재시작 없이도 프롬프트 목록을 유연하게 변경하고 적용할 수 있습니다.

---

## 결론

MCP는 프롬프트를 단순한 문자열이 아닌 **관리 가능한 자산(Asset)**으로 다룹니다. 프롬프트의 명세를 구조화하고, 동적 생성 로직을 중앙 서버에서 관리하며, 변경 사항을 클라이언트에 실시간으로 알리는 매커니즘을 통해, AI 애플리케이션의 프롬프트 엔지니어링을 한 차원 높은 수준으로 끌어올립니다.

이를 통해 개발자는 프롬프트의 품질을 일관되게 유지하고, 재사용성을 극대화하며, 비즈니스 요구사항에 맞춰 신속하게 대응할 수 있는 강력한 기반을 마련하게 됩니다. 더 나아가 고급 프롬프트 체이닝이나 멀티모달 프롬프트 작성법 같은 복잡한 기법을 적용하는 발판이 될 수 있습니다.