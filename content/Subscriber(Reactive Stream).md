```java
package org.reactivestreams;

public interface Subscriber<T> {

    public void onSubscribe(Subscription s);

    public void onNext(T t);

    public void onError(Throwable t);

    public void onComplete();
}
```

**`Subscriber` 인터페이스의 역할:**

1. **데이터 발행자(Publisher)에게 데이터 처리 대기를 알리는 역할:**
    - `Publisher`의 `subscribe()` 메소드에 `Subscriber` 자신을 전달하면 연결이 시작됩니다.
2. **데이터 흐름을 제어하는 역할:**
    - 단순히 기다리는 게 아니라, **언제 얼마나 데이터를 받을지 직접 요청**합니다.
3. **`onSubscribe(Subscription s)`:**
    -  `Publisher`에게 구독 신청(`subscribe()`)을 하면 가장 먼저 호출됩니다.
    -  `Subscription`이라는 특별한 "데이터 요청 도구"를 받습니다. 이 도구를 사용해야만 데이터를 요청할 수 있습니다.
    - 이 메소드가 호출되었다고 해서 바로 데이터가 오는 것은 아닙니다. **반드시 `Subscription`의 `request()` 메소드를 호출해야 데이터가 오기 시작합니다.**
    - 식당에서 주문하고 나서, "이제 음식 1개 주세요"라고 말해야 음식이 나오기 시작하는 것과 같습니다. `onSubscribe`는 주문 확인증(`Subscription`)을 받는 단계입니다.
4. **`onNext(T t)`:**
    - `Subscription`의 `request(n)`를 통해 데이터를 요청했을 때, `Publisher`가 데이터를 보내주면 호출됩니다.
    - 실제 데이터(`t`)를 받아서 처리합니다.
    - `request(n)`으로 요청한 개수만큼, 최대 `n`번까지 호출될 수 있습니다.
    - **비유:** "음식 1개 주세요"(`request(1)`)라고 요청하면, 음식이 나올 때마다(`onNext`) 받아서 먹는 것과 같습니다.
5. **`onError(Throwable t)`:**
    - 데이터 처리 중 `Publisher` 쪽에서 에러가 발생했을 때 호출됩니다.
    - 에러 정보(`t`)를 받아서 처리합니다. (예: 로그 남기기, 사용자에게 알림 등)
    - 이 메소드가 호출되면 데이터 스트림은 **비정상적으로 종료**됩니다. 더 이상 `onNext`나 `onComplete`는 호출되지 않습니다. (`request()`를 또 호출해도 소용없습니다.)
    - 음식을 받다가 식당 주방에 불이 나면(`onError`), 더 이상 음식을 받을 수 없고 주문은 실패로 끝나는 것과 같습니다.
6. **`onComplete()`:**
    - `Publisher`가 모든 데이터를 성공적으로 다 보냈을 때 호출됩니다.
    - 데이터 스트림이 **정상적으로 완료**되었음을 알립니다. 마무리 작업을 할 수 있습니다.
    - 이 메소드가 호출되면 데이터 스트림은 **정상적으로 종료**됩니다. 더 이상 `onNext`나 `onError`는 호출되지 않습니다. (`request()`를 또 호출해도 소용없습니다.)
    - 주문한 음식을 모두 다 받아서 식사가 끝나면(`onComplete`), 더 이상 음식이 나오지 않는 것과 같습니다.