1. **CPU 바운드 작업**: 계산 집약적인 작업으로, CPU의 처리 능력이 제한 요소가 됩니다. 예를 들어 복잡한 수학 계산, 이미지 처리, 암호화 등이 있습니다.
    
2. **I/O 바운드 작업**: 외부 리소스와의 상호작용에 의존하는 작업으로, 디스크 읽기/쓰기, 네트워크 요청, 데이터베이스 쿼리 등이 포함됩니다. 이런 작업은 대부분의 시간을 외부 리소스의 응답을 기다리는 데 소비합니다.
    

## I/O 바운드 작업에서의 동시성 이점

I/O 바운드 작업에서 동시성이 성능을 크게 향상시키는 방식을 살펴보겠습니다:

### 블로킹 I/O 모델의 문제점

전통적인 블로킹 I/O 모델에서는 스레드가 I/O 작업이 완료될 때까지 대기합니다. 이 시간 동안 스레드는 아무 작업도 수행하지 않고 단순히 기다리기만 합니다.

### 비동기 I/O를 통한 성능 향상

비동기 I/O 모델에서는 I/O 작업이 진행되는 동안 스레드가 다른 작업을 계속 수행할 수 있습니다. I/O 작업이 완료되면 콜백 함수나 이벤트를 통해 결과를 처리합니다.

```mermaid
sequenceDiagram
    participant A as 애플리케이션
    participant DB1 as 데이터베이스 1
    participant DB2 as 데이터베이스 2
    participant File as 파일 시스템
    
    Note over A: CPU 활성화
    A->>+DB1: 쿼리 요청 (비동기)
    Note over A: CPU 계속 활성화
    A->>+DB2: 쿼리 요청 (비동기)
    Note over A: CPU 계속 활성화
    A->>+File: 파일 읽기 요청 (비동기)
    Note over A: 다른 작업 처리 가능
    
    DB1-->>-A: 응답
    Note over A: DB1 응답 처리
    
    File-->>-A: 응답
    Note over A: 파일 응답 처리
    
    DB2-->>-A: 응답
    Note over A: DB2 응답 처리
    
    Note over A: 총 소요 시간 = 가장 오래 걸리는 작업 시간 + 처리 시간
```

비동기 모델에서는 여러 I/O 작업을 동시에 시작하고, 각 작업이 완료될 때마다 결과를 처리할 수 있습니다. 이렇게 하면 전체 처리 시간이 크게 단축됩니다.

## 실제 예시

웹 서버는 동시성의 이점을 잘 보여주는 대표적인 예입니다. 수많은 클라이언트 요청을 처리해야 하는 웹 서버에서 동시성을 활용하는 방법을 살펴보겠습니다.

### 블로킹 방식의 웹 서버

```java
// 블로킹 방식의 단일 스레드 웹 서버 (의사 코드)
public class BlockingWebServer {
    public static void main(String[] args) throws IOException {
        ServerSocket serverSocket = new ServerSocket(8080);
        
        while (true) {
            // 클라이언트 연결 대기 (블로킹)
            Socket clientSocket = serverSocket.accept();
            
            // 요청 처리 (블로킹)
            handleRequest(clientSocket);
        }
    }
    
    private static void handleRequest(Socket clientSocket) throws IOException {
        // 클라이언트 요청 읽기
        BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
        
        // 요청 처리 (DB 쿼리, 파일 읽기 등 I/O 작업 포함)
        // 이 과정에서 DB나 파일 I/O를 기다리는 동안 다른 클라이언트는 대기해야 함
        
        // 클라이언트에 응답 전송
        OutputStream out = clientSocket.getOutputStream();
        // ...
        
        // 연결 종료
        clientSocket.close();
    }
}
```

이 방식에서는 한 번에 하나의 클라이언트 요청만 처리할 수 있습니다. 각 요청이 처리되는 동안 다른 클라이언트는 대기해야 합니다. 특히 요청 처리 과정에서 데이터베이스 쿼리나 파일 읽기와 같은 I/O 작업이 포함된 경우, 그 대기 시간 동안 서버는 아무 일도 하지 않게 됩니다.

### 동시성을 활용한 웹 서버

```java
// 스레드 풀을 사용한 웹 서버
public class ConcurrentWebServer {
    public static void main(String[] args) throws IOException {
        ServerSocket serverSocket = new ServerSocket(8080);
        // 스레드 풀 생성
        ExecutorService executorService = Executors.newFixedThreadPool(100);
        
        while (true) {
            // 클라이언트 연결 대기 (블로킹)
            Socket clientSocket = serverSocket.accept();
            
            // 요청 처리를 스레드 풀에 위임
            executorService.submit(() -> {
                try {
                    handleRequest(clientSocket);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            });
        }
    }
    
    private static void handleRequest(Socket clientSocket) throws IOException {
        // 요청 처리 (위와 동일)
        // ...
    }
}
```

이 방식에서는 스레드 풀을 사용하여 여러 클라이언트 요청을 동시에 처리할 수 있습니다. 한 요청이 데이터베이스 응답을 기다리는 동안 다른 스레드가 다른 요청을 처리할 수 있으므로, 서버의 자원이 효율적으로 활용됩니다.

### 비동기 I/O를 활용한 웹 서버

더 나아가, Java의 NIO(New I/O) 패키지나 Netty와 같은 비동기 I/O 프레임워크를 사용하면 더 적은 수의 스레드로도 높은 동시성을 달성할 수 있습니다.

```java
// Netty를 사용한 비동기 웹 서버 (간략한 예시)
public class AsyncWebServer {
    public static void main(String[] args) throws Exception {
        EventLoopGroup bossGroup = new NioEventLoopGroup(1);
        EventLoopGroup workerGroup = new NioEventLoopGroup();
        
        try {
            ServerBootstrap b = new ServerBootstrap();
            b.group(bossGroup, workerGroup)
             .channel(NioServerSocketChannel.class)
             .childHandler(new ChannelInitializer<SocketChannel>() {
                 @Override
                 public void initChannel(SocketChannel ch) {
                     ch.pipeline().addLast(new HttpServerCodec(),
                                          new HttpRequestHandler());
                 }
             });
            
            Channel ch = b.bind(8080).sync().channel();
            ch.closeFuture().sync();
        } finally {
            bossGroup.shutdownGracefully();
            workerGroup.shutdownGracefully();
        }
    }
}

class HttpRequestHandler extends SimpleChannelInboundHandler<HttpObject> {
    @Override
    protected void channelRead0(ChannelHandlerContext ctx, HttpObject msg) {
        if (msg instanceof HttpRequest) {
            // 비동기 데이터베이스 쿼리
            CompletableFuture<String> dbResult = CompletableFuture.supplyAsync(() -> {
                // 데이터베이스 작업 (시간이 오래 걸린다고 가정)
                return "데이터베이스 결과";
            });
            
            // 비동기 파일 읽기
            CompletableFuture<String> fileResult = CompletableFuture.supplyAsync(() -> {
                // 파일 읽기 작업 (시간이 오래 걸린다고 가정)
                return "파일 내용";
            });
            
            // 두 비동기 작업이 모두 완료되면 응답 전송
            CompletableFuture.allOf(dbResult, fileResult).thenAccept(v -> {
                // HTTP 응답 생성 및 전송
                FullHttpResponse response = new DefaultFullHttpResponse(
                    HttpVersion.HTTP_1_1, HttpResponseStatus.OK,
                    Unpooled.copiedBuffer(dbResult.join() + fileResult.join(), CharsetUtil.UTF_8));
                ctx.writeAndFlush(response).addListener(ChannelFutureListener.CLOSE);
            });
        }
    }
}
```

이 방식에서는 이벤트 루프 기반의 비동기 I/O를 사용하여, I/O 작업이 진행되는 동안 스레드가 블록되지 않고 다른 요청을 처리할 수 있습니다. 데이터베이스 쿼리와 파일 읽기 같은 여러 I/O 작업도 동시에 진행할 수 있어, 전체 처리 시간이 크게 단축됩니다.

## 스프링에서의 비동기 처리 예시

스프링 프레임워크에서는 `@Async` 어노테이션을 사용하여 메서드를 비동기적으로 실행할 수 있습니다.

```java
@Service
public class UserService {
    
    private final RestTemplate restTemplate;
    private final UserRepository userRepository;
    
    // 생성자 주입
    public UserService(RestTemplate restTemplate, UserRepository userRepository) {
        this.restTemplate = restTemplate;
        this.userRepository = userRepository;
    }
    
    // 동기 방식
    public UserProfile getUserProfileSync(Long userId) {
        // 1. 데이터베이스에서 사용자 정보 조회 (I/O 작업)
        User user = userRepository.findById(userId).orElseThrow();
        
        // 2. 외부 API에서 사용자 활동 이력 조회 (I/O 작업)
        UserActivity activity = restTemplate.getForObject(
            "https://api.example.com/activities/{userId}", 
            UserActivity.class, userId);
        
        // 3. 외부 API에서 사용자 프로필 이미지 조회 (I/O 작업)
        ProfileImage image = restTemplate.getForObject(
            "https://api.example.com/profile-images/{userId}",
            ProfileImage.class, userId);
        
        // 4. 조회한 정보 조합
        return new UserProfile(user, activity, image);
    }
    
    // 비동기 방식
    public CompletableFuture<UserProfile> getUserProfileAsync(Long userId) {
        // 1. 데이터베이스에서 사용자 정보 조회 (비동기)
        CompletableFuture<User> userFuture = CompletableFuture.supplyAsync(() -> 
            userRepository.findById(userId).orElseThrow());
        
        // 2. 외부 API에서 사용자 활동 이력 조회 (비동기)
        CompletableFuture<UserActivity> activityFuture = CompletableFuture.supplyAsync(() ->
            restTemplate.getForObject(
                "https://api.example.com/activities/{userId}",
                UserActivity.class, userId));
        
        // 3. 외부 API에서 사용자 프로필 이미지 조회 (비동기)
        CompletableFuture<ProfileImage> imageFuture = CompletableFuture.supplyAsync(() ->
            restTemplate.getForObject(
                "https://api.example.com/profile-images/{userId}",
                ProfileImage.class, userId));
        
        // 4. 세 비동기 작업이 모두 완료되면 결과 조합
        return CompletableFuture.allOf(userFuture, activityFuture, imageFuture)
            .thenApply(v -> new UserProfile(
                userFuture.join(),
                activityFuture.join(),
                imageFuture.join()));
    }
}
```

## 결론

동시성 프로그래밍은 특히 I/O 바운드 작업이 많은 애플리케이션에서 큰 성능 향상을 가져올 수 있습니다. 외부 리소스와의 상호작용 중 발생하는 대기 시간 동안 다른 작업을 수행함으로써, CPU 활용률을 높이고 전체 처리 시간을 단축할 수 있습니다.

Java와 스프링 프레임워크는 스레드, ExecutorService, CompletableFuture, 비동기 I/O 등 다양한 동시성 도구를 제공하여, 개발자가 효율적인 동시성 애플리케이션을 구현할 수 있도록 지원합니다.

다만, 동시성 프로그래밍은 경쟁 상태, 교착 상태 등의 문제를 일으킬 수 있으므로, 적절한 동기화 기법과 디자인 패턴을 함께 활용하는 것이 중요합니다. 