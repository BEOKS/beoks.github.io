MCP(Model Context Protocol) 아키텍처에서 **전송 계층(Transport Layer)**은 클라이언트와 서버 간의 실제 데이터 전송을 담당하는 가장 기본적인 계층입니다. 이 계층의 주된 목적은 복잡한 네트워크 통신의 세부 사항을 숨기고, 그 위의 [[MCP 프로토콜 계층 (Protocol Layer)]]이 일관된 방식으로 데이터를 주고받을 수 있도록 신뢰성 있는 통로를 제공하는 것입니다.

비유하자면, 전송 계층은 메시지를 실어 나르는 '배송 트럭'과 같습니다. 프로토콜 계층은 어떤 메시지를 보낼지, 받은 메시지를 어떻게 해석할지 결정하는 '물류 센터'의 역할을 하고, 전송 계층은 그저 빠르고 안전하게 화물(데이터)을 A지점에서 B지점으로 옮기는 임무에만 집중합니다.

---

## 핵심 책임 (Core Responsibilities)

MCP의 전송 계층은 `Transport` 인터페이스에 정의된 다음과 같은 핵심적인 책임을 가집니다.

1. **연결 수립 및 종료 (Connection Establishment and Termination)**
    
    - `start()`: 통신을 시작하기 위해 필요한 모든 초기화 작업을 수행합니다. 예를 들어, WebSocket 핸드셰이크를 하거나 서버 소켓을 여는 등의 작업을 포함합니다.
    - `close()`: 사용 중인 모든 리소스를 정리하고 연결을 안전하게 종료합니다.
2. **데이터 송수신 (Data Sending and Receiving)**
    
    - `send(message)`: 상위 프로토콜 계층으로부터 받은 `JSONRPCMessage` 객체를 직렬화하여 상대방에게 전송합니다.
    - `onMessage(callback)`: 외부로부터 데이터를 수신했을 때, 이를 역직렬화하여 완전한 `JSONRPCMessage` 객체로 만든 후, 상위 계층에 등록된 콜백 함수로 전달합니다.
3. **메시지 프레이밍 (Message Framing)**
    
    - 네트워크 통신은 대부분 경계가 없는 스트림(Stream) 형태입니다. 전송 계층은 이 스트림에서 하나의 완전한 JSON 메시지가 어디서 시작하고 끝나는지를 정확히 구분해내는 **메시지 프레이밍** 역할을 수행해야 합니다.
    - 예를 들어, `StdioTransport`는 줄바꿈 문자(`\n`)를 기준으로 메시지를 구분하고, `WebSocketTransport`는 웹소켓 프로토콜 자체에 내장된 메시지 프레임 기능을 활용합니다.
4. **이벤트 통지 (Event Notification)**
    
    - `onClose`, `onError`와 같은 콜백 인터페이스를 통해 연결 종료나 오류 발생과 같은 중요한 네트워크 이벤트를 상위 계층에 통지합니다. 이를 통해 프로토콜 계층은 연결 상태를 파악하고 적절한 재연결 로직이나 오류 복구 로직을 수행할 수 있습니다.

---

## 구현의 유연성: 다양한 전송 방식

MCP의 가장 큰 장점 중 하나는 **전송 계층의 독립성(Transport Agnosticism)**입니다. 이는 `Transport` 인터페이스를 구현하기만 하면 어떤 통신 기술이든 MCP의 전송 방식으로 사용할 수 있음을 의미합니다. 제공된 SDK는 다음과 같은 다양한 구현체를 제공합니다.

- [[WebSocketClientTransport]]
    
    - **특징**: 실시간 양방향 통신을 지원하는 웹소켓을 사용합니다. 한 번 연결되면 클라이언트와 서버가 언제든지 서로에게 메시지를 보낼 수 있어 지연 시간이 매우 짧습니다.
    - **주요 용도**: 채팅 애플리케이션이나 실시간 협업 도구처럼 즉각적인 상호작용이 필요한 웹 기반의 리치 클라이언트에 가장 적합합니다.
- [[SseClientTransport]]
    
    - **특징**: 서버-전송 이벤트(Server-Sent Events)를 사용합니다. 서버에서 클라이언트로의 단방향 이벤트 스트림을 기본으로 하며, 클라이언트에서 서버로의 메시지는 별도의 HTTP POST 요청을 통해 전송됩니다.
    - **주요 용도**: 웹소켓을 사용하기 어려운 환경이나, 주로 서버가 클라이언트에게 상태 변경을 통지하는 시나리오에 유용합니다.
- **StdioClientTransport**
    
    - **특징**: 표준 입출력(Standard I/O)을 통신 채널로 사용합니다. 즉, 하나의 프로세스가 다른 프로세스의 입출력 스트림에 직접 메시지를 쓰고 읽습니다.
    - **주요 용도**: IDE 플러그인과 언어 서버(LSP)처럼, 로컬 환경에서 두 프로세스 간의 통신(IPC)이 필요할 때 매우 효과적입니다. CLI 도구나 데스크톱 애플리케이션의 백그라운드 프로세스를 연동하는 데 이상적입니다.

---

## 프로토콜 계층과의 관계

전송 계층과 프로토콜 계층은 명확하게 역할을 분담하여 협력합니다.

- **전송 계층**은 "데이터 덩어리가 도착했습니다" 또는 "데이터를 저쪽으로 보내주세요"와 같은 저수준의 물리적인 역할을 수행합니다.
- **프로토콜 계층**은 전송 계층이 전달한 데이터 덩어리를 보고, "이것은 ID가 123인 `tools/call` 요청이므로, 등록된 도구 핸들러를 실행하고 결과를 응답 메시지로 만들어 전송 계층에 전달해야겠다"와 같은 지능적인 판단을 내립니다.

이러한 관심사의 분리(Separation of Concerns)는 MCP 아키텍처의 핵심이며, 시스템 전체의 유지보수성과 확장성을 크게 향상시키는 중요한 설계 원칙입니다.