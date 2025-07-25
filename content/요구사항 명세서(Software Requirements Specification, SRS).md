"대충 이런 기능 만들어주세요"라는 한 마디로 시작된 프로젝트가 산으로 가는 경험, 다들 한 번쯤은 겪어보셨을 겁니다. SRS는 바로 이런 비극을 막기 위해 존재하는, 프로젝트의 '헌법'과도 같은 문서입니다.

---

## 🤷‍♀️ 요구사항 명세서(SRS)가 도대체 무엇인가요?

**요구사항 명세서(SRS)**는 개발하려는 소프트웨어가 무엇을 해야 하는지, 어떤 기능을 가져야 하는지, 그리고 어떤 제약 조건 하에서 만들어져야 하는지를 상세하고 명확하게 기술한 공식 문서입니다.

이는 단순히 기능 목록을 나열하는 것을 넘어, **개발팀과 고객(또는 기획팀) 사이의 공식적인 약속**입니다. 모든 이해관계자(개발자, 기획자, QA, 디자이너, 고객 등)가 동일한 목표를 바라보고, "우리가 만들고자 하는 것이 이것이 맞다"라고 합의하는 기준점이 됩니다.

잘못 끼운 첫 단추가 옷 전체를 망가뜨리듯, 부실한 SRS는 프로젝트 전체를 혼란에 빠뜨리고 막대한 재작업 비용을 발생시킬 수 있습니다.

---

## ✅ 왜 SRS가 반드시 필요한가요?

- **오해와 혼선의 방지**: "알아서 잘", "적당히 빠르게"와 같은 모호한 표현 대신, 명확한 글로 요구사항을 정의하여 모두가 동일하게 이해하도록 돕습니다.
- **개발의 명확한 방향 제시**: 개발팀은 '무엇을' 만들어야 하는지 명확히 인지하고 개발에 집중할 수 있습니다. 이는 '어떻게' 만들지에 대한 [[설계(Design)]] 단계의 중요한 입력값이 됩니다.
- **검증의 기준**: 잘 작성된 SRS의 각 항목은 테스트의 기준이 됩니다. "요구사항대로 동작하는가?"를 검증함으로써 소프트웨어의 품질을 보장할 수 있습니다.
- **변경 관리의 기초**: 프로젝트 도중 요구사항 변경은 불가피합니다. SRS는 변경의 영향 범위를 분석하고, 추가될 리소스와 일정을 예측하는 객관적인 근거가 됩니다.


```mermaid
graph TD
    subgraph "요구사항 정의 과정"
        A(이해관계자 요구 수집) -- 인터뷰, 설문 등 --> B{요구사항 분석 및 정리};
        B -- "명확화, 구체화" --> C[SRS 초안 작성];
        C -- "피드백 반영" --> D{검토 및 수정};
        D -- "모두 동의?" --> E((최종 SRS 확정));
        D -- "아니요" --> C;
    end
    subgraph "개발 및 검증 과정"
       E -- "개발 지침" --> F[구현];
       E -- "테스트 기준" --> G[테스트];
    end
```


---

## 🏗️ SRS의 핵심 구성 요소

SRS의 표준 양식은 [[ISO_IEC_IEEE 29148]] 표준을 많이 따르지만, 프로젝트의 성격에 따라 유연하게 조정될 수 있습니다. 하지만 일반적으로 다음과 같은 핵심 요소들을 포함합니다.

### 1. 서론 (Introduction)

- **목적 (Purpose)**: 이 문서가 무엇을 위해 작성되었는지, 어떤 시스템에 대한 것인지 기술합니다.
- **범위 (Scope)**: 만들고자 하는 소프트웨어의 이름, 주요 목표, 그리고 반대로 '포함되지 않는' 범위는 무엇인지 명확히 하여 기대 수준을 조절합니다.
- **용어 정의 (Definitions, Acronyms)**: 프로젝트 내에서 사용될 특정 용어나 약어를 정의하여 혼선을 방지합니다.

### 2. 전체 설명 (Overall Description)

- **제품 관점 (Product Perspective)**: 이 소프트웨어가 완전히 새로운 제품인지, 기존 시스템의 일부인지, 다른 시스템과 어떻게 연동되는지를 설명합니다.
- **사용자 특징 (User Characteristics)**: 이 소프트웨어를 사용할 주 사용자는 누구이며, 그들의 기술 수준이나 배경은 어떠한지를 기술합니다.
- **제약 조건 (Constraints)**: 반드시 사용해야 하는 특정 기술 스택, 데이터베이스, 플랫폼이나 법적/제도적 제약사항 등을 명시합니다.
- **가정 및 종속성 (Assumptions and Dependencies)**: 프로젝트가 성공하기 위해 반드시 전제되어야 하는 조건(예: '특정 API가 정상적으로 제공되어야 함')들을 기술합니다.

### 3. 상세 요구사항 (Specific Requirements)

가장 중요하고 상세한 부분으로, 보통 기능적 요구사항과 비기능적 요구사항으로 나뉩니다.

#### 기능적 요구사항(Functional Requirement)

- 시스템이 **무엇을(What) 해야 하는가**에 대한 정의입니다. 사용자가 시스템을 통해 얻고자 하는 핵심 기능들을 구체적으로 설명합니다.
- **예시**:
    - `(FR-001) 사용자는 자신의 아이디와 비밀번호를 사용하여 시스템에 로그인할 수 있어야 한다.`
    - `(FR-002) 사용자는 상품 리스트에서 상품명을 기준으로 상품을 검색할 수 있어야 한다.`
    - `(FR-003) 관리자는 일별 매출 통계를 확인할 수 있어야 한다.`

#### 비기능적 요구사항(Non-functional Requirement)

- 시스템이 **어떻게(How) 동작해야 하는가**에 대한 정의입니다. 기능 외에 시스템이 갖춰야 할 품질 속성을 다룹니다.
- **성능 (Performance)**: `(NFR-001) 상품 검색 결과는 2초 이내에 사용자에게 보여져야 한다.`
- **보안 (Security)**: `(NFR-002) 사용자의 비밀번호는 암호화되어 데이터베이스에 저장되어야 한다.`
- **가용성 (Availability)**: `(NFR-003) 시스템은 99.9%의 시간 동안 정상적으로 운영되어야 한다.`
- **사용성 (Usability)**: `(NFR-004) 모든 기능은 마우스 클릭 3번 이내에 접근 가능해야 한다.`

---

## ✍️ 좋은 SRS를 작성하기 위한 팁

- **명확하고 모호하지 않게 (Unambiguous)**: "빠른 응답" 대신 "2초 이내의 응답"처럼 구체적인 수치를 사용하세요.
- **완전하게 (Complete)**: 모든 요구사항을 빠짐없이 기술하세요.
- **일관성 있게 (Consistent)**: 요구사항 간에 서로 충돌하는 내용이 없어야 합니다.
- **검증 가능하게 (Verifiable)**: 모든 요구사항은 테스트를 통해 확인이 가능해야 합니다.
- **추적 가능하게 (Traceable)**: 각 요구사항에 고유 ID(예: FR-001)를 부여하여 변경과 추적을 용이하게 하세요.

---

## 맺음말

요구사항 명세서(SRS) 작성은 시간과 노력이 많이 드는, 때로는 지루하게 느껴질 수 있는 과정입니다. 하지만 이 단계를 충실히 거치는 것이 결국에는 더 높은 품질의 소프트웨어를 더 적은 비용과 시간으로 만드는 가장 확실한 길입니다.

---

### 📚 참고 자료

1. Visure Solutions - How to Write an SRS Document: [https://visuresolutions.com/ko/요구-사항-관리-추적성-가이드/시스템-요구-사항-문서-작성-방법/](https://www.google.com/search?q=https://visuresolutions.com/ko/%EC%9A%94%EA%B5%AC-%EC%82%AC%ED%95%AD-%EA%B4%80%EB%A6%AC-%EC%B6%94%EC%A0%81%EC%84%B1-%EA%B0%80%EC%9D%B4%EB%93%9C/%EC%8B%9C%EC%8A%A4%ED%85%9C-%EC%9A%94%EA%B5%AC-%EC%82%AC%ED%95%AD-%EB%AC%B8%EC%84%9C-%EC%9E%91%EC%84%B1-%EB%B0%A9%EB%B2%95/)
2. IEEE Std 830-1998 - IEEE Recommended Practice for Software Requirements Specifications
3. velog - [Project] 사용자 요구사항 정의서 (SRS)란?: [https://velog.io/@bagt/%EC%82%AC%EC%9A%A9%EC%9E%90-%EC%9A%94%EA%B5%AC%EC%82%AC%ED%95%AD-%EC%A0%95%EC%9D%98%EC%84%9C-SRS%EB%9E%80](https://velog.io/@bagt/%EC%82%AC%EC%9A%A9%EC%9E%90-%EC%9A%94%EA%B5%AC%EC%82%AC%ED%95%AD-%EC%A0%95%EC%9D%98%EC%84%9C-SRS%EB%9E%80)