> [!info]
> 이 설치방법은 7.4.2 버전 기준이며, 버전 업에 따라 방법이 달라질 수 있습니다. 최신 내용은 [공식 문서](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/install-redis-on-mac-os/)를 참고해주세요.
## 사전 준비

1. **Homebrew 설치 확인**:
   터미널을 열고 아래 명령어로 Homebrew 설치 여부를 확인하세요.

   ```bash
   brew --version
   ```

   Homebrew가 설치되어 있지 않다면 [Homebrew 설치 가이드](https://brew.sh/)를 참고하여 설치하시기 바랍니다.

## 설치 과정

1. **Redis 설치**:
   터미널에서 다음 명령어를 입력하여 Redis를 설치합니다.

   ```bash
   brew install redis
   ```

   위 명령어를 실행하면 시스템에 Redis가 설치됩니다.

## Redis 시작 및 종료

1. **포어그라운드에서 Redis 시작 및 종료**:
   설치 확인을 위해 다음 명령어로 Redis 서버를 시작할 수 있습니다.

   ```bash
   redis-server
   ```

   성공적으로 시작되면 Redis 서버의 시작 로그가 보이며, 포어그라운드에서 실행됩니다. 종료하려면 `Ctrl-C`를 입력하세요.

2. **launchd를 이용해 백그라운드에서 시작 및 종료**:
   Redis를 백그라운드 서비스로 실행하고 싶다면 다음 명령어를 사용하세요.

   ```bash
   brew services start redis
   ```

   이렇게 하면 Redis가 백그라운드에서 실행되며 로그인 시 자동으로 시작됩니다. 서비스 상태를 확인하려면 다음 명령어를 사용하세요.

   ```bash
   brew services info redis
   ```

   서비스를 종료하려면 다음과 같이 실행하세요.

   ```bash
   brew services stop redis
   ```

## Redis 연결

1. **Redis 클라이언트 연결 테스트**:
   Redis가 실행 중이라면 `redis-cli`로 연결하고 작동을 테스트할 수 있습니다.

   ```bash
   redis-cli
   ```

   연결 후, 다음과 같이 `ping` 명령어로 테스트하여 'PONG' 응답을 확인합니다.

   ```bash
   127.0.0.1:6379> ping
   PONG
   ```

   또한, Redis Insight를 사용하여 서버 상태를 확인할 수도 있습니다.

## 다음 단계

이제 Redis 인스턴스가 실행 중이라면:

- Redis CLI 튜토리얼을 시도해보세요.
- 다양한 Redis 클라이언트를 사용해 보세요.
- 프로덕션 환경에서 사용할 수 있도록 적절히 Redis를 설정해보세요.

이 글이 여러분의 macOS 환경에서의 Redis 설치에 도움이 되길 바랍니다. 추가적인 질문이나 피드백은 댓글로 남겨주세요. Redis와 함께 성공적인 개발 여정을 이어가시길 바랍니다!