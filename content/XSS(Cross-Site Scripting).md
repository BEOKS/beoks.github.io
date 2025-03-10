## 개요

Cross-Site Scripting(XSS)는 웹 애플리케이션에서 자주 발견되는 보안 취약점 중 하나로, 공격자가 악의적인 스크립트를 타인의 웹 페이지에 삽입하여 사용자의 브라우저에서 실행되도록 하는 공격입니다. 이를 통해 공격자는 사용자의 세션을 탈취하거나, 웹 사이트 변조, 악성 사이트로의 리디렉션 등 다양한 공격을 수행할 수 있습니다.

## XSS의 종류

XSS는 발생 방식에 따라 세 가지로 분류됩니다.

### 1. 저장형 XSS (Stored XSS)

저장형 XSS는 공격 스크립트가 서버에 영구적으로 저장되어 다수의 사용자에게 전파되는 유형입니다. 게시판, 댓글, 프로필 정보 등 사용자 입력을 저장하고 표시하는 기능에서 주로 발생합니다.

### 2. 반사형 XSS (Reflected XSS)

반사형 XSS는 사용자의 요청에 포함된 입력 값이 검증 없이 즉시 응답에 반영되어 발생합니다. 공격자는 악의적인 스크립트를 포함한 URL을 생성하여 사용자가 이를 클릭하도록 유도합니다.

### 3. DOM 기반 XSS (DOM-based XSS)

DOM 기반 XSS는 클라이언트 측에서 DOM(Document Object Model)을 조작하여 발생하는 취약점입니다. 서버와의 통신 없이 브라우저에서 스크립트가 실행되므로 탐지와 방어가 어렵습니다.

## XSS 공격의 동작 원리

1. **스크립트 삽입**: 공격자는 취약한 웹 애플리케이션에 악의적인 스크립트를 삽입합니다.
2. **스크립트 전달**: 삽입된 스크립트는 다른 사용자의 브라우저로 전달됩니다.
3. **스크립트 실행**: 사용자의 브라우저는 전달받은 스크립트를 실행합니다.
4. **공격 성공**: 스크립트는 사용자의 세션 정보 탈취, 키로깅, 피싱 등의 악의적인 행위를 수행합니다.

```html
<!-- 예시: 입력 값을 그대로 출력하는 취약한 코드 -->
<p>안녕하세요, <span id="username"></span>님!</p>

<script>
  var params = new URLSearchParams(window.location.search);
  var username = params.get('name');
  document.getElementById('username').innerHTML = username;
</script>
```

위 코드는 URL 파라미터 `name`의 값을 검증 없이 페이지에 출력하고 있어 XSS 공격에 취약합니다.

## XSS의 영향

- **개인 정보 유출**: 사용자의 쿠키 정보를 탈취하여 세션을 하이재킹할 수 있습니다.
- **웹 사이트 변조**: 페이지 내용을 변경하여 피싱 페이지로 유도하거나 허위 정보를 표시할 수 있습니다.
- **악성 코드 유포**: 사용자의 브라우저에 악성 코드를 설치하거나 다른 공격의 매개체로 활용할 수 있습니다.

## XSS 방어 방법

1. **입력 값 검증(Input Validation)**: 사용자로부터 입력받은 데이터는 화이트리스트 방식을 통해 허용된 값만 처리합니다.

2. **출력 값 인코딩(Output Encoding)**: HTML, JavaScript, URL 등 **출력되는 위치**에 따라 적절한 인코딩을 적용합니다.

   ```javascript
   // 안전한 코드: 입력 값을 인코딩하여 출력
   var username = params.get('name');
   document.getElementById('username').textContent = username;
   ```

3. **[[콘텐츠 보안 정책(Content Security Policy) 설정]]**: `Content-Security-Policy` 헤더를 통해 스크립트 실행 소스를 제한합니다.

   ```
   Content-Security-Policy: default-src 'self';
   ```

4. **HTTP 전송 보안 강화**: [[HttpOnly 쿠키]]] 및 `Secure` 쿠키 속성을 사용하여 쿠키의 보안을 강화합니다.

5. **프레임워크의 보안 기능 활용**: 대부분의 웹 프레임워크는 XSS 방어를 위한 기능을 제공합니다. 이를 적극 활용합니다.