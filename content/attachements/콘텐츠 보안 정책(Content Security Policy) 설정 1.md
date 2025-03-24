## 개요

**콘텐츠 보안 정책(Content Security Policy, CSP)**은 웹 애플리케이션에서 발생할 수 있는 [[XSS(Cross-Site Scripting)]] 및 데이터 인젝션 공격을 방지하기 위한 보안 표준입니다. CSP는 웹 페이지에서 로드되거나 실행될 수 있는 리소스의 출처를 지정함으로써, 악의적인 스크립트의 실행을 차단합니다.

## CSP의 필요성

현대의 웹 애플리케이션은 여러 외부 리소스(스크립트, 스타일시트, 이미지 등)에 의존합니다. 그러나 이러한 외부 리소스는 보안 취약점을 야기할 수 있으며, 공격자는 이를 이용하여 악성 코드를 삽입할 수 있습니다. CSP를 활용하면 신뢰할 수 없는 소스로부터의 리소스 로드를 제한하여 이러한 공격을 예방할 수 있습니다.

## CSP의 동작 원리

1. **정책 설정**: 서버는 HTTP 응답 헤더에 `Content-Security-Policy`를 포함하여 브라우저에 정책을 전달합니다.
2. **정책 적용**: 브라우저는 페이지를 로드할 때 해당 정책을 적용하여 리소스의 로드 및 실행을 제어합니다.
3. **위반 감지 및 보고**: 정책을 위반하는 리소스 로드 시 브라우저는 이를 차단하고, 필요에 따라 서버로 보고합니다.

## CSP 정책 구성

CSP는 다양한 지시어(Directive)와 소스 표현(Source Expression)을 조합하여 정책을 구성합니다.

### 주요 지시어

- **default-src**: 다른 지시어에서 별도로 지정하지 않은 모든 리소스 유형에 대한 기본 소스 목록을 설정합니다.
- **script-src**: 스크립트(`<script>` 태그, 인라인 스크립트, 이벤트 핸들러 등)의 소스를 지정합니다.
- **style-src**: 스타일시트(`<style>` 태그, 인라인 스타일 등)의 소스를 지정합니다.
- **img-src**: 이미지의 소스를 지정합니다.
- **connect-src**: AJAX, WebSocket 등의 연결 대상의 소스를 지정합니다.
- **font-src**: 웹폰트의 소스를 지정합니다.
- **media-src**: 오디오 및 비디오 등의 미디어 소스를 지정합니다.
- **object-src**: `<object>`, `<embed>`, `<applet>` 등의 소스를 지정합니다.
- **frame-src**: `<frame>` 및 `<iframe>`의 소스를 지정합니다.

### 소스 표현 방법

- **'self'**: 현재 페이지와 동일한 출처(Origin)을 의미합니다.
- **'none'**: 해당 리소스의 로드를 모두 차단합니다.
- **'unsafe-inline'**: 인라인 리소스를 허용합니다. (보안 취약점 발생 가능)
- **'unsafe-eval'**: `eval()` 함수와 같은 동적 코드 실행을 허용합니다. (보안 취약점 발생 가능)
- **데이터 스키마**: `data:` 스키마를 통해 인라인 데이터를 허용합니다.
- **URL**: 특정 도메인이나 경로를 지정할 수 있습니다. 예) `https://example.com`

## CSP 적용 방법

### 1. HTTP 응답 헤더 설정

서버 측에서 `Content-Security-Policy` 헤더를 설정하여 정책을 전달합니다.

**예시:**

```http
Content-Security-Policy: default-src 'self'; img-src 'self' https://images.example.com; script-src 'self' 'unsafe-inline'
```

### 2. 메타 태그 사용

HTML 문서의 `<head>` 섹션에 메타 태그로 정책을 지정할 수 있습니다.

```html
<meta http-equiv="Content-Security-Policy" content="default-src 'self';">
```

**주의:** 메타 태그를 통한 설정은 외부 스크립트 로드 이전에 적용되지 않을 수 있으므로 가능하면 HTTP 헤더를 사용하는 것이 좋습니다.

## CSP 예제

### 기본 정책 설정

```http
Content-Security-Policy: default-src 'self';
```

- 모든 리소스는 현재 출처에서만 로드됩니다.

### 외부 이미지 및 스크립트 허용

```http
Content-Security-Policy: 
    default-src 'self';
    img-src 'self' https://images.example.com;
    script-src 'self' https://cdn.example.com;
```

- 이미지는 현재 출처와 `https://images.example.com`에서 로드 가능
- 스크립트는 현재 출처와 `https://cdn.example.com`에서 로드 가능

### 인라인 스크립트 및 스타일 허용

```http
Content-Security-Policy: 
    default-src 'self';
    script-src 'self' 'unsafe-inline';
    style-src 'self' 'unsafe-inline';
```

- 인라인 스크립트와 스타일을 허용하지만, 보안상 위험할 수 있으므로 신중히 사용해야 합니다.

## CSP 보고서 설정

정책 위반 시 브라우저가 서버로 보고서를 전송하도록 설정할 수 있습니다.

```http
Content-Security-Policy: default-src 'self'; report-uri /csp-report-endpoint
```

- `/csp-report-endpoint`는 정책 위반 보고서를 수신하여 처리하는 서버의 엔드포인트입니다.

**참고:** 보고서 전송은 `report-uri` 지시어로 지정하며, 최신 CSP 표준에서는 `report-to` 지시어를 사용합니다.

## CSP 설정 시 주의 사항

- **점진적인 도입 권장**: CSP를 처음 적용할 때는 너무 엄격한 정책보다는 점진적으로 도입하여 정상적인 기능에 영향이 없도록 합니다.
- **테스트 모드 활용**: `Content-Security-Policy-Report-Only` 헤더를 사용하여 정책을 실제로 적용하지 않고 위반 사항만 보고받을 수 있습니다.
  
```http
  Content-Security-Policy-Report-Only: default-src 'self';
```
  
- **신뢰할 수 없는 소스 허용 주의**: `'unsafe-inline'`, `'unsafe-eval'`은 가능하면 사용하지 않습니다.
- **서비스 특성에 맞는 정책 구성**: CDN을 이용하거나 외부 API를 사용하는 경우 해당 도메인을 명시적으로 허용해야 합니다.

## CSP의 한계와 보완점

- **완벽한 방어 수단은 아님**: CSP는 강력한 보안 도구이지만, 모든 XSS 공격을 방어할 수 있는 것은 아닙니다. 다른 보안 수단과 병행하여 사용해야 합니다.
- **정교한 설정 필요**: 잘못된 설정은 정상적인 기능을 방해할 수 있으므로, 서비스에 맞는 정교한 정책 구성이 필요합니다.
- **브라우저 호환성**: 모든 브라우저에서 CSP를 동일하게 지원하지 않을 수 있으므로 호환성을 고려해야 합니다.
