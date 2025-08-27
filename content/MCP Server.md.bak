## MCP 서버의 핵심 동작 원리

MCP 서버의 가장 큰 특징은 클라이언트(AI 에이전트)와 서버 간의 상호작용이 명확한 프로토콜 위에 정의되어 있다는 점입니다. 모든 통신은 [[JSON-RPC]]를 기반으로 이루어지며, 서버와 클라이언트는 미리 정해진 규칙에 따라 메시지를 주고받습니다.

전체적인 통신 흐름은 다음과 같이 요약할 수 있습니다.

```mermaid
sequenceDiagram
    participant Client as 클라이언트 (AI 에이전트)
    participant Server as MCP 서버

    Client->>Server: 1. InitializeRequest (클라이언트 정보 및 기능 알림)
    Server-->>Client: 2. InitializeResult (서버 정보 및 기능 응답)
    Client->>Server: 3. InitializedNotification (초기화 완료 알림)

    Note over Client,Server: 초기화 및 기능 협상 완료

    Client->>Server: 4. Request (예: 도구 목록 요청)
    Server-->>Client: 5. Response (요청 결과 반환)

    Server->>Client: 6. Notification (예: 리소스 목록 변경 알림)
```

1. **초기화 및 기능 협상(Handshake)**: 클라이언트가 처음 연결되면, 자신의 기능(`ClientCapabilities`)을 서버에 알립니다. 서버 역시 자신이 제공할 수 있는 기능(`ServerCapabilities`)으로 응답하며 서로가 사용할 수 있는 기능의 범위를 확인합니다. 이 과정은 [[MCP 기능 협상]] 노트에서 더 자세히 다룹니다.
2. **요청과 응답(Request/Response)**: 클라이언트는 서버에 필요한 기능(예: "날씨 알려주는 도구 실행해줘")을 요청하고, 서버는 그에 대한 결과를 응답합니다.
3. **알림(Notification)**: 서버는 클라이언트에게 특정 이벤트(예: "새로운 도구가 추가되었어")를 일방적으로 알릴 수 있습니다. 클라이언트가 응답할 필요는 없습니다.

---

## MCP 서버의 세 가지 핵심 요소

MCP 서버는 AI에게 컨텍스트와 능력을 제공하기 위해 크게 세 가지 요소를 관리하고 제공합니다.

### 1. 도구 (Tools)

서버는 AI가 사용할 수 있는 구체적인 기능, 즉 '도구'를 등록하고 관리합니다. 예를 들어, '현재 날씨 조회', '메일 보내기', '데이터베이스 검색'과 같은 기능들을 도구로 제공할 수 있습니다.

AI는 자신이 필요한 작업을 수행하기 위해 서버에 등록된 도구를 호출하고 그 결과를 받아 활용합니다. 이는 AI가 단순히 텍스트 생성에만 머무는 것이 아니라, 실질적인 행동을 수행하는 에이전트로 기능하게 만드는 핵심입니다.

자세한 구현 방법은 [[MCP 서버 도구 등록 및 관리]]에서 확인하실 수 있습니다.

### 2. 프롬프트 (Prompts)

서버는 특정 작업에 최적화된 '프롬프트 템플릿'을 제공할 수 있습니다. 클라이언트는 이 템플릿을 가져와 필요한 인자를 채워 넣어 완성된 프롬프트를 만들 수 있습니다.

이를 통해 복잡한 프롬프트를 클라이언트 측에서 매번 생성할 필요 없이, 서버에서 체계적으로 관리하고 재사용성을 높일 수 있습니다. 예를 들어, '주어진 내용을 전문적인 톤의 비즈니스 메일 형식으로 바꿔주는 프롬프트'를 서버에 등록해두고 필요할 때마다 가져와 사용하는 식입니다.

자세한 구현 방법은 [[MCP프롬프트 등록 및 관리]]에서 확인하실 수 있습니다.

### 3. 리소스 (Resources)

AI가 작업을 수행하는 데 필요한 데이터나 파일(예: PDF 문서, CSV 파일, 웹 페이지 내용)을 '리소스'로 제공합니다. AI는 서버에 등록된 리소스 목록을 확인하고, 특정 리소스의 내용을 읽어와 작업의 컨텍스트로 활용할 수 있습니다.

이는 AI가 외부 정보에 접근하여 더 정확하고 풍부한 답변을 생성하도록 돕습니다.

---

## 유연한 전송 계층 (Transport Layer)

MCP 서버는 특정 통신 방식에 얽매이지 않도록 **전송 계층을 추상화**했다는 중요한 특징을 가집니다. 제공된 SDK 코드에서도 볼 수 있듯이, 개발자는 필요에 따라 다음과 같은 다양한 통신 방식을 선택하거나 직접 구현할 수 있습니다.

- **WebSocket**: 실시간 양방향 통신이 필요할 때 적합합니다.
- **SSE (Server-Sent Events)**: 서버가 클라이언트에게 지속적으로 데이터를 푸시하는 단방향 통신에 유리합니다.
- **Stdio (Standard I/O)**: 로컬 환경에서 CLI(Command Line Interface) 기반으로 동작하는 도구와 연동할 때 유용합니다.

이러한 유연성 덕분에 MCP 서버는 웹 서비스, 데스크톱 애플리케이션, 커맨드라인 도구 등 다양한 환경에 쉽게 통합될 수 있습니다. 더 자세한 내용은 MCP 전송 계층 문서를 참고해 주세요.

---

## Spring Boot를 활용한 MCP 서버 도구 구현 예시

MCP의 개념을 Java와 Spring Boot 환경에 적용하여 간단한 도구를 구현하는 예시를 살펴보겠습니다. 여기서는 '사용자 이름을 받아 인사말을 반환하는' 도구를 만들어 보겠습니다.

먼저, MCP 서버의 도구 요청을 처리할 서비스 클래스를 정의합니다.

Java

```java
import org.springframework.stereotype.Service;
import java.util.Map;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;

// MCP 서버의 도구 핸들러 역할을 하는 스프링 서비스
@Service
public class GreetingToolService {

    private final ObjectMapper objectMapper = new ObjectMapper();

    /**
     * 'greet' 도구가 호출되었을 때 실행될 로직입니다.
     * MCP의 CallToolRequest에 해당하는 정보를 받아 CallToolResult를 반환합니다.
     *
     * @param arguments MCP 클라이언트가 보낸 도구의 인자 (예: {"name": "World"})
     * @return MCP 클라이언트에게 반환될 결과
     */
    public CallToolResult greet(Map<String, JsonNode> arguments) {
        // 1. 필수 인자 'name'이 있는지 확인합니다.
        if (!arguments.containsKey("name")) {
            return CallToolResult.error("인자 'name'이 필요합니다.");
        }

        // 2. 'name' 인자를 추출합니다.
        String name = arguments.get("name").asText();
        String greetingMessage = "안녕하세요, " + name + "님! 만나서 반갑습니다.";

        // 3. 성공 결과를 CallToolResult 형태로 생성하여 반환합니다.
        return CallToolResult.ok(greetingMessage);
    }

    // --- 아래는 MCP SDK의 CallToolResult를 가상으로 구현한 Helper 클래스입니다. ---

    public static class CallToolResult {
        private final JsonNode content;
        private final boolean isError;

        private CallToolResult(JsonNode content, boolean isError) {
            this.content = content;
            this.isError = isError;
        }

        public static CallToolResult ok(String textContent) {
            ObjectMapper mapper = new ObjectMapper();
            ObjectNode contentNode = mapper.createObjectNode();
            contentNode.put("type", "text");
            contentNode.put("text", textContent);
            return new CallToolResult(contentNode, false);
        }

        public static CallToolResult error(String errorMessage) {
            ObjectMapper mapper = new ObjectMapper();
            ObjectNode contentNode = mapper.createObjectNode();
            contentNode.put("type", "text");
            contentNode.put("text", "오류: " + errorMessage);
            return new CallToolResult(contentNode, true);
        }

        // Getter...
        public JsonNode getContent() { return content; }
        public boolean isError() { return isError; }
    }
}
```

위 예시는 MCP의 핵심 개념인 '도구 호출'을 스프링 서비스 메서드로 어떻게 구현할 수 있는지 보여줍니다. 실제 MCP 서버를 구축할 때는 라우팅 설정에서 들어온 `CallToolRequest`를 분석하여 적절한 서비스의 메서드를 호출하고, 그 결과를 다시 `CallToolResult`로 포장하여 클라이언트에게 반환하는 로직을 추가하게 될 것입니다.

---

## 결론

MCP 서버는 AI가 외부 세계와 소통하고 상호작용하는 방식을 표준화하는 강력한 패러다임입니다. 도구, 프롬프트, 리소스를 체계적으로 제공함으로써 AI 애플리케이션의 **모듈성, 확장성, 재사용성**을 크게 향상시킵니다.

AI를 단순한 정보 검색 도구가 아닌, 복잡한 문제를 해결하는 능동적인 에이전트로 발전시키고자 한다면, MCP는 그 청사진을 제시하는 훌륭한 출발점이 될 것입니다.

---

## 참고 자료

- Model Context Protocol Kotlin SDK (제공된 코드의 가상 저장소 링크): [https://github.com/model-context-protocol/mcp-kotlin-sdk](https://www.google.com/search?q=https://github.com/model-context-protocol/mcp-kotlin-sdk)
- JSON-RPC 2.0 Specification: [https://www.jsonrpc.org/specification](https://www.jsonrpc.org/specification)