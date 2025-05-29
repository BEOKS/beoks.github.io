[[요구사항 명세서(Software Requirements Specification, SRS)]]를 통해 '무엇을(What)' 만들지 정의했다면, 이제 **'어떻게(How)' 만들 것인지**에 대한 첫 번째 단계를 밟을 차례입니다. 그 첫 단계가 바로 **아키텍처 설계(Architecture Design)**, 다른 말로는 **고수준 설계(High-Level Design, HLD)**입니다.

소프트웨어 아키텍처 설계는 건물을 짓기 전, 전체적인 구조와 외형, 그리고 각 층의 용도와 배치를 결정하는 '청사진'을 그리는 것과 같습니다. 어떤 방에 어떤 색의 벽지를 바를지(상세 설계)를 고민하기 전에, 건물이 몇 층짜리인지, 철골 구조로 지을지, 주차장은 어디에 둘지를 먼저 정하는 것이죠.

---

## 🎯 아키텍처 설계란 무엇인가요?

**[[아키텍처]] 설계**는 소프트웨어 시스템의 **전체적인 구조, 주요 구성 요소(컴포넌트), 그리고 그들 사이의 관계와 상호작용 방식**을 정의하는 과정입니다. 시스템의 뼈대를 세우는 일이며, 이 단계에서 내려진 결정은 프로젝트 전체의 방향성과 품질, 그리고 미래의 확장성에 지대한 영향을 미칩니다.

주요 목표는 [[요구사항 명세서(Software Requirements Specification, SRS)|요구사항 명세서]]에 명시된 기능적, 비기능적 요구사항(성능, 보안, 확장성 등)을 모두 만족시킬 수 있는 **최적의 기술적 밑그림**을 그리는 것입니다.

### 고수준 설계(HLD) vs. [[상세 설계(저수준 설계)]] (LLD)

|   |   |   |
|---|---|---|
|**구분**|**아키텍처 설계 (고수준 설계, HLD)**|**[[상세 설계(저수준 설계)]] (LLD)**|
|**관점**|숲 (전체 시스템)|나무 (개별 컴포넌트)|
|**목표**|시스템의 전체 구조, 기술 스택, 주요 컴포넌트 정의|각 컴포넌트의 내부 로직, 클래스, 함수, 알고리즘 정의|
|**결정사항**|사용할 아키텍처 패턴, 데이터베이스 종류, 서버 구성|클래스 다이어그램, 특정 함수의 로직, 변수명, 데이터 타입|
|**산출물**|아키텍처 다이어그램, 기술 스택 명세, 데이터 모델|클래스/시퀀스 다이어그램, API 명세, 코딩 가이드라인|

---

## 🏛️ 아키텍처 설계의 핵심 결정 사항

이 단계에서는 다음과 같은 중요한 기술적 결정을 내립니다.

1. **아키텍처 패턴(Architectural Pattern) 선택**: 시스템의 구조를 어떤 형태로 가져갈지 결정합니다. 이는 시스템의 특성과 비기능적 요구사항에 따라 신중하게 선택해야 합니다.
    
    - **[[계층형 아키텍처 (Layered Architecture)]]**: 가장 일반적인 구조. 표현(Presentation), 비즈니스(Business), 데이터 접근(Data Access) 계층으로 분리하여 각자의 역할에 집중합니다.
    - **[[마이크로서비스 아키텍처 (Microservices Architecture)]]**: 시스템을 독립적으로 배포 가능한 작은 서비스의 조합으로 구성합니다. 유연성과 확장성이 매우 뛰어나지만 복잡성이 높습니다.
    - **[[이벤트 기반 아키텍처(Event-Driven Architecture)]]**: 시스템 구성 요소들이 '이벤트'를 발생(Publish)하고 구독(Subscribe)하며 상호작용합니다. 비동기 처리에 강점을 가집니다.
    - **모놀리식 아키텍처 (Monolithic Architecture)**: 모든 기능이 하나의 큰 애플리케이션 안에 통합된 구조입니다. 개발 초기에는 단순하지만, 시스템이 커질수록 유지보수가 어려워집니다.
2. **기술 스택(Technology Stack) 정의**: 시스템을 구현할 프로그래밍 언어, 프레임워크, 라이브러리 등을 선정합니다.
    
    - **예시**: Java/Spring Boot, Python/Django, Node.js/Express, React/Vue 등
3. **데이터베이스 설계**: 데이터의 전체적인 구조(Schema)를 설계하고, 어떤 종류의 데이터베이스를 사용할지 결정합니다.
    
    - **예시**: 관계형 데이터베이스(MySQL, PostgreSQL) 또는 NoSQL(MongoDB, Redis)
4. **주요 컴포넌트 및 인터페이스 정의**: 시스템을 구성하는 핵심 모듈이나 서비스는 무엇이며, 이들이 서로 어떻게 통신(e.g., REST API, gRPC, Message Queue)할지를 정의합니다.
    

---

## 🎨 시각화 예시: 3계층 아키텍처

아키텍처 설계의 결과물은 보통 다이어그램으로 시각화됩니다. 가장 보편적인 **계층형 아키텍처(3-Tier Architecture)**를 Mermaid를 통해 표현해 보겠습니다.

```mermaid
graph TD
    subgraph "사용자"
        A[💻<br>웹 브라우저]
    end

    subgraph "웹 서버 (Presentation Layer)"
        B[UI / API Endpoints]
    end

    subgraph "애플리케이션 서버 (Business Layer)"
        C[비즈니스 로직<br>인증, 예약 처리 등]
    end

    subgraph "데이터베이스 서버 (Data Access Layer)"
        D[(🛢️<br>Database)]
    end

    A -- HTTP Request --> B
    B -- 로직 호출 --> C
    C -- 데이터 요청 --> D
    D -- 데이터 반환 --> C
    C -- 결과 반환 --> B
    B -- HTTP Response --> A
```


이 다이어그램은 시스템이 사용자 인터페이스, 비즈니스 로직, 데이터 저장소라는 세 개의 큰 논리적 단위로 나뉘어 있음을 명확히 보여줍니다. 각 계층이 어떤 역할을 하는지, 데이터 흐름이 어떻게 되는지를 한눈에 파악할 수 있죠. 이것이 바로 고수준 설계의 힘입니다.

---

## ✨ 마치며

아키텍처 설계는 단순히 기술을 나열하는 것이 아니라, 프로젝트의 목표와 제약 조건 속에서 **최적의 균형점**을 찾아내는 창의적인 과정입니다. 잘 된 아키텍처 설계는 당장의 개발 효율성을 높일 뿐만 아니라, 미래의 변화에 유연하게 대응하고 지속 가능한 시스템을 만드는 튼튼한 기반이 됩니다.

이제 이 청사진을 바탕으로 각 방의 내부를 꾸미는 [[상세 설계(저수준 설계)]]로 나아갈 준비가 되었습니다.

---

### 📚 참고 자료 (References)

1. **IBM - What is software architecture?**: 소프트웨어 아키텍처의 정의와 중요성에 대해 설명합니다. [https://www.ibm.com/cloud/learn/software-architecture](https://www.google.com/search?q=https://www.ibm.com/cloud/learn/software-architecture)
2. **Microsoft - N-tier architecture style**: 계층형 아키텍처 패턴에 대한 상세한 가이드입니다. [https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/n-tier](https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/n-tier)
3. **Red Hat - What is a microservices architecture?**: 마이크로서비스 아키텍처의 개념과 장단점을 설명합니다. [https://www.redhat.com/en/topics/microservices/what-are-microservices](https://www.redhat.com/en/topics/microservices/what-are-microservices)
4. **GeeksforGeeks - High Level Design (HLD) vs. Low Level Design (LLD)**: 고수준 설계와 저수준 설계의 차이점을 명확하게 비교하고 설명합니다. [https://www.geeksforgeeks.org/high-level-design-vs-low-level-design/](https://www.google.com/search?q=https://www.geeksforgeeks.org/high-level-design-vs-low-level-design/)