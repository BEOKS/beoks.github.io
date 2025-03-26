CompletableFuture는 Java 8에서 도입된 [[비동기(Asynchronous)]] 프로그래밍을 위한 클래스로, java.util.concurrent 패키지의 일부입니다. 기존의 Future 인터페이스를 확장하여 더 풍부한 기능을 제공하며, 비동기 작업의 완료 여부를 확인하고 결과를 처리하는 다양한 방법을 제공합니다.

## Future와 CompletableFuture의 차이점

CompletableFuture를 이해하기 위해서는 먼저 [[Future 인터페이스]]와의 차이점을 이해하는 것이 중요합니다. Future는 Java 5부터 제공된 인터페이스로, 비동기 작업의 결과를 나타냅니다. 그러나 Future는 다음과 같은 한계를 가지고 있습니다:

1. **블로킹 메소드**: `get()` 메소드가 블로킹 방식으로 동작하여 결과를 기다리는 동안 스레드가 차단됩니다.
2. **체인 불가능**: 여러 비동기 작업을 조합하거나 체인으로 연결할 수 없습니다.
3. **예외 처리의 어려움**: 예외 처리를 위한 특별한 메커니즘이 없습니다.
4. **수동 완료 불가능**: 외부에서 완료 시점을 제어할 수 없습니다.

CompletableFuture는 이러한 한계를 극복하기 위해 설계되었으며, 다음과 같은 주요 기능을 제공합니다:

1. **[[논블로킹(Non-blocking)]] 방식**: 콜백 메소드를 통해 논블로킹 방식으로 결과 처리가 가능합니다.
2. **작업 조합**: 여러 비동기 작업을 연결하고 조합할 수 있습니다.
3. **예외 처리**: 비동기 작업의 예외를 효과적으로 처리할 수 있는 메소드를 제공합니다.
4. **수동 완료**: 외부에서 비동기 작업의 완료를 직접 제어할 수 있습니다.

## CompletableFuture의 기본 사용법

### 1. CompletableFuture 생성

CompletableFuture를 생성하는 방법은 여러 가지가 있습니다:

```java
// 이미 완료된 CompletableFuture 생성
CompletableFuture<String> completedFuture = CompletableFuture.completedFuture("결과");

// 빈 CompletableFuture 생성 (나중에 완료 가능)
CompletableFuture<String> future = new CompletableFuture<>();

// 비동기 작업으로 CompletableFuture 생성
CompletableFuture<String> asyncFuture = CompletableFuture.supplyAsync(() -> {
    // 시간이 걸리는 작업
    try {
        Thread.sleep(1000);
    } catch (InterruptedException e) {
        Thread.currentThread().interrupt();
    }
    return "비동기 작업 결과";
});
```

### 2. 결과 처리하기

CompletableFuture의 결과는 다양한 메소드를 통해 처리할 수 있습니다:

```java
CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> "Hello");

// thenApply: 결과를 변환
CompletableFuture<Integer> lengthFuture = future.thenApply(s -> s.length());

// thenAccept: 결과를 소비 (반환값 없음)
future.thenAccept(s -> System.out.println("결과: " + s));

// thenRun: 결과를 사용하지 않고 다른 작업 실행
future.thenRun(() -> System.out.println("작업 완료"));

// get: 결과 블로킹 방식으로 가져오기 (가능하면 피해야 함)
try {
    String result = future.get(); // 블로킹 호출
} catch (InterruptedException | ExecutionException e) {
    e.printStackTrace();
}
```

## CompletableFuture의 고급 기능

### 1. 여러 작업 조합하기

여러 비동기 작업을 조합하는 다양한 방법을 제공합니다:

```java
CompletableFuture<String> future1 = CompletableFuture.supplyAsync(() -> "Hello");
CompletableFuture<String> future2 = CompletableFuture.supplyAsync(() -> "World");

// thenCompose: 두 작업을 순차적으로 실행 (첫 번째 작업의 결과를 두 번째 작업에 전달)
CompletableFuture<String> composedFuture = future1.thenCompose(
    s -> CompletableFuture.supplyAsync(() -> s + " Composed"));

// thenCombine: 두 작업의 결과를 조합
CompletableFuture<String> combinedFuture = future1.thenCombine(
    future2, (s1, s2) -> s1 + " " + s2);

// allOf: 모든 CompletableFuture가 완료될 때까지 기다림
CompletableFuture<Void> allFuture = CompletableFuture.allOf(future1, future2);

// anyOf: 가장 먼저 완료되는 CompletableFuture의 결과를 반환
CompletableFuture<Object> anyFuture = CompletableFuture.anyOf(future1, future2);
```

### 2. 비동기 실행 제어

CompletableFuture는 작업의 실행 스레드를 제어할 수 있는 메소드를 제공합니다:

```java
// 기본 ForkJoinPool의 공통 스레드 풀 사용
CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> "작업 결과");

// 커스텀 Executor 사용
ExecutorService executor = Executors.newFixedThreadPool(4);
CompletableFuture<String> futureWithExecutor = CompletableFuture.supplyAsync(
    () -> "작업 결과", executor);

// 후속 작업에 대한 Executor 지정
futureWithExecutor.thenApplyAsync(s -> s + " 처리됨", executor);
```

### 3. 예외 처리

CompletableFuture는 비동기 작업의 예외를 처리하기 위한 다양한 메소드를 제공합니다:

```java
CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
    if (Math.random() > 0.5) {
        throw new RuntimeException("작업 실패");
    }
    return "작업 성공";
});

// exceptionally: 예외 발생 시 대체 값 제공
CompletableFuture<String> recoveredFuture = future.exceptionally(ex -> {
    System.err.println("예외 발생: " + ex.getMessage());
    return "대체 결과";
});

// handle: 정상 완료와 예외 모두 처리 가능
CompletableFuture<String> handledFuture = future.handle((result, ex) -> {
    if (ex != null) {
        return "예외 처리: " + ex.getMessage();
    } else {
        return "정상 결과: " + result;
    }
});

// whenComplete: 결과나 예외를 처리하지만 값을 변경하지 않음
future.whenComplete((result, ex) -> {
    if (ex != null) {
        System.err.println("예외 발생: " + ex.getMessage());
    } else {
        System.out.println("작업 완료: " + result);
    }
});
```

## 실용적인 CompletableFuture 사용 예시

### 1. 순차적인 작업 처리

여러 작업을 순차적으로 처리하는 예시입니다:

```java
public CompletableFuture<Order> processOrder(Long orderId) {
    return CompletableFuture.supplyAsync(() -> orderRepository.findById(orderId))
        .thenApply(order -> {
            // 재고 확인
            order.setStatus("재고 확인됨");
            return order;
        })
        .thenApply(order -> {
            // 결제 처리
            order.setStatus("결제 완료");
            return order;
        })
        .thenApply(order -> {
            // 배송 준비
            order.setStatus("배송 준비 중");
            return order;
        })
        .exceptionally(ex -> {
            log.error("주문 처리 중 오류 발생", ex);
            Order failedOrder = new Order(orderId);
            failedOrder.setStatus("처리 실패");
            return failedOrder;
        });
}
```

### 2. 병렬 작업 처리

여러 작업을 병렬로 처리한 후 결과를 조합하는 예시입니다:

```java
public CompletableFuture<ProductDetails> getProductDetails(Long productId) {
    CompletableFuture<Product> productFuture = 
        CompletableFuture.supplyAsync(() -> productRepository.findById(productId));
    
    CompletableFuture<List<Review>> reviewsFuture = 
        CompletableFuture.supplyAsync(() -> reviewRepository.findByProductId(productId));
    
    CompletableFuture<Inventory> inventoryFuture = 
        CompletableFuture.supplyAsync(() -> inventoryService.getInventory(productId));
    
    return productFuture.thenCombine(reviewsFuture, (product, reviews) -> {
        ProductDetails details = new ProductDetails();
        details.setProduct(product);
        details.setReviews(reviews);
        return details;
    }).thenCombine(inventoryFuture, (details, inventory) -> {
        details.setInventory(inventory);
        return details;
    });
}
```

### 3. 타임아웃 처리

CompletableFuture에 타임아웃을 설정하는 예시입니다(Java 9 이상):

```java
public CompletableFuture<String> getDataWithTimeout() {
    CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
        // 시간이 오래 걸리는 작업
        try {
            Thread.sleep(5000); // 5초 대기
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        return "데이터";
    });
    
    // Java 9 이상에서 사용 가능
    return future.orTimeout(3, TimeUnit.SECONDS)
        .exceptionally(ex -> {
            if (ex instanceof TimeoutException) {
                return "타임아웃 발생";
            }
            return "기타 오류 발생: " + ex.getMessage();
        });
}
```

Java 8에서는 다음과 같이 구현할 수 있습니다:

```java
public CompletableFuture<String> getDataWithTimeoutJava8() {
    CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
        // 시간이 오래 걸리는 작업
        try {
            Thread.sleep(5000); // 5초 대기
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        return "데이터";
    });
    
    CompletableFuture<String> timeout = timeoutAfter(3, TimeUnit.SECONDS);
    
    return CompletableFuture.anyOf(future, timeout)
        .thenApply(result -> (String) result)
        .exceptionally(ex -> "타임아웃 또는 오류 발생");
}

private <T> CompletableFuture<T> timeoutAfter(long timeout, TimeUnit unit) {
    CompletableFuture<T> result = new CompletableFuture<>();
    Executors.newScheduledThreadPool(1).schedule(
        () -> result.completeExceptionally(new TimeoutException("Timeout")),
        timeout, unit);
    return result;
}
```

## 스프링 프레임워크에서의 CompletableFuture 활용

스프링 프레임워크는 CompletableFuture를 활용한 비동기 처리를 지원합니다:

### 1. 비동기 컨트롤러

```java
@RestController
@RequestMapping("/api/products")
public class ProductController {
    
    private final ProductService productService;
    
    @Autowired
    public ProductController(ProductService productService) {
        this.productService = productService;
    }
    
    @GetMapping("/{id}")
    public CompletableFuture<ResponseEntity<ProductDetails>> getProductDetails(@PathVariable Long id) {
        return productService.getProductDetails(id)
            .thenApply(details -> ResponseEntity.ok(details))
            .exceptionally(ex -> {
                if (ex.getCause() instanceof ProductNotFoundException) {
                    return ResponseEntity.notFound().build();
                }
                return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
            });
    }
}
```

### 2. @Async와 CompletableFuture

```java
@Service
public class ProductService {
    
    private final ProductRepository productRepository;
    private final ReviewRepository reviewRepository;
    
    @Autowired
    public ProductService(ProductRepository productRepository, ReviewRepository reviewRepository) {
        this.productRepository = productRepository;
        this.reviewRepository = reviewRepository;
    }
    
    @Async
    public CompletableFuture<Product> getProduct(Long id) {
        return CompletableFuture.completedFuture(productRepository.findById(id));
    }
    
    @Async
    public CompletableFuture<List<Review>> getReviews(Long productId) {
        return CompletableFuture.completedFuture(reviewRepository.findByProductId(productId));
    }
    
    public CompletableFuture<ProductDetails> getProductDetails(Long id) {
        CompletableFuture<Product> productFuture = getProduct(id);
        CompletableFuture<List<Review>> reviewsFuture = getReviews(id);
        
        return productFuture.thenCombine(reviewsFuture, (product, reviews) -> {
            ProductDetails details = new ProductDetails();
            details.setProduct(product);
            details.setReviews(reviews);
            return details;
        });
    }
}
```

이를 사용하기 위해서는 @EnableAsync 설정이 필요합니다:

```java
@Configuration
@EnableAsync
public class AsyncConfig {
    
    @Bean
    public Executor asyncExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(4);
        executor.setMaxPoolSize(10);
        executor.setQueueCapacity(50);
        executor.setThreadNamePrefix("AsyncTask-");
        executor.initialize();
        return executor;
    }
}
```

## CompletableFuture와 다른 비동기 프로그래밍 기법 비교

CompletableFuture는 다른 비동기 프로그래밍 기법과 비교하여 다음과 같은 특징을 가집니다:

### 1. CompletableFuture vs [[콜백 체인(Callback Chain)]]

- **가독성**: CompletableFuture는 메소드 체이닝을 통한 선형적인 코드 작성이 가능하여 깊은 중첩이 발생하는 콜백 체인보다 가독성이 좋습니다.
- **예외 처리**: CompletableFuture는 통합된 예외 처리 메커니즘을 제공합니다.
- **유연성**: 다양한 조합 메소드를 통해 복잡한 비동기 흐름을 표현할 수 있습니다.

### 2. CompletableFuture vs [[반응형 프로그래밍(Reactive Programming)]]

- **데이터 흐름**: CompletableFuture는 단일 값/결과에 중점을 둔 반면, 반응형 프로그래밍(Reactor, RxJava)은 데이터 스트림 처리에 중점을 둡니다.
- **백프레셔**: CompletableFuture는 백프레셔(생산자와 소비자 간의 처리 속도 조절) 메커니즘이 없습니다.
- **오퍼레이터**: 반응형 프로그래밍은 더 풍부한 연산자와 변환 기능을 제공합니다.

### 3. CompletableFuture vs [[코루틴(Coroutine)]]

- **구현 방식**: CompletableFuture는 콜백 기반인 반면, 코루틴은 중단 가능한 함수를 통해 구현됩니다.
- **가독성**: 코루틴은 비동기 코드를 동기 코드처럼 작성할 수 있어 가독성이 더 좋을 수 있습니다.
- **자원 효율성**: 코루틴은 일반적으로 스레드보다 가벼워 더 많은 동시성을 제공할 수 있습니다.

## CompletableFuture 모범 사례

CompletableFuture를 효과적으로 사용하기 위한 모범 사례는 다음과 같습니다:

### 1. 스레드 풀 관리

```java
// 기본 ForkJoinPool 대신 용도에 맞는 커스텀 스레드 풀을 사용합니다
ExecutorService ioExecutor = Executors.newFixedThreadPool(10,
    new ThreadFactoryBuilder().setNameFormat("io-executor-%d").build());
    
ExecutorService cpuExecutor = Executors.newWorkStealingPool(
    Runtime.getRuntime().availableProcessors());
    
// I/O 작업을 위한 CompletableFuture
CompletableFuture<byte[]> ioFuture = CompletableFuture.supplyAsync(
    () -> readFileBytes("large_file.dat"), ioExecutor);
    
// CPU 작업을 위한 CompletableFuture
CompletableFuture<Result> cpuFuture = ioFuture.thenApplyAsync(
    bytes -> processData(bytes), cpuExecutor);
```

### 2. 예외 처리 철저히 하기

```java
CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
    // 비동기 작업
    if (someCondition) {
        throw new RuntimeException("오류 발생");
    }
    return "결과";
})
.exceptionally(ex -> {
    logger.error("작업 실패", ex);
    return "기본값";
})
.whenComplete((result, ex) -> {
    if (ex != null) {
        logger.error("작업 완료 후 예외 처리", ex);
    } else {
        logger.info("작업 성공적으로 완료: {}", result);
    }
});
```

### 3. 타임아웃 설정하기

```java
// Java 9 이상
CompletableFuture<String> future = service.getLongRunningData()
    .orTimeout(5, TimeUnit.SECONDS)
    .exceptionally(ex -> {
        if (ex instanceof TimeoutException) {
            return "타임아웃 발생";
        }
        return "기타 오류: " + ex.getMessage();
    });
```

### 4. 리소스 정리

```java
ExecutorService executor = Executors.newFixedThreadPool(4);
try {
    CompletableFuture<String> future = CompletableFuture.supplyAsync(
        () -> processData(), executor);
    
    // 작업 처리
    String result = future.join();
    
} finally {
    // 작업이 끝나면 Executor 종료
    executor.shutdown();
    try {
        if (!executor.awaitTermination(5, TimeUnit.SECONDS)) {
            executor.shutdownNow();
        }
    } catch (InterruptedException e) {
        executor.shutdownNow();
    }
}
```

## CompletableFuture 디버깅 기법

비동기 코드의 디버깅은 어려울 수 있지만, 다음과 같은 방법으로 CompletableFuture를 효과적으로 디버깅할 수 있습니다:

### 1. 로깅 활용

```java
CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
    logger.info("작업 시작");
    String result = performTask();
    logger.info("작업 완료: {}", result);
    return result;
}).thenApply(result -> {
    logger.info("변환 작업 시작");
    String transformed = transform(result);
    logger.info("변환 작업 완료: {}", transformed);
    return transformed;
});
```

### 2. 각 단계의 결과 확인

```java
CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> "Step 1")
    .thenApply(s -> {
        String result = s + " -> Step 2";
        System.out.println("중간 결과: " + result);
        return result;
    })
    .thenApply(s -> {
        String result = s + " -> Step 3";
        System.out.println("중간 결과: " + result);
        return result;
    });
```

### 3. 스레드 정보 확인

```java
CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
    System.out.println("supplyAsync 실행 스레드: " + Thread.currentThread().getName());
    return "결과";
}).thenApplyAsync(s -> {
    System.out.println("thenApplyAsync 실행 스레드: " + Thread.currentThread().getName());
    return s + " 처리됨";
});
```

## 결론

CompletableFuture는 Java에서 비동기 프로그래밍을 위한 강력한 도구입니다. 콜백 체인의 가독성 문제를 해결하고, 다양한 비동기 작업의 조합을 가능하게 하며, 효과적인 예외 처리 메커니즘을 제공합니다. 특히 여러 서비스 간의 통합, API 호출, 데이터베이스 작업 등 다양한 비동기 작업을 처리할 때 유용하게 활용할 수 있습니다.

Java의 비동기 프로그래밍 생태계는 계속 발전하고 있으며, CompletableFuture는 그 중심에 있습니다. 완전한 반응형 시스템이 필요한 경우 Reactor나 RxJava와 같은 라이브러리를 고려할 수 있지만, 단일 값이나 결과를 처리하는 대부분의 비동기 작업에는 CompletableFuture가 간결하고 효과적인 해결책을 제공합니다.

자세한 사용 사례와 심화 내용은 [[비동기 프로그래밍 모범 사례]], [[Java 비동기 프로그래밍 기법 비교]], [[반응형 프로그래밍 vs CompletableFuture]]를 참고해주세요.

## 참고 자료

- Modern Java in Action - Raoul-Gabriel Urma, Mario Fusco, Alan Mycroft
- Java Concurrency in Practice - Brian Goetz
- 스프링 공식 문서(https://docs.spring.io/spring-framework/docs/current/reference/html/web-reactive.html)
- Java 8 Documentation(https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/CompletableFuture.html)