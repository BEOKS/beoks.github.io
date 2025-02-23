# Redis 기본 명령어 정리

Redis는 메모리 기반의 고성능 키-값 저장소로 매우 빠른 속도와 다양한 데이터 구조를 지원합니다. 이번 글에서는 Redis를 처음 접하는 개발자들을 위해 기본적인 명령어들을 정리하였습니다.

---

## Redis 시작하기

[[Redis 설치하기]] 문서를 이용해 환경에 따라 설치 및 접속할 수 있습니다.

---

## 기본 키-값 명령어

### SET: 키 값 설정

특정 키에 값을 설정합니다.

```bash
SET <key> <value>
```

**예시:**

```bash
SET name "Alice"
```

### GET: 키에 대한 값 가져오기

특정 키에 저장된 값을 가져옵니다.

```bash
GET <key>
```

**예시:**

```bash
GET name
```

### DEL: 키 삭제

특정 키를 삭제합니다.

```bash
DEL <key>
```

**예시:**

```bash
DEL name
```

### EXISTS: 키의 존재 확인

특정 키가 존재하는지 확인합니다.

```bash
EXISTS <key>
```

**예시:**

```bash
EXISTS name
```

---

## 데이터 구조별 명령어

Redis는 다양한 데이터 구조를 지원합니다. 각 구조마다 사용되는 명령어가 다릅니다.

### 숫자형(Numeric)

**SET**과 **GET** 명령어를 사용하여 문자열 값을 설정하고 가져옵니다.

**예시:**

```bash
SET name alice
GET name
```
### [리스트(List)](.https://redis.io/docs/latest/develop/data-types/lists/)

순서가 있는 값들의 목록을 저장합니다. Linked List 로 구현되며 주로 스택과 큐를 구현할때 사용합니다.

**LPUSH**: 리스트의 왼쪽(앞쪽)에 요소를 추가합니다.

```bash
LPUSH mylist "apple"
```

**RPUSH**: 리스트의 오른쪽(뒤쪽)에 요소를 추가합니다.

```bash
RPUSH mylist "banana"
```

**LRANGE**: 리스트의 특정 범위의 요소들을 가져옵니다.

```bash
LRANGE mylist 0 -1
```

**예시:**

```bash
LPUSH mylist "orange"
LRANGE mylist 0 -1
```

### 집합(Set)

순서가 없고 중복이 없는 값들의 집합을 저장합니다.

**SADD**: 집합에 요소를 추가합니다.

```bash
SADD myset "apple"
```

**SMEMBERS**: 집합의 모든 요소를 가져옵니다.

```bash
SMEMBERS myset
```

**예시:**

```bash
SADD myset "banana"
SADD myset "cherry"
SMEMBERS myset
```

### 해시(Hash)

필드와 값의 쌍으로 이루어진 데이터를 저장합니다.

**HSET**: 해시에 필드와 값을 설정합니다.

```bash
HSET user:1 name "Alice"
HSET user:1 age 30
```

**HGET**: 특정 해시 필드의 값을 가져옵니다.

```bash
HGET user:1 name
```

**HGETALL**: 해시의 모든 필드와 값을 가져옵니다.

```bash
HGETALL user:1
```

### 정렬된 집합(Sorted Set)

각 요소가 점수와 함께 저장되며 점수를 기준으로 정렬됩니다.

**ZADD**: 정렬된 집합에 요소와 점수를 추가합니다.

```bash
ZADD leaderboard 100 "Alice"
```

**ZRANGE**: 정렬된 집합에서 일정 범위의 요소를 가져옵니다.

```bash
ZRANGE leaderboard 0 -1 WITHSCORES
```

**예시:**

```bash
ZADD leaderboard 150 "Bob"
ZADD leaderboard 200 "Charlie"
ZRANGE leaderboard 0 -1 WITHSCORES
```

---

## 기타 유용한 명령어

### KEYS: 패턴에 매칭되는 키 목록

특정 패턴에 매칭되는 모든 키를 가져옵니다.

```bash
KEYS <pattern>
```

**예시:**

```bash
KEYS user:*
```

### EXPIRE: 키에 유효기간 설정

특정 키에 대해 유효기간(초 단위)을 설정합니다.
설정하지 않는 경우 -1(유효기가 없음)로 기본 설정됩니다.

```bash
EXPIRE <key> <seconds>
```

**예시:**

```bash
EXPIRE session:12345 3600
```

### TTL: 키의 남은 유효기간 확인

특정 키의 남은 유효기간(초 단위)을 확인합니다.

```bash
TTL <key>
```

**예시:**

```bash
TTL session:12345
```

---

## 마치며

이번 글에서는 Redis의 기본적인 명령어들에 대해 살펴보았습니다. Redis는 높은 성능과 다양한 데이터 구조를 지원하여 웹 애플리케이션, 캐싱, 세션 관리 등 다양한 분야에서 활용되고 있습니다. 더욱 다양한 명령어와 고급 기능을 학습하여 Redis를 효과적으로 활용해 보시기 바랍니다.

---

**참고 자료:**

- [Redis 공식 문서](https://redis.io/docs/latest/develop/data-types/)
- [Redis 명령어 목록](https://redis.io/commands)