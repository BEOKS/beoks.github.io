Spring 에서 사용자 정보 관리를 위해 [[세션(Session)]]을 사용하는 경우가 많습니다. Spring Sesison 의 기본 [[세션 스토리지(Session Storage)]]는 서버 인메모리입니다. 이는 여러 서버에 공유되지 않아 여러 서버가 공유하기 어렵고 서버 재실행 시 초기화된다는 단점이 있습니다. 이 포스트는 Spring Session 에서 [[Redis]]를 [[세션 스토리지(Session Storage)]]로 이용하는 방법을 소개합니다.

---

## 적용 방법
Spring Boot 를 사용하는 경우 코드 작성 없이 라이브러리 추가와 Redis 정보 입력 만으로 적용이 가능합니다.
### 의존성 라이브러리 추가

먼저 필요한 라이브러리를 의존성에 추가합니다.
- spring-boot-starter-data-redis : Spring Data 기반 Redis JDBC 라이브러리
- spring-session-data-redis : Spring Session 저장소에 Redis 를 자동으로 등록하는 라이브러리
```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.session</groupId>
        <artifactId>spring-session-data-redis</artifactId>
    </dependency>
</dependencies>
```

```groovy
implementation("org.springframework.session:spring-session-data-redis")
```


```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-redis</artifactId>
    </dependency>
</dependencies>
```

```groovy
implementation("org.springframework.boot:spring-boot-starter-data-redis")
```

### Redis 정보 추가
`main > resource `디렉토리에서 `application.yaml` 또는 `application.properties` 파일에 Redis 정보를 다음과 같이 추가합니다.

```yaml
spring:  
  data:  
    redis:  
      host: "localhost" 
      port: "6379"  
      password: 
```
위 값은 디퐅트 값이며, 만약 접속 환경이 디폴트와 동일하다면 Redis 정보 추가 없이 사용할 수 있습니다.

## 결론

### 참고자료
- [Spring Session - Spring Boot](https://docs.spring.io/spring-session/reference/guides/boot-redis.html)