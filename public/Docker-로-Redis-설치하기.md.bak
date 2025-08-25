# Docker로 Redis 설치하기

개발을 진행하다 보면 캐시나 메시지 브로커로 Redis를 사용할 일이 많습니다. 이번 포스팅에서는 Docker를 이용하여 Redis를 설치하고 실행하는 방법에 대해 알아보겠습니다.

---

## Docker 설치 여부 확인

먼저 Docker가 설치되어 있는지 확인해야 합니다. 터미널에 다음 명령어를 입력하여 Docker 버전을 확인합니다.

```bash
docker --version
```

만약 Docker가 설치되어 있지 않다면 [Docker 공식 사이트](https://www.docker.com/get-started)에서 운영체제에 맞는 버전을 다운로드하여 설치해주세요.

## Redis 이미지 다운로드

Docker Hub에는 다양한 버전의 Redis 이미지가 존재합니다. 기본적인 최신 버전을 받기 위해 다음 명령어를 실행합니다.

```bash
docker pull redis
```

명령어를 실행하면 Docker가 Redis의 최신 이미지를 다운로드합니다.

## Redis 컨테이너 실행

이미지를 다운로드했다면 이제 컨테이너를 생성하고 실행할 차례입니다. 다음 명령어를 통해 Redis 컨테이너를 백그라운드에서 실행합니다.

```bash
docker run -d --name my-redis -p 6379:6379 redis
```

- `-d`: 컨테이너를 백그라운드(detached) 모드로 실행합니다.
- `--name my-redis`: 컨테이너의 이름을 `my-redis`로 지정합니다.
- `-p 6379:6379`: 호스트의 포트 6379를 컨테이너의 포트 6379에 매핑합니다.

## Redis 접속 및 테스트

Redis 클라이언트를 사용하여 Redis 서버에 접속해보겠습니다. Redis 컨테이너에 접속하려면 다음 명령어를 사용합니다.

```bash
docker exec -it my-redis redis-cli
```

접속에 성공하면 다음과 같은 프롬프트가 나타납니다.

```
127.0.0.1:6379>
```

간단한 set/get 명령으로 동작을 확인해봅니다.

```bash
127.0.0.1:6379> SET test "Hello, Redis!"
OK
127.0.0.1:6379> GET test
"Hello, Redis!"
```

데이터가 정상적으로 저장되고 조회되는 것을 확인할 수 있습니다.

### Docker Compose 로 Redis 설정하기
[[Docker Compose로 Redis 설정하기]]


## 마치며

Docker를 이용하여 Redis를 손쉽게 설치하고 실행하는 방법에 대해 알아보았습니다. Docker를 사용하면 복잡한 설치 과정 없이도 필요한 서비스들을 빠르게 구축하고 테스트할 수 있어 개발 생산성을 높일 수 있습니다.

Redis를 활용하여 다양한 애플리케이션에 캐싱 또는 메시지 브로커 기능을 추가해보세요!

---

**참고 자료**

- [Docker Hub - Redis](https://hub.docker.com/_/redis)
- [Redis 공식 문서](https://redis.io/documentation)