---
draft: false
tags:
  - 암호화
  - 보안
  - 해시
  - 인증
description: HMAC(Hash-based Message Authentication Code)에 대한 심층적인 이해와 구현 방법을 설명합니다.
---
현대 소프트웨어 개발에서 데이터의 무결성과 인증은 필수적인 요소입니다. 특히 네트워크를 통해 전송되는 데이터나 저장된 데이터가 변조되지 않았음을 확인하는 것은 보안의 기본입니다. HMAC(Hash-based Message Authentication Code)는 이러한 요구를 충족시키기 위한 암호학적 기법으로, 메시지의 무결성과 함께 발신자의 인증을 제공합니다. 이 글에서는 HMAC의 개념, 작동 원리, 구현 방법, 그리고 실제 사용 사례에 대해 상세히 알아보겠습니다.

## HMAC이란?

HMAC은 Hash-based Message Authentication Code의 약자로, 메시지의 무결성을 검증하고 인증을 제공하는 특수한 형태의 [[메시지 인증 코드]]입니다. 일반적인 해시 함수와 달리, HMAC은 비밀 키를 사용하여 해시 값을 생성합니다. 이를 통해 메시지가 전송 중에 변경되지 않았음을 확인할 수 있을 뿐만 아니라, 메시지가 실제로 키를 알고 있는 발신자로부터 왔다는 것을 인증할 수 있습니다.

HMAC은 RFC 2104에서 정의되었으며, 다양한 [[해시 함수]]와 함께 사용할 수 있습니다. 가장 일반적으로 사용되는 조합은 HMAC-SHA256, HMAC-SHA1, HMAC-MD5 등이 있습니다.

## HMAC의 보안 강도

HMAC의 보안 강도는 다음 요소에 의해 결정됩니다:

1. **사용되는 해시 함수의 강도**: HMAC은 기본 해시 함수의 강도에 의존합니다. 예를 들어, HMAC-SHA256은 SHA-256 해시 함수를 사용하므로 그 보안 강도는 SHA-256의 강도와 관련이 있습니다.
    
2. **키의 길이와 무작위성**: 키가 길고 무작위적일수록 HMAC은 더 안전합니다. 키의 길이는 최소한 해시 함수의 출력 길이와 같거나 그 이상이어야 합니다.
    
3. **키의 기밀성**: HMAC의 보안은 키의 기밀성에 의존합니다. 키가 노출되면 공격자가 유효한 HMAC을 생성할 수 있으므로 키를 안전하게 관리하는 것이 중요합니다.
    

HMAC은 현재까지 알려진 공격에 대해 강력한 보안을 제공합니다. 특히, 이중 해싱 구조는 길이 확장 공격을 효과적으로 방지합니다.

## Java에서의 HMAC 구현

Java에서 HMAC을 구현하는 것은 `javax.crypto` 패키지를 사용하여 비교적 간단하게 할 수 있습니다. 다음은 HMAC-SHA256을 구현하는 예시 코드입니다:

```java
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.nio.charset.StandardCharsets;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.util.Base64;

public class HMACExample {
    public static String calculateHMAC(String message, String key) 
            throws NoSuchAlgorithmException, InvalidKeyException {
        Mac mac = Mac.getInstance("HmacSHA256");
        SecretKeySpec secretKeySpec = new SecretKeySpec(
            key.getBytes(StandardCharsets.UTF_8), "HmacSHA256");
        mac.init(secretKeySpec);
        byte[] hmacBytes = mac.doFinal(message.getBytes(StandardCharsets.UTF_8));
        return Base64.getEncoder().encodeToString(hmacBytes);
    }
    
    public static void main(String[] args) {
        try {
            String message = "안녕하세요, 이것은 HMAC 테스트 메시지입니다.";
            String key = "비밀키_12345";
            String hmacResult = calculateHMAC(message, key);
            System.out.println("메시지: " + message);
            System.out.println("HMAC 결과: " + hmacResult);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

이 코드는 다음과 같은 단계로 작동합니다:

1. "HmacSHA256" 알고리즘을 사용하는 Mac 인스턴스를 생성합니다.
2. 비밀 키로부터 SecretKeySpec 객체를 생성합니다.
3. Mac 인스턴스를 초기화합니다.
4. 메시지에 대해 HMAC을 계산합니다.
5. 결과를 Base64로 인코딩하여 반환합니다.

다른 해시 알고리즘(예: HmacSHA1, HmacMD5)을 사용하려면 "HmacSHA256" 대신 해당 알고리즘 이름을 지정하면 됩니다.

## Spring 프레임워크에서의 HMAC 활용

Spring Security는 HMAC을 활용한 보안 기능을 제공합니다. 특히 RESTful API 인증에서 HMAC을 사용하는 방법을 살펴보겠습니다:

```java
import org.springframework.security.crypto.codec.Hex;
import org.springframework.stereotype.Component;

import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.nio.charset.StandardCharsets;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;

@Component
public class HMACAuthenticationService {
    private final String secretKey = "애플리케이션_비밀키";
    
    public String generateHMAC(String data) {
        try {
            Mac hmac = Mac.getInstance("HmacSHA256");
            SecretKeySpec secretKeySpec = new SecretKeySpec(
                secretKey.getBytes(StandardCharsets.UTF_8), "HmacSHA256");
            hmac.init(secretKeySpec);
            byte[] hmacBytes = hmac.doFinal(data.getBytes(StandardCharsets.UTF_8));
            return new String(Hex.encode(hmacBytes));
        } catch (NoSuchAlgorithmException | InvalidKeyException e) {
            throw new RuntimeException("HMAC 생성 중 오류 발생", e);
        }
    }
    
    public boolean validateHMAC(String data, String providedHMAC) {
        String calculatedHMAC = generateHMAC(data);
        return calculatedHMAC.equals(providedHMAC);
    }
}
```

이 서비스는 Spring 애플리케이션에서 다음과 같이 사용할 수 있습니다:

1. API 요청에 대한 HMAC을 생성합니다.
2. 클라이언트가 제공한 HMAC과 서버에서 계산한 HMAC을 비교하여 요청의 무결성과 인증을 확인합니다.

실제 구현에서는 비밀 키를 안전하게 관리하기 위해 환경 변수나 Spring의 프로퍼티 관리 시스템을 사용하는 것이 좋습니다.

## HMAC의 실제 사용 사례

HMAC은 다양한 보안 애플리케이션에서 사용됩니다:

1. **API 인증**: 많은 웹 API가 HMAC을 사용하여 요청의 무결성과 인증을 확인합니다. 예를 들어, AWS API는 HMAC을 사용하여 요청에 서명합니다.
    
2. **웹 토큰**: JWT(JSON Web Token)와 같은 웹 토큰은 HMAC을 사용하여 토큰의 무결성을 보장합니다.
    
3. **비밀번호 저장**: 비밀번호를 안전하게 저장하기 위해 HMAC을 사용할 수 있습니다. 이 경우 HMAC은 솔트와 함께 사용되어 레인보우 테이블 공격을 방지합니다.
    
4. **메시지 인증**: 안전한 통신 채널에서 메시지의 무결성과 인증을 확인하기 위해 HMAC을 사용합니다.
    
5. **파일 무결성 검사**: 파일이 변조되지 않았는지 확인하기 위해 HMAC을 사용할 수 있습니다.
    

## HMAC과 다른 인증 기법의 비교

HMAC은 다른 인증 기법과 비교하여 몇 가지 장단점이 있습니다:

### HMAC vs 일반 해시 함수

- **장점**: HMAC은 비밀 키를 사용하므로 인증 기능을 제공합니다. 일반 해시 함수는 무결성만 제공합니다.
- **단점**: HMAC은 키 관리가 필요하므로 추가적인 복잡성이 있습니다.

### HMAC vs 디지털 서명

- **장점**: HMAC은 대칭 키를 사용하므로 계산이 빠릅니다.
- **단점**: HMAC은 부인 방지(non-repudiation) 기능을 제공하지 않습니다. 발신자와 수신자 모두 동일한 키를 가지고 있기 때문입니다.

### HMAC vs CBC-MAC

- **장점**: HMAC은 특별히 설계된 MAC 알고리즘으로, 블록 암호의 취약점에 영향을 받지 않습니다.
- **단점**: CBC-MAC은 블록 암호를 이미 사용하는 시스템에서 구현이 더 간단할 수 있습니다.

## 결론

HMAC은 메시지의 무결성과 인증을 보장하는 강력한 암호학적 기법입니다. 다양한 해시 함수와 함께 사용할 수 있으며, 특히 HMAC-SHA256은 현재 가장 널리 사용되는 조합 중 하나