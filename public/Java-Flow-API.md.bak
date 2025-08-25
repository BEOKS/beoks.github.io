Java Flow API는 Java 9에서 도입된 [[반응형 프로그래밍(Reactive Programming)]]을 위한 표준 인터페이스 집합입니다. 이 API는 비동기적으로 데이터 스트림을 처리하고 [[백프레셔(Backpressure)]]를 관리하기 위한 표준 방식을 제공합니다. Flow API는 리액티브 스트림(Reactive Streams) 사양을 Java 표준 라이브러리에 통합한 것으로, 다양한 리액티브 라이브러리 간의 상호 운용성을 가능하게 합니다.

## Flow API의 핵심 개념

Java Flow API는 `java.util.concurrent.Flow` 클래스 내에 정의된 4개의 핵심 인터페이스로 구성되어 있습니다:

1. **Publisher**: 데이터 항목을 생성하고 구독자에게 전달합니다.
2. **Subscriber**: Publisher로부터 데이터 항목을 수신하고 처리합니다.
3. **Subscription**: Publisher와 Subscriber 간의 연결을 나타내며, 요청 및 취소 신호를 관리합니다.
4. **Processor**: Publisher와 Subscriber의 기능을 모두 가진 중간 구성 요소입니다.

이 인터페이스들 간의 상호작용은 다음과 같은 흐름으로 이루어집니다:

```mermaid
sequenceDiagram
    participant P as Publisher
    participant S as Subscriber
    P->>S: 1. subscribe(Subscriber)
    P->>S: 2. onSubscribe(Subscription)
    S->>P: 3. Subscription.request(n)
    P->>S: 4. onNext(item)
    S->>P: 5. Subscription.request(m)
    P->>S: 6. onNext(item)
    P->>S: 7. onComplete() / onError()
```

## Flow API의 주요 인터페이스

### 1. Publisher 인터페이스

Publisher는 잠재적으로 무한한 데이터 항목의 시퀀스를 제공하며, Subscriber의 요청에 따라 데이터를 생성합니다.

```java
@FunctionalInterface
public static interface Publisher<T> {
    public void subscribe(Subscriber<? super T> subscriber);
}
```

Publisher는 단 하나의 메서드만 가지고 있으며, 이 메서드는 Subscriber가 데이터 스트림을 구독할 때 호출됩니다.

### 2. Subscriber 인터페이스

Subscriber는 Publisher로부터 데이터를 수신하고 처리하는 역할을 합니다.

```java
public static interface Subscriber<T> {
    public void onSubscribe(Subscription subscription);
    public void onNext(T item);
    public void onError(Throwable throwable);
    public void onComplete();
}
```

- **onSubscribe(Subscription)**: 구독이 시작될 때 호출되며, Subscription 객체를 통해 데이터 요청과 구독 취소를 관리합니다.
- **onNext(T item)**: 새로운 데이터 항목이 발행될 때마다 호출됩니다.
- **onError(Throwable)**: 오류가 발생했을 때 호출됩니다.
- **onComplete()**: 모든 데이터 항목이 성공적으로 발행된 후 호출됩니다.

### 3. Subscription 인터페이스

Subscription은 Publisher와 Subscriber 간의 연결을 나타내며, 데이터 요청과 구독 취소를 관리합니다.

```java
public static interface Subscription {
    public void request(long n);
    public void cancel();
}
```

- **request(long n)**: Subscriber가 n개의 데이터 항목을 요청합니다. 이것이 [[백프레셔(Backpressure)]]를 구현하는 핵심 메커니즘입니다.
- **cancel()**: 구독을 취소하고 리소스를 정리합니다.

### 4. Processor 인터페이스

Processor는 Publisher와 Subscriber의 기능을 모두 가진 중간 처리 단계로, 데이터 변환이나 필터링 등의 작업을 수행할 수 있습니다.

```java
public static interface Processor<T, R> extends Subscriber<T>, Publisher<R> {
}
```

Processor는 별도의 메서드를 추가하지 않고, Publisher와 Subscriber 인터페이스를 결합합니다.

## Flow API의 동작 원리

Flow API의 동작은 다음과 같은 순서로 이루어집니다:

1. Subscriber가 Publisher에게 `subscribe()`를 호출하여 구독을 시작합니다.
2. Publisher는 Subscriber에게 `onSubscribe(Subscription)`을 호출하여 Subscription 객체를 전달합니다.
3. Subscriber는 Subscription의 `request(n)` 메서드를 호출하여 n개의 데이터 항목을 요청합니다.
4. Publisher는 요청받은 개수만큼 데이터를 생성하여 Subscriber의 `onNext(item)` 메서드를 통해 전달합니다.
5. 데이터 처리가 완료되면 Publisher는 Subscriber의 `onComplete()`를 호출합니다.
6. 오류가 발생하면 Publisher는 Subscriber의 `onError(throwable)`를 호출합니다.

이 과정에서 중요한 것은 Subscriber가 처리할 수 있는 만큼의 데이터만 요청한다는 점입니다. 이것이 바로 백프레셔 메커니즘으로, 빠른 Publisher와 느린 Subscriber 간의 균형을 맞추는 데 중요한 역할을 합니다.

## 간단한 구현 예제

다음은 Flow API를 사용한 간단한 예제입니다:

```java
import java.util.concurrent.Flow;
import java.util.concurrent.Flow.Publisher;
import java.util.concurrent.Flow.Subscriber;
import java.util.concurrent.Flow.Subscription;
import java.util.concurrent.SubmissionPublisher;
import java.util.function.Function;

public class FlowExample {

    public static void main(String[] args) throws InterruptedException {
        // Publisher 생성
        SubmissionPublisher<Integer> publisher = new SubmissionPublisher<>();
        
        // Processor 생성
        TransformProcessor<Integer, String> processor = 
            new TransformProcessor<>(i -> "변환된 값: " + i);
        
        // Subscriber 생성
        SimpleSubscriber subscriber = new SimpleSubscriber();
        
        // Publisher -> Processor -> Subscriber 연결
        publisher.subscribe(processor);
        processor.subscribe(subscriber);
        
        // 데이터 발행
        System.out.println("데이터 발행 시작");
        for (int i = 1; i <= 5; i++) {
            publisher.submit(i);
        }
        
        // 발행 완료
        publisher.close();
        
        // 잠시 대기하여 비동기 처리 완료 기다림
        Thread.sleep(1000);
    }
    
    // 간단한 Processor 구현
    static class TransformProcessor<T, R> extends SubmissionPublisher<R>
            implements Flow.Processor<T, R> {
        
        private final Function<T, R> function;
        private Subscription subscription;
        
        TransformProcessor(Function<T, R> function) {
            this.function = function;
        }
        
        @Override
        public void onSubscribe(Subscription subscription) {
            this.subscription = subscription;
            subscription.request(1);
        }
        
        @Override
        public void onNext(T item) {
            submit(function.apply(item));
            subscription.request(1);
        }
        
        @Override
        public void onError(Throwable throwable) {
            throwable.printStackTrace();
            closeExceptionally(throwable);
        }
        
        @Override
        public void onComplete() {
            close();
        }
    }
    
    // 간단한 Subscriber 구현
    static class SimpleSubscriber implements Flow.Subscriber<String> {
        private Subscription subscription;
        private int count = 0;
        
        @Override
        public void onSubscribe(Subscription subscription) {
            this.subscription = subscription;
            subscription.request(1);
            System.out.println("구독 시작");
        }
        
        @Override
        public void onNext(String item) {
            System.out.println("수신: " + item);
            count++;
            subscription.request(1);
        }
        
        @Override
        public void onError(Throwable throwable) {
            throwable.printStackTrace();
        }
        
        @Override
        public void onComplete() {
            System.out.println("완료! 총 " + count + "개 항목 처리");
        }
    }
}
```

이 예제에서는 다음과 같은 과정이 진행됩니다:

1. `SubmissionPublisher`(Java 9에서 제공하는 Publisher 구현체)를 생성합니다.
2. 데이터를 변환하는 Processor를 구현합니다.
3. 데이터를 수신하는 Subscriber를 구현합니다.
4. Publisher -> Processor -> Subscriber 순으로 연결합니다.
5. Publisher가 데이터를 발행하고, Processor가 이를 변환한 후, Subscriber가 처리합니다.

## 백프레셔(Backpressure)의 중요성

Flow API의 가장 중요한 특징 중 하나는 백프레셔 메커니즘입니다. 백프레셔는 데이터 생산자(Publisher)가 데이터 소비자(Subscriber)의 처리 능력을 초과하는 속도로 데이터를 발행하지 않도록 하는 메커니즘입니다.

백프레셔가 없다면 다음과 같은 문제가 발생할 수 있습니다:

- 메모리 부족(OOM) 오류
- 시스템 응답성 저하
- 데이터 손실

Flow API에서는 Subscriber가 `Subscription.request(n)` 메서드를 통해 처리할 수 있는 데이터의 양을 명시적으로 요청함으로써 백프레셔를 구현합니다. 자세한 내용은 [[백프레셔 구현 방법]]을 참고해주세요.

## Flow API와 기존 비동기 프로그래밍 모델의 비교

Flow API는 기존의 비동기 프로그래밍 모델과 몇 가지 중요한 차이점이 있습니다:

|특성|Flow API|CompletableFuture|콜백 기반 API|
|---|---|---|---|
|데이터 개수|0~N개(스트림)|정확히 1개|다양|
|백프레셔|지원|미지원|미지원|
|취소 지원|지원|제한적 지원|일반적으로 미지원|
|오류 처리|내장|내장|수동 구현 필요|

기존 비동기 모델과의 자세한 비교는 [[Java 비동기 프로그래밍 모델 비교]]를 참고해주세요.

## Spring WebFlux와 Flow API

Spring WebFlux는 Spring 5에서 도입된 리액티브 웹 프레임워크로, Project Reactor를 기반으로 하며 Java Flow API와 호환됩니다. WebFlux에서는 `Mono<T>`와 `Flux<T>`라는 두 가지 주요 타입을 사용하는데, 이들은 각각 0-1개와 0-N개의 결과를 비동기적으로 처리합니다.

Spring WebFlux와 Flow API를 함께 사용하는 간단한 예제입니다:

```java
@RestController
public class ReactiveController {
    
    @GetMapping(value = "/numbers", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Publisher<Integer> getNumbers() {
        return subscriber -> {
            SubmissionPublisher<Integer> publisher = new SubmissionPublisher<>();
            publisher.subscribe(subscriber);
            
            // 비동기적으로 데이터 발행
            CompletableFuture.runAsync(() -> {
                for (int i = 1; i <= 10; i++) {
                    try {
                        Thread.sleep(1000); // 1초마다 숫자 발행
                        publisher.submit(i);
                    } catch (InterruptedException e) {
                        publisher.closeExceptionally(e);
                        return;
                    }
                }
                publisher.close();
            });
        };
    }
}
```

이 예제에서는 클라이언트에게 Server-Sent Events(SSE) 형식으로 1초마다 숫자를 스트리밍합니다. 자세한 Spring WebFlux 활용법은 [[Spring WebFlux 활용법]]을 참고해주세요.

## Flow API 사용 시 주의사항

Flow API를 사용할 때 주의해야 할 몇 가지 사항이 있습니다:

1. **구독 관리**: 더 이상 필요하지 않은 구독은 반드시 `cancel()`을 호출하여 리소스 누수를 방지해야 합니다.
2. **스레드 안전성**: Publisher와 Subscriber는 여러 스레드에서 동시에 호출될 수 있으므로 스레드 안전성을 보장해야 합니다.
3. **신호 규칙 준수**: 리액티브 스트림 사양에 정의된 신호 규칙(예: `onNext` 후 `onComplete`나 `onError`가 호출될 수 없음)을 준수해야 합니다.
4. **요청 수량 관리**: Subscriber는 처리할 수 있는 양만큼만 데이터를 요청해야 합니다.

## 실제 사용 사례

Flow API는 다음과 같은 상황에서 특히 유용합니다:

1. **비동기 I/O 처리**: 네트워크 요청, 파일 I/O 등의 비차단 처리
2. **이벤트 스트리밍**: 센서 데이터, 주식 시세, 소셜 미디어 피드 등 실시간 데이터 스트림 처리
3. **마이크로서비스 통신**: 서비스 간 비동기 통신
4. **대용량 데이터 처리**: 메모리 효율적인 방식으로 대용량 데이터셋 처리

## Flow API의 제한사항

Flow API는 단지 인터페이스 집합일 뿐이므로, 실제 사용을 위해서는 이를 구현한 라이브러리가 필요합니다. Java 9는 `SubmissionPublisher`라는 기본 구현체를 제공하지만, 더 풍부한 기능을 위해서는 다음과 같은 외부 라이브러리를 고려할 수 있습니다:

- **RxJava**: 풍부한 연산자와 스케줄러 지원
- **Project Reactor**: Spring WebFlux의 기반이 되는 리액티브 라이브러리
- **Akka Streams**: 분산 시스템을 위한 리액티브 스트림 구현체

이러한 라이브러리들은 Flow API와 호환되는 동시에 더 다양한 기능을 제공합니다. 라이브러리 선택에 대한 자세한 내용은 리액티브 라이브러리 비교를 참고해주세요.

## 결론

Java Flow API는 비동기 데이터 스트림을 처리하기 위한 표준화된 접근 방식을 제공합니다. 백프레셔 메커니즘을 통해 데이터 생산자와 소비자 간의 균형을 맞추고, 리소스를 효율적으로 사용할 수 있게 합니다. 비록 기본 구현은 제한적이지만, 다양한 리액티브 라이브러리와의 상호 운용성을 통해 복잡한 비동기 애플리케이션을 구축하는 데 강력한 기반을 제공합니다.

현대적인 애플리케이션 개발에서는 비동기 및 논블로킹 프로그래밍의 중요성이 계속 증가하고 있으며, Java Flow API는 이러한 패러다임 전환을 지원하는 중요한 도구입니다. 특히 마이크로서비스 아키텍처, 실시간 데이터 처리, 반응형 사용자 인터페이스 등의 분야에서 Flow API의 활용 가치는 더욱 높아질 것입니다.

## 참고 자료

- Java SE 9 Documentation - java.util.concurrent.Flow
- Reactive Streams 사양 (http://www.reactive-streams.org/)
- Reactive Programming with JDK 9 Flow API - Venkat Subramaniam
- Spring WebFlux 문서 (https://docs.spring.io/spring-framework/docs/current/reference/html/web-reactive.html)