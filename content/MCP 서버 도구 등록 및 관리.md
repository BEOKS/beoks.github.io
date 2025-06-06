[[MCP Server]]의 가장 핵심적인 기능은 AI 에이전트가 실제 세계와 상호작용할 수 있도록 **도구(Tool)를 제공**하는 것입니다. 도구 관리는 단순히 함수를 만드는 것을 넘어, AI가 '언제', '어떻게' 이 도구를 사용해야 하는지 명확하게 알려주는 **명세(Specification)를 정의**하고, 서버의 전체 생명주기 동안 이를 **안정적으로 관리**하는 모든 과정을 포함합니다.

이 문서에서는 MCP 서버에서 도구를 정의하고, 실제 로직을 구현하며, 서버에 등록하여 관리하는 전체 흐름을 상세히 설명합니다.

---

## 1. 도구(Tool)의 구성 요소

효과적인 도구를 만들기 위해서는 먼저 AI와 서버가 모두 이해할 수 있는 명확한 '계약'을 정의해야 합니다. MCP에서 하나의 도구는 다음과 같은 세 가지 핵심 요소로 구성됩니다.

1. **이름 (Name)**
    
    - 도구를 고유하게 식별하는 문자열입니다. (예: `getCurrentWeather`)
    - 클라이언트(AI)는 이 이름을 사용하여 특정 도구의 실행을 요청합니다.
2. **설명 (Description)**
    
    - **LLM(거대 언어 모델)이 도구의 용도를 파악하는 데 가장 중요한 정보입니다.**
    - "어떤 상황에서 이 도구를 사용해야 하는가?"에 대한 답을 명확하고 상세하게 서술해야 합니다.
    - 예시: "특정 지역의 현재 날씨 정보를 가져옵니다. 사용자가 '오늘 날씨 어때?' 또는 '부산 지금 더워?'와 같이 날씨를 물어볼 때 사용해야 합니다."
    
    > [중요]
    > 
    > 설명의 품질이 AI의 도구 사용 능력(Tool-Use)을 결정합니다. 설명이 모호하면 AI는 도구를 잘못 사용하거나, 필요할 때 사용하지 못할 수 있습니다.
    
3. **입력 스키마 (Input Schema)**
    
    - 도구가 실행될 때 필요한 파라미터(인자)들을 정의하는 명세입니다.
    - 주로 [[JSON Schema]] 형식을 사용하여 각 파라미터의 이름, 타입, 필수 여부, 설명 등을 기술합니다.
    - 예시: `getCurrentWeather` 도구는 `location`이라는 문자열 파라미터가 필수라고 정의할 수 있습니다.
    
    ```json
    {
      "type": "object",
      "properties": {
        "location": {
          "type": "string",
          "description": "날씨를 조회할 지역의 이름 (예: '서울', '부산')"
        }
      },
      "required": ["location"]
    }
    ```
    

---

## 2. Spring Boot로 도구 핸들러 구현하기

도구의 명세가 정의되었다면, 이제 실제 로직을 담고 있는 **핸들러(Handler)**를 구현해야 합니다. 핸들러는 클라이언트로부터 도구 실행 요청(`CallToolRequest`)을 받았을 때, 정의된 작업을 수행하고 그 결과를 `CallToolResult` 형태로 반환하는 역할을 합니다.

다음은 특정 도시의 날씨 정보를 반환하는 `WeatherToolService`를 Spring Boot로 구현한 예시입니다.

```java
import org.springframework.stereotype.Service;
import com.fasterxml.jackson.databind.JsonNode;
import java.util.Map;

import com.example.api.WeatherApiClient;
import com.example.api.WeatherInfo;

// MCP 서버의 도구 핸들러를 구현한 서비스
@Service
public class WeatherToolService {

    private final WeatherApiClient weatherApiClient;

    // 외부 API 클라이언트를 주입받습니다.
    public WeatherToolService(WeatherApiClient weatherApiClient) {
        this.weatherApiClient = weatherApiClient;
    }

    /**
     * 'getCurrentWeather' 도구의 실제 실행 로직입니다.
     * @param arguments 클라이언트가 보낸 인자 맵 (예: {"location": "서울"})
     * @return 도구 실행 결과 (성공 시 날씨 정보, 실패 시 에러 메시지)
     */
    public McpServer.CallToolResult getCurrentWeather(Map<String, JsonNode> arguments) {
        // 1. 입력 스키마에 따라 'location' 인자를 확인하고 추출합니다.
        JsonNode locationNode = arguments.get("location");
        if (locationNode == null || !locationNode.isTextual()) {
            return McpServer.CallToolResult.error("필수 인자 'location'이 없거나 형식이 올바르지 않습니다.");
        }
        String location = locationNode.asText();

        try {
            // 2. 외부 API를 호출하여 비즈니스 로직을 수행합니다.
            WeatherInfo weatherInfo = weatherApiClient.fetchWeatherFor(location);

            // 3. 성공 결과를 포맷하여 반환합니다.
            String resultMessage = String.format(
                "%s의 현재 날씨는 %s이며, 온도는 %.1f°C입니다.",
                location,
                weatherInfo.getCondition(),
                weatherInfo.getTemperature()
            );
            return McpServer.CallToolResult.ok(resultMessage);

        } catch (Exception e) {
            // 4. 예외 발생 시, 표준화된 오류를 반환합니다.
            return McpServer.CallToolResult.error("날씨 정보를 가져오는 중 오류가 발생했습니다: " + e.getMessage());
        }
    }
}
```

---

## 3. 서버에 도구 등록 및 관리

도구 핸들러가 준비되었다면, MCP 서버가 이를 인식하고 클라이언트의 요청에 연결할 수 있도록 **등록(Register)**해야 합니다. 실제 운영 환경에서는 서버가 시작될 때, Spring의 IoC 컨테이너에 등록된 관련 서비스들을 찾아 자동으로 도구를 등록하는 방식을 사용하는 것이 효율적입니다.

다음은 도구를 동적으로 등록하고 제거하는 `McpToolManager`의 개념적인 구현 예시입니다.


```java
import org.springframework.stereotype.Component;
import javax.annotation.PostConstruct;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.function.Function;

// MCP 서버의 도구들을 총괄 관리하는 매니저
@Component
public class McpToolManager {

    // 도구 이름과 실제 실행 핸들러(함수)를 매핑하는 저장소
    private final Map<String, Function<Map<String, JsonNode>, McpServer.CallToolResult>> toolRegistry = new ConcurrentHashMap<>();
    
    private final WeatherToolService weatherToolService;
    private final McpNotificationService mcpNotificationService;

    public McpToolManager(WeatherToolService weatherToolService, McpNotificationService mcpNotificationService) {
        this.weatherToolService = weatherToolService;
        this.mcpNotificationService = mcpNotificationService;
    }

    // 서버가 시작된 후, Spring이 관리하는 빈(Bean)들을 사용하여 도구를 등록합니다.
    @PostConstruct
    public void initializeTools() {
        // 'getCurrentWeather' 이름으로 WeatherToolService의 메서드를 핸들러로 등록
        addTool("getCurrentWeather", weatherToolService::getCurrentWeather);
        
        // ... 다른 도구들도 여기에 등록 ...
    }

    /**
     * 서버에 새로운 도구를 등록합니다.
     * @param name 도구 이름
     * @param handler 도구 실행 로직
     */
    public void addTool(String name, Function<Map<String, JsonNode>, McpServer.CallToolResult> handler) {
        toolRegistry.put(name, handler);
        System.out.println("도구 등록됨: " + name);
        
        // 클라이언트에게 도구 목록이 변경되었음을 알립니다.
        mcpNotificationService.sendToolListChanged();
    }

    /**
     * 등록된 도구를 제거합니다.
     * @param name 제거할 도구 이름
     */
    public void removeTool(String name) {
        toolRegistry.remove(name);
        System.out.println("도구 제거됨: " + name);
        
        // 클라이언트에게 도구 목록이 변경되었음을 알립니다.
        mcpNotificationService.sendToolListChanged();
    }

    /**
     * 이름으로 등록된 도구 핸들러를 찾아 반환합니다.
     * @param name 찾을 도구 이름
     * @return 도구 핸들러 (없으면 null)
     */
    public Function<Map<String, JsonNode>, McpServer.CallToolResult> getToolHandler(String name) {
        return toolRegistry.get(name);
    }
}
```

---

## 4. 동적 도구 목록 관리와 클라이언트 알림

애플리케이션은 정적이지 않습니다. 운영 중에 새로운 플러그인이 설치되어 새 도구가 추가되거나, 특정 도구가 비활성화될 수 있습니다. 이때 MCP 서버는 **`ToolListChangedNotification`** 알림을 클라이언트에게 보내야 합니다.

이 알림을 받은 클라이언트(AI)는 서버의 도구 목록을 다시 요청하여 최신 상태를 유지할 수 있습니다. 이를 통해 AI가 존재하지 않는 도구를 호출하는 오류를 방지하고, 새로 추가된 도구를 즉시 활용할 수 있게 됩니다.

위 `McpToolManager` 예시의 `addTool`과 `removeTool` 메서드에서 `mcpNotificationService.sendToolListChanged()`를 호출하는 부분이 바로 이 역할을 수행합니다.

---

## 결론

MCP 서버에서 도구를 효과적으로 등록하고 관리하는 것은 성공적인 AI 에이전트 시스템을 구축하기 위한 필수 과정입니다. 핵심은 다음과 같이 요약할 수 있습니다.

1. **명확한 정의**: AI가 이해할 수 있도록 도구의 `이름`, `설명`, `입력 스키마`를 명확하게 정의해야 합니다.
2. **모듈화된 구현**: 도구의 실제 로직은 비즈니스 도메인에 맞게 서비스 클래스로 구현하여 관리합니다.
3. **체계적인 등록**: 서버가 시작될 때나 동적으로 도구를 등록하고 해제할 수 있는 중앙 관리 매커니즘을 구축합니다.
4. **능동적인 상태 전파**: 도구 목록에 변경이 생기면 즉시 클라이언트에게 알려 상태 불일치를 방지합니다.

이러한 원칙을 따르면, 확장 가능하고 안정적이며, AI가 자신의 능력을 최대한 발휘할 수 있는 강력한 MCP 서버를 구축할 수 있을 것입니다.