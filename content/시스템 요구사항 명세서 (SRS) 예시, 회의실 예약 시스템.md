이 문서는 [[ISO/IEC/IEEE 29148]] 표준에 따라 작성된 **회의실 예약 시스템** 의 시스템 요구사항 명세서(SRS) 예시입니다.

---

### **문서 정보**

|   |   |
|---|---|
|**항목**|**내용**|
|**문서 버전**|v1.0|
|**작성일**|2025-05-28|
|**작성자**|홍길동 (시스템 분석가)|
|**상태**|초안 (Draft)|

---

## 1. 서론 (Introduction)

### 1.1. 목적 (Purpose)

이 문서는 'Book-It' 회의실 예약 시스템의 기능, 성능, 제약 조건 및 기타 요구사항을 상세히 정의하는 것을 목적으로 한다. 이 문서는 개발팀, QA팀, 기획팀 등 모든 프로젝트 이해관계자 간의 합의된 기준선 역할을 한다.

### 1.2. 범위 (Scope)

본 시스템은 사내 직원을 위한 웹 기반 회의실 검색, 예약, 취소 및 관리 기능을 제공한다.

- **포함되는 범위**:
    - 사용자 인증 및 권한 관리
    - 회의실 정보 및 현황 조회
    - 회의실 예약 및 수정/취소
    - 관리자를 위한 회의실 및 예약 관리 기능
- **포함되지 않는 범위**:
    - 외부인을 위한 예약 기능
    - 예약 비용 결제 기능
    - 화상 회의 장비 연동 기능

### 1.3. 용어 정의 (Definitions)

|   |   |
|---|---|
|**용어**|**설명**|
|**사용자**|시스템에 로그인하여 회의실을 예약하고 사용하는 일반 사내 직원|
|**관리자**|시스템의 마스터 데이터(회의실, 사용자 권한 등)를 관리하는 특수 사용자|
|**예약**|특정 시간대에 특정 회의실을 사용하기 위해 시스템에 등록하는 행위|
|**SSO**|Single Sign-On. 사내 통합 인증 시스템|

### 1.4. 참고 자료 (References)

- 사내 SSO 연동 가이드 v1.2

## 2. 전체 설명 (Overall Description)

### 2.1. 제품 관점 (Product Perspective)

'Book-It'은 현재 수동(오프라인 화이트보드 및 구두 협의)으로 이루어지는 회의실 예약 방식을 대체하는 새로운 독립형 웹 기반 시스템이다. 모든 데이터는 자체 데이터베이스에 저장되며, 사용자 인증은 사내 SSO 시스템과 연동하여 처리한다.

### 2.2. 사용자 특징 (User Characteristics)

|   |   |
|---|---|
|**사용자 분류**|**특징**|
|**일반 사용자**|- 사내 모든 직원&lt;br>- 기본적인 웹 브라우저 사용 능력 보유|
|**시스템 관리자**|- IT 지원팀 소속&lt;br>- 시스템 설정 및 데이터 관리에 대한 이해 보유|

### 2.3. 제약 조건 (Constraints)

- 시스템은 웹 브라우저(Chrome, Edge 최신 버전) 환경에서 동작해야 한다.
- 사용자 인증은 반드시 사내 SSO를 통해서만 이루어져야 한다.
- 서버 측 애플리케이션은 Java Spring Boot 프레임워크를 사용해야 한다.
- 모든 시스템 로그는 사내 표준 로그 서버로 전송되어야 한다.

### 2.4. 가정 및 종속성 (Assumptions and Dependencies)

- 사내 SSO 시스템 API는 프로젝트 기간 동안 안정적으로 제공되며, 관련 기술 문서는 최신 상태로 유지된다고 가정한다.
- 시스템은 사내 인트라넷 환경에서만 접근 가능하다.

## 3. 상세 요구사항 (Specific Requirements)

### 3.1. 기능 요구사항 (Functional Requirements)

|   |   |   |
|---|---|---|
|**ID**|**요구사항 명**|**설명**|
|**FR-AUTH-001**|SSO를 통한 로그인|사용자는 사내 SSO 계정을 통해 시스템에 로그인할 수 있어야 한다.|
|**FR-AUTH-002**|로그아웃|사용자는 시스템에서 안전하게 로그아웃할 수 있어야 한다.|
|**FR-SEARCH-001**|회의실 목록 조회|사용자는 전체 회의실 목록과 기본 정보(이름, 위치, 최대 수용 인원)를 조회할 수 있어야 한다.|
|**FR-SEARCH-002**|조건부 검색|사용자는 날짜, 시간, 예상 참석 인원 수로 예약 가능한 회의실을 검색할 수 있어야 한다.|
|**FR-BOOK-001**|회의실 예약|사용자는 원하는 시간대를 선택하여 회의실을 예약할 수 있어야 한다. 예약 시 회의 제목을 필수로 입력해야 한다.|
|**FR-BOOK-002**|예약 중복 방지|이미 예약된 시간대에는 다른 사용자가 중복으로 예약할 수 없어야 한다.|
|**FR-BOOK-003**|내 예약 조회|사용자는 자신이 예약한 내역을 목록 형태로 조회할 수 있어야 한다.|
|**FR-BOOK-004**|예약 취소|사용자는 자신이 예약한 건에 한해 예약을 취소할 수 있어야 한다.|
|**FR-ADMIN-001**|회의실 정보 관리|관리자는 새로운 회의실을 등록하고, 기존 회의실 정보를 수정/삭제할 수 있어야 한다.|

### 3.2. 비기능적 요구사항 (Non-functional Requirements)

#### 3.2.1. 사용성 요구사항 (Usability Requirements)

|   |   |   |
|---|---|---|
|**ID**|**요구사항 명**|**설명**|
|**US-001**|예약 프로세스 간소화|사용자는 로그인 후 3번의 클릭 이내에 회의실 예약 과정을 완료할 수 있어야 한다.|
|**US-002**|직관적인 UI|모든 기능은 별도의 매뉴얼 없이도 사용자가 직관적으로 인지하고 사용할 수 있도록 디자인되어야 한다.|

#### 3.2.2. 성능 요구사항 (Performance Requirements)

|   |   |   |
|---|---|---|
|**ID**|**요구사항 명**|**설명**|
|**PERF-001**|검색 응답 시간|회의실 검색 결과는 평균 2초 이내에 화면에 표시되어야 한다.|
|**PERF-002**|동시 접속자 수|시스템은 최소 100명의 동시 접속자를 지연 없이 처리할 수 있어야 한다.|

#### 3.2.3. 보안 요구사항 (Security Requirements)

|   |   |   |
|---|---|---|
|**ID**|**요구사항 명**|**설명**|
|**SEC-001**|권한 분리|관리자 기능은 오직 '관리자' 권한을 가진 사용자만 접근할 수 있어야 한다.|
|**SEC-002**|세션 관리|사용자가 일정 시간(30분) 동안 활동이 없으면 세션이 자동으로 만료되어야 한다.|

### 3.3. 시스템 인터페이스 (System Interfaces)

- **INT-001 (SSO 연동 인터페이스)**: 시스템은 사내 SSO 시스템과 OAuth 2.0 프로토콜을 사용하여 사용자 인증 정보를 교환해야 한다.
- **INT-002 (Google 캘린더 연동 - 선택사항)**: 사용자는 자신의 예약 내역을 개인 Google 캘린더에 동기화하는 옵션을 선택할 수 있어야 한다.

## 4. 검증 (Verification)

각 요구사항이 올바르게 구현되었는지 검증하기 위한 방법을 정의합니다.

|   |   |
|---|---|
|**요구사항 ID**|**검증 방법**|
|FR-AUTH-001|테스트 (Test), 시연 (Demonstration)|
|FR-SEARCH-002|테스트 (Test)|
|US-001|테스트 (Test), 분석 (Analysis)|
|PERF-001|테스트 (Test) - 부하 테스트 도구 사용|
|SEC-001|테스트 (Test), 검사 (Inspection)|