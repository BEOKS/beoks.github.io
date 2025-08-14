# JSON Web Token (JWT) 이해하기

## 개요

JSON Web Token(JWT)은 JSON 객체를 사용하여 양 당사자 사이에서 정보를 안전하게 전달하기 위한 개방형 표준(RFC 7519)입니다. 주로 인증 및 권한 부여를 위해 사용되며, 토큰 기반 인증 시스템에서 널리 활용되고 있습니다.

## JWT의 구조

JWT는 마침표(`.`)로 구분된 세 가지 부분으로 구성됩니다:

1. **헤더(Header)**
2. **페이로드(Payload)**
3. **서명(Signature)**

예시:

```
xxxxx.yyyyy.zzzzz
```

### 1. 헤더(Header)

헤더에는 토큰의 타입과 해싱 알고리즘 정보가 포함됩니다.

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

- `alg`: 해싱 알고리즘 (예: HS256, RS256)
- `typ`: 토큰 타입 (JWT)

### 2. 페이로드(Payload)

페이로드에는 클레임(Claims)이라고 하는 인증 정보가 포함됩니다. 클레임은 등록된 클레임, 공개 클레임, 비공개 클레임으로 나뉩니다.

**예시**

```json
{
  "sub": "1234567890",
  "name": "홍길동",
  "admin": true
}
```

- `sub`: subject의 약자, 토큰의 주체를 식별하는 데 사용
- `name`: 사용자 이름
- `admin`: 관리자 여부

### 3. 서명(Signature)

서명은 토큰의 무결성을 검증하기 위해 사용됩니다.

서명 생성 과정:

```
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secret
)
```

- `secret`: 서버만 알고 있는 비밀 키

## JWT의 작동 방식

1. **사용자 인증 요청**: 사용자가 아이디와 비밀번호로 로그인 시도
2. **서버에서 사용자 인증**: 아이디와 비밀번호 확인
3. **JWT 생성 및 발급**: 인증에 성공하면 서버는 JWT를 생성하여 클라이언트에 전달
4. **클라이언트에서 JWT 저장**: 브라우저 로컬 스토리지나 쿠키에 JWT 저장
5. **인증이 필요한 요청 시 JWT 전송**: 클라이언트는 서버로 요청을 보낼 때 JWT를 포함
6. **서버에서 JWT 검증 및 응답**: 서버는 JWT의 유효성을 검증하고 요청 처리

## JWT의 장점

- **무상태(stateless) 서버 구현**: 서버 측 세션 관리가 필요 없음
- **확장성**: 서버 간 토큰 공유로 마이크로서비스에 적합
- **모바일 친화적**: 모바일 환경에서 효율적인 인증 가능

## [[세션(Session)]] vs JWT
![[세션(Session)과 JWT(JSON Web Token)의 비교]]


## 보안 고려 사항

- **비밀 키 관리**: 서명에 사용되는 비밀 키는 안전하게 관리해야 함
- **토큰 탈취 위험**: JWT가 탈취되면 악용될 수 있으므로 HTTPS 사용 등 보안 강화 필요
- **짧은 만료 시간 설정**: 토큰의 유효 기간을 짧게 설정하여 위험 감소
- **토큰 폐기 메커니즘**: 로그아웃이나 권한 변경 시 토큰을 무효화하는 방법 고려

## 사용 예시

### 토큰 생성 (Node.js 예시)

```javascript
const jwt = require('jsonwebtoken');

const payload = {
  sub: '1234567890',
  name: '홍길동',
  admin: true
};

const secret = 'your-256-bit-secret';

const token = jwt.sign(payload, secret, { expiresIn: '1h' });

console.log(token);
```

### 토큰 검증

```javascript
jwt.verify(token, secret, (err, decoded) => {
  if (err) {
    // 토큰 검증 실패
    console.error('토큰이 유효하지 않습니다.');
  } else {
    // 토큰 검증 성공
    console.log(decoded);
  }
});
```

## 결론

JWT는 현대 웹 애플리케이션에서 인증과 권한 관리를 효율적으로 수행할 수 있는 강력한 도구입니다. 이해하기 쉽고 구현이 간단하지만, 보안에 대한 충분한 고려가 필요합니다. 올바른 사용 방식을 준수하여 안전하고 확장성 있는 인증 시스템을 구축해 보세요.

## 참고 자료

- [RFC 7519 - JSON Web Token (JWT)](https://tools.ietf.org/html/rfc7519)
- [JWT 공식 웹사이트](https://jwt.io/)