API 응답 데이터를 다양한 형식으로 제공해야 하는 요구사항은 현대 웹 서비스 개발에서 자주 마주치는 과제입니다. 특히 관리자 페이지나 보고서 시스템에서는 JSON 형태의 API 응답을 엑셀 파일로 다운로드할 수 있는 기능이 필요한 경우가 많습니다.

이 글에서는 Spring Framework에서 컨텐트 협상(Content Negotiation)을 활용하여 동일한 API 엔드포인트에서 JSON과 엑셀 파일을 모두 제공할 수 있는 기능을 구현하는 방법을 소개합니다.

## 요구사항과 해결 접근법

### 기본 요구사항

- 기존 JSON API의 수정 없이 엑셀 다운로드 기능 추가
- 클라이언트가 Accept 헤더를 통해 원하는 응답 형식 선택
- 중첩된 JSON 구조를 평면화하여 엑셀 시트로 변환
- Swagger 문서에서 두 형식 모두 지원

### 해결 접근법

Accept 헤더를 활용한 [[컨텐트 협상(Content Negotiation)]]을 통해 동일한 엔드포인트에서 다른 형식의 응답을 제공하는 방식을 채택했습니다. 이 방법은 RESTful API 설계 원칙에 부합하며, 클라이언트가 필요에 따라 적절한 형식을 선택할 수 있는 유연성을 제공합니다.

## 핵심 구현: ExcelExportFilter

엑셀 다운로드 기능의 핵심은 `ExcelExportFilter` 클래스입니다. 이 필터는 HTTP 요청을 가로채서 Accept 헤더를 확인하고, 엑셀 형식이 요청되었을 때 JSON 응답을 엑셀 파일로 변환합니다.

### Filter 기본 구조

```java
@Slf4j
@Component
public class ExcelExportFilter extends OncePerRequestFilter {
    
    private static final String EXCEL_CONTENT_TYPE = 
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";
    private final ObjectMapper objectMapper = new ObjectMapper();

    @Override
    protected void doFilterInternal(HttpServletRequest request, 
                                  HttpServletResponse response, 
                                  FilterChain filterChain)
            throws ServletException, IOException {

        String acceptHeader = request.getHeader("Accept");
        if (acceptHeader != null && acceptHeader.contains(EXCEL_CONTENT_TYPE)) {
            // 엑셀 변환 로직 실행
            processExcelRequest(request, response, filterChain);
        } else {
            // 일반 요청 처리
            filterChain.doFilter(request, response);
        }
    }
}
```

### Request/Response Wrapper 활용

엑셀 형식 요청 시 다음과 같은 처리 과정을 거칩니다:

1. **RequestWrapper**를 통해 Accept 헤더를 `application/json`으로 변경
2. **ResponseWrapper**를 통해 JSON 응답을 캡처
3. 캡처된 JSON을 엑셀 형식으로 변환하여 최종 응답

```java
private void processExcelRequest(HttpServletRequest request, 
                               HttpServletResponse response, 
                               FilterChain filterChain) 
        throws ServletException, IOException {
    
    RequestWrapper requestWrapper = new RequestWrapper(request);
    ResponseWrapper responseWrapper = new ResponseWrapper(response);
    
    filterChain.doFilter(requestWrapper, responseWrapper);
    
    String jsonResponse = responseWrapper.getCapturedResponse();
    if (jsonResponse != null && !jsonResponse.trim().isEmpty()) {
        convertJsonToExcel(jsonResponse, response);
    }
}
```

## JSON을 엑셀로 변환하는 로직

### Apache POI 라이브러리 활용

엑셀 파일 생성을 위해 Apache POI 라이브러리를 사용합니다:

```kotlin
// build.gradle.kts
dependencies {
    implementation("org.apache.poi:poi:5.2.5")
    implementation("org.apache.poi:poi-ooxml:5.2.5")
}
```

### JSON 평면화 (Flattening)

중첩된 JSON 구조를 엑셀 시트에 표현하기 위해 평면화 과정을 거칩니다:

```java
private List<Map<String, Object>> flattenJsonToList(JsonNode jsonNode) {
    List<Map<String, Object>> result = new ArrayList<>();
    
    if (jsonNode.isArray()) {
        for (JsonNode item : jsonNode) {
            Map<String, Object> flattened = flattenJsonObject(item, "");
            result.add(flattened);
        }
    } else if (jsonNode.isObject()) {
        Map<String, Object> flattened = flattenJsonObject(jsonNode, "");
        result.add(flattened);
    }
    
    return result;
}

private Map<String, Object> flattenJsonObject(JsonNode node, String prefix) {
    Map<String, Object> flattened = new HashMap<>();
    
    if (node.isObject()) {
        Iterator<Map.Entry<String, JsonNode>> fields = node.fields();
        while (fields.hasNext()) {
            Map.Entry<String, JsonNode> field = fields.next();
            String key = prefix.isEmpty() ? field.getKey() : prefix + "." + field.getKey();
            JsonNode value = field.getValue();
            
            if (value.isObject() || value.isArray()) {
                // 중첩 구조 재귀 처리
                Map<String, Object> nestedFlattened = flattenJsonObject(value, key);
                flattened.putAll(nestedFlattened);
            } else {
                // 기본값 처리
                flattened.put(key, convertJsonValue(value));
            }
        }
    }
    
    return flattened;
}
```

### 엑셀 워크북 생성

```java
private void convertJsonToExcel(String jsonResponse, HttpServletResponse response) 
        throws IOException {
    
    JsonNode jsonNode = objectMapper.readTree(jsonResponse);
    List<Map<String, Object>> flattenedData = flattenJsonToList(jsonNode);
    
    Workbook workbook = new XSSFWorkbook();
    Sheet sheet = workbook.createSheet("Data");
    
    // 헤더 생성
    Set<String> allKeys = new LinkedHashSet<>();
    for (Map<String, Object> item : flattenedData) {
        allKeys.addAll(item.keySet());
    }
    
    createHeaderRow(sheet, new ArrayList<>(allKeys), workbook);
    createDataRows(sheet, flattenedData, new ArrayList<>(allKeys));
    
    // 응답 설정
    response.setContentType(EXCEL_CONTENT_TYPE);
    response.setHeader("Content-Disposition", 
        "attachment; filename=\"export_" + System.currentTimeMillis() + ".xlsx\"");
    
    workbook.write(response.getOutputStream());
    workbook.close();
}
```

## Swagger 문서화

API 문서에서 두 가지 응답 형식을 모두 표시하기 위해 `OpenApiConfig`를 수정합니다:

```java
@Bean
public OperationCustomizer operationCustomizer() {
    return (Operation operation, HandlerMethod handlerMethod) -> {
        io.swagger.v3.oas.annotations.tags.Tag tagAnnotation = 
            handlerMethod.getBeanType().getAnnotation(io.swagger.v3.oas.annotations.tags.Tag.class);
        
        if (tagAnnotation != null && "보안 관제 자동화를 위한 API".equals(tagAnnotation.name())) {
            addMultipleMediaTypesSupport(operation);
        }
        return operation;
    };
}

private void addMultipleMediaTypesSupport(Operation operation) {
    ApiResponses responses = operation.getResponses();
    if (responses != null) {
        ApiResponse successResponse = responses.get("200");
        if (successResponse == null) {
            successResponse = new ApiResponse().description("성공");
            responses.addApiResponse("200", successResponse);
        }
        
        Content content = successResponse.getContent();
        if (content == null) {
            content = new Content();
            successResponse.setContent(content);
        }
        
        // JSON과 엑셀 Media Type 모두 추가
        content.addMediaType("application/json", new MediaType());
        content.addMediaType(EXCEL_CONTENT_TYPE, new MediaType());
    }
}
```

## 테스트 코드 작성

엑셀 변환 기능에 대한 포괄적인 테스트를 작성합니다:

### 기본 변환 테스트

```java
@Test
@DisplayName("Accept 헤더가 엑셀 형식인 경우 JSON을 엑셀로 변환")
void shouldConvertJsonToExcelWhenAcceptHeaderIsExcel() throws Exception {
    // Given
    MockHttpServletRequest request = new MockHttpServletRequest();
    MockHttpServletResponse response = new MockHttpServletResponse();
    request.addHeader("Accept", EXCEL_CONTENT_TYPE);

    String jsonResponse = "[{\"id\":1,\"name\":\"홍길동\",\"age\":30}]";

    doAnswer(invocation -> {
        HttpServletResponse resp = invocation.getArgument(1);
        resp.getWriter().write(jsonResponse);
        return null;
    }).when(filterChain).doFilter(any(), any());

    // When
    excelExportFilter.doFilterInternal(request, response, filterChain);

    // Then
    assertEquals(EXCEL_CONTENT_TYPE, response.getContentType());
    assertTrue(response.getHeader("Content-Disposition").contains("attachment"));
    
    // 엑셀 파일 내용 검증
    byte[] excelData = response.getContentAsByteArray();
    validateExcelContent(excelData, 1, new String[]{"id", "name", "age"});
}
```

## Docker 환경 설정

openjdk:21-slim 과 같은 이미지를 사용하는 경우 Apache POI 라이브러리가 사용하는 폰트 데이터가 없어 에러가 발생할 수 있습니다. 이를 방지하기 위해 엑셀 파일 생성 시 필요한 폰트 라이브러리를 Docker 이미지에 포함시킵니다.

```dockerfile
# 필요한 패키지 설치 (Apache POI용 폰트 라이브러리 포함)
RUN apt-get update && apt-get install -y \
    curl \
    fontconfig \
    libfreetype6 \
    libfontconfig1 \
    fonts-dejavu-core \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*
```

이 설정이 없으면 Docker 컨테이너에서 엑셀 파일 생성 시 폰트 관련 오류가 발생할 수 있습니다.

## 사용법

구현된 기능은 다음과 같이 사용할 수 있습니다:

### JSON 응답 요청
```bash
curl -H "Accept: application/json" \
     http://localhost:8080/api/data
```

### 엑셀 파일 다운로드 요청
```bash
curl -H "Accept: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" \
     -o data.xlsx \
     http://localhost:8080/api/data
```

## 고려사항과 제한점

### 성능 고려사항

1. **메모리 사용량**: 대용량 데이터의 경우 JSON 응답을 메모리에 캐시하므로 메모리 사용량이 증가할 수 있습니다.
2. **변환 시간**: JSON 파싱과 엑셀 생성 과정에서 추가적인 처리 시간이 소요됩니다.

### 데이터 구조 제한

1. **깊은 중첩**: 과도하게 깊은 중첩 구조는 엑셀 컬럼 헤더가 복잡해질 수 있습니다.
2. **배열 처리**: 배열 내 객체들의 구조가 다를 경우 일관성 있는 표현이 어려울 수 있습니다.


## 결론

Spring Framework의 Filter를 활용하여 기존 JSON API를 수정하지 않고 엑셀 다운로드 기능을 추가하는 방법을 살펴보았습니다. 이 접근 방식의 주요 장점은 다음과 같습니다:

1. **비침습적 구현**: 기존 컨트롤러 로직 수정 없음
2. **표준 준수**: HTTP 컨텐트 협상 표준 활용
3. **확장성**: 다른 형식 지원으로 쉽게 확장 가능
4. **테스트 용이성**: 각 구성 요소를 독립적으로 테스트 가능

이 기능을 통해 관리자나 사용자가 동일한 API 엔드포인트에서 필요에 따라 JSON 데이터나 엑셀 파일을 선택적으로 받을 수 있게 되어, 더 나은 사용자 경험을 제공할 수 있습니다.

## 참고 자료

- Spring Framework 공식 문서
- Apache POI 공식 문서  
- HTTP Content Negotiation 표준 (RFC 7231) 