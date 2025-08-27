MCP(Model Context Protocol) 통신의 모든 상호작용은 잘 정의된 **메시지(Message)**를 통해 이루어집니다. 이 메시지 구조는 산업 표준인 [[JSON-RPC]]을 기반으로 하며, 그 위에 MCP만의 특화된 데이터 모델과 지능적인 직렬화(Serialization) 전략을 더해 높은 수준의 유연성과 확장성을 갖추었습니다.

이 글에서는 MCP 메시지가 어떻게 구성되고, 다양한 종류의 데이터를 어떻게 효율적으로 표현하는지 그 구조적 특징을 자세히 살펴보겠습니다.

---

### 1. 기본 구조: JSON-RPC 2.0

MCP는 모든 메시지의 기본 뼈대로 **JSON-RPC 2.0** 명세를 따릅니다. 이는 통신의 기본 규칙을 명확히 하여, 어떤 프로그래밍 언어로 구현되더라도 상호 호환성을 보장합니다.

JSON-RPC 2.0에는 세 가지 기본 메시지 유형이 있습니다.

1. **요청 (Request Object)**: 상대방에게 어떤 작업을 수행하도록 요청하고, 반드시 응답을 받아야 하는 메시지입니다. 고유한 `id` 값을 가집니다.
    
    ```json
    {
      "jsonrpc": "2.0",
      "method": "tools/list",
      "params": { "cursor": null },
      "id": 1
    }
    ```
    
2. **응답 (Response Object)**: 요청에 대한 결과물입니다. 성공 시 `result` 필드를, 실패 시 `error` 필드를 가지며, 원래 요청과 동일한 `id`를 포함하여 어떤 요청에 대한 응답인지 식별합니다.
    
    
    ```json
    // 성공 응답
    {
      "jsonrpc": "2.0",
      "result": { "tools": [...] },
      "id": 1
    }
    ```
    
3. **알림 (Notification Object)**: 상대방에게 단순히 정보를 전달할 뿐, 응답을 요구하지 않는 단방향 메시지입니다. `id` 필드가 없습니다.
    
    ```json
    {
      "jsonrpc": "2.0",
      "method": "notifications/resources/list_changed",
      "params": {}
    }
    ```
    

MCP의 모든 구체적인 요청(`InitializeRequest`, `CallToolRequest` 등)과 결과(`InitializeResult`, `CallToolResult` 등)는 이 기본 구조의 `params`와 `result` 필드에 담겨 전송됩니다.

---

### 2. MCP 고유 데이터 모델

MCP는 JSON-RPC 2.0의 뼈대 위에 자신만의 풍부한 데이터 모델을 정의합니다. 모든 모델은 특정 역할을 수행하는 `sealed interface`를 상속받아 계층적으로 관리됩니다.

- `Request`: `InitializeRequest`, `ListToolsRequest` 등 서버에 보내는 모든 요청의 최상위 인터페이스입니다.
- `Notification`: `ResourceListChangedNotification` 등 응답이 필요 없는 모든 알림의 최상위 인터페이스입니다.
- `RequestResult`: `ListToolsResult`, `GetPromptResult` 등 모든 요청 결과의 최상위 인터페이스입니다.

예를 들어, 클라이언트가 `callTool` 메서드를 통해 "파일 쓰기"라는 도구를 호출한다면, `CallToolRequest` 객체를 생성합니다. 이 객체는 `Protocol` 계층에서 `method`가 "tools/call"이고 `params`가 `CallToolRequest`의 내용인 `JSONRPCRequest` 메시지로 변환되어 전송됩니다.

---

### 3. 핵심 기술: 내용 기반 다형성 (Content-Based Polymorphism)

다양한 종류의 `RequestResult`를 어떻게 하나의 `result` 필드로 처리할 수 있을까요? MCP는 **다형성(Polymorphism)** 처리 기능을 매우 독창적인 방식으로 활용합니다.

일반적으로 다형성 객체를 직렬화할 때는 `{"type": "ListToolsResult", ...}` 와 같이 객체의 타입을 명시하는 별도의 필드(Class Discriminator)를 두는 방식을 많이 사용합니다. 하지만 MCP는 `JsonContentPolymorphicSerializer`라는 커스텀 직렬화기를 통해 **내용 기반 다형성**을 구현합니다.

이는 JSON 객체 내에 어떤 **고유한 키(key)가 존재**하는지를 보고 데이터의 실제 타입을 추론하는 방식입니다.

예를 들어, [[MCP 프로토콜 계층 (Protocol Layer)]]이 서버로부터 응답(`JSONRPCResponse`)을 받으면, `result` 필드의 내용을 분석합니다.

- 만약 `result` 객체 안에 `"tools": [...]` 라는 키가 있다면, 이 객체를 `ListToolsResult` 타입으로 해석합니다.
- 만약 `"capabilities": {...}` 라는 키가 있다면, `InitializeResult` 타입으로 해석합니다.
- 만약 `"completion": {...}` 라는 키가 있다면, `CompleteResult` 타입으로 해석합니다.

이러한 접근 방식은 불필요한 메타데이터 필드 없이 JSON 메시지 자체를 더 깔끔하고 자연스럽게 유지하면서도, 매우 유연하게 다양한 데이터 타입을 처리할 수 있게 해주는 MCP의 핵심적인 기술입니다.

---

### 4. 커스텀 직렬화기 (Custom Serializers)

내용 기반 다형성 외에도, MCP는 특정 데이터 타입을 효율적으로 처리하기 위해 여러 커스텀 직렬화기를 사용합니다.

- **`RequestIdSerializer`**: JSON-RPC 명세에 따라 `id` 필드는 문자열(String) 또는 숫자(Number)일 수 있습니다. 이 직렬화기는 두 가지 타입을 모두 오류 없이 처리하여 명세 호환성을 보장합니다.
- **`ErrorCodeSerializer`**: `ErrorCode` 열거형을 단순한 정수(Integer) 코드로 변환하여 메시지 크기를 줄입니다.
- **`RequestMethodSerializer`**: `Method` 타입을 문자열(String) 값으로 변환합니다.

## 결론

MCP의 메시지 구조는 검증된 표준인 JSON-RPC 2.0 위에, **내용 기반 다형성**이라는 현대적이고 지능적인 직렬화 전략을 결합한 결과물입니다. 이를 통해 프로토콜의 메시지는 간결함을 유지하면서도, `tools`, `prompts`, `resources` 등 풍부하고 다양한 기능을 표현할 수 있는 확장성을 확보했습니다. 이처럼 잘 설계된 메시지 구조는 MCP가 복잡한 AI 상호작용을 안정적으로 지원하는 근간이 됩니다.