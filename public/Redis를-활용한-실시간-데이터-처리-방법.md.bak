[[Redis]]는 [[인메모리 데이터 구조 저장소]]로서, 다양한 데이터 구조를 지원하며 높은 속도과 유연성을 제공합니다. [[실시간 데이터 처리]]는 빠른 읽기/쓰기 속도와 낮은 지연 시간이 핵심인데, Redis는 이러한 요구 사항을 충족시키기에 적합한 도구입니다. 이번 글에서는 Redis를 활용하여 어떻게 실시간 데이터 처리가 가능한지 살펴보겠습니다.

## Redis의 주요 데이터 구조

Redis는 다양한 데이터 구조를 지원하여 여러 가지 용도로 활용될 수 있습니다.

- **Strings**: 단순한 키-값 저장.
- **Hashes**: 필드와 값의 쌍으로 이루어진 맵(Map) 타입.
- **Lists**: 연결 리스트로, 요소의 삽입 및 제거가 빠릅니다.
- **Sets**: 중복되지 않는 요소들의 집합.
- **Sorted Sets**: 점수(score)를 기준으로 정렬된 집합.
- **Streams**: 로그 및 메시지 스트림 처리에 사용.

각 데이터 구조는 특정한 사용 사례에 적합하며, 이를 조합하여 복잡한 기능을 구현할 수 있습니다. 인메모리 기반의 빠른 속도로 다양한 데이터 구조를 활용할 수 있어 여러 실시간 데이터 처리 사례에 활용할 수 있습니다.
## 실시간 데이터 처리를 위한 Redis 기능

### Pub/Sub (발행/구독)

Redis의 Pub/Sub 기능은 메시지 브로커와 유사하게 동작하여, 실시간 메시징 시스템을 구축할 수 있습니다.

- **Publish**: 특정 채널에 메시지를 발행.
- **Subscribe**: 특정 채널을 구독하고 메시지를 수신.

#### 예제

```shell
# 채널 'news'에 메시지 발행
PUBLISH news "Breaking news!"

# 채널 'news'를 구독
SUBSCRIBE news
```

### [Redis Streams](https://redis.io/docs/latest/develop/data-types/streams/)

Redis 5.0부터 추가된 Streams는 실시간 데이터 스트리밍을 위한 강력한 데이터 구조입니다.

- **메시지 저장 및 조회**: 스트림 내의 메시지를 저장하고 필요한 시점에 조회.
- **컨슈머 그룹**: 여러 컨슈머가 스트림의 데이터를 효율적으로 처리할 수 있도록 지원.
#### 예제

```shell
# 스트림에 데이터 추가
XADD mystream * field1 value1 field2 value2

# 스트림에서 데이터 읽기
XRANGE mystream - +
```

### Lists와 Sorted Sets

Lists와 Sorted Sets는 실시간 데이터 처리를 위한 큐나 랭킹 시스템을 구축하는 데 유용합니다.

- **Lists**: 왼쪽/오른쪽에서 요소를 삽입/제거하여 큐나 스택처럼 사용.
- **Sorted Sets**: 점수(score)를 기반으로 순서가 정해져 있어 랭킹 시스템에 적합.

#### 큐 예제 (Lists)

```shell
# 작업 추가 (큐의 오른쪽에 삽입)
RPUSH task_queue "task1"

# 작업 처리 (큐의 왼쪽에서 가져오기)
LPOP task_queue
```

#### 랭킹 예제 (Sorted Sets)

```shell
# 플레이어 점수 추가
ZADD leaderboard 100 "player1"

# 상위 10명 조회
ZREVRANGE leaderboard 0 9 WITHSCORES
```

## 실시간 애플리케이션 사례

1. **채팅 애플리케이션**: Pub/Sub을 이용하여 **실시간 메시징 및 채팅 시스템 구현**.
2. **실시간 분석**: Streams를 활용하여 이벤트 로그를 수집하고 **실시간 분석** 수행.
3. **랭킹 시스템**: Sorted Sets를 통해 게임이나 앱의 **실시간 랭킹** 제공.
4. **세션 관리**: 사용자 세션 데이터를 Redis에 저장하여 **빠른 액세스와 업데이트.**
---

**참고 자료**

- [Redis 공식 문서](https://redis.io/documentation)
- [Redis Streams 소개](https://redis.io/topics/streams-intro)
- [Redis를 이용한 실시간 애플리케이션 개발](https://redis.io/topics/uses)