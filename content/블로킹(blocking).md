블로킹(Blocking)은 프로그래밍에서 특정 작업이 완료될 때까지 프로그램의 진행을 멈추는 동작 방식을 의미합니다. 이는 특히 입출력(I/O) 작업, 네트워크 통신, 동기화 메커니즘 등에서 자주 발생합니다. 블로킹 방식에서는 작업이 완료될 때까지 해당 스레드가 대기 상태에 머물러 있으며 다른 작업을 수행하지 못합니다. 블로킹의 개념을 더 깊이 이해하기 위해서는 [[논블로킹(Non-blocking)]]과의 차이점을 살펴보는 것이 중요합니다.

## 블로킹의 기본 개념

블로킹 작업의 핵심 특성은 다음과 같습니다:

1. **대기 상태**: 호출된 작업이 완료될 때까지 호출한 스레드가 대기합니다.
2. **자원 점유**: 블로킹된 스레드는 시스템 자원(CPU 시간)을 거의 사용하지 않지만, 메모리는 계속 점유합니다.
3. **컨텍스트 전환**: 운영체제는 블로킹된 스레드에서 다른 스레드로 컨텍스트를 전환하여 CPU 사용을 최적화합니다.
4. **순차적 실행**: 블로킹 방식에서는 코드가 순차적으로 실행됩니다.

## 블로킹 동작 방식

블로킹 작업의 기본적인 동작 흐름은 다음과 같습니다:

```mermaid
sequenceDiagram
    participant A as 애플리케이션 스레드
    participant B as 시스템 리소스(파일, 네트워크 등)
    
    A->>B: 작업 요청(예: 파일 읽기)
    Note over A: 스레드 블로킹 (대기 상태)
    B-->>A: 작업 완료 및 결과 반환
    Note over A: 스레드 활성화 (실행 상태)
    A->>A: 다음 작업 수행
```

이 다이어그램에서 볼 수 있듯이, 애플리케이션 스레드는 시스템 리소스에 작업을 요청한 후 해당 작업이 완료될 때까지 블로킹 상태에 머물러 있습니다.

## 블로킹과 논블로킹의 차이

자세한 내용은 [[블로킹과 논블로킹의 차이]]를 참고해주세요.

## 블로킹 작업의 종류

### 1. I/O 블로킹

가장 일반적인 블로킹 작업으로, 파일 읽기/쓰기, 네트워크 통신 등이 포함됩니다:

```java
// 파일 읽기 블로킹 예제
try (FileInputStream fis = new FileInputStream("data.txt")) {
    byte[] buffer = new byte[1024];
    int bytesRead = fis.read(buffer); // 이 호출은 데이터를 읽을 때까지 블로킹됩니다
    // 파일 읽기가 완료된 후에만 실행됩니다
    System.out.println("읽은 바이트 수: " + bytesRead);
} catch (IOException e) {
    e.printStackTrace();
}
```

### 2. 스레드 동기화 블로킹

`synchronized` 블록, 락(Lock), 세마포어(Semaphore) 등의 동기화 메커니즘에서 발생합니다:

```java
private final Object lock = new Object();

public void synchronizedMethod() {
    synchronized (lock) {
        // 다른 스레드가 이미 lock을 획득한 경우, 이 지점에서 블로킹됩니다
        // lock을 획득한 후에만 실행됩니다
        performCriticalOperation();
    }
}
```

### 3. 스레드 조인(Join) 블로킹

한 스레드가 다른 스레드의 완료를 기다릴 때 발생합니다:

```java
Thread worker = new Thread(() -> {
    // 작업 수행
    try {
        Thread.sleep(2000); // 작업 시뮬레이션
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
});

worker.start();
try {
    worker.join(); // worker 스레드가 완료될 때까지 현재 스레드가 블로킹됩니다
    // worker 스레드가 완료된 후에만 실행됩니다
    System.out.println("작업자 스레드 완료");
} catch (InterruptedException e) {
    e.printStackTrace();
}
```

### 4. 네트워크 소켓 블로킹

소켓 통신에서 데이터를 기다릴 때 발생합니다:

```java
try (ServerSocket serverSocket = new ServerSocket(8080)) {
    Socket clientSocket = serverSocket.accept(); // 클라이언트 연결을 기다리며 블로킹됩니다
    // 클라이언트가 연결된 후에만 실행됩니다
    handleClientConnection(clientSocket);
} catch (IOException e) {
    e.printStackTrace();
}
```

## 블로킹 작업의 장단점

### 장점

1. **단순성**: 코드가 직관적이고 이해하기 쉽습니다.
2. **순차적 실행**: 작업의 순서가 명확하게 보장됩니다.
3. **자원 효율성**: 대기 중인 스레드는 CPU를 거의 사용하지 않습니다.
4. **오류 처리 용이성**: 작업 실패 시 즉시 예외가 발생하여 처리할 수 있습니다.
5. **디버깅 용이성**: 실행 흐름이 명확하여 디버깅이 쉽습니다.

### 단점

1. **스레드 낭비**: 블로킹된 스레드는 다른 작업을 수행할 수 없어 자원이 낭비됩니다.
2. **성능 제한**: 많은 동시 요청을 처리할 때 성능 병목 현상이 발생할 수 있습니다.
3. **확장성 제한**: 동시 작업 처리 능력이 제한됩니다.
4. **데드락 위험**: 부적절한 블로킹은 데드락(교착 상태)을 유발할 수 있습니다.
5. **응답성 저하**: UI 스레드가 블로킹되면 애플리케이션이 응답하지 않는 것처럼 보일 수 있습니다.

## 블로킹의 상태와 전환

스레드가 블로킹 상태에 들어가면 일반적으로 다음과 같은 상태 전환이 일어납니다:

```mermaid
stateDiagram-v2
    실행중 --> 블로킹: I/O 작업, 락 획득 시도 등
    블로킹 --> 준비: 작업 완료, 락 획득 성공 등
    준비 --> 실행중: 스케줄러에 의해 선택됨
    실행중 --> 종료: 작업 완료
    블로킹 --> 종료: 인터럽트 등으로 인한 예외
```

이 다이어그램은 스레드의 상태 전환을 보여줍니다. 블로킹된 스레드는 해당 작업이 완료되면 '준비' 상태로 전환되고, 스케줄러에 의해 다시 '실행중' 상태로 전환될 수 있습니다.

## Java에서의 블로킹 API

Java는 기본적으로 많은 블로킹 API를 제공합니다:

### 1. 표준 I/O API

```java
// 블로킹 I/O 예제
try (BufferedReader reader = new BufferedReader(new FileReader("large-file.txt"))) {
    String line;
    while ((line = reader.readLine()) != null) { // 각 readLine() 호출은 블로킹됩니다
        processLine(line);
    }
} catch (IOException e) {
    e.printStackTrace();
}
```

### 2. JDBC (데이터베이스 접근)

```java
// JDBC 블로킹 예제
try (Connection conn = DriverManager.getConnection(DB_URL, USER, PASS);
     Statement stmt = conn.createStatement();
     ResultSet rs = stmt.executeQuery("SELECT * FROM users")) { // 쿼리 실행 동안 블로킹됩니다
    
    while (rs.next()) {
        String username = rs.getString("username");
        System.out.println(username);
    }
} catch (SQLException e) {
    e.printStackTrace();
}
```

### 3. Socket API

```java
// 소켓 블로킹 예제
try (Socket socket = new Socket("example.com", 80);
     OutputStream out = socket.getOutputStream();
     InputStream in = socket.getInputStream()) {
    
    // 요청 전송
    out.write("GET / HTTP/1.1\r\nHost: example.com\r\n\r\n".getBytes());
    
    // 응답 읽기 (블로킹됨)
    byte[] buffer = new byte[4096];
    int bytesRead = in.read(buffer); // 서버 응답을 기다리며 블로킹됩니다
    
    System.out.println(new String(buffer, 0, bytesRead));
} catch (IOException e) {
    e.printStackTrace();
}
```

### 4. 스레드 동기화

```java
// 스레드 동기화 블로킹 예제
private final ReentrantLock lock = new ReentrantLock();

public void lockExample() {
    lock.lock(); // 락을 획득할 때까지 블로킹됩니다
    try {
        // 임계 영역
        performCriticalOperation();
    } finally {
        lock.unlock();
    }
}
```

## 블로킹 처리의 최적화 기법

블로킹 작업의 제한 사항을 완화하기 위한 몇 가지 최적화 기법은 다음과 같습니다:

### 1. [[멀티스레딩(Multithreading)]]

여러 스레드를 사용하여 블로킹 작업을 병렬로 처리합니다:

```java
ExecutorService executor = Executors.newFixedThreadPool(10);

for (Task task : tasks) {
    executor.submit(() -> {
        // 각 스레드에서 블로킹 작업 수행
        performBlockingTask(task);
    });
}

executor.shutdown();
```

멀티스레딩에 대한 자세한 내용은 [[멀티스레딩과 블로킹]]을 참고해주세요.

### 2. 타임아웃 설정

블로킹 작업에 타임아웃을 설정하여 무한정 대기하는 것을 방지합니다:

```java
// 소켓 타임아웃 예제
Socket socket = new Socket();
socket.connect(new InetSocketAddress("example.com", 80), 5000); // 5초 타임아웃
socket.setSoTimeout(3000); // 읽기 작업에 3초 타임아웃 설정

try (InputStream in = socket.getInputStream()) {
    byte[] buffer = new byte[4096];
    int bytesRead = in.read(buffer); // 최대 3초간 블로킹됩니다
    // 처리 로직
} catch (SocketTimeoutException e) {
    System.out.println("읽기 타임아웃 발생");
} catch (IOException e) {
    e.printStackTrace();
}
```

### 3. 폴링 대신 이벤트 기반 접근

폴링보다 이벤트 기반 접근 방식을 사용하여 블로킹을 줄입니다:

```java
// NIO 선택기를 사용한 이벤트 기반 접근
Selector selector = Selector.open();
channel.configureBlocking(false); // 논블로킹 모드 설정
channel.register(selector, SelectionKey.OP_READ);

while (true) {
    int readyChannels = selector.select(); // 이벤트 발생까지 블로킹됨
    if (readyChannels == 0) continue;
    
    Set<SelectionKey> selectedKeys = selector.selectedKeys();
    Iterator<SelectionKey> keyIterator = selectedKeys.iterator();
    
    while (keyIterator.hasNext()) {
        SelectionKey key = keyIterator.next();
        if (key.isReadable()) {
            // 데이터 읽기 가능
            processData((SocketChannel) key.channel());
        }
        keyIterator.remove();
    }
}
```

### 4. 비동기 API 활용

가능한 경우 블로킹 API 대신 비동기 API를 사용합니다:

```java
// CompletableFuture를 사용한 비동기 처리
CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
    // 블로킹 작업을 별도 스레드에서 수행
    return performBlockingOperation();
});

// 비블로킹 방식으로 결과 처리
future.thenAccept(result -> {
    System.out.println("결과: " + result);
});

// 현재 스레드는 블로킹되지 않고 다른 작업 수행 가능
performOtherTasks();
```

비동기 API에 대한 자세한 내용은 [[비동기 프로그래밍과 블로킹 회피]]를 참고해주세요.

## 스프링 프레임워크에서의 블로킹 처리

스프링 프레임워크는 기본적으로 블로킹 방식으로 작동하지만, 비블로킹 방식도 지원합니다:

### 블로킹 컨트롤러 (기본 방식)

```java
@RestController
@RequestMapping("/api")
public class BlockingController {
    
    @Autowired
    private UserService userService;
    
    @GetMapping("/users/{id}")
    public ResponseEntity<User> getUser(@PathVariable Long id) {
        // 데이터베이스 조회는 블로킹 작업입니다
        User user = userService.findById(id);
        return ResponseEntity.ok(user);
    }
}
```

이 예제에서 컨트롤러는 `userService.findById(id)` 호출 중에 블로킹됩니다. 이는 Tomcat과 같은 서블릿 기반 서버에서 스레드 풀을 사용하여 처리됩니다.

### 블로킹 작업의 비동기 처리

스프링에서는 블로킹 작업을 비동기적으로 처리할 수 있는 방법도 제공합니다:

```java
@Service
public class AsyncUserService {
    
    @Async
    public CompletableFuture<User> findByIdAsync(Long id) {
        // 블로킹 작업이지만 별도 스레드에서 실행됨
        User user = findUserFromDatabase(id);
        return CompletableFuture.completedFuture(user);
    }
}

@RestController
@RequestMapping("/api")
public class AsyncController {
    
    @Autowired
    private AsyncUserService userService;
    
    @GetMapping("/users/{id}/async")
    public CompletableFuture<ResponseEntity<User>> getUserAsync(@PathVariable Long id) {
        return userService.findByIdAsync(id)
                .thenApply(ResponseEntity::ok);
    }
}
```

이 방식에서는 블로킹 작업이 별도의 스레드 풀에서 실행되므로 메인 스레드가 블로킹되지 않습니다.

## 블로킹으로 인한 문제와 해결 방법

### 데드락(교착 상태)

여러 스레드가 서로 블로킹되어 아무도 진행할 수 없는 상태가 발생할 수 있습니다:

```java
// 데드락 위험이 있는 코드
public class DeadlockRisk {
    private final Object resource1 = new Object();
    private final Object resource2 = new Object();
    
    public void method1() {
        synchronized (resource1) {
            System.out.println("method1: resource1 획득");
            try { Thread.sleep(100); } catch (InterruptedException e) {}
            
            synchronized (resource2) {
                System.out.println("method1: resource2 획득");
            }
        }
    }
    
    public void method2() {
        synchronized (resource2) {
            System.out.println("method2: resource2 획득");
            try { Thread.sleep(100); } catch (InterruptedException e) {}
            
            synchronized (resource1) {
                System.out.println("method2: resource1 획득");
            }
        }
    }
}
```

해결 방법:

- 락 순서 일관성 유지 (항상 같은 순서로 락 획득)
- 타임아웃 사용
- 락 계층 구조 설계
- [[트라이락(tryLock)]] 메서드 활용

### 스레드 풀 고갈

모든 스레드가 블로킹 작업을 수행하면 스레드 풀이 고갈될 수 있습니다:

```java
@Service
public class SlowService {
    
    @Autowired
    private ExternalApiClient client;
    
    public Result processRequest() {
        // 오래 걸리는 외부 API 호출 (블로킹)
        ExternalData data = client.fetchData(); // 10초 소요
        return processData(data);
    }
}
```

해결 방법:

- 적절한 스레드 풀 크기 설정
- 블로킹 작업에 별도의 스레드 풀 사용
- 비동기 처리 방식 도입
- 타임아웃 설정
- [[서킷 브레이커(Circuit Breaker)]] 패턴 적용

## 블로킹 디버깅 기법

블로킹 관련 문제를 디버깅하는 방법은 다음과 같습니다:

### 1. 스레드 덤프 분석

Java에서는 `jstack` 도구를 사용하여 스레드 덤프를 생성하고 분석할 수 있습니다:

```bash
jstack [JVM 프로세스 ID] > thread_dump.txt
```

스레드 덤프에서 'BLOCKED' 상태의 스레드와 해당 스레드가 기다리고 있는 락을 확인합니다.

### 2. 프로파일링 도구 사용

VisualVM, JProfiler, YourKit 등의 프로파일링 도구를 사용하여 블로킹 지점과 스레드 상태를 시각적으로 분석합니다.

### 3. 로깅 추가

블로킹 의심 지점 전후에 타임스탬프가 포함된 로그를 추가합니다:

```java
long startTime = System.currentTimeMillis();
log.info("데이터베이스 조회 시작");
Result result = performDatabaseQuery(); // 블로킹 작업
long endTime = System.currentTimeMillis();
log.info("데이터베이스 조회 완료: 소요 시간 {}ms", (endTime - startTime));
```

### 4. 타임아웃 추가

디버깅 중에 임시로 타임아웃을 추가하여 블로킹 지점을 식별합니다:

```java
ExecutorService executor = Executors.newSingleThreadExecutor();
Future<Result> future = executor.submit(() -> performBlockingOperation());

try {
    Result result = future.get(5, TimeUnit.SECONDS); // 5초 타임아웃
    processResult(result);
} catch (TimeoutException e) {
    log.error("작업이 5초 이상 블로킹됨");
    future.cancel(true);
} finally {
    executor.shutdown();
}
```

## 블로킹 성능 측정

블로킹 작업의 성능을 측정하는 방법은 다음과 같습니다:

### 1. 응답 시간 측정

```java
long startTime = System.nanoTime();
result = performBlockingOperation();
long endTime = System.nanoTime();
double durationMs = (endTime - startTime) / 1_000_000.0;
System.out.printf("작업 소요 시간: %.2f ms%n", durationMs);
```

### 2. 스루풋 측정

```java
int totalOperations = 1000;
long startTime = System.currentTimeMillis();

for (int i = 0; i < totalOperations; i++) {
    performBlockingOperation();
}

long endTime = System.currentTimeMillis();
double durationSec = (endTime - startTime) / 1000.0;
double throughput = totalOperations / durationSec;
System.out.printf("초당 처리량: %.2f 작업/초%n", throughput);
```

### 3. 병목 지점 식별

JMeter, Gatling 등의 부하 테스트 도구를 사용하여 블로킹으로 인한 병목 지점을 식별합니다.

## 블로킹이 적합한 상황

블로킹 방식이 더 적합한 경우도 있습니다:

1. **단순한 애플리케이션**: 동시성 요구사항이 낮은 경우
2. **리소스 제약 환경**: 메모리나 CPU가 제한된 환경에서는 블로킹 방식이 오버헤드가 적을 수 있습니다
3. **트랜잭션 처리**: 데이터 일관성이 중요한 트랜잭션에서는 블로킹 방식이 단순하고 안전합니다
4. **순차적 처리 필요**: 작업이 순차적으로 처리되어야 하는 경우
5. **개발 용이성**: 단순한 동기 코드가 복잡한 비동기 코드보다 개발 및 디버깅이 쉬울 수 있습니다

## 실제 사용 사례

블로킹은 다양한 상황에서 활용됩니다:

1. **데이터베이스 트랜잭션**: ACID 속성을 보장하기 위한 블로킹
2. **파일 I/O**: 디스크에서 파일을 읽고 쓰는 작업
3. **네트워크 통신**: 클라이언트-서버 통신에서의 요청/응답 패턴
4. **동기화 메커니즘**: 멀티스레드 환경에서의 데이터 일관성 유지
5. **사용자 입력 처리**: 사용자 입력을 기다리는 콘솔 애플리케이션

## 결론

블로킹은 프로그래밍에서 가장 기본적인 실행 모델로, 직관적이고 이해하기 쉽다는 장점이 있습니다. 그러나 고성능, 고확장성 애플리케이션에서는 블로킹으로 인한 제약 사항이 중요한 고려 사항이 됩니다.

현대적인 애플리케이션 개발에서는 블로킹과 논블로킹 방식을 상황에 맞게 적절히 조합하여 사용하는 것이 중요합니다. 특히 Java와 스프링 생태계에서는 [[CompletableFuture]], [[WebFlux]], [[코루틴(Coroutine)]] 등 블로킹의 제약을 극복하기 위한 다양한 대안이 제공되고 있습니다.

블로킹의 특성과 제약을 이해하고, 애플리케이션의 요구사항에 맞는 적절한 처리 방식을 선택함으로써 효율적이고 안정적인 시스템을 구축할 수 있습니다.

## 참고 자료

- Java Concurrency in Practice - Brian Goetz
- Clean Architecture - Robert C. Martin
- Spring in Action - Craig Walls
- 스프링 공식 문서(https://docs.spring.io/spring-framework/docs/current/reference/html/)
- Effective Java, 3rd Edition - Joshua Bloch