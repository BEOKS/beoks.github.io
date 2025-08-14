컨텐트 협상(Content Negotiation)은 [[HTTP(HyperText Transfer Protocol)]] 프로토콜에서 클라이언트와 서버가 동일한 리소스에 대해 가장 적합한 표현(representation)을 선택하는 메커니즘입니다. 이는 [[RESTful API]] 설계의 핵심 원칙 중 하나로, 하나의 엔드포인트에서 여러 형식의 응답을 제공할 수 있게 해줍니다.

## 컨텐트 협상의 개념

웹에서 동일한 리소스가 다양한 형태로 표현될 수 있습니다. 예를 들어, 사용자 정보라는 리소스는 JSON, XML, HTML, 또는 심지어 엑셀 파일 형태로도 제공될 수 있습니다. 컨텐트 협상은 클라이언트가 원하는 형식을 서버에 알리고, 서버가 가능한 형식 중에서 가장 적절한 것을 선택하여 응답하는 과정입니다.

이 메커니즘을 통해 개발자는 각 형식별로 별도의 엔드포인트를 만들 필요 없이, 하나의 엔드포인트에서 다양한 형식의 응답을 제공할 수 있습니다.

## HTTP 헤더를 통한 협상

### Accept 헤더

클라이언트가 선호하는 미디어 타입(Media Type)을 서버에 알리는 데 사용합니다:

```http
Accept: application/json
Accept: application/xml
Accept: text/html
Accept: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
```

여러 형식을 동시에 요청할 때는 품질 값(quality value)을 사용하여 우선순위를 지정할 수 있습니다:

```http
Accept: application/json;q=0.9, application/xml;q=0.8, text/html;q=0.7
```

### Accept-Language 헤더

클라이언트가 선호하는 언어를 지정합니다:

```http
Accept-Language: ko-KR, en-US;q=0.8, en;q=0.6
```

### Accept-Encoding 헤더

클라이언트가 지원하는 압축 방식을 지정합니다:

```http
Accept-Encoding: gzip, deflate, br
```

### Accept-Charset 헤더

클라이언트가 선호하는 문자 인코딩을 지정합니다:

```http
Accept-Charset: utf-8, iso-8859-1;q=0.5
```

## Spring에서의 컨텐트 협상 구현

### 기본 설정

Spring Boot에서는 기본적으로 컨텐트 협상이 활성화되어 있습니다. `WebMvcConfigurer`를 통해 추가 설정이 가능합니다:

```java
@Configuration
public class ContentNegotiationConfig implements WebMvcConfigurer {
    
    @Override
    public void configureContentNegotiation(ContentNegotiationConfigurer configurer) {
        configurer
            .favorParameter(false)  // 파라미터 기반 협상 비활성화
            .favorPathExtension(false)  // 확장자 기반 협상 비활성화
            .ignoreAcceptHeader(false)  // Accept 헤더 사용
            .defaultContentType(MediaType.APPLICATION_JSON)
            .mediaType("json", MediaType.APPLICATION_JSON)
            .mediaType("xml", MediaType.APPLICATION_XML)
            .mediaType("xlsx", MediaType.parseMediaType("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"));
    }
}
```

### Controller에서의 구현

동일한 엔드포인트에서 여러 형식을 지원하는 컨트롤러를 작성할 수 있습니다:

```java
@RestController
@RequestMapping("/api/users")
public class UserController {
    
    @GetMapping(produces = {
        MediaType.APPLICATION_JSON_VALUE,
        MediaType.APPLICATION_XML_VALUE,
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    })
    public ResponseEntity<List<User>> getUsers(HttpServletRequest request) {
        List<User> users = userService.getAllUsers();
        
        String acceptHeader = request.getHeader("Accept");
        
        // Accept 헤더에 따른 처리는 Spring의 MessageConverter가 자동으로 처리
        return ResponseEntity.ok(users);
    }
}
```

### Message Converter 활용

Spring은 HttpMessageConverter를 통해 객체를 다양한 형식으로 변환합니다:

```java
@Configuration
public class MessageConverterConfig implements WebMvcConfigurer {
    
    @Override
    public void configureMessageConverters(List<HttpMessageConverter<?>> converters) {
        // JSON Converter (기본 제공)
        converters.add(new MappingJackson2HttpMessageConverter());
        
        // XML Converter
        converters.add(new MappingJackson2XmlHttpMessageConverter());
        
        // Custom Excel Converter
        converters.add(new ExcelHttpMessageConverter());
    }
}
```

## 실제 사용 예시

### 클라이언트 요청 예시

같은 엔드포인트에 대해 다른 Accept 헤더로 요청:

```bash
# JSON 응답 요청
curl -H "Accept: application/json" \
     http://localhost:8080/api/users

# XML 응답 요청  
curl -H "Accept: application/xml" \
     http://localhost:8080/api/users

# 엑셀 파일 다운로드 요청
curl -H "Accept: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" \
     -o users.xlsx \
     http://localhost:8080/api/users
```

### 서버 응답 헤더

서버는 실제 응답 형식을 `Content-Type` 헤더로 알려줍니다:

```http
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 1234

{"users": [...]}
```

## 컨텐트 협상 전략

### 1. Accept 헤더 기반 (권장)

가장 표준적인 방법으로, HTTP 스펙을 준수합니다:

```http
GET /api/data
Accept: application/json
```

### 2. URL 파라미터 기반

일부 시스템에서 사용하지만 권장되지 않습니다:

```http
GET /api/data?format=json
GET /api/data?format=xml
```

### 3. 파일 확장자 기반

과거에 사용되었지만 현재는 권장되지 않습니다:

```http
GET /api/data.json
GET /api/data.xml
```

## 오류 처리

클라이언트가 요청한 형식을 서버가 지원하지 않는 경우 `406 Not Acceptable` 상태 코드를 반환합니다:

```java
@ExceptionHandler(HttpMediaTypeNotAcceptableException.class)
public ResponseEntity<String> handleNotAcceptable(HttpMediaTypeNotAcceptableException ex) {
    return ResponseEntity
        .status(HttpStatus.NOT_ACCEPTABLE)
        .body("요청된 미디어 타입을 지원하지 않습니다: " + ex.getSupportedMediaTypes());
}
```

## 장점과 활용 사례

### 장점

1. **API 단순화**: 하나의 엔드포인트로 여러 형식 지원
2. **RESTful 원칙 준수**: HTTP 표준을 올바르게 활용
3. **유연성**: 클라이언트 요구사항에 맞는 형식 제공
4. **유지보수성**: 비즈니스 로직은 그대로 두고 표현만 변경

### 활용 사례

1. **API 버전 관리**: 같은 데이터를 다른 스키마로 제공
2. **다국가 서비스**: 언어별 응답 제공
3. **모바일/웹 대응**: 플랫폼별 최적화된 응답
4. **리포팅 시스템**: JSON/XML/Excel 등 다양한 형식으로 데이터 제공

## Spring Boot에서의 고급 설정

### 우선순위 설정

여러 협상 전략의 우선순위를 설정할 수 있습니다:

```java
@Configuration
public class ContentNegotiationConfig implements WebMvcConfigurer {
    
    @Override
    public void configureContentNegotiation(ContentNegotiationConfigurer configurer) {
        configurer
            .strategies(Arrays.asList(
                new HeaderContentNegotiationStrategy(),  // Accept 헤더 기반
                new ParameterContentNegotiationStrategy(Map.of(
                    "json", MediaType.APPLICATION_JSON,
                    "xml", MediaType.APPLICATION_XML
                ))  // 파라미터 기반
            ))
            .defaultContentType(MediaType.APPLICATION_JSON);
    }
}
```

### 커스텀 미디어 타입 등록

```java
@Configuration
public class CustomMediaTypeConfig implements WebMvcConfigurer {
    
    @Override
    public void configureContentNegotiation(ContentNegotiationConfigurer configurer) {
        configurer
            .mediaType("csv", MediaType.parseMediaType("text/csv"))
            .mediaType("pdf", MediaType.parseMediaType("application/pdf"))
            .mediaType("excel", MediaType.parseMediaType("application/vnd.ms-excel"));
    }
}
```

## 실제 구현 시 고려사항

### 성능 최적화

각 형식별로 다른 변환 비용이 발생할 수 있으므로 이를 고려해야 합니다:

```java
@Service
public class DataExportService {
    
    @Cacheable(value = "exportCache", key = "#format + '_' + #dataId")
    public byte[] exportData(String format, Long dataId) {
        // 형식별 변환 로직
        switch (format) {
            case "json":
                return convertToJson(dataId);
            case "excel":
                return convertToExcel(dataId);  // 시간이 많이 소요
            default:
                throw new UnsupportedOperationException();
        }
    }
}
```

### 보안 고려사항

특정 형식에 대해서는 접근 권한을 제한할 수 있습니다:

```java
@PreAuthorize("hasRole('ADMIN') or #format != 'excel'")
public ResponseEntity<?> exportData(@RequestParam String format) {
    // 일반 사용자는 엑셀 다운로드 불가
}
```

## 테스트 작성

컨텐트 협상 기능에 대한 테스트를 작성할 때는 다양한 Accept 헤더를 테스트해야 합니다:

```java
@SpringBootTest
@AutoConfigureTestDatabase
class ContentNegotiationTest {
    
    @Autowired
    private MockMvc mockMvc;
    
    @Test
    @DisplayName("JSON 형식 요청 시 JSON 응답")
    void shouldReturnJsonWhenAcceptJson() throws Exception {
        mockMvc.perform(get("/api/users")
                .accept(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andExpect(content().contentType(MediaType.APPLICATION_JSON))
                .andExpect(jsonPath("$").isArray());
    }
    
    @Test
    @DisplayName("엑셀 형식 요청 시 엑셀 파일 응답")
    void shouldReturnExcelWhenAcceptExcel() throws Exception {
        mockMvc.perform(get("/api/users")
                .accept("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"))
                .andExpect(status().isOk())
                .andExpect(content().contentType("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"))
                .andExpect(header().string("Content-Disposition", containsString("attachment")));
    }
    
    @Test
    @DisplayName("지원하지 않는 형식 요청 시 406 에러")
    void shouldReturn406WhenUnsupportedMediaType() throws Exception {
        mockMvc.perform(get("/api/users")
                .accept("application/unsupported"))
                .andExpect(status().isNotAcceptable());
    }
}
```

## 결론

컨텐트 협상은 현대 웹 API 설계에서 매우 중요한 개념입니다. 이를 통해 단일 엔드포인트에서 다양한 클라이언트 요구사항을 만족시킬 수 있으며, [[RESTful API]]의 원칙을 올바르게 구현할 수 있습니다.

Spring Framework는 이러한 컨텐트 협상을 쉽게 구현할 수 있는 강력한 기능들을 제공하므로, 이를 적절히 활용하면 더 유연하고 확장 가능한 API를 설계할 수 있습니다.

컨텐트 협상을 구현할 때는 성능, 보안, 사용자 경험을 모두 고려하여 적절한 전략을 선택하는 것이 중요합니다. 특히 캐싱 전략, 인증과 인가, 에러 핸들링 등과 함께 종합적으로 설계해야 합니다.

## 참고 자료

- RFC 7231 - HTTP/1.1 Semantics and Content
- Spring Framework Reference Documentation
- MDN Web Docs - Content Negotiation 