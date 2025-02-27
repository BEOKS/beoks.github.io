# HttpOnly 쿠키란 무엇이고 왜 중요한가?

웹 개발을 하다 보면 쿠키를 사용하여 세션 정보를 저장하거나 사용자 상태를 유지하는 일이 빈번합니다. 그러나 쿠키는 보안 취약점에 노출될 수 있으며, 특히 [[XSS(Cross-Site Scripting)]]에 취약합니다. 이러한 위험을 줄이기 위해 **HttpOnly 쿠키**를 사용합니다. 이번 글에서는 HttpOnly 쿠키가 무엇이며, 어떻게 보안을 강화하는지에 대해 알아보겠습니다.

---
## HttpOnly 쿠키란?

**HttpOnly 쿠키**는 쿠키의 속성 중 하나로, JavaScript를 통해 접근할 수 없도록 설정된 쿠키입니다. 쿠키에 `HttpOnly` 속성을 추가하면, 클라이언트 측 스크립트에서 해당 쿠키를 읽거나 수정할 수 없습니다.

```plaintext
Set-Cookie: sessionId=abc123; HttpOnly
```

### 어떻게 작동하나요?

`HttpOnly` 속성이 설정된 쿠키는 웹 브라우저에서 HTTP 요청 시에만 전송되며, `document.cookie` 등을 통해 접근이 불가능합니다. 이것은 쿠키 탈취를 목적으로 하는 XSS 공격을 어렵게 만듭니다.

## 왜 HttpOnly 쿠키를 사용해야 하나요?

### XSS 공격으로부터의 보호

`HttpOnly` 속성을 사용하면 클라이언트 측 스크립트에서 쿠키에 접근할 수 없으므로, XSS 공격을 통한 쿠키 탈취 위험을 줄일 수 있습니다.

**예시:**

```javascript
// 일반 쿠키에 접근
console.log(document.cookie); // "sessionId=abc123"

// HttpOnly 쿠키에 접근
console.log(document.cookie); // ""
```

위 예시에서 `sessionId` 쿠키가 `HttpOnly`로 설정되어 있다면 `document.cookie`를 통해서는 해당 쿠키를 확인할 수 없습니다.

## HttpOnly 쿠키의 한계

- **XSS 공격을 완전히 방어하지는 못함**: `HttpOnly` 쿠키를 사용하더라도, [[XSS(Cross-Site Scripting)]]를 막을 수는 없습니다. 공격자는 여전히 HTML 조작이나 사용자 입력 변조 등의 기법을 사용할 수 있습니다.
- **CSRF(Cross-Site Request Forgery) 공격에는 취약**: `HttpOnly` 쿠키는 CSRF 공격을 방어하지 못합니다. CSRF 방어를 위해서는 CSRF 토큰 등의 추가적인 조치가 필요합니다.

## HttpOnly 쿠키 사용 방법

### 서버 측 설정

대부분의 웹 애플리케이션 프레임워크에서는 쿠키 설정 시 `HttpOnly` 옵션을 제공합니다.
HTTP 응답 헤더에서 직접 `HttpOnly` 속성을 추가할 수 있습니다.

```plaintext
Set-Cookie: sessionId=abc123; HttpOnly
```

## 결론

웹 애플리케이션의 보안을 강화하기 위해서는 다양한 측면에서의 접근이 필요합니다. `HttpOnly` 쿠키는 쿠키 탈취를 목적으로 하는 XSS 공격을 방지하는 효과적인 방법입니다. 그러나 이것만으로 모든 보안 문제가 해결되는 것은 아니므로, CSP(Content Security Policy), 입력 검증, CSRF 토큰 등의 추가적인 보안 조치를 함께 고려해야 합니다.

---

## 참고 자료

- [MDN Web Docs - HttpOnly](https://developer.mozilla.org/ko/docs/Web/HTTP/Cookies#restrict_access_to_cookies)
- [OWASP Cheat Sheet - XSS Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [Web Security Academy - HttpOnly cookies](https://portswigger.net/web-security/cross-site-scripting/preventing)
- [RFC 6265 - HTTP State Management Mechanism](https://datatracker.ietf.org/doc/html/rfc6265)