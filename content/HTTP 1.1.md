HTTP 1.1은 웹의 기반이 되는 [[HTTP(HyperText Transfer Protocol)]]의 두 번째 주요 버전으로, 1997년에 RFC 2068을 통해 처음 표준화되었고 1999년 RFC 2616에서 업데이트되었습니다. 이전 버전인 [[HTTP 1.0]]의 한계를 개선하여 웹 통신의 효율성과 기능성을 크게 향상시켰습니다.

## HTTP 1.1의 주요 특징

### 1. 연결 재사용 (Connection Reuse)

HTTP 1.1의 가장 중요한 개선점 중 하나는 **지속 연결(Persistent Connection)** 기능입니다. 이전의 HTTP 1.0에서는 각 요청마다 새로운 TCP 연결을 설정하고 닫아야 했습니다. 그러나 HTTP 1.1은 기본적으로 연결을 유지하여 여러 요청에 재사용할 수 있습니다.

이 특징은 다음과 같은 이점을 제공합니다:

- TCP 핸드셰이크 오버헤드 감소
- 네트워크 혼잡 감소
- 지연 시간 감소
- 웹 페이지 로딩 시간 개선

```
Connection: keep-alive
```

### 2. 파이프라이닝 (Pipelining)

HTTP 1.1은 **요청 파이프라이닝**을 도입했습니다. 이를 통해 클라이언트는 이전 요청에 대한 응답을 기다리지 않고도 여러 요청을 서버에 보낼 수 있습니다. 서버는 요청을 받은 순서대로 응답을 처리하고 반환합니다.

그러나 파이프라이닝은 HOL(Head-of-Line) 차단 문제로 인해 실제 구현에서는 제한적으로 사용되었습니다. 첫 번째 응답이 지연되면 그 뒤의 모든 응답도 함께 지연되기 때문입니다.

### 3. 호스트 헤더 필수화

HTTP 1.1에서는 요청에 **Host 헤더**가 필수가 되었습니다. 이를 통해 같은 IP 주소에서 여러 도메인을 호스팅하는 **가상 호스팅**이 가능해졌습니다.

```
Host: www.example.com
```

### 4. [[청크드 전송 인코딩(Chunked Transfer Encoding)]]

HTTP 1.1은 **청크 전송 인코딩**을 도입하여 콘텐츠의 전체 크기를 미리 알지 못하더라도 데이터를 전송할 수 있게 했습니다. 이는 동적 콘텐츠 생성이나 대용량 파일 전송에 유용합니다.

```
Transfer-Encoding: chunked
```

### 5. 캐시 제어 메커니즘

HTTP 1.1은 향상된 **캐시 제어 메커니즘**을 제공합니다. `Cache-Control` 헤더를 통해 더 세밀한 캐싱 정책을 설정할 수 있게 되었습니다.

```
Cache-Control: max-age=3600, public
```

캐시 제어에 대한 자세한 내용은 HTTP 캐싱을 참고해주세요.

### 6. 범위 요청 (Range Requests)

HTTP 1.1에서는 **범위 요청**을 사용하여 리소스의 일부만 요청할 수 있습니다. 이는 대용량 파일 다운로드나 다운로드 재개에 특히 유용합니다.

```
Range: bytes=500-999
```

### 7. 압축 지원

HTTP 1.1은 `Content-Encoding` 헤더를 통해 **콘텐츠 압축**을 지원합니다. 클라이언트는 `Accept-Encoding` 헤더로 지원하는 압축 방식을 알릴 수 있습니다.

```
Accept-Encoding: gzip, deflate
Content-Encoding: gzip
```

### 8. 추가된 HTTP 메서드

HTTP 1.1은 기존의 GET, POST, HEAD 외에도 여러 메서드를 추가했습니다:

- **PUT**: 리소스 생성 또는 수정
- **DELETE**: 리소스 삭제
- **OPTIONS**: 서버가 지원하는 메서드 정보 요청
- **TRACE**: 요청 메시지 루프백 테스트
- **CONNECT**: 프록시를 통한 터널 연결 설정

## HTTP 1.1의 한계

HTTP 1.1은 크게 개선되었지만, 여전히 몇 가지 한계점이 있습니다:

### 1. HOL 차단 문제

파이프라이닝에서의 **HOL(Head-of-Line) 차단** 문제는 HTTP 1.1의 가장 큰 제약 중 하나입니다. 하나의 요청이 처리되지 않으면 그 뒤의 모든 요청도 차단됩니다.

### 2. 헤더 중복

HTTP 1.1은 각 요청마다 **헤더를 반복적으로 전송**하게 되어, 특히 쿠키가 큰 경우 상당한 오버헤드가 발생할 수 있습니다.

### 3. 제한된 병렬 처리

브라우저는 일반적으로 도메인당 연결 수를 제한하기 때문에, 많은 리소스를 병렬로 로드하는 데 한계가 있습니다. 이로 인해 개발자들은 종종 도메인 샤딩(Domain Sharding)과 같은 방식으로 이를 우회했습니다.

HTTP 1.1의 한계점과 이를 극복하기 위한 기술에 대한 자세한 내용은 HTTP 성능 최적화 기법을 참고해주세요.

## Java에서 HTTP 1.1 클라이언트 구현 예시

Java에서 HTTP 1.1 클라이언트를 구현하는 간단한 예시입니다:

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class Http11Client {
    
    public static void main(String[] args) {
        try {
            URL url = new URL("https://api.example.com/data");
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            
            // HTTP 메서드 설정
            connection.setRequestMethod("GET");
            
            // 연결 재사용 설정
            connection.setRequestProperty("Connection", "keep-alive");
            
            // 압축 지원
            connection.setRequestProperty("Accept-Encoding", "gzip, deflate");
            
            // 필수 Host 헤더 설정
            connection.setRequestProperty("Host", url.getHost());
            
            // 응답 코드 확인
            int responseCode = connection.getResponseCode();
            System.out.println("Response Code: " + responseCode);
            
            // 응답 내용 읽기
            BufferedReader in = new BufferedReader(
                new InputStreamReader(connection.getInputStream()));
            String inputLine;
            StringBuilder response = new StringBuilder();
            
            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }
            in.close();
            
            // 결과 출력
            System.out.println(response.toString());
            
            // 연결 종료
            connection.disconnect();
            
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

최신 Java 애플리케이션에서는 `HttpURLConnection` 대신 더 현대적인 HTTP 클라이언트인 `HttpClient`를 사용하는 것이 권장됩니다. 자세한 내용은 Java HTTP 클라이언트 API를 참고해주세요.

## 스프링에서의 HTTP 1.1 활용

스프링 프레임워크에서는 RestTemplate이나 WebClient를 통해 HTTP 요청을 쉽게 처리할 수 있습니다:

```java
@Service
public class ApiService {
    
    private final RestTemplate restTemplate;
    
    public ApiService(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }
    
    public ResponseEntity<String> fetchData() {
        HttpHeaders headers = new HttpHeaders();
        headers.set(HttpHeaders.ACCEPT, MediaType.APPLICATION_JSON_VALUE);
        
        HttpEntity<?> entity = new HttpEntity<>(headers);
        
        return restTemplate.exchange(
            "https://api.example.com/data",
            HttpMethod.GET,
            entity,
            String.class
        );
    }
}
```

스프링의 HTTP 클라이언트에 대한 자세한 내용은 스프링 HTTP 클라이언트를 참고해주세요.

## HTTP 1.1과 현대적 웹 개발

HTTP 1.1은 여전히 인터넷에서 광범위하게 사용되는 프로토콜이지만, 웹 애플리케이션이 점점 더 복잡해지고 리소스 요구사항이 증가함에 따라 그 한계가 드러나고 있습니다. 이러한 한계를 극복하기 위해 [[HTTP 2.0]]와 [[HTTP 3.0]]과 같은 새로운 버전이 개발되었습니다.

그럼에도 불구하고, HTTP 1.1은 웹의 기초를 다진 중요한 프로토콜로, 웹 개발자라면 반드시 이해해야 하는 기술입니다.

## 실제 사용 사례

HTTP 1.1은 다음과 같은 다양한 상황에서 사용됩니다:

1. **웹 브라우징**: 대부분의 웹 사이트는 아직도 HTTP 1.1을 통해 접근 가능합니다.
2. **RESTful API**: 많은 웹 API가 HTTP 1.1 기반으로 구현되어 있습니다.
3. **웹 서버**: Apache, Nginx 등의 대부분의 웹 서버는 HTTP 1.1을 기본적으로 지원합니다.
4. **마이크로서비스**: 서비스 간 통신에서 HTTP 1.1이 여전히 널리 사용됩니다.

## 결론

HTTP 1.1은 연결 재사용, 파이프라이닝, 호스트 헤더, 청크 전송 등 다양한 개선점을 통해 웹의 성능과 확장성을 크게 향상시켰습니다. 현대 웹의 기초를 다진 프로토콜로, 많은 웹 애플리케이션에서 여전히 널리 사용되고 있습니다.

그러나 HOL 차단, 헤더 중복, 제한된 병렬 처리 등의 한계점이 있어, 이를 극복하기 위한 HTTP/2, HTTP/3와 같은 새로운 버전이 등장했습니다. 웹 개발자로서 HTTP의 역사와 진화를 이해하는 것은 효율적인 웹 애플리케이션을 개발하는 데 큰 도움이 됩니다.

## 참고 자료

- RFC 2616: HTTP/1.1 (1999)
- RFC 7230-7235: HTTP/1.1 (2014 개정)
- "HTTP: The Definitive Guide" - David Gourley, Brian Totty
- "Web Performance in Action" - Jeremy Wagner
- MDN Web Docs: HTTP/1.1