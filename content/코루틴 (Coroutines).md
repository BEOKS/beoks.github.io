코루틴(Coroutine)은 비동기 프로그래밍을 위한 경량 스레드(lightweight thread)입니다. 스레드와 유사하게 [[동시성(Concurrency)]]을 제공하지만, 운영체제가 아닌 사용자 레벨에서 스케줄링되어 스레드보다 훨씬 적은 자원을 사용하고 오버헤드가 적습니다. 이로 인해 수많은 코루틴을 생성하고 관리하는 것이 가능하며, 복잡한 비동기 작업을 동기 코드처럼 간결하게 작성할 수 있게 해줍니다.

### 왜 코루틴을 사용해야 할까요?

전통적인 비동기 프로그래밍 방식은 콜백(Callback)을 사용하거나 Future/Promise 패턴을 사용하는 경우가 많습니다. 하지만 이러한 방식은 다음과 같은 문제점을 가질 수 있습니다.

*   **콜백 지옥 (Callback Hell)**: 여러 비동기 작업이 순차적으로 실행되어야 할 때, 콜백 함수가 중첩되어 코드의 가독성과 유지보수성이 급격히 떨어집니다.
*   **예외 처리의 어려움**: 비동기 작업 중 발생하는 예외를 일관되게 처리하기 어렵습니다.
*   **코드의 복잡성**: 비동기 로직을 동기 코드처럼 직관적으로 작성하기 어렵습니다.

코루틴은 이러한 문제들을 해결하며, 비동기 코드를 마치 순차적인 동기 코드처럼 작성할 수 있게 하여 코드의 가독성과 생산성을 크게 향상시킵니다.

### 코루틴의 작동 방식

코루틴의 핵심은 **일시 중단(suspension)**과 **재개(resumption)**입니다. 코루틴은 특정 지점에서 실행을 일시 중단하고, 나중에 필요한 시점에 중단된 지점부터 다시 실행을 재개할 수 있습니다. 이러한 일시 중단은 스레드를 블로킹하지 않으므로, 하나의 스레드에서 여러 코루틴을 효율적으로 실행할 수 있습니다.

코루틴은 스레드와 달리 컨텍스트 스위칭(Context Switching) 비용이 매우 낮습니다. 스레드의 컨텍스트 스위칭은 운영체제 커널 레벨에서 이루어지며 많은 비용이 들지만, 코루틴의 일시 중단 및 재개는 사용자 레벨에서 이루어져 훨씬 빠릅니다.

코루틴의 내부 동작 방식에 대한 더 자세한 내용은 코루틴 동작 방식을 참고해주세요.

### Kotlin에서의 코루틴

Kotlin은 언어 레벨에서 코루틴을 지원하며, `kotlinx.coroutines` 라이브러리를 통해 강력한 기능을 제공합니다.

#### 주요 개념

*   **`suspend` 함수**: 코루틴 내에서만 호출될 수 있으며, 실행을 일시 중단할 수 있는 함수입니다. `suspend` 키워드는 함수가 블로킹 없이 비동기 작업을 수행할 수 있음을 나타냅니다.
*   **`CoroutineScope`**: 코루틴의 생명주기를 관리하는 스코프입니다. 이 스코프 내에서 시작된 코루틴들은 스코프가 취소될 때 함께 취소됩니다.
*   **`launch`**: 새로운 코루틴을 시작하고 결과를 반환하지 않는 빌더입니다.
*   **`async`**: 새로운 코루틴을 시작하고 `Deferred` 객체를 반환하여 나중에 결과를 받을 수 있는 빌더입니다.
*   **`withContext`**: 코루틴의 실행 컨텍스트(예: 스레드 풀)를 변경할 때 사용합니다.

#### Kotlin 코루틴 예시

Kotlin 코루틴은 `launch`, `async`, `withContext` 등의 빌더와 `suspend` 함수를 통해 다양한 비동기 시나리오를 처리할 수 있습니다.

##### 1. `launch`를 사용한 비동기 작업 시작

`launch`는 새로운 코루틴을 시작하고 결과를 반환하지 않는 빌더입니다. 주로 "실행하고 잊어버리는(fire-and-forget)" 방식의 비동기 작업에 사용됩니다.

```kotlin
import kotlinx.coroutines.*

fun main() = runBlocking {
    println("[Main] 메인 스레드 시작")

    // launch를 사용하여 백그라운드에서 실행될 코루틴 시작
    launch {
        delay(1000L) // 1초 동안 코루틴 일시 중단 (스레드는 블로킹되지 않음)
        println("[Coroutine 1] 1초 후 작업 완료")
    }

    launch {
        delay(500L) // 0.5초 동안 코루틴 일시 중단
        println("[Coroutine 2] 0.5초 후 작업 완료")
    }

    println("[Main] 메인 스레드 계속 진행")
    // runBlocking 스코프가 종료될 때까지 내부의 모든 코루틴이 완료되기를 기다립니다.
}
```

**출력 예시:**

```
[Main] 메인 스레드 시작
[Main] 메인 스레드 계속 진행
[Coroutine 2] 0.5초 후 작업 완료
[Coroutine 1] 1초 후 작업 완료
```

이 예시에서 `launch`로 시작된 두 코루틴은 비동기적으로 실행되며, `delay` 함수는 스레드를 블로킹하지 않으므로 메인 스레드는 계속 진행됩니다.

##### 2. `async`를 사용한 결과 반환 비동기 작업

`async`는 새로운 코루틴을 시작하고 `Deferred` 객체를 반환하여 나중에 결과를 받을 수 있는 빌더입니다. 여러 비동기 작업의 결과를 조합해야 할 때 유용합니다. `await()` 함수를 호출하여 `Deferred` 객체의 결과를 기다립니다.

```kotlin
import kotlinx.coroutines.*

fun main() = runBlocking {
    println("[Main] 메인 스레드 시작")

    // async를 사용하여 결과를 반환하는 비동기 작업 시작
    val result1 = async {
        delay(1000L)
        println("[Async 1] 첫 번째 비동기 작업 완료")
        "데이터 1"
    }

    val result2 = async {
        delay(500L)
        println("[Async 2] 두 번째 비동기 작업 완료")
        "데이터 2"
    }

    println("[Main] 비동기 작업 결과 대기 중...")

    // await()를 호출하여 각 비동기 작업의 결과를 기다립니다.
    val data1 = result1.await()
    val data2 = result2.await()

    println("[Main] 모든 비동기 작업 완료. 결과: $data1, $data2")
    println("[Main] 메인 스레드 종료")
}
```

**출력 예시:**

```
[Main] 메인 스레드 시작
[Main] 비동기 작업 결과 대기 중...
[Async 2] 두 번째 비동기 작업 완료
[Async 1] 첫 번째 비동기 작업 완료
[Main] 모든 비동기 작업 완료. 결과: 데이터 1, 데이터 2
[Main] 메인 스레드 종료
```

`result1.await()`가 호출될 때 `result1`이 아직 완료되지 않았다면 해당 코루틴은 일시 중단되고, `result1`이 완료되면 다시 실행됩니다.

##### 3. `withContext`를 사용한 컨텍스트 전환

`withContext`는 코루틴의 실행 컨텍스트(예: 스레드 풀)를 변경할 때 사용합니다. 특히 I/O 작업이나 CPU 집약적인 작업을 특정 스레드 풀에서 실행하도록 지정할 때 유용합니다.

*   `Dispatchers.Default`: CPU 집약적인 작업에 최적화된 공유 스레드 풀 (CPU 코어 수에 비례)
*   `Dispatchers.IO`: I/O 작업에 최적화된 공유 스레드 풀 (필요에 따라 스레드 생성)
*   `Dispatchers.Main`: UI 스레드 (안드로이드 등 UI 애플리케이션에서 사용)

```kotlin
import kotlinx.coroutines.*

fun main() = runBlocking {
    println("[Main] 현재 스레드: ${Thread.currentThread().name}")

    // I/O 작업 시뮬레이션 (네트워크 요청, 파일 읽기 등)
    val ioResult = withContext(Dispatchers.IO) {
        println("[IO Context] I/O 작업 시작. 스레드: ${Thread.currentThread().name}")
        delay(1000L) // I/O 작업 대기 시뮬레이션
        "I/O 작업 완료 데이터"
    }
    println("[Main] I/O 작업 결과: $ioResult. 현재 스레드: ${Thread.currentThread().name}")

    // CPU 집약적인 작업 시뮬레이션
    val cpuResult = withContext(Dispatchers.Default) {
        println("[Default Context] CPU 작업 시작. 스레드: ${Thread.currentThread().name}")
        var sum = 0L
        for (i in 1..1_000_000) { // 복잡한 계산 시뮬레이션
            sum += i
        }
        "CPU 작업 완료 데이터 (합계: $sum)"
    }
    println("[Main] CPU 작업 결과: $cpuResult. 현재 스레드: ${Thread.currentThread().name}")
}
```

**출력 예시:**

```
[Main] 현재 스레드: main
[IO Context] I/O 작업 시작. 스레드: DefaultDispatcher-worker-1
[Main] I/O 작업 결과: I/O 작업 완료 데이터. 현재 스레드: main
[Default Context] CPU 작업 시작. 스레드: DefaultDispatcher-worker-1
[Main] CPU 작업 결과: CPU 작업 완료 데이터 (합계: 500000500000). 현재 스레드: main
```

`withContext` 블록 내의 코루틴은 지정된 디스패처의 스레드에서 실행되지만, 블록이 완료되면 원래의 컨텍스트(여기서는 `runBlocking`의 메인 스레드)로 돌아와 나머지 코드가 실행됩니다.

##### 4. 코루틴 예외 처리

코루틴에서 발생하는 예외는 일반적인 Kotlin/Java 예외 처리 방식과 유사하게 `try-catch` 블록을 사용하여 처리할 수 있습니다. 하지만 `launch`와 `async`는 예외 처리 방식에 약간의 차이가 있습니다.

*   **`launch`**: 예외가 발생하면 해당 코루틴 스코프 내에서 즉시 전파되어 처리됩니다. `CoroutineExceptionHandler`를 사용하여 전역적으로 처리할 수 있습니다.
*   **`async`**: 예외가 발생해도 즉시 전파되지 않고, `await()`가 호출될 때 예외가 발생합니다.

```kotlin
import kotlinx.coroutines.*

fun main() = runBlocking {
    // launch를 사용한 예외 처리
    val handler = CoroutineExceptionHandler { _, exception ->
        println("[ExceptionHandler] launch 코루틴에서 예외 발생: $exception")
    }

    val job = launch(handler) {
        println("[Launch] 예외 발생 전")
        throw IllegalStateException("launch에서 발생한 예외")
        println("[Launch] 이 메시지는 출력되지 않습니다.")
    }
    job.join() // launch 코루틴이 완료될 때까지 대기

    println("------------------------------------")

    // async를 사용한 예외 처리
    val deferred = async {
        println("[Async] 예외 발생 전")
        throw IllegalArgumentException("async에서 발생한 예외")
        println("[Async] 이 메시지는 출력되지 않습니다.")
        "결과"
    }

    try {
        val result = deferred.await()
        println("[Async] 결과: $result")
    } catch (e: Exception) {
        println("[Main] async 코루틴에서 예외 처리: $e")
    }

    println("[Main] 모든 코루틴 예제 완료")
}
```

**출력 예시:**

```
[Launch] 예외 발생 전
[ExceptionHandler] launch 코루틴에서 예외 발생: java.lang.IllegalStateException: launch에서 발생한 예외
------------------------------------
[Async] 예외 발생 전
[Main] async 코루틴에서 예외 처리: java.lang.IllegalArgumentException: async에서 발생한 예외
[Main] 모든 코루틴 예제 완료
```

`launch`는 예외 발생 시 즉시 전파되므로 `CoroutineExceptionHandler`를 통해 처리할 수 있습니다. 반면 `async`는 `await()` 호출 시점에 예외가 발생하므로, `await()`를 `try-catch` 블록으로 감싸서 처리해야 합니다.

이처럼 Kotlin 코루틴은 다양한 상황에 맞는 유연하고 강력한 비동기 프로그래밍 모델을 제공합니다. 적절한 빌더와 컨텍스트를 활용하여 코드의 가독성과 안정성을 높일 수 있습니다.

### 코루틴과 스레드의 차이

코루틴과 스레드는 모두 동시성을 구현하는 방법이지만, 중요한 차이점이 있습니다.

| 특징         | 스레드 (Thread)                               | 코루틴 (Coroutine)                                  |
| :----------- | :-------------------------------------------- | :-------------------------------------------------- |
| **관리 주체**  | 운영체제 (OS)                                 | 사용자 레벨 (라이브러리/프레임워크)                 |
| **자원 소모**  | 무거움 (각 스레드마다 스택 메모리 할당)       | 가벼움 (하나의 스레드에서 여러 코루틴 실행 가능)    |
| **컨텍스트 스위칭** | 비용이 큼 (커널 모드 전환)                    | 비용이 적음 (사용자 모드에서 전환)                  |
| **블로킹**     | 블로킹 작업 시 스레드 전체가 대기              | `suspend` 함수를 통해 비블로킹 일시 중단 가능       |
| **생성 개수**  | 제한적 (수천 개 이상 생성 시 성능 저하)       | 매우 많음 (수십만 개 이상 생성 가능)                |
| **디버깅**     | 비교적 직관적                                 | 비동기 흐름 추적이 어려울 수 있음 (도구의 도움 필요) |

코루틴은 스레드 위에 추상화된 개념으로, 스레드 풀(Thread Pool) 위에서 실행될 수 있습니다. 즉, 코루틴은 스레드를 대체하는 것이 아니라, 스레드를 더 효율적으로 사용하여 비동기 작업을 처리하는 방법입니다.

### 코루틴의 활용 분야

코루틴은 다양한 분야에서 활용될 수 있습니다.

*   **안드로이드 개발**: UI 스레드를 블로킹하지 않고 네트워크 요청, 데이터베이스 접근 등 백그라운드 작업을 처리하여 애플리케이션의 응답성을 향상시킵니다.
*   **서버 사이드 개발**: 웹 서버에서 수많은 동시 요청을 효율적으로 처리하여 높은 처리량(throughput)을 달성합니다. 스프링 웹플럭스(Spring WebFlux)와 같은 리액티브 프레임워크와 함께 사용될 때 시너지를 낼 수 있습니다.
*   **데이터 처리**: 대용량 데이터를 비동기적으로 처리하거나, 여러 비동기 작업을 파이프라인 형태로 구성할 때 유용합니다.

### 결론

코루틴은 현대적인 비동기 프로그래밍의 복잡성을 해결하고, 개발자가 더 간결하고 직관적인 코드를 작성할 수 있도록 돕는 강력한 도구입니다. 특히 Kotlin에서는 언어 차원의 지원과 풍부한 라이브러리를 통해 코루틴을 쉽게 활용할 수 있습니다. 코루틴을 이해하고 적절히 활용한다면 애플리케이션의 성능과 응답성을 크게 향상시킬 수 있을 것입니다.

## 참고 자료

*   Kotlin Coroutines 공식 문서: [https://kotlinlang.org/docs/coroutines-overview.html](https://kotlinlang.org/docs/coroutines-overview.html)
*   [Kotlin Coroutines by Example](https://kotlinlang.org/docs/coroutines-basics.html)
*   [[비동기(Asynchronous)]]
*   [[스레드(Thread)]]
*   [[동시성(Concurrency)]]