IP 주소(Internet Protocol Address)는 인터넷 프로토콜을 사용하는 [[Network]]에서 각 장치를 고유하게 식별하기 위한 숫자 식별자입니다. 인터넷에 연결된 모든 장치(컴퓨터, 스마트폰, 서버 등)는 통신을 위해 최소한 하나의 IP 주소를 가져야 합니다.

IP 주소는 네트워크 계층([[OSI 모델]])에서 사용되며, 데이터 패킷이 올바른 목적지에 도달할 수 있도록 라우팅 정보를 제공합니다. IP 주소를 이해하기 위해서는 먼저 [[Network]], [[네트워크 계층]], [[Router]], [[라우팅(Routing)]]의 개념을 이해하는 것이 중요합니다.

## IP 주소의 등장 배경

초기 컴퓨터 [[Network]]에서는 각 컴퓨터를 물리적 주소인 MAC 주소로만 식별했습니다. 하지만 [[Network]]가 확장되면서 다음과 같은 문제들이 발생했습니다.

1. **확장성 문제** : MAC 주소는 하드웨어에 고정되어 있어 네트워크 구조 변경 시 관리가 어렵습니다.
2. **라우팅 복잡성** : 물리적 주소만으로는 계층적 네트워크 구조를 효율적으로 관리할 수 없습니다.
3. **주소 관리** : 대규모 네트워크에서 수많은 장치의 주소를 체계적으로 관리할 방법이 필요했습니다.

IP 주소는 이러한 문제들을 해결하기 위해 등장했습니다. IP 주소는 논리적 주소로, [[Network]] 구조에 따라 유연하게 할당하고 관리할 수 있으며, 계층적 구조를 통해 효율적인 라우팅을 가능하게 합니다.

## IP 주소의 종류

IP 주소는 크게 두 가지 버전으로 나뉩니다:

### IPv4 (Internet Protocol version 4)

IPv4는 현재 가장 널리 사용되는 IP 주소 체계입니다. 32비트 주소 공간을 사용하여 약 43억 개의 고유한 주소를 표현할 수 있습니다.

**IPv4 주소 형식**:
- 점으로 구분된 4개의 10진수로 표현됩니다 (예: 192.168.1.1)
- 각 숫자는 0부터 255까지의 값을 가질 수 있습니다
- 총 32비트로 구성됩니다 (각 옥텟은 8비트)

**IPv4 주소 클래스**:
IPv4 주소는 전통적으로 클래스로 구분되었습니다:

- **클래스 A**: 0.0.0.0 ~ 127.255.255.255 (대규모 네트워크용)
- **클래스 B**: 128.0.0.0 ~ 191.255.255.255 (중규모 네트워크용)
- **클래스 C**: 192.0.0.0 ~ 223.255.255.255 (소규모 네트워크용)
- **클래스 D**: 224.0.0.0 ~ 239.255.255.255 (멀티캐스트용)
- **클래스 E**: 240.0.0.0 ~ 255.255.255.255 (실험용)

현대에는 클래스 기반 주소 체계 대신 [[CIDR(Classless Inter-Domain Routing)]]를 사용하여 더 효율적으로 주소를 할당합니다.

### IPv6 (Internet Protocol version 6)

IPv4 주소의 고갈 문제를 해결하기 위해 개발된 차세대 IP 주소 체계입니다. 128비트 주소 공간을 사용하여 거의 무한대에 가까운 주소를 제공합니다.

**IPv6 주소 형식**:
- 콜론으로 구분된 8개의 16진수 그룹으로 표현됩니다 (예: 2001:0db8:85a3:0000:0000:8a2e:0370:7334)
- 연속된 0 그룹은 `::`로 축약할 수 있습니다 (예: 2001:db8:85a3::8a2e:370:7334)
- 총 128비트로 구성됩니다

IPv6에 대한 자세한 내용은 [[IPv6 주소 체계]]를 참고해주세요.

## IP 주소의 구조

IP 주소는 두 부분으로 구성됩니다:

### 네트워크 ID (Network ID)
네트워크를 식별하는 부분입니다. 같은 네트워크에 속한 모든 장치는 동일한 네트워크 ID를 가집니다.

### 호스트 ID (Host ID)
네트워크 내에서 특정 장치를 식별하는 부분입니다. 같은 네트워크 내에서 각 장치는 고유한 호스트 ID를 가져야 합니다.

네트워크 ID와 호스트 ID의 경계는 [[서브넷 마스크(Subnet Mask)]]로 결정됩니다. 서브넷 마스크는 IP 주소의 어느 부분이 네트워크 ID이고 어느 부분이 호스트 ID인지를 나타냅니다.

## IP 주소의 분류

### 공인 IP 주소 (Public IP Address)
인터넷에서 전역적으로 고유한 IP 주소입니다. 인터넷에 직접 연결된 장치가 사용하며, 전 세계에서 유일해야 합니다. 공인 IP 주소는 인터넷 서비스 제공자(ISP)로부터 할당받습니다.

### 사설 IP 주소 (Private IP Address)
로컬 네트워크 내에서만 사용되는 IP 주소입니다. 인터넷에 직접 노출되지 않으며, 같은 네트워크 내에서만 고유하면 됩니다. 사설 IP 주소는 [[NAT(Network Address Translation)]]를 통해 공인 IP 주소로 변환되어 인터넷과 통신합니다.

**사설 IP 주소 대역**:
- 10.0.0.0 ~ 10.255.255.255 (10.0.0.0/8)
- 172.16.0.0 ~ 172.31.255.255 (172.16.0.0/12)
- 192.168.0.0 ~ 192.168.255.255 (192.168.0.0/16)

### 특수 IP 주소

- **루프백 주소 (Loopback Address)**: 127.0.0.1 (localhost) - 자신의 장치를 가리킵니다
- **브로드캐스트 주소**: 네트워크의 모든 장치에 메시지를 전송할 때 사용합니다
- **멀티캐스트 주소**: 특정 그룹의 장치들에게 메시지를 전송할 때 사용합니다

## IP 주소 할당 방법

### 정적 IP 주소 (Static IP Address)
수동으로 설정하여 고정된 IP 주소입니다. 서버나 네트워크 장비처럼 주소가 변경되면 안 되는 장치에 사용합니다.

### 동적 IP 주소 (Dynamic IP Address)
[[DHCP(Dynamic Host Configuration Protocol)]]를 통해 자동으로 할당되는 IP 주소입니다. 대부분의 클라이언트 장치는 동적 IP 주소를 사용합니다.

## Java에서 IP 주소 다루기

Java에서는 `java.net.InetAddress` 클래스를 사용하여 IP 주소를 다룰 수 있습니다:

```java
import java.net.InetAddress;
import java.net.UnknownHostException;

public class IPAddressExample {
    
    // 호스트 이름으로 IP 주소 조회
    public static void getIPByHostname(String hostname) throws UnknownHostException {
        InetAddress address = InetAddress.getByName(hostname);
        System.out.println("호스트 이름: " + address.getHostName());
        System.out.println("IP 주소: " + address.getHostAddress());
    }
    
    // 로컬 호스트 IP 주소 조회
    public static void getLocalhostIP() throws UnknownHostException {
        InetAddress localhost = InetAddress.getLocalHost();
        System.out.println("로컬 호스트 이름: " + localhost.getHostName());
        System.out.println("로컬 IP 주소: " + localhost.getHostAddress());
    }
    
    // IP 주소 유효성 검사
    public static boolean isValidIP(String ip) {
        try {
            InetAddress.getByName(ip);
            return true;
        } catch (UnknownHostException e) {
            return false;
        }
    }
    
    // IPv4와 IPv6 구분
    public static void checkIPVersion(String ip) throws UnknownHostException {
        InetAddress address = InetAddress.getByName(ip);
        if (address instanceof java.net.Inet4Address) {
            System.out.println("IPv4 주소입니다.");
        } else if (address instanceof java.net.Inet6Address) {
            System.out.println("IPv6 주소입니다.");
        }
    }
}
```

## 스프링에서 IP 주소 활용

스프링 프레임워크에서는 HTTP 요청의 클라이언트 IP 주소를 추출하는 기능을 제공합니다:

```java
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import javax.servlet.http.HttpServletRequest;

@RestController
public class IPController {
    
    @RequestMapping("/client-ip")
    public String getClientIP(HttpServletRequest request) {
        String ip = request.getHeader("X-Forwarded-For");
        if (ip == null || ip.isEmpty() || "unknown".equalsIgnoreCase(ip)) {
            ip = request.getHeader("Proxy-Client-IP");
        }
        if (ip == null || ip.isEmpty() || "unknown".equalsIgnoreCase(ip)) {
            ip = request.getHeader("WL-Proxy-Client-IP");
        }
        if (ip == null || ip.isEmpty() || "unknown".equalsIgnoreCase(ip)) {
            ip = request.getRemoteAddr();
        }
        return ip;
    }
}
```

프록시나 로드 밸런서를 거치는 경우, 실제 클라이언트 IP는 `X-Forwarded-For` 헤더에 포함될 수 있으므로 이를 확인해야 합니다.

## IP 주소와 보안

IP 주소는 보안 정책에서 중요한 역할을 합니다:

### IP 기반 접근 제어
특정 IP 주소나 IP 대역에서만 접근을 허용하거나 차단할 수 있습니다. 스프링 시큐리티에서는 다음과 같이 설정할 수 있습니다:

```java
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;

@EnableWebSecurity
public class SecurityConfig {
    
    public void configure(HttpSecurity http) throws Exception {
        http.authorizeRequests()
            .antMatchers("/admin/**")
            .hasIpAddress("192.168.1.0/24") // 특정 IP 대역만 허용
            .anyRequest().permitAll();
    }
}
```

### IP 주소 스푸핑 방지
공격자가 다른 IP 주소로 위장하는 것을 방지하기 위해, 신뢰할 수 있는 프록시나 로드 밸런서를 통해서만 `X-Forwarded-For` 헤더를 신뢰해야 합니다.

## IP 주소 관리 시 주의사항

1. **주소 고갈**: IPv4 주소는 이미 고갈되었으므로, 새로운 서비스는 가능한 한 IPv6를 고려해야 합니다.

2. **사설 IP 주소 충돌**: 여러 네트워크를 통합할 때 사설 IP 주소 범위가 겹치지 않도록 주의해야 합니다.

3. **동적 IP 주소의 불안정성**: 동적 IP 주소는 변경될 수 있으므로, IP 주소에 의존하는 설정은 피해야 합니다.

4. **보안 정책**: IP 주소만으로는 충분한 보안을 제공할 수 없습니다. IP 주소는 보안 정책의 일부로만 사용해야 합니다.

5. **NAT 트래버설**: 사설 IP 주소를 사용하는 장치와 직접 통신하려면 [[NAT 트래버설]] 기법이 필요할 수 있습니다.

## 실제 활용 사례

1. **로드 밸런싱**: 클라이언트 IP 주소를 기반으로 요청을 분산시킵니다.
2. **지리적 라우팅**: IP 주소의 지리적 위치를 기반으로 최적의 서버로 라우팅합니다.
3. **DDoS 방어**: 의심스러운 IP 주소에서 오는 요청을 차단합니다.
4. **세션 관리**: IP 주소를 세션 추적의 보조 수단으로 사용합니다.
5. **로그 분석**: 접근 로그에서 IP 주소를 분석하여 사용자 행동을 파악합니다.

## 결론

IP 주소는 네트워크 통신의 핵심 요소로, 인터넷에서 장치를 식별하고 데이터를 올바른 목적지로 전달하는 데 필수적입니다. IPv4와 IPv6의 차이점을 이해하고, 공인 IP와 사설 IP의 역할을 명확히 구분하는 것이 중요합니다.

또한 IP 주소는 보안 정책의 일부로 활용될 수 있지만, IP 주소만으로는 충분한 보안을 제공할 수 없으므로 다른 보안 메커니즘과 함께 사용해야 합니다.

[[Network]] 설계 시에는 [[서브넷(Subnet)]], [[서브넷팅]], [[CIDR(Classless Inter-Domain Routing)]], [[NAT]] 등의 개념을 함께 고려하여 효율적이고 확장 가능한 [[Network]] 구조를 설계해야 합니다.

## 참고 자료

- RFC 791 - Internet Protocol
- RFC 2460 - Internet Protocol, Version 6 (IPv6) Specification
- Java Network Programming, 4th Edition - Elliotte Rusty Harold
- 스프링 시큐리티 공식 문서

