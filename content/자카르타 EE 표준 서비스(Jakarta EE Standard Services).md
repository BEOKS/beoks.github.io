# HTTP

HTTP 클라이언트 API는 java.net 패키지에 정의되어 있습니다. HTTP 서버 API는 Jakarta 서블릿, Jakarta 서버 페이지 및 Jakarta 서버 인터페이스와 웹 서비스 지원으로 정의되어 있으며, 이는 Jakarta EE 플랫폼의 선택적 부분입니다.

# HTTPS

SSL 프로토콜 위에서 HTTP 프로토콜을 사용하는 것은 HTTP와 동일한 클라이언트 및 서버 API에 의해 지원됩니다.

# Jakarta Transaction API (JTA)

Jakarta 트랜잭션은 두 부분으로 구성됩니다:

- 컨테이너 및 애플리케이션 구성 요소가 트랜잭션 경계를 설정하는 데 사용하는 애플리케이션 수준 경계 인터페이스.
- 트랜잭션 관리자와 자원 관리자의 인터페이스로, Jakarta EE SPI 레벨에서 사용됩니다.

# RMI-IIOP (Optional)

Jakarta EE 에서는 IIOP 및 자바 IDL 사용을 포함한 CORBA 지원이 선택적입니다. 선택적 Jakarta 기술을 참조하세요.

# Java IDL (Optional)

Jakarta EE 에서는 IIOP 및 자바 IDL 사용을 포함한 CORBA 지원이 선택적입니다. 선택적 Jakarta 기술을 참조하세요.

# JDBC™ API

JDBC API는 관계형 데이터베이스 시스템과의 연결성을 위한 API입니다. JDBC API는 두 부분으로 구성됩니다: 데이터베이스 접근을 위한 애플리케이션 수준 인터페이스, 및 JDBC 드라이버를 Jakarta EE 플랫폼에 연결하는 서비스 제공자 인터페이스. 서비스 제공자 인터페이스는 Jakarta EE 제품에서 필수적이지 않습니다. 대신, JDBC 드라이버는 Jakarta EE 제품과 인터페이스하기 위해 커넥터 API의 기능을 사용하는 리소스 어댑터로 패키징되어야 합니다. JDBC API는 Java SE에 포함되어 있지만, 이 사양에는 JDBC 장치 드라이버에 대한 추가 요구 사항이 포함되어 있습니다.

# Jakarta Persistence API

Jakarta Persistence는 지속성 관리 및 객체/관계 매핑의 표준 API입니다. 이는 자바 도메인 모델을 사용하여 관계형 데이터베이스를 관리하는 애플리케이션 개발자를 위한 객체/관계 매핑 기능을 제공합니다. Jakarta Persistence는 Jakarta EE에서 지원되어야 합니다. 또한, Java SE 환경에서도 사용할 수 있습니다.

# Jakarta™ Messaging

Jakarta Messaging은 신뢰할 수 있는 지점 대 지점 메시징과 발행-구독 모델을 지원하는 표준 메시징 API입니다. 이 사양은 지점 대 지점 메시징과 발행-구독 메시징을 모두 구현하는 Jakarta Messaging 제공자를 요구합니다. Jakarta EE 제품 제공자는 애플리케이션이 이 JMS 제공자에 접근할 때 사용할 사전 구성된 기본 Jakarta Messaging 연결 팩토리도 제공해야 합니다. 기본 Jakarta Messaging 연결 팩토리를 참조하세요.

# Java Naming and Directory Interface™ (JNDI)

JNDI API는 명명 및 디렉토리 접근을 위한 표준 API입니다. JNDI API는 두 부분으로 구성됩니다: 애플리케이션 구성 요소가 명명 및 디렉토리 서비스를 접근하는 데 사용하는 애플리케이션 수준 인터페이스, 및 명명 및 디렉토리 서비스 제공자를 연결하기 위한 서비스 제공자 인터페이스. JNDI API는 Java SE에 포함되어 있지만, 이 사양은 추가 요구 사항을 정의합니다.

# Jakarta™ Mail

많은 인터넷 애플리케이션이 이메일 알림을 보내는 기능이 필요하기 때문에, Jakarta EE 플랫폼은 Jakarta Mail API와 자카르타 메일 서비스 제공자를 포함하여 애플리케이션 구성 요소가 인터넷 메일을 보내도록 합니다. Jakarta Mail API는 두 부분으로 구성됩니다: 애플리케이션 구성 요소가 메일을 보내는 데 사용하는 애플리케이션 수준 인터페이스, 및 Jakarta EE SPI 레벨에서 사용되는 서비스 제공자 인터페이스.

# Jakarta Activation Framework (JAF)

JAF API는 다양한 MIME 타입, 형식 및 위치에서 기원한 데이터를 처리하기 위한 프레임워크를 제공합니다. Jakarta Mail API는 JAF API를 사용합니다. Jakarta EE 에서는 Jakarta Activation Framework가 Jakarta EE 플랫폼의 일부로 포함되었습니다.

# XML Processing

Java™ API for XML Processing (JAXP)은 XML 문서 파싱을 위한 산업 표준인 SAX 및 DOM API를 지원하며, XSLT 변환 엔진을 지원합니다. Streaming API for XML (StAX)은 XML을 위한 풀 파싱 API를 제공합니다. JAXP 및 StAX API는 Java SE에 포함되어 있어 Jakarta EE 애플리케이션에서 사용할 수 있습니다.

# Jakarta Connectors

Jakarta Connectors는 엔터프라이즈 정보 시스템에 대한 접근을 지원하는 리소스 어댑터를 모든 Jakarta EE 제품에 플러그인할 수 있게 해주는 Jakarta EE SPI입니다. 커넥터 아키텍처는 Jakarta EE 서버와 리소스 어댑터 간의 시스템 수준 계약의 표준 세트를 정의합니다. 

# Security Services

Java™ Authentication and Authorization Service (JAAS)는 사용자의 인증 및 접근 제어를 시행할 수 있는 서비스를 제공합니다. 이는 표준 플러그형 인증 모듈 (PAM) 프레임워크의 자바 기술 버전을 구현하며, 사용자 기반의 권한 부여를 지원합니다. Jakarta™ Authorization은 Jakarta EE 애플리케이션 서버와 권한 부여 서비스 제공자 간의 계약을 정의하여, 사용자 정의 권한 부여 서비스 제공자가 모든 Jakarta EE 제품에 플러그인될 수 있게 합니다. Jakarta™ Authentication은 메시지 인증 메커니즘을 구현하는 인증 제공자가 클라이언트 또는 서버 메시지 처리 컨테이너 또는 런타임에 통합될 수 있도록 하는 SPI를 정의합니다. Jakarta Security는 Jakarta Authentication을 활용하지만 웹 애플리케이션 사용자를 인증하기 위한 더 쉬운 사용의 SPI를 제공하며, 인증 및 권한 부여를 위한 신원 저장소 API를 정의합니다.

# XML Web Services (Optional)

Jakarta EE는 웹 서비스 클라이언트와 웹 서비스 엔드포인트 둘 다에 대한 완전한 지원을 선택적으로 제공합니다. 여러 Jakarta 기술이 웹 서비스 지원을 제공하기 위해 함께 작동합니다.

# Jakarta JSON Processing

Jakarta JSON Processing은 JSON 텍스트를 처리(파싱, 생성, 변환 및 쿼리)하는 편리한 방법을 제공합니다.

# Jakarta JSON Binding

Jakarta JSON Binding은 JSON 텍스트와 자바 객체 간의 변환을 위한 편리한 방법을 제공합니다.

# Jakarta WebSocket

Jakarta WebSocket은 웹소켓 애플리케이션을 생성하기 위한 표준 API입니다.

# Jakarta RESTful Web Services

Jakarta RESTful Web Services는 REST 스타일을 사용하는 웹 서비스 지원을 제공합니다. RESTful 웹 서비스는 웹의 설계 스타일과 더 잘 맞으며 다양한 프로그래밍 언어를 사용하여 더 쉽게 접근할 수 있는 경우가 많습니다.

# Jakarta Concurrency

Jakarta Concurrency는 관리형 실행 서비스, 관리형 스케줄링 실행 서비스, 관리형 스레드 팩토리 및 컨텍스트 서비스를 통해 Jakarta EE 애플리케이션 구성 요소에 비동기 기능을 제공하는 표준 API입니다.

# Jakarta Batch

Jakarta Batch API는 배치 애플리케이션을 위한 프로그래밍 모델과 작업을 스케줄링하고 실행하기 위한 런타임을 제공합니다.

# Jakarta Enterprise Beans

플랫폼 사양에서는 다음 두 기능이 제거되었습니다.

- 컨테이너와 빈이 관리하는 지속성을 모두 포함하는 엔티티 빈
- Embeddable EJB 컨테이너