```java
package org.reactivestreams;

public interface Subscription {

    public void request(long n);

    public void cancel();
}
```
**`Subscription`의 핵심 역할:**

- `Subscriber`가 `Publisher`에게 **데이터를 요청**하거나, **구독을 취소**할 때 사용됩니다.
- 하나의 `Subscriber`와 `Publisher` 간의 **단 한 번의 구독 생명주기** 동안만 유효합니다. 즉, 구독할 때마다 새로운 `Subscription` 객체가 생성됩니다.

**주요 메소드 설명:**

1. **`request(long n)`:**
    -  `Publisher`에게 "데이터를 **n개** 만큼 보내주세요!" 라고 **요청**하는 메소드입니다.
    - `Subscriber`가 `onSubscribe`를 통해 `Subscription`을 받은 후, 이 `request(n)` 메소드를 **호출해야만** `Publisher`가 데이터를 보내기 시작합니다. (호출하지 않으면 데이터는 오지 않습니다.)
    - `Subscriber`가 데이터를 처리할 준비가 되었을 때, 필요한 만큼 호출할 수 있습니다. 여러 번 호출하면 요청한 `n`의 개수가 누적됩니다.
    - `n`은 반드시 0보다 큰 양수여야 합니다. 또한, `Subscriber`가 실제로 처리할 수 있는 만큼만 요청해야 합니다. 너무 많이 요청하면 문제가 생길 수 있습니다. (`Publisher`는 요청받은 `n`개보다 적게 보낼 수도 있습니다. 예를 들어 데이터가 더 이상 없으면 `onComplete`나 `onError`를 호출하고 종료합니다.)
    - 식당에서 받은 주문 확인증(`Subscription`)에 있는 "음식 `n`개 가져다 주세요" 버튼을 누르는 것과 같습니다. 이 버튼을 눌러야(`request(n)`) 음식이 서빙되기 시작합니다(`onNext`).
2. **`cancel()`:**
    - `Publisher`에게 "더 이상 데이터를 보내지 마세요. 구독을 **취소**합니다." 라고 **요청**하는 메소드입니다.
    -  `Subscriber`가 더 이상 데이터를 받을 필요가 없거나, 중간에 구독을 중단하고 싶을 때 호출합니다.
    - `Publisher`는 데이터 전송을 중단하고 관련 리소스를 정리할 수 있습니다.
    - `cancel()`을 호출하기 직전에 이미 `request(n)`으로 요청했던 데이터가 있다면, `cancel()` 호출 이후에도 일부 데이터가 `onNext`로 전달될 수 있습니다. 하지만 그 이후에는 더 이상 데이터가 오지 않습니다.
    - 식당에서 받은 주문 확인증(`Subscription`)에 있는 "주문 취소" 버튼을 누르는 것과 같습니다. 이미 만들고 있던 음식(`request`로 요청된 데이터)은 나올 수 있지만, 그 이후로는 더 이상 음식을 만들거나 가져다주지 않습니다.