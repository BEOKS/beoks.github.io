HTTP(HyperText Transfer Protocol)는 웹에서 데이터를 주고받기 위한 애플리케이션 계층의 통신 프로토콜입니다. Tim Berners-Lee가 1989년에 처음 제안하였으며, WWW(World Wide Web)의 핵심 기술로 자리잡았습니다. HTTP는 클라이언트와 서버 간의 요청-응답 프로토콜로, 주로 웹 브라우저와 웹 서버 간의 통신에 사용됩니다.

## HTTP의 기본 원리

HTTP는 기본적으로 클라이언트-서버 아키텍처를 따르는 비연결성(Connectionless), 무상태(Stateless) 프로토콜입니다. 이 두 가지 특성은 HTTP의 가장 기본적인 특징입니다.

### 비연결성(Connectionless)

HTTP는 기본적으로 요청에 대한 응답을 마치면 연결을 끊는 비연결성 프로토콜입니다. 이는 서버의 자원 낭비를 줄이고 더 많은 클라이언트를 수용할 수 있게 해주지만, 매 요청마다 새로운 연결을 맺어야 하는 오버헤드가 발생합니다. [[HTTP 1.1]]에서는 이 문제를 해결하기 위해 keep-alive 헤더를 통한 지속 연결을 도입했습니다.

### 무상태(Stateless)

HTTP는 각 요청이 독립적으로 처리되는 무상태 프로토콜입니다. 서버는 이전 요청에 대한 정보를 저장하지 않으므로, 클라이언트는 필요한 모든 정보를 매 요청마다 포함해야 합니다. 이 특성으로 인해 서버의 확장성은 높아지지만, 사용자 세션 관리와 같이 상태 유지가 필요한 경우에는 추가적인 메커니즘(쿠키, 세션, 토큰 등)이 필요합니다.

## HTTP 메시지 구조

HTTP 메시지는 크게 요청(Request)과 응답(Response)으로 나뉩니다.

### HTTP 요청 메시지

```
GET /index.html HTTP/1.1
Host: www.example.com
User-Agent: Mozilla/5.0
Accept: text/html,application/xhtml+xml
```

HTTP 요청 메시지는 다음과 같은 구조를 가집니다:

1. **요청 라인(Request Line)**: 메서드, 요청 URI, HTTP 버전으로 구성
2. **헤더(Headers)**: 요청에 대한 추가 정보를 포함하는 헤더 필드
3. **공백 라인(Empty Line)**: 헤더와 본문을 구분하는 빈 줄
4. **본문(Body)**: 요청 데이터를 포함하는 본문(선택적)

### HTTP 응답 메시지

```
HTTP/1.1 200 OK
Date: Mon, 23 May 2023 22:38:34 GMT
Content-Type: text/html; charset=UTF-8
Content-Length: 138

<!DOCTYPE html>
<html>
<head>
  <title>Example Page</title>
</head>
<body>
  <h1>Hello, World!</h1>
</body>
</html>
```

HTTP 응답 메시지는 다음과 같은 구조를 가집니다:

1. **상태 라인(Status Line)**: HTTP 버전, 상태 코드, 상태 메시지로 구성
2. **헤더(Headers)**: 응답에 대한 추가 정보를 포함하는 헤더 필드
3. **공백 라인(Empty Line)**: 헤더와 본문을 구분하는 빈 줄
4. **본문(Body)**: 응답 데이터를 포함하는 본문

## HTTP 메서드

HTTP는 클라이언트가 서버에 특정 동작을 요청하기 위한 다양한 메서드를 제공합니다:

1. **GET**: 리소스를 요청합니다. 데이터를 가져오는 용도로만 사용되며, URL에 쿼리 파라미터로 데이터를 전송합니다.
2. **POST**: 서버에 데이터를 제출합니다. 새로운 리소스 생성, 데이터 처리 등에 사용됩니다.
3. **PUT**: 특정 리소스를 생성하거나 수정합니다.
4. **DELETE**: 특정 리소스를 삭제합니다.
5. **HEAD**: GET과 동일하지만 응답 본문을 반환하지 않고 헤더만 반환합니다.
6. **OPTIONS**: 서버가 지원하는 메서드 종류를 요청합니다.
7. **PATCH**: 리소스의 부분적인 수정을 요청합니다.
8. **TRACE**: 요청 메시지가 서버에 도달하기까지의 경로를 추적합니다.
9. **CONNECT**: 프록시를 통한 SSL 터널을 설정합니다.

HTTP 메서드의 특성과 적절한 사용법에 대한 자세한 내용은 [[HTTP 메서드와 RESTful API]]를 참고해주세요.

## HTTP 상태 코드

HTTP 응답은 요청의 성공 여부와 결과를 나타내는 상태 코드를 포함합니다. 상태 코드는 세 자리 숫자로, 다섯 가지 클래스로 분류됩니다:

1. **1xx (정보)**: 요청이 수신되어 처리 중임을 나타냅니다.
    
    - 100 Continue
    - 101 Switching Protocols
2. **2xx (성공)**: 요청이 성공적으로 처리되었음을 나타냅니다.
    
    - 200 OK
    - 201 Created
    - 204 No Content
3. **3xx (리다이렉션)**: 요청 완료를 위해 추가 조치가 필요함을 나타냅니다.
    
    - 301 Moved Permanently
    - 302 Found
    - 304 Not Modified
4. **4xx (클라이언트 오류)**: 요청에 오류가 있음을 나타냅니다.
    
    - 400 Bad Request
    - 401 Unauthorized
    - 403 Forbidden
    - 404 Not Found
5. **5xx (서버 오류)**: 서버가 요청을 처리하는 동안 오류가 발생했음을 나타냅니다.
    
    - 500 Internal Server Error
    - 502 Bad Gateway
    - 503 Service Unavailable

상태 코드의 의미와 처리 방법에 대한 자세한 내용은 [[HTTP 상태 코드의 이해]]를 참고해주세요.

## HTTP 헤더

HTTP 헤더는 HTTP 메시지에 추가 정보를 제공합니다. 헤더는 이름과 값의 쌍으로 구성되며, 콜론(:)으로 구분됩니다. 주요 헤더 카테고리는 다음과 같습니다:

### 일반 헤더(General Headers)

요청과 응답 모두에서 사용되는 헤더입니다.

- `Date`: 메시지가 생성된 날짜와 시간
- `Connection`: 연결 관리 옵션
- `Cache-Control`: 캐싱 정책

### 요청 헤더(Request Headers)

클라이언트가 서버에 추가 정보를 제공하는 헤더입니다.

- `Host`: 요청하는 호스트의 도메인 이름과 포트
- `User-Agent`: 클라이언트 애플리케이션 정보
- `Accept`: 클라이언트가 수용 가능한 콘텐츠 유형
- `Cookie`: 서버에 저장된 쿠키 정보
- `Authorization`: 인증 토큰 정보

### 응답 헤더(Response Headers)

서버가 응답에 대한 추가 정보를 제공하는 헤더입니다.

- `Server`: 서버 소프트웨어 정보
- `Set-Cookie`: 클라이언트에 쿠키 설정
- `Content-Type`: 응답 본문의 미디어 타입
- `Content-Length`: 응답 본문의 길이
- `Location`: 리다이렉션 대상 URL

### 엔티티 헤더(Entity Headers)

요청이나 응답의 본문에 대한 정보를 제공하는 헤더입니다.

- `Content-Encoding`: 본문 인코딩 방식
- `Content-Language`: 본문 언어
- `Expires`: 콘텐츠 만료 시간
- `Last-Modified`: 리소스 최종 수정 시간

HTTP 헤더에 대한 자세한 내용은 [[HTTP 헤더의 종류와 활용]]을 참고해주세요.

## HTTP의 진화

HTTP는 시간이 지남에 따라 여러 버전으로 발전해왔습니다:

### HTTP/0.9 (1991)

- 매우 단순한 프로토콜
- GET 메서드만 지원
- HTML 문서만 전송 가능

### HTTP/1.0 (1996)

- 버전 정보, 상태 코드, 헤더 개념 도입
- 다양한 파일 형식 지원
- 각 요청마다 새로운 연결 필요

### HTTP/1.1 (1997)

- 지속 연결(Persistent Connection) 도입
- 파이프라이닝(Pipelining) 지원
- 호스트 헤더 필수화로 가상 호스팅 지원
- 청크 전송 인코딩 도입
- 캐시 제어 메커니즘 개선

### HTTP/2 (2015)

- 바이너리 프로토콜로 변경
- 헤더 압축
- 서버 푸시 기능
- 요청의 다중화로 HOL 차단 문제 해결
- 스트림 우선순위 지정

### HTTP/3 (2022)

- UDP 기반의 QUIC 프로토콜 사용
- 연결 설정 시간 단축
- 혼잡 제어 개선
- 패킷 손실에 더 강한 내성

HTTP의 각 버전에 대한 자세한 내용은 [[HTTP의 버전별 특징]]을 참고해주세요.

## Java에서의 HTTP 통신

Java에서 HTTP 통신을 구현하는 방법에는 여러 가지가 있습니다:

### HttpURLConnection 사용 (Java SE 기본 제공)

```java
URL url = new URL("https://api.example.com/data");
HttpURLConnection connection = (HttpURLConnection) url.openConnection();
connection.setRequestMethod("GET");

int responseCode = connection.getResponseCode();
BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
String inputLine;
StringBuilder response = new StringBuilder();

while ((inputLine = in.readLine()) != null) {
    response.append(inputLine);
}
in.close();
```

### HttpClient 사용 (Java 11 이상)

```java
HttpClient client = HttpClient.newHttpClient();
HttpRequest request = HttpRequest.newBuilder()
        .uri(URI.create("https://api.example.com/data"))
        .GET()
        .build();

HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
System.out.println(response.body());
```

### 스프링의 RestTemplate 사용

```java
RestTemplate restTemplate = new RestTemplate();
String result = restTemplate.getForObject("https://api.example.com/data", String.class);
```

### 스프링의 WebClient 사용 (비동기)

```java
WebClient webClient = WebClient.create();
Mono<String> result = webClient.get()
        .uri("https://api.example.com/data")
        .retrieve()
        .bodyToMono(String.class);
```

Java에서의 HTTP 통신 구현에 대한 자세한 내용은 [[Java HTTP 클라이언트 API]]를 참고해주세요.

## HTTP의 보안

HTTP는 기본적으로 암호화되지 않은 평문 통신이므로, 중간자 공격(Man-in-the-Middle Attack)에 취약합니다. 이러한 보안 문제를 해결하기 위해 HTTPS(HTTP Secure)가 개발되었습니다.

### HTTPS

HTTPS는 HTTP 통신을 TLS(Transport Layer Security) 또는 SSL(Secure Sockets Layer) 프로토콜로 암호화하여 안전하게 전송합니다. HTTPS는 다음과 같은 보안 기능을 제공합니다:

1. **데이터 암호화**: 통신 내용을 암호화하여 제3자가 내용을 읽을 수 없게 합니다.
2. **서버 인증**: 인증서를 통해 클라이언트가 접속한 서버가 신뢰할 수 있는 서버인지 확인합니다.
3. **데이터 무결성**: 전송 중 데이터 변조를 방지합니다.

HTTPS에 대한 자세한 내용은 [[HTTPS와 SSL/TLS]]를 참고해주세요.

## HTTP 인증

HTTP는 다양한 인증 메커니즘을 제공합니다:

1. **Basic 인증**: 사용자 이름과 비밀번호를 Base64로 인코딩하여 전송합니다.
2. **Digest 인증**: 비밀번호의 해시값을 사용하여 보안을 강화합니다.
3. **Bearer 토큰**: OAuth나 JWT와 같은 토큰 기반 인증에 사용됩니다.
4. **API 키**: 요청 헤더나 쿼리 파라미터에 API 키를 포함시켜 인증합니다.

HTTP 인증에 대한 자세한 내용은 [[HTTP 인증 메커니즘]]을 참고해주세요.

## 결론

HTTP는 웹의 기반이 되는 핵심 프로토콜로, 웹 브라우저와 웹 서버 간의 통신을 가능하게 합니다. 비연결성과 무상태성이라는 특성으로 인해 확장성이 뛰어나며, 다양한 메서드와 상태 코드, 헤더를 통해 풍부한 기능을 제공합니다.

시간이 지남에 따라 HTTP는 계속 발전하여 더 나은 성능과 보안을 제공하고 있으며, 현대 웹 개발에서는 HTTP/2, HTTP/3와 같은 최신 버전과 HTTPS를 통한 보안 강화가 중요해지고 있습니다.

웹 개발자로서 HTTP 프로토콜의 원리와 특성을 이해하는 것은 효율적이고 안전한 웹 애플리케이션을 개발하는 데 있어 필수적인 요소입니다.

## 참고 자료

- RFC 7230-7235: HTTP/1.1 (2014)
- RFC 9110: HTTP Semantics (2022)
- "HTTP: The Definitive Guide" - David Gourley, Brian Totty
- MDN Web Docs: HTTP
- W3C HTTP Documentation