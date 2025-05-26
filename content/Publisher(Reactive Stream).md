### 역할
```java
package org.reactivestreams;  
 */public interface Publisher<T> {  
         public void subscribe(Subscriber<? super T> s);  
}
```
`Publisher`는 잠재적으로 **무한한 개수의 순서화된 요소(데이터 또는 이벤트)** 를 생성하고 제공하는 주체입니다.

데이터를 일방적으로 밀어내는 것이 아니라, 데이터를 소비하는 `Subscriber`(구독자)로부터 **요청(demand)** 을 받을 때 그에 맞춰 데이터를 발행(publish)합니다. 이는 [[리액티브 스트림(Reactive Streams)]]의 핵심 원칙인 [[역압력(back pressure)]]를 구현하는 기반이 됩니다. 즉, 소비자가 처리할 수 있는 만큼만 데이터를 받도록 조절합니다.

하나의 `Publisher`는 여러 명의 `Subscriber`에게 데이터를 제공할 수 있습니다. 각 `Subscriber`는 `subscribe` 메소드를 통해 동적으로 구독을 시작할 수 있습니다. 이 메소드는 `Subscriber`가 `Publisher`에게 **"데이터 스트림을 받고 싶습니다"** 라고 요청하는 진입점입니다. `Publisher`에게 데이터 스트리밍을 시작하도록 요청하는 역할을 합니다.

이 메소드는 여러 번 호출될 수 있습니다. 호출될 때마다 Publisher와 해당 Subscriber 사이의 새로운 Subscription(구독 관계) 이 시작됩니다. 즉, subscribe 호출은 특정 구독자와 발행자 간의 상호작용 세션을 설정하는 과정이라고 볼 수 있습니다.

각 Subscription은 오직 하나의 Subscriber 를 위해서만 작동합니다. 즉, subscribe를 호출하여 생성된 구독 관계는 해당 호출에 사용된 특정 Subscriber 인스턴스에 고유합니다. **하나의 `Subscriber`는 하나의 `Publisher`에 한 번만 구독해야 합니다.**

만약 `Publisher`가 어떤 이유로든 구독 요청을 거부하거나 구독 과정에서 실패하면, `Publisher`는 전달받은 `Subscriber`의 `onError(Throwable)` 메소드를 호출하여 오류 상황을 알려야 합니다.