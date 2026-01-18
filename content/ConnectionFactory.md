---
draft: true
tags:
  - r2dbc
  - database
---

ConnectionFactory는 R2DBC에서 데이터베이스 연결을 생성하는 진입점이다. JDBC의 `DataSource`와 유사한 역할을 하지만, `Publisher<Connection>`을 반환하여 논블로킹 방식으로 동작한다.

---

## 인터페이스 정의

```java
public interface ConnectionFactory {
    // 비동기적으로 Connection 생성
    Publisher<? extends Connection> create();

    // 팩토리 메타데이터 반환
    ConnectionFactoryMetadata getMetadata();
}
```

`create()` 메서드가 `Publisher`를 반환하는 것이 핵심이다. 커넥션 생성은 네트워크 I/O를 포함하므로 시간이 걸릴 수 있는데, 이를 블로킹하지 않고 비동기로 처리한다.

## ConnectionFactory 생성

### URL 방식

가장 간단한 방법은 R2DBC URL을 사용하는 것이다.

```java
ConnectionFactory factory = ConnectionFactories.get(
    "r2dbc:mysql://user:password@localhost:3306/mydb"
);
```

URL 형식:
```
r2dbc:[driver]:[protocol]://[user:password@]host[:port][/database][?option=value]
```

### 프로그래매틱 방식

`ConnectionFactoryOptions.Builder`를 사용하여 세밀하게 설정할 수 있다.

```java
ConnectionFactoryOptions options = ConnectionFactoryOptions.builder()
    .option(DRIVER, "mysql")
    .option(HOST, "localhost")
    .option(PORT, 3306)
    .option(USER, "myuser")
    .option(PASSWORD, "mypassword")
    .option(DATABASE, "mydb")
    // 드라이버별 옵션
    .option(Option.valueOf("sslMode"), "REQUIRED")
    .option(Option.valueOf("connectTimeout"), Duration.ofSeconds(10))
    .build();

ConnectionFactory factory = ConnectionFactories.get(options);
```

## 주요 옵션

R2DBC SPI가 정의하는 표준 옵션들이다.

| 옵션 | 설명 |
|-----|------|
| `DRIVER` | 드라이버 식별자 (mysql, postgresql 등) |
| `PROTOCOL` | 프로토콜 (선택적) |
| `HOST` | 호스트 주소 |
| `PORT` | 포트 번호 |
| `USER` | 사용자 이름 |
| `PASSWORD` | 비밀번호 |
| `DATABASE` | 데이터베이스 이름 |
| `CONNECT_TIMEOUT` | 연결 타임아웃 |
| `STATEMENT_TIMEOUT` | 쿼리 타임아웃 |
| `SSL` | SSL 사용 여부 |

각 드라이버는 추가로 고유한 옵션을 정의할 수 있다.

## 커넥션 획득과 사용

```java
Mono.from(factory.create())
    .flatMap(connection -> {
        return Mono.from(connection.createStatement("SELECT 1").execute())
            .doFinally(signal -> Mono.from(connection.close()).subscribe());
    })
    .subscribe();
```

커넥션은 명시적으로 닫아야 한다. `doFinally`나 try-with-resources 패턴처럼 리소스 정리를 보장하는 방식을 사용한다.

## 내부 동작: r2dbc-mysql 예시

r2dbc-mysql의 `MySqlConnectionFactory.create()` 내부를 살펴보면.

```mermaid
sequenceDiagram
    participant App as Application
    participant CF as MySqlConnectionFactory
    participant Client as ReactorNettyClient
    participant Server as MySQL Server

    App->>CF: create()
    CF->>Client: TCP 연결 (Reactor Netty)
    Client->>Server: 연결 요청
    Server->>Client: Handshake 패킷
    Client->>Server: 인증 응답
    Server->>Client: OK 또는 Error
    Client->>CF: Connection 객체 생성
    CF->>App: Publisher<Connection>
```

1. Reactor Netty로 TCP 연결 수립
2. MySQL 핸드셰이크 프로토콜 수행
3. 인증 (다양한 방식 지원: mysql_native_password, caching_sha2_password 등)
4. 세션 초기화 (타임존, 캐릭터셋 설정)
5. Connection 객체 반환

## ConnectionFactory와 커넥션 풀

`ConnectionFactory`는 호출할 때마다 새 커넥션을 생성한다. 실제 프로덕션에서는 [[Connection Pool]]을 사용해야 한다.

r2dbc-pool을 사용한 예시:

```java
ConnectionFactory connectionFactory = ConnectionFactories.get("r2dbc:mysql://...");

ConnectionPoolConfiguration configuration = ConnectionPoolConfiguration.builder(connectionFactory)
    .maxSize(20)
    .initialSize(5)
    .maxIdleTime(Duration.ofMinutes(30))
    .build();

ConnectionPool pool = new ConnectionPool(configuration);

// pool도 ConnectionFactory를 구현하므로 동일하게 사용
Mono.from(pool.create())
    .flatMap(connection -> ...)
    .subscribe();
```

## ConnectionFactoryMetadata

```java
ConnectionFactoryMetadata metadata = factory.getMetadata();
String productName = metadata.getName();  // 예: "MySQL"
```

드라이버 제품명을 반환한다. 디버깅이나 로깅에 유용하다.

## References

- [[R2DBC 동작 원리]]
- [[Service Provider Interface]]
- [[Connection Pool]]
