청크드 전송 인코딩은 [[HTTP 1.1]]에서 도입된 데이터 전송 방식으로, 전체 콘텐츠의 크기를 미리 알지 못하는 상황에서도 데이터를 점진적으로 전송할 수 있게 해주는 메커니즘입니다. 이 방식은 웹 서버가 응답의 최종 크기를 계산하지 않고도 콘텐츠를 효율적으로 스트리밍할 수 있게 해주어 웹 애플리케이션의 성능과 사용자 경험을 크게 향상시켰습니다.

## 등장 배경

초기 [[HTTP 1.0]]에서는 응답을 전송할 때 Content-Length 헤더를 통해 응답 본문의 크기를 미리 명시해야 했습니다. 이로 인해 서버는 다음과 같은 제약에 직면했습니다:

1. 응답을 전송하기 전에 전체 응답 내용을 메모리에 버퍼링해야 했습니다.
2. 동적으로 생성되는, 크기를 미리 알 수 없는 콘텐츠를 효율적으로 처리할 수 없었습니다.
3. 장시간 실행되는 프로세스나 스트리밍과 같은 작업에 적합하지 않았습니다.

이러한 문제를 해결하기 위해 HTTP/1.1에서는 청크드 전송 인코딩이 도입되었습니다.

## 청크드 전송 인코딩의 작동 방식

청크드 전송 인코딩은 다음과 같은 형식으로 데이터를 전송합니다:

```
[청크 크기(16진수)]\r\n
[청크 데이터]\r\n
[청크 크기(16진수)]\r\n
[청크 데이터]\r\n
...
0\r\n
[선택적 푸터 헤더들]\r\n
\r\n
```

주요 특징은 다음과 같습니다:

1. 각 청크는 크기를 나타내는 16진수와 그 뒤에 오는 실제 데이터로 구성됩니다.
2. 청크의 크기는 16진수로 표현되고, 그 뒤에 CR LF(\r\n)가 옵니다.
3. 청크 데이터 다음에도 CR LF가 따릅니다.
4. 마지막 청크는 크기가 0인 청크로 표시되며, 그 뒤에 선택적으로 푸터 헤더가 올 수 있습니다.
5. 전송은 빈 라인(\r\n)으로 종료됩니다.

### 예시

```
HTTP/1.1 200 OK
Content-Type: text/plain
Transfer-Encoding: chunked

7\r\n
Mozilla\r\n
9\r\n
Developer\r\n
7\r\n
Network\r\n
0\r\n
\r\n
```

이 예제에서는 "Mozilla", "Developer", "Network"라는 세 개의 청크가 전송되고 있습니다. 각 청크 앞에는 해당 청크의 바이트 크기(16진수)가 표시되어 있습니다.

## 청크드 전송 인코딩의 장점

청크드 전송 인코딩은 다음과 같은 여러 이점을 제공합니다:

1. **메모리 효율성**: 전체 응답을 메모리에 버퍼링할 필요 없이 생성되는 대로 데이터를 전송할 수 있습니다.
2. **자원 활용 최적화**: 데이터가 생성되는 즉시 전송할 수 있어 서버 자원이 효율적으로 활용됩니다.
3. **사용자 경험 향상**: 클라이언트가 전체 응답을 기다리지 않고 데이터를 점진적으로 받아 처리할 수 있습니다.
4. **연결 재사용**: HTTP/1.1의 지속적 연결(Keep-Alive)과 결합하여 여러 요청에 같은 연결을 재사용할 수 있습니다.
5. **무한 스트리밍**: 종료 시점을 미리 알 수 없는 데이터 스트림을 전송할 수 있습니다.

## HTTP 헤더와의 관계

청크드 전송 인코딩을 사용하기 위해서는 응답 헤더에 다음과 같은 설정이 필요합니다:

```
Transfer-Encoding: chunked
```

이 헤더가 존재하면 Content-Length 헤더는 무시됩니다. 두 헤더는 상호 배타적이므로 함께 사용해서는 안 됩니다.

## 실제 활용 사례

청크드 전송 인코딩은 다양한 시나리오에서 유용하게 활용됩니다:

1. **대용량 파일 다운로드**: 대용량 파일을 청크로 나누어 전송함으로써 클라이언트가 점진적으로 다운로드 진행 상황을 확인할 수 있습니다.
2. **실시간 데이터 스트리밍**: 뉴스 피드, 채팅 메시지, 로그 데이터 등 실시간으로 생성되는 데이터를 효율적으로 스트리밍할 수 있습니다.
3. **서버-전송 이벤트(SSE)**: 서버에서 클라이언트로의 단방향 실시간 업데이트를 위해 청크드 전송 인코딩을 활용합니다.
4. **점진적 페이지 렌더링**: 웹 페이지의 일부를 먼저 전송하여 사용자가 전체 페이지 로딩을 기다리지 않고도 콘텐츠를 볼 수 있게 합니다.

## 자바에서의 청크드 전송 인코딩 구현

자바에서는 HTTP 클라이언트와 서버 모두에서 청크드 전송 인코딩을 지원합니다. 다음은 스프링 프레임워크를 사용한 간단한 구현 예시입니다:

### 서버 측 구현 (스프링 부트)

```java
@RestController
public class StreamingController {
    
    @GetMapping(value = "/stream-data", produces = MediaType.TEXT_PLAIN_VALUE)
    public ResponseEntity<StreamingResponseBody> streamData() {
        StreamingResponseBody responseBody = outputStream -> {
            for (int i = 0; i < 10; i++) {
                outputStream.write(("데이터 청크 #" + i + "\n").getBytes());
                outputStream.flush();
                
                try {
                    Thread.sleep(1000); // 실제 시나리오에서는 데이터 생성 지연을 시뮬레이션
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        };
        
        return ResponseEntity.ok()
                .header(HttpHeaders.TRANSFER_ENCODING, "chunked")
                .body(responseBody);
    }
}
```

이 예제에서는 스프링의 `StreamingResponseBody`를 사용하여 1초 간격으로 10개의 데이터 청크를 생성하고 전송합니다. 스프링은 자동으로 청크드 전송 인코딩을 적용합니다.

### 클라이언트 측 구현 (자바 11 HttpClient)

```java
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;

public class ChunkedClient {
    
    public static void main(String[] args) throws Exception {
        HttpClient client = HttpClient.newBuilder()
                .connectTimeout(Duration.ofSeconds(10))
                .build();
        
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("http://localhost:8080/stream-data"))
                .GET()
                .build();
        
        client.send(request, HttpResponse.BodyHandlers.ofLines())
                .body()
                .forEach(line -> {
                    System.out.println("수신된 청크: " + line);
                });
    }
}
```

이 클라이언트는 서버로부터 청크드 응답을 수신하고, 각 라인을 받을 때마다 처리합니다.

## 청크드 전송과 압축의 조합

청크드 전송 인코딩은 콘텐츠 압축과 함께 사용할 수 있어 더욱 효율적인 데이터 전송이 가능합니다:

```
HTTP/1.1 200 OK
Content-Type: text/html
Transfer-Encoding: chunked
Content-Encoding: gzip

[압축된 청크 데이터]
```

이 경우 서버는 먼저 콘텐츠를 압축한 다음, 압축된 데이터를 청크로 나누어 전송합니다. 클라이언트는 청크를 수신하고 재조립한 후 압축을 해제하여 원본 콘텐츠를 복원합니다.

## [[HTTP 2.0]]와 청크드 전송 인코딩

HTTP/2에서는 기존의 청크드 전송 인코딩이 더 이상 필요하지 않습니다. HTTP/2는 자체적인 바이너리 프레이밍 계층을 통해 데이터 스트리밍을 처리하며, 이는 HTTP/1.1의 청크드 전송보다 더 효율적입니다.

그러나 HTTP/1.1에서 HTTP/2로의 점진적인 마이그레이션 과정에서 많은 시스템이 여전히 청크드 전송 인코딩을 사용하고 있습니다. 또한 HTTP/1.1 클라이언트와 서버 간의 통신에서는 청크드 전송 인코딩이 여전히 중요한 역할을 합니다.

## 디버깅 및 문제 해결

청크드 전송 인코딩을 사용할 때 발생할 수 있는 일반적인 문제와 해결 방법은 다음과 같습니다:

1. **청크 형식 오류**: 각 청크의 형식이 올바르지 않으면 클라이언트가 응답을 제대로 해석할 수 없습니다. 네트워크 모니터링 도구를 사용하여 청크 형식을 검증하세요.
2. **헤더 충돌**: Content-Length와 Transfer-Encoding: chunked를 함께 사용하면 문제가 발생할 수 있습니다. 두 헤더 중 하나만 사용하세요.
3. **버퍼링 문제**: 일부 프록시나 미들웨어가 청크드 응답을 완전히 버퍼링하여 스트리밍 이점을 무효화할 수 있습니다. 네트워크 구성을 확인하세요.
4. **타임아웃 관리**: 장시간 실행되는 청크드 전송은 타임아웃과 충돌할 수 있습니다. 클라이언트와 서버의 타임아웃 설정을 적절히 조정하세요.

자세한 디버깅 방법은 HTTP 디버깅 기법을 참고해주세요.

## 결론

청크드 전송 인코딩은 웹 애플리케이션에서 동적 콘텐츠와 스트리밍 데이터를 효율적으로 처리하기 위한 강력한 도구입니다. 크기를 미리 알 수 없는 콘텐츠를 점진적으로 생성하고 전송할 수 있게 함으로써, 서버의 메모리 사용을 최적화하고 사용자 경험을 향상시키는 데 크게 기여합니다.

현대 웹 개발에서는 서버-전송 이벤트(SSE), 롱 폴링(Long Polling), 웹소켓(WebSocket) 등 다양한 실시간 통신 기술이 발전했지만, 청크드 전송 인코딩은 여전히 HTTP/1.1 기반 애플리케이션에서 단순하고 효과적인 스트리밍 솔루션으로 널리 사용되고 있습니다.

웹 개발자라면 청크드 전송 인코딩의 원리와 활용법을 이해하는 것이 서버 성능 최적화와 사용자 경험 향상을 위한 중요한 역량이 될 것입니다.

## 참고 자료

- HTTP/1.1 Specification (RFC 7230)
- 스프링 프레임워크 공식 문서(https://docs.spring.io/spring-framework/docs/current/reference/html/web.html#mvc-ann-async-http-streaming)
- Java HTTP Client 문서(https://docs.oracle.com/en/java/javase/11/docs/api/java.net.http/java/net/http/HttpClient.html)
- HTTP: The Definitive Guide - David Gourley, Brian Totty

