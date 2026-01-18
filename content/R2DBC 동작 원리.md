---
draft: true
tags:
  - database
  - reactive
  - java
---

R2DBC(Reactive Relational Database Connectivity)는 관계형 데이터베이스에 대한 리액티브, 논블로킹 접근을 가능하게 하는 명세다. 기존 [[JDBC]]가 블로킹 방식으로 설계되어 리액티브 애플리케이션의 병목이 되는 문제를 해결하기 위해 탄생했다.

---

## 왜 R2DBC인가

전통적인 JDBC는 "하나의 스레드가 하나의 커넥션을 점유"하는 모델을 사용한다. 쿼리를 실행하면 결과가 돌아올 때까지 해당 스레드는 아무 일도 하지 못하고 대기한다. 동시 요청이 1,000개라면 1,000개의 스레드가 필요하고, 대부분의 시간을 대기 상태로 보내게 된다.

R2DBC는 이 문제를 근본적으로 다른 방식으로 해결한다. [[리액티브 스트림(Reactive Streams)]] 명세를 기반으로 설계되어 적은 수의 스레드로 많은 동시 요청을 처리할 수 있다. 데이터베이스 응답을 기다리는 동안 스레드는 다른 작업을 처리하고, 응답이 도착하면 이벤트로 통지받아 처리를 재개한다.

```mermaid
sequenceDiagram
    participant App as Application
    participant T as Thread
    participant DB as Database

    Note over App,DB: JDBC 방식
    App->>T: 쿼리 요청
    T->>DB: SQL 실행
    Note over T: 블로킹 대기
    DB-->>T: 결과 반환
    T-->>App: 결과 전달

    Note over App,DB: R2DBC 방식
    App->>T: 쿼리 요청
    T->>DB: SQL 실행 (비동기)
    Note over T: 다른 작업 처리
    DB-->>T: 결과 이벤트
    T-->>App: 결과 스트림
```

## 핵심 아키텍처

R2DBC는 [[Service Provider Interface]] 패턴으로 설계되어 있다. 명세(SPI)와 구현(Driver)이 분리되어 있으며, 드라이버 벤더는 SPI를 구현하고 애플리케이션은 SPI를 통해 데이터베이스에 접근한다.

```mermaid
graph TB
    subgraph "Application Layer"
        App[Spring Data R2DBC<br/>또는 직접 사용]
    end

    subgraph "R2DBC SPI"
        CF[ConnectionFactory]
        Conn[Connection]
        Stmt[Statement]
        Res[Result]
    end

    subgraph "Driver Implementation"
        MySQL[r2dbc-mysql]
        PostgreSQL[r2dbc-postgresql]
        H2[r2dbc-h2]
    end

    subgraph "Database"
        MySQLDB[(MySQL)]
        PostgreSQLDB[(PostgreSQL)]
        H2DB[(H2)]
    end

    App --> CF
    CF --> Conn
    Conn --> Stmt
    Stmt --> Res

    MySQL --> MySQLDB
    PostgreSQL --> PostgreSQLDB
    H2 --> H2DB

    CF -.-> MySQL
    CF -.-> PostgreSQL
    CF -.-> H2
```

## 핵심 인터페이스

R2DBC SPI는 몇 가지 핵심 인터페이스로 구성된다.

### ConnectionFactory

[[ConnectionFactory]]는 데이터베이스 연결의 진입점이다. JDBC의 `DataSource`와 유사한 역할을 하지만, `Publisher<Connection>`을 반환하여 비동기적으로 커넥션을 생성한다.

```java
// URL 방식
ConnectionFactory factory = ConnectionFactories.get(
    "r2dbc:mysql://user:password@localhost:3306/mydb"
);

// 프로그래매틱 방식
ConnectionFactory factory = ConnectionFactories.get(
    ConnectionFactoryOptions.builder()
        .option(DRIVER, "mysql")
        .option(HOST, "localhost")
        .option(PORT, 3306)
        .option(USER, "user")
        .option(PASSWORD, "password")
        .option(DATABASE, "mydb")
        .build()
);
```

### Connection

Connection 인터페이스는 데이터베이스와의 실제 연결을 나타낸다. 트랜잭션 관리, Statement 생성, 연결 상태 관리 등을 담당한다. 모든 메서드가 `Publisher`를 반환하는 것이 특징이다.

```java
Mono.from(factory.create())
    .flatMap(connection -> {
        // 트랜잭션 시작
        return Mono.from(connection.beginTransaction())
            .then(Mono.from(connection.createStatement("INSERT INTO users (name) VALUES ($1)")
                .bind(0, "Alice")
                .execute()))
            .then(Mono.from(connection.commitTransaction()))
            .doFinally(signal -> connection.close());
    });
```

### Statement

[[Statement]]는 SQL 문을 표현하고 파라미터를 바인딩하는 역할을 한다. 인덱스 기반(`$1`, `?`)과 이름 기반(`:name`) 파라미터 바인딩을 모두 지원한다.

```java
connection.createStatement("SELECT * FROM users WHERE age > $1 AND city = $2")
    .bind(0, 25)
    .bind(1, "Seoul")
    .execute()
```

### Result

[[Result]]는 쿼리 실행 결과를 스트림으로 제공한다. 단순히 행(Row)뿐만 아니라 업데이트 카운트, 에러 메시지 등 다양한 세그먼트(Segment)로 구성된다.

```java
result.map((row, metadata) -> {
    return new User(
        row.get("id", Long.class),
        row.get("name", String.class),
        row.get("email", String.class)
    );
})
```

## 드라이버 구현의 내부 동작

r2dbc-mysql 드라이버를 예로 들어 실제 구현이 어떻게 이루어지는지 살펴보자.

### 네트워크 통신 계층

드라이버는 [[논블로킹(Non-blocking)|Non-blocking IO]]를 사용하여 데이터베이스와 통신한다. r2dbc-mysql은 Reactor Netty를 사용하여 이벤트 기반의 네트워크 처리를 구현했다.

```mermaid
graph LR
    subgraph "Application"
        App[Statement.execute]
    end

    subgraph "r2dbc-mysql"
        Client[ReactorNettyClient]
        Encoder[MessageEncoder]
        Decoder[MessageDecoder]
    end

    subgraph "Network"
        Channel[Netty Channel]
    end

    subgraph "MySQL"
        Server[MySQL Server]
    end

    App --> Client
    Client --> Encoder
    Encoder --> Channel
    Channel --> Server
    Server --> Channel
    Channel --> Decoder
    Decoder --> Client
    Client --> App
```

### 메시지 프로토콜

[[MySQL 프로토콜]]을 직접 구현하여 서버와 통신한다. 주요 메시지 타입은 다음과 같다.

**클라이언트 → 서버:**
- `TextQueryMessage`: 평문 SQL 쿼리
- `PrepareQueryMessage`: Prepared Statement 준비
- `PreparedExecuteMessage`: Prepared Statement 실행
- `HandshakeResponse`: 인증 응답

**서버 → 클라이언트:**
- `OkMessage`: 명령 성공
- `ErrorMessage`: 에러 발생
- `RowMessage`: 결과 행 데이터
- `DefinitionMetadataMessage`: 컬럼 메타데이터

### 코덱 시스템

[[Codec]]은 Java 타입과 MySQL 타입 간의 변환을 담당한다. r2dbc-mysql은 약 30개의 기본 코덱을 제공한다.

```java
// 코덱이 처리하는 변환의 예
// MySQL BIGINT ↔ Java Long
// MySQL VARCHAR ↔ Java String
// MySQL DATETIME ↔ Java LocalDateTime
// MySQL BLOB ↔ Java ByteBuffer 또는 Blob (리액티브 스트림)
```

특히 BLOB이나 CLOB 같은 대용량 데이터는 `Publisher<ByteBuffer>` 형태로 스트리밍되어 메모리 효율적으로 처리된다.

### 쿼리 캐싱

드라이버는 두 가지 레벨의 캐싱을 제공한다.

1. **Query Cache**: SQL 문자열을 파싱한 결과를 캐싱
2. **Prepare Cache**: 서버 측 Prepared Statement ID를 캐싱

```mermaid
graph TD
    SQL[SQL 문자열]
    QC{Query Cache}
    PC{Prepare Cache}
    Parse[SQL 파싱]
    Prepare[서버 PREPARE]
    Execute[실행]

    SQL --> QC
    QC -->|Hit| PC
    QC -->|Miss| Parse
    Parse --> PC
    PC -->|Hit| Execute
    PC -->|Miss| Prepare
    Prepare --> Execute
```

## Backpressure와 흐름 제어

R2DBC의 가장 중요한 특징 중 하나는 [[역압력(back pressure)|Backpressure]] 지원이다. 데이터베이스에서 데이터를 읽을 때, 소비자(Consumer)가 처리할 수 있는 속도에 맞춰 데이터를 요청할 수 있다.

```java
// fetchSize를 통한 backpressure 힌트
connection.createStatement("SELECT * FROM large_table")
    .fetchSize(100)  // 한 번에 100개씩 가져오기
    .execute()
    .flatMap(result -> result.map((row, meta) -> processRow(row)))
    .subscribe(
        item -> System.out.println(item),
        error -> error.printStackTrace(),
        () -> System.out.println("Done")
    );
```

이 메커니즘 덕분에 대용량 결과셋을 처리할 때도 메모리가 폭발하지 않는다.

## 성능 특성

R2DBC는 모든 상황에서 JDBC보다 빠른 것은 아니다. 다음과 같은 특성을 이해하고 적절한 상황에서 사용해야 한다.

| 상황 | R2DBC | JDBC |
|------|-------|------|
| 높은 동시성 (200+ 요청) | 우수 | 스레드 고갈 위험 |
| 낮은 동시성 | 오버헤드로 인해 불리 | 우수 |
| 대용량 결과셋 스트리밍 | 우수 (backpressure) | 메모리 이슈 가능 |
| 단순 CRUD | 비슷하거나 약간 느림 | 비슷하거나 약간 빠름 |

리액티브 프로그래밍 자체에 오버헤드가 있기 때문에, 소규모 결과셋의 단순 쿼리에서는 JDBC가 더 나을 수 있다.

## 실제 사용 예시

Spring Data R2DBC를 사용하면 Repository 패턴으로 편리하게 사용할 수 있다.

```java
@Repository
public interface UserRepository extends ReactiveCrudRepository<User, Long> {
    Flux<User> findByAgeGreaterThan(int age);

    @Query("SELECT * FROM users WHERE city = :city")
    Flux<User> findByCity(String city);
}
```

또는 `DatabaseClient`를 사용하여 더 세밀한 제어가 가능하다.

```java
@Autowired
DatabaseClient client;

public Flux<User> findActiveUsers() {
    return client.sql("SELECT * FROM users WHERE active = true")
        .map((row, metadata) -> new User(
            row.get("id", Long.class),
            row.get("name", String.class)
        ))
        .all();
}
```

## 정리

R2DBC는 리액티브 애플리케이션에서 관계형 데이터베이스를 사용할 때 발생하는 "리액티브 갭"을 해결한다. 핵심은 다음과 같다.

1. **Reactive Streams 기반**: 모든 연산이 `Publisher`를 반환하여 논블로킹 처리 가능
2. **SPI 아키텍처**: 명세와 구현의 분리로 다양한 데이터베이스 지원
3. **Backpressure**: 소비자 속도에 맞춘 데이터 흐름 제어
4. **효율적인 리소스 사용**: 적은 스레드로 높은 동시성 처리

다만 모든 상황에서 JDBC를 대체하는 것은 아니며, 높은 동시성과 리액티브 스택이 필요한 경우에 적합하다.

## References

- [R2DBC 공식 사이트](https://r2dbc.io/)
- [R2DBC GitHub](https://github.com/r2dbc)
- [r2dbc-mysql](https://github.com/asyncer-io/r2dbc-mysql)
- [r2dbc-spi](https://github.com/r2dbc/r2dbc-spi)
- [Baeldung - R2DBC](https://www.baeldung.com/r2dbc)
- [Spring: Blocking vs non-blocking: R2DBC vs JDBC](https://technology.amis.nl/software-development/performance-and-tuning/spring-blocking-vs-non-blocking-r2dbc-vs-jdbc-and-webflux-vs-web-mvc/)
