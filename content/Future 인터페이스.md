Future 인터페이스는 Java 5(Java SE 5.0)에서 도입된 java.util.concurrent 패키지의 일부로, 비동기 연산의 결과를 나타내는 인터페이스입니다. 비동기 작업을 시작한 후 미래의 어느 시점에 결과를 얻을 수 있도록 해주는 핵심 추상화를 제공합니다.

## Future 인터페이스의 기본 개념

Future는 비동기 계산이 완료되었는지 확인하고, 완료되었다면 그 결과값을 얻기 위한 메소드를 제공합니다. 비동기 작업이 완료될 때까지 결과를 기다리거나, 작업을 취소하는 기능을 포함하고 있습니다.

Future 인터페이스의 핵심 아이디어는 비동기 작업의 결과를 얻기 위한 "프록시" 또는 "플레이스홀더"를 제공하는 것입니다. 작업이 시작되면 즉시 Future 객체가 반환되며, 이 객체를 통해 나중에 결과를 조회할 수 있습니다.

## Future 인터페이스의 주요 메소드

Future 인터페이스는 다음과 같은 다섯 가지 주요 메소드를 정의합니다:

1. **`boolean cancel(boolean mayInterruptIfRunning)`**
    
    - 작업 취소를 시도합니다.
    - `mayInterruptIfRunning`이 true이면 실행 중인 스레드를 인터럽트하여 취소를 시도합니다.
    - 작업이 성공적으로 취소되면 true를 반환합니다.
2. **`boolean isCancelled()`**
    
    - 작업이 취소되었는지 확인합니다.
    - 작업이 취소되었으면 true를 반환합니다.
3. **`boolean isDone()`**
    
    - 작업이 완료되었는지 확인합니다.
    - 작업이 정상적으로 완료되었거나, 예외가 발생했거나, 취소되었으면 true를 반환합니다.
4. **`V get() throws InterruptedException, ExecutionException`**
    
    - 작업의 결과를 가져옵니다.
    - 작업이 완료될 때까지 블로킹됩니다.
    - 작업이 취소되면 CancellationException을 발생시킵니다.
    - 작업 실행 중 예외가 발생하면 ExecutionException을 발생시킵니다.
    - 스레드가 인터럽트되면 InterruptedException을 발생시킵니다.
5. **`V get(long timeout, TimeUnit unit) throws InterruptedException, ExecutionException, TimeoutException`**
    
    - 지정된 시간 동안만 작업 결과를 기다립니다.
    - 지정된 시간 내에 결과를 얻지 못하면 TimeoutException을 발생시킵니다.

## Future의 일반적인 사용 패턴

Future는 주로 ExecutorService와 함께 사용되어 비동기 작업을 제출하고 그 결과를 나중에 얻는 데 활용됩니다:

```java
// ExecutorService 생성
ExecutorService executor = Executors.newSingleThreadExecutor();

// 비동기 작업 제출
Future<Integer> future = executor.submit(() -> {
    // 시간이 오래 걸리는 계산
    Thread.sleep(2000);
    return 42;
});

// 다른 작업 수행
System.out.println("비동기 작업이 진행 중입니다...");

try {
    // 결과 얻기 (블로킹 호출)
    Integer result = future.get();
    System.out.println("결과: " + result);
} catch (InterruptedException | ExecutionException e) {
    e.printStackTrace();
}

// ExecutorService 종료
executor.shutdown();
```

## Future의 구현 클래스: FutureTask

Java에서 제공하는 Future 인터페이스의 주요 구현체는 FutureTask 클래스입니다. FutureTask는 Future와 Runnable 인터페이스를 모두 구현하여, 비동기 작업의 결과를 나타내면서도 직접 실행 가능한 작업으로 사용할 수 있습니다.

```java
// Callable을 사용한 FutureTask 생성
Callable<Integer> callable = () -> {
    Thread.sleep(2000);
    return 42;
};
FutureTask<Integer> futureTask = new FutureTask<>(callable);

// 스레드에서 FutureTask 실행
new Thread(futureTask).start();

// 결과 얻기
try {
    Integer result = futureTask.get();
    System.out.println("결과: " + result);
} catch (InterruptedException | ExecutionException e) {
    e.printStackTrace();
}
```

## Future의 제한 사항

Future 인터페이스는 비동기 프로그래밍의 기초를 제공하지만, 다음과 같은 제한 사항이 있습니다:

1. **블로킹 특성**: `get()` 메소드는 결과가 준비될 때까지 현재 스레드를 차단합니다.
2. **작업 조합 불가**: 여러 Future를 조합하거나 체이닝하는 기능이 없습니다.
3. **콜백 미지원**: 작업이 완료되었을 때 자동으로 실행되는 콜백을 등록할 수 없습니다.
4. **예외 처리의 제한**: 비동기 작업에서 발생한 예외를 처리하기 위한 특별한 메커니즘이 없습니다.
5. **수동 완료 불가**: 외부에서 Future의 완료를 직접 제어할 수 없습니다.

이러한 제한 사항을 해결하기 위해 Java 8에서 [[CompletableFuture]] 클래스가 도입되었습니다.

## Future와 ExecutorService의 관계

Future는 일반적으로 ExecutorService와 함께 사용됩니다. ExecutorService는 비동기 작업을 제출하고 실행하기 위한 인터페이스로, 작업을 제출하면 Future 객체를 반환합니다:

```java
ExecutorService executor = Executors.newFixedThreadPool(4);

// Callable 작업 제출
Future<String> future1 = executor.submit(() -> {
    Thread.sleep(1000);
    return "작업 1 완료";
});

// Runnable 작업 제출 (결과 없음)
Future<?> future2 = executor.submit(() -> {
    System.out.println("작업 2 실행 중");
});

// 특정 결과와 함께 Runnable 작업 제출
Future<String> future3 = executor.submit(() -> {
    System.out.println("작업 3 실행 중");
}, "작업 3 완료");

// 작업 결과 수집
List<Future<?>> futures = Arrays.asList(future1, future2, future3);
for (Future<?> future : futures) {
    try {
        System.out.println(future.get());
    } catch (Exception e) {
        e.printStackTrace();
    }
}

executor.shutdown();
```

## ExecutorService와 함께 Future 사용 시 주의 사항

ExecutorService와 Future를 함께 사용할 때 주의해야 할 점들이 있습니다:

### 1. 스레드 풀 크기 설정

스레드 풀의 크기를 적절하게 설정하는 것이 중요합니다. 너무 작으면 병렬 처리 효과가 떨어지고, 너무 크면 스레드 관리 오버헤드가 커집니다.

```java
// CPU 집약적 작업을 위한 스레드 풀
int processors = Runtime.getRuntime().availableProcessors();
ExecutorService cpuBoundPool = Executors.newFixedThreadPool(processors);

// I/O 집약적 작업을 위한 스레드 풀
ExecutorService ioBoundPool = Executors.newFixedThreadPool(100);
```

### 2. ExecutorService 종료

애플리케이션이 종료되기 전에 ExecutorService를 적절히 종료해야 합니다:

```java
executor.shutdown();  // 새 작업 접수 중단, 기존 작업은 완료

// 모든 작업이 완료될 때까지 대기
try {
    if (!executor.awaitTermination(60, TimeUnit.SECONDS)) {
        executor.shutdownNow();  // 실행 중인 작업 중단 시도
    }
} catch (InterruptedException e) {
    executor.shutdownNow();
    Thread.currentThread().interrupt();
}
```

### 3. 타임아웃 설정

get() 메소드가 무한정 블로킹되는 것을 방지하기 위해 타임아웃을 설정합니다:

```java
try {
    // 최대 5초 동안 결과를 기다림
    String result = future.get(5, TimeUnit.SECONDS);
    System.out.println("결과: " + result);
} catch (TimeoutException e) {
    System.out.println("작업이 시간 초과되었습니다.");
    future.cancel(true);  // 작업 취소 시도
}
```

## Future의 실용적인 사용 예시

### 1. 여러 서비스 병렬 호출

```java
public class ServiceAggregator {
    private final UserService userService;
    private final ProductService productService;
    private final ReviewService reviewService;
    private final ExecutorService executor;
    
    public ServiceAggregator() {
        this.userService = new UserService();
        this.productService = new ProductService();
        this.reviewService = new ReviewService();
        this.executor = Executors.newFixedThreadPool(3);
    }
    
    public Dashboard getDashboard(Long userId) throws Exception {
        // 병렬로 여러 서비스 호출
        Future<User> userFuture = executor.submit(() -> userService.getUser(userId));
        Future<List<Product>> productsFuture = executor.submit(() -> productService.getRecentProducts());
        Future<List<Review>> reviewsFuture = executor.submit(() -> reviewService.getUserReviews(userId));
        
        // 결과 수집 (각 호출은 블로킹됨)
        User user = userFuture.get(2, TimeUnit.SECONDS);
        List<Product> products = productsFuture.get(2, TimeUnit.SECONDS);
        List<Review> reviews = reviewsFuture.get(2, TimeUnit.SECONDS);
        
        // 결과 조합
        return new Dashboard(user, products, reviews);
    }
    
    public void shutdown() {
        executor.shutdown();
    }
}
```

### 2. 작업 취소 구현

```java
public class SearchService {
    private final ExecutorService executor;
    
    public SearchService() {
        this.executor = Executors.newCachedThreadPool();
    }
    
    public Future<List<Result>> search(String query) {
        return executor.submit(() -> {
            List<Result> results = new ArrayList<>();
            // 오래 걸리는 검색 작업
            for (int i = 0; i < 100 && !Thread.currentThread().isInterrupted(); i++) {
                Thread.sleep(100);  // 검색 작업 시뮬레이션
                results.add(new Result("결과 " + i));
                
                // 인터럽트 확인으로 취소 처리 지원
                if (Thread.currentThread().isInterrupted()) {
                    System.out.println("검색 작업이 취소되었습니다.");
                    break;
                }
            }
            return results;
        });
    }
    
    public void shutdown() {
        executor.shutdown();
    }
}

// 사용 예:
SearchService searchService = new SearchService();
Future<List<Result>> future = searchService.search("Java Future");

// 사용자가 검색 취소를 요청
new Thread(() -> {
    try {
        Thread.sleep(1500);  // 사용자가 1.5초 후 취소
        System.out.println("사용자가 검색을 취소했습니다.");
        future.cancel(true);
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
}).start();

try {
    List<Result> results = future.get();
    System.out.println("총 " + results.size() + "개의 결과를 찾았습니다.");
} catch (CancellationException e) {
    System.out.println("검색이 취소되었습니다.");
} catch (Exception e) {
    e.printStackTrace();
}
```

## Future vs CompletableFuture

Future와 [[CompletableFuture]]의 주요 차이점은 다음과 같습니다:

|기능|Future|CompletableFuture|
|---|---|---|
|블로킹 방식|get() 메소드는 블로킹됨|비블로킹 콜백 지원|
|작업 조합|지원하지 않음|thenApply, thenCompose 등 다양한 조합 가능|
|예외 처리|try-catch로만 처리|exceptionally, handle 등 전용 메소드 제공|
|콜백|지원하지 않음|thenAccept, thenRun 등 다양한 콜백 지원|
|수동 완료|지원하지 않음|complete, completeExceptionally 메소드 제공|
|타임아웃|get(timeout, unit)으로 구현|Java 9부터 orTimeout 메소드 제공|

## Future 디버깅 기법

Future를 사용한 비동기 코드 디버깅은 도전적일 수 있습니다. 다음은 몇 가지 유용한 디버깅 기법입니다:

### 1. 로깅 활용

```java
Future<String> future = executor.submit(() -> {
    try {
        logger.info("작업 시작 - 스레드: {}", Thread.currentThread().getName());
        // 작업 수행
        String result = performTask();
        logger.info("작업 완료 - 결과: {}", result);
        return result;
    } catch (Exception e) {
        logger.error("작업 실패", e);
        throw e;
    }
});
```

### 2. Future 상태 모니터링

```java
Future<String> future = executor.submit(() -> performTask());

// Future 상태 모니터링
new Thread(() -> {
    try {
        while (!future.isDone()) {
            System.out.println("Future 상태: " + 
                (future.isCancelled() ? "취소됨" : "실행 중"));
            Thread.sleep(500);
        }
        System.out.println("Future 상태: 완료됨");
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
}).start();
```

### 3. 타임아웃 활용

```java
try {
    // 단계별 진행 확인을 위한 다양한 타임아웃 설정
    System.out.println("1초 동안 기다려보겠습니다...");
    Object result = future.get(1, TimeUnit.SECONDS);
    System.out.println("결과: " + result);
} catch (TimeoutException e) {
    System.out.println("1초 내에 완료되지 않았습니다. 계속 기다립니다...");
    try {
        Object result = future.get(5, TimeUnit.SECONDS);
        System.out.println("결과: " + result);
    } catch (TimeoutException e2) {
        System.out.println("5초 후에도 완료되지 않았습니다. 작업을 취소합니다.");
        future.cancel(true);
    }
}
```

## Future 사용 시 주의사항 및 모범 사례

### 1. 블로킹 get() 호출 주의

Future의 get() 메소드는 블로킹 호출이므로, UI 스레드나 제한된 스레드 풀에서 직접 호출하지 않도록 주의해야 합니다.

```java
// 잘못된 사용 - UI 스레드 차단
button.setOnClickListener(e -> {
    try {
        // UI 스레드가 차단됨!
        String result = future.get();
        resultLabel.setText(result);
    } catch (Exception ex) {
        ex.printStackTrace();
    }
});

// 개선된 사용
button.setOnClickListener(e -> {
    new Thread(() -> {
        try {
            String result = future.get();
            // UI 업데이트는 UI 스레드로 다시 전달
            Platform.runLater(() -> resultLabel.setText(result));
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }).start();
});
```

### 2. 정리(Cleanup) 보장

Future 작업이 완료되거나 취소된 후에 리소스가 적절히 정리되는지 확인해야 합니다.

```java
Future<Result> future = executor.submit(() -> {
    Resource resource = new Resource();
    try {
        return processWithResource(resource);
    } finally {
        // Future가 취소되더라도 리소스 정리 보장
        resource.close();
    }
});
```

### 3. 적절한 취소 처리

작업 취소를 위해서는 interrupt를 체크하는 로직을 구현해야 합니다.

```java
Future<List<Data>> future = executor.submit(() -> {
    List<Data> results = new ArrayList<>();
    for (int i = 0; i < sources.size(); i++) {
        // 취소 요청 확인
        if (Thread.currentThread().isInterrupted()) {
            System.out.println("작업이 취소되었습니다.");
            break;
        }
        
        DataSource source = sources.get(i);
        results.add(source.fetchData());
    }
    return results;
});
```

### 4. 종료 처리 철저히

애플리케이션 종료 시 모든 ExecutorService를 적절히 종료해야 리소스 누수를 방지할 수 있습니다.

```java
public void shutdown() {
    List<Runnable> pendingTasks = executor.shutdownNow();
    System.out.println(pendingTasks.size() + "개의 대기 작업이 취소되었습니다.");
    
    try {
        if (!executor.awaitTermination(5, TimeUnit.SECONDS)) {
            System.err.println("ExecutorService가 5초 내에 종료되지 않았습니다.");
        }
    } catch (InterruptedException e) {
        Thread.currentThread().interrupt();
    }
}
```

## 스프링 프레임워크에서의 Future 활용

스프링 프레임워크는 @Async 어노테이션을 통해 Future를 활용한 비동기 처리를 지원합니다:

```java
@Service
public class AsyncService {
    
    @Async
    public Future<String> asyncMethod() {
        try {
            Thread.sleep(2000);
            return new AsyncResult<>("비동기 작업 완료");
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return new AsyncResult<>("작업 중단");
        }
    }
    
    @Async
    public ListenableFuture<String> listenableAsyncMethod() {
        try {
            Thread.sleep(2000);
            return new AsyncResult<>("Listenable 비동기 작업 완료");
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return new AsyncResult<>("작업 중단");
        }
    }
}
```

사용하기 위해서는 @EnableAsync 설정이 필요합니다:

```java
@Configuration
@EnableAsync
public class AsyncConfig {
    
    @Bean
    public Executor taskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(5);
        executor.setMaxPoolSize(10);
        executor.setQueueCapacity(25);
        executor.setThreadNamePrefix("AsyncTask-");
        executor.initialize();
        return executor;
    }
}
```

## 결론

Future 인터페이스는 Java의 비동기 프로그래밍에서 가장 기본적인 요소로, 비동기 작업의 결과를 표현하고 관리하는 기능을 제공합니다. 단순한 비동기 작업을 처리하는 데 유용하지만, 작업 조합, 콜백, 비블로킹 처리 등 고급 기능이 필요한 경우에는 한계가 있습니다.

Java 8 이후로는 CompletableFuture, Spring의 ListenableFuture, Reactor 및 RxJava와 같은 반응형 라이브러리 등 더 강력한 비동기 프로그래밍 도구가 등장했습니다. 그러나 Future의 기본 개념과 동작 원리를 이해하는 것은 더 고급 비동기 프로그래밍 기법을 마스터하기 위한 필수적인 기반이 됩니다.

비동기 프로그래밍의 다양한 측면과 고급 기법에 대한 자세한 내용은 비동기 프로그래밍 패러다임, [[CompletableFuture]], Java 동시성 프로그래밍을 참고해주세요.

## 참고 자료

- Java Concurrency in Practice - Brian Goetz
- Modern Java in Action - Raoul-Gabriel Urma, Mario Fusco, Alan Mycroft
- Java API 공식 문서(https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/Future.html)
- 스프링 공식 문서(https://docs.spring.io/spring-framework/docs/current/reference/html/integration.html#scheduling)