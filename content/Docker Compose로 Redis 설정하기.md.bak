[[Docker 로 Redis 설치하기|앞선 포스팅]]에서는 Docker를 이용하여 Redis를 설치하고 실행하는 방법에 대해 알아보았습니다. 이번에는 `docker-compose`를 활용하여 Redis를 설정하고, 인증 정보 등을 포함한 다양한 설정을 적용하는 방법을 알아보겠습니다.

---
## Redis용 docker-compose.yml 작성

`docker-compose.yml` 파일을 작성하여 Redis 컨테이너를 설정할 수 있습니다. 해당 파일에서 환경 변수나 볼륨, 포트 매핑 등을 지정하여 원하는 설정을 적용할 수 있습니다.

### 디렉토리 구조

프로젝트를 위한 새로운 디렉토리를 만들고, 그 안에 `docker-compose.yml` 파일을 생성합니다.

```bash
mkdir redis-docker-compose
cd redis-docker-compose
touch docker-compose.yml
```

### docker-compose.yml 내용

`docker-compose.yml` 파일에 다음과 같이 내용을 작성합니다.

```yaml
version: '3.8'

services:
  redis:
    image: redis:latest
    container_name: redis-server
    ports:
      - "6379:6379"
    volumes:
      - ./redis.conf:/usr/local/etc/redis/redis.conf
    command: ["redis-server", "/usr/local/etc/redis/redis.conf"]
```

- `image`: 사용할 Redis 이미지입니다.
- `container_name`: 컨테이너의 이름을 지정합니다.
- `ports`: 호스트와 컨테이너의 포트를 매핑합니다.
- `volumes`: 호스트의 [redis.conf](https://redis.io/docs/latest/operate/oss_and_stack/management/config/) 파일을 컨테이너 내부로 마운트합니다.
- `command`: 컨테이너 실행 시 실행할 명령어를 지정합니다. 여기서는 우리가 제공한 `redis.conf` 파일을 사용하도록 설정합니다.

## Redis 설정 파일 작성

Redis에 인증을 적용하려면 `redis.conf` 파일에서 관련 설정을 변경해야 합니다.

### redis.conf 파일 생성

현재 디렉토리에 `redis.conf` 파일을 생성합니다.

```bash
touch redis.conf
```

### redis.conf 내용

`redis.conf` 파일에 다음과 같이 내용을 작성합니다.

```conf
# Redis 기본 포트 설정
port 6379

# 외부 접속을 허용하기 위해 모든 인터페이스에서 연결을 수락
bind 0.0.0.0

# Redis 에서 인증을 요구하도록 설정
requirepass your_redis_password
```

- `port`: Redis가 수신할 포트 번호입니다.
- `bind`: 접속을 허용할 IP를 지정합니다. `0.0.0.0`은 모든 인터페이스에서의 접속을 허용합니다.
- `requirepass`: Redis 접속 시 요구되는 비밀번호를 설정합니다. 원하는 비밀번호로 변경해주세요.

## Docker Compose로 Redis 실행

이제 준비된 `docker-compose.yml` 파일을 이용하여 Redis 컨테이너를 실행합니다.

```bash
docker-compose up -d
```

명령어를 실행하면 Docker Compose가 정의된 서비스들을 백그라운드에서 실행합니다.

실행 중인 컨테이너를 확인하려면 다음 명령어를 사용합니다.

```bash
docker-compose ps
```

## Redis 접속 및 인증 확인

설정된 Redis에 접속하여 인증이 제대로 적용되었는지 확인해보겠습니다.

### Redis CLI 설치 (호스트 머신에 Redis CLI 없을 경우)

만약 호스트 머신에 Redis CLI (`redis-cli`)가 설치되어 있지 않다면, Docker를 이용하여 Redis CLI를 실행할 수 있습니다.

```bash
docker run -it --rm --network host redis redis-cli -h 127.0.0.1 -p 6379
```

여기서 `--network host` 옵션은 호스트의 네트워크 스택을 사용하도록 합니다.

### Redis에 접속

`redis-cli`를 실행하여 Redis 서버에 접속합니다.

```bash
redis-cli -h 127.0.0.1 -p 6379
```

접속 후 인증을 하지 않고 명령을 실행하면 오류가 발생합니다.

```bash
127.0.0.1:6379> GET test
(error) NOAUTH Authentication required.
```

### AUTH 명령으로 인증

`AUTH` 명령을 사용하여 설정한 비밀번호로 인증합니다.

```bash
127.0.0.1:6379> AUTH your_redis_password
OK
```

인증에 성공하면 이제 Redis 명령을 정상적으로 사용할 수 있습니다.

```bash
127.0.0.1:6379> SET test "Hello, Redis with Auth!"
OK
127.0.0.1:6379> GET test
"Hello, Redis with Auth!"
```

## 마치며

이번 포스팅에서는 Docker Compose를 이용하여 Redis를 설정하고, 인증 정보를 포함한 다양한 설정을 적용하는 방법에 대해 알아보았습니다.

Docker Compose를 사용하면 복잡한 설정이 필요한 경우에도 구성 파일을 통해 손쉽게 컨테이너를 관리할 수 있습니다. 특히 여러 개의 서비스가 연동되는 환경에서 효율적으로 사용할 수 있습니다.

---

**참고 자료**

- [Docker Compose 공식 문서](https://docs.docker.com/compose/)
- [Redis 보안 가이드](https://redis.io/topics/security)
- [Docker Hub - Redis](https://hub.docker.com/_/redis)