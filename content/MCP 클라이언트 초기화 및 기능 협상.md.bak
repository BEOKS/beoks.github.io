**기능 협상(Capability Negotiation)**은 [[MCP Client]]와 서버가 통신을 시작하는 초기 단계에서 서로가 지원하는 기능과 프로토콜 버전을 교환하여 호환성을 확인하고, 이후의 상호작용 방식을 결정하는 핵심적인 프로세스입니다.

이는 단순히 "연결" 그 이상의 의미를 가지며, 서로 다른 버전의 클라이언트와 서버가 만나더라도 안정적으로 통신할 수 있는 기반을 마련하는 Handshake와 같습니다.

---

### 기능 협상이 중요한 이유

기능 협상은 MCP 생태계의 안정성과 확장성을 위해 반드시 필요합니다.

1. **상호운용성 및 호환성 보장**: 클라이언트와 서버는 독립적으로 개발되고 업데이트될 수 있습니다. 기능 협상을 통해 최신 클라이언트가 구버전 서버에 접속하더라도, 서버가 지원하지 않는 기능을 호출하여 오류를 발생시키는 상황을 미연에 방지할 수 있습니다.
2. **우아한 성능 저하(Graceful Degradation)**: 서버가 특정 기능(예: `tools` 호출)을 지원하지 않는다는 것을 협상 단계에서 파악하면, 클라이언트는 해당 기능을 비활성화하거나 대체 방안을 사용자에게 제시할 수 있습니다. 이는 애플리케이션이 갑작스럽게 중단되는 대신, 제한된 환경에서도 최선을 다해 동작하도록 만듭니다.
3. **프로토콜 확장성**: 미래에 새로운 기능(예: `realtime-debugging`)이 프로토콜에 추가되더라도, 기존 클라이언트와 서버는 이 협상 메커니즘 덕분에 영향을 받지 않습니다. 구버전 클라이언트는 새로운 기능을 인지하지 못하고 무시할 것이며, 시스템은 안정적으로 유지됩니다.
4. **자원 최적화**: 클라이언트가 특정 알림(예: 파일 시스템의 모든 변경사항)을 처리할 수 있는 기능이 있다고 서버에 알려야만 서버가 해당 알림을 보내도록 설정할 수 있습니다. 이를 통해 불필요한 트래픽과 자원 낭비를 줄일 수 있습니다.

---

### 기능 협상 과정

기능 협상은 클라이언트가 `connect` 메서드를 호출할 때 시작되는 초기화 시퀀스의 일부입니다.


```mermaid
sequenceDiagram
    participant C as 클라이언트
    participant S as MCP 서버

    C->>S: 연결 요청 (Transport Layer)
    S-->>C: 연결 수락 (Transport Layer)

    Note over C, S: 초기화 및 기능 협상 시작

    C->>S: InitializeRequest (내 버전: 1.1, 내 기능: [prompts, tools, ...])
    S->>S: 요청 분석 (버전 호환성, 클라이언트 기능 확인)
    S-->>C: InitializeResult (서버 버전: 1.0, 서버 기능: [prompts, resources, ...])

    Note over C, S: 협상 완료. 상호 기능 인지.

    C->>C: 서버 기능(ServerCapabilities) 저장
    C->>S: InitializedNotification (초기화 완료 알림)

    Note over C, S: 이제부터 협상된 기능 기반으로 통신

    C->>S: ListPromptsRequest (prompts 기능 사용)
    S-->>C: ListPromptsResult

    C->>C: 'tools' 기능 사용 시도
    Note right of C: 서버가 'tools'를 지원하지 않음을 확인<br/>(serverCapabilities.tools == null)
    C--xS: CallToolRequest (요청 보내지 않음 / 에러 처리)
```

1. **초기화 요청 (InitializeRequest)**: 클라이언트는 서버에 `InitializeRequest` 메시지를 보냅니다. 이 메시지에는 다음 정보가 포함됩니다.
    
    - `protocolVersion`: 클라이언트가 지원하는 [[Model Context Protocol (MCP)]]의 버전.
    - `clientInfo`: 클라이언트 애플리케이션의 이름과 버전.
    - `capabilities`: **클라이언트가 지원하는 기능 목록** (예: `roots.listChanged` 알림을 처리할 수 있음).
2. **서버의 응답 (InitializeResult)**: 서버는 클라이언트의 요청을 받고 자신의 상태와 비교한 후 `InitializeResult`로 응답합니다.
    
    - `protocolVersion`: 서버가 동의한 프로토콜 버전. 만약 클라이언트의 버전과 호환되지 않으면 연결이 거부될 수 있습니다.
    - `serverInfo`: 서버 구현체의 이름과 버전.
    - `capabilities`: **서버가 제공하는 기능 목록** (예: `prompts`, `resources.subscribe` 등).
3. **협상 완료**: 클라이언트는 서버로부터 받은 `InitializeResult`를 분석하여 서버의 기능(`serverCapabilities`)을 내부에 저장합니다. 이제 클라이언트는 특정 기능을 요청하기 전에, 저장된 `serverCapabilities`를 확인하여 서버가 해당 요청을 처리할 수 있는지 미리 판단할 수 있습니다.
    

---

### 주요 기능(Capabilities)의 종류

협상되는 기능에는 여러 종류가 있으며, 대표적인 예는 다음과 같습니다.

- **`prompts`**: 서버가 프롬프트 조회(`prompts/list`) 및 완성(`completion/complete`) 기능을 지원하는지 여부.
- **`tools`**: 서버가 외부 도구 조회(`tools/list`) 및 호출(`tools/call`) 기능을 지원하는지 여부.
- **`resources`**: 서버가 파일과 같은 리소스 조회(`resources/read`), 목록 보기(`resources/list`), 그리고 변경사항 구독(`resources/subscribe`)을 지원하는지 여부. `subscribe`는 별도의 불리언 값으로 지원 여부가 명시될 수 있습니다.
- **`logging`**: 서버의 로깅 레벨을 원격으로 제어할 수 있는지 여부.
- **`roots`**: 클라이언트 측 기능으로, 클라이언트가 작업공간의 루트 디렉터리 변경 알림(`roots/listChanged`)을 처리할 수 있음을 서버에 알리는 데 사용될 수 있습니다.
