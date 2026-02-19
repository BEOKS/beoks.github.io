AI 에이전트(AI Agent)는 환경을 인식하고, 자율적으로 판단하여 행동하는 시스템을 의미합니다. 단순히 입력에 대해 출력을 반환하는 프로그램과 달리, 에이전트는 목표 지향적이며 시간에 걸쳐 지속적으로 환경과 상호작용합니다. 이 개념은 인공지능의 가장 근본적인 구성 단위이자, 현대 멀티 에이전트 시스템과 지능형 위임 프레임워크의 출발점입니다.

---

## 에이전트의 학술적 정의

에이전트라는 용어는 분야와 맥락에 따라 다양하게 정의되어 왔습니다. 아래는 이 분야에서 가장 높은 인용 수를 기록한 논문들의 정의입니다.

### Russell & Norvig의 정의

인공지능 분야의 표준 교과서로 전 세계 1,500개 이상의 대학에서 사용되는 Artificial Intelligence: A Modern Approach에서는 에이전트를 다음과 같이 정의합니다:

> "An agent is anything that can be viewed as perceiving its environment through sensors and acting upon that environment through actuators."
> (에이전트란 센서를 통해 환경을 인식하고, 작동기를 통해 환경에 작용하는 모든 것이다.) [^1]

이 정의는 의도적으로 넓게 설정되어 있습니다. 소프트웨어 프로그램, 로봇, 심지어 인간까지 이 정의에 포함될 수 있습니다. 핵심은 인식(perception)과 행동(action)의 순환 구조입니다. 나아가 합리적 에이전트(rational agent)를 "자신의 지식과 과거 경험에 기반하여 가능한 최선의 결과를 달성하려는 에이전트"로 정의하며, 인공지능 분야 전체를 "합리적 에이전트의 연구와 설계"로 프레이밍합니다.

에이전트의 내부 구조는 에이전트 함수(agent function)로 모델링됩니다. 이는 지각 시퀀스(percept sequence)를 행동(action)으로 매핑하는 함수이며, 에이전트 프로그램(agent program)이 이를 구현합니다.

### Wooldridge & Jennings의 정의

Knowledge Engineering Review에 게재된 Intelligent Agents: Theory and Practice는 에이전트 연구 분야에서 가장 많이 인용된 논문 중 하나입니다. 이 논문은 에이전트의 속성을 약한 개념(weak notion)과 강한 개념(strong notion)으로 구분합니다. [^2]

약한 개념의 에이전트(Weak Notion of Agency)는 다음 네 가지 속성을 갖춘 하드웨어 또는 소프트웨어 기반 시스템입니다:

| 속성 | 설명 |
|------|------|
| 자율성 (Autonomy) | 인간이나 다른 존재의 직접적 개입 없이 작동하며, 자신의 행동과 내부 상태에 대한 일정한 통제력을 가짐 |
| 사회적 능력 (Social Ability) | 에이전트 통신 언어를 통해 다른 에이전트(또는 인간)와 상호작용 |
| 반응성 (Reactivity) | 환경을 인식하고, 환경의 변화에 적시에 대응 |
| 능동성 (Pro-activeness) | 단순한 반응을 넘어 목표 지향적 행동을 주도적으로 취함 |

강한 개념의 에이전트(Stronger Notion of Agency)는 위 속성에 더해, 인간적 개념으로 에이전트를 기술하거나 구현하는 것을 포함합니다. 지식, 믿음, 의도, 의무 같은 정신적 속성(mentalistic attributes)이나, 감정적 속성을 에이전트에 부여하는 BDI(Belief-Desire-Intention) 모델이 대표적입니다.

### Franklin & Graesser의 정의

Is It an Agent, or Just a Program?: A Taxonomy for Autonomous Agents에서는 에이전트와 단순 프로그램의 경계를 명확히 하기 위해 다음과 같이 정의합니다: [^3]

> "An autonomous agent is a system situated within and a part of an environment that senses that environment and acts on it, over time, in pursuit of its own agenda and so as to effect what it senses in the future."
> (자율 에이전트란 환경 안에 위치하여 그 일부를 이루는 시스템으로, 환경을 감지하고 그 위에서 행동하며, 시간에 걸쳐 자신의 의제를 추구하고 미래에 감지할 것에 영향을 미치는 시스템이다.)

이 정의의 핵심은 세 가지 차별점입니다:
1. 환경 내 위치성(situated): 에이전트는 환경과 분리된 존재가 아니라 환경의 일부
2. 시간적 지속성(over time): 일회성 실행이 아닌 지속적 작동
3. 자기 의제(own agenda): 외부의 명시적 지시가 아닌 내재화된 목표 추구

이 논문은 또한 반응성, 자율성, 목표 지향성, 지속적 작동, 의사소통 능력, 학습, 이동성, 유연성 등의 속성을 기준으로 자율 에이전트의 분류 체계(taxonomy)를 제시합니다.

### Maes의 정의

MIT Media Lab의 Pattie Maes는 Artificial Life Meets Entertainment: Lifelike Autonomous Agents에서 다음과 같이 정의합니다: [^4]

> "Autonomous agents are computational systems that inhabit some complex dynamic environment, sense and act autonomously in this environment, and by doing so realize a set of goals or tasks for which they are designed."
> (자율 에이전트란 복잡하고 동적인 환경에 거주하며, 그 환경에서 자율적으로 감지하고 행동하여, 설계된 목표나 작업을 실현하는 계산 시스템이다.)

Maes의 정의가 다른 정의와 구별되는 점은 환경의 복잡성과 동적성을 명시적으로 요구한다는 것입니다. 단순하고 정적인 환경에서 작동하는 시스템은 이 정의에서 에이전트로 분류되지 않습니다.

---

## 정의들의 공통 요소

위 정의들을 종합하면, 에이전트의 본질적 속성으로 다음이 도출됩니다:

| 공통 요소 | 설명 |
|-----------|------|
| 환경 인식 (Perception) | 센서, API, 데이터 스트림 등을 통해 환경의 상태를 감지 |
| 자율적 행동 (Autonomous Action) | 외부의 직접적 제어 없이 스스로 판단하고 행동 |
| 목표 지향성 (Goal-directedness) | 사전에 정의된 목표나 내재화된 의제를 추구 |
| 환경과의 상호작용 (Interaction) | 행동의 결과가 환경을 변화시키고, 그 변화를 다시 인식 |
| 시간적 지속성 (Temporal Continuity) | 일회성이 아닌, 시간에 걸친 지속적 작동 |

---

## 에이전트와 단순 프로그램의 차이

Franklin & Graesser의 분류 기준을 빌리면, 에이전트와 일반 프로그램의 차이는 다음과 같습니다:

| 특성 | 일반 프로그램 | 에이전트 |
|------|-------------|---------|
| 실행 방식 | 호출 시 실행, 결과 반환 후 종료 | 지속적으로 작동하며 환경을 감시 |
| 환경 인식 | 명시적 입력만 처리 | 환경 변화를 능동적으로 감지 |
| 자율성 | 호출자의 지시에 따라 동작 | 자체 판단에 의한 행동 결정 |
| 적응성 | 동일 입력에 동일 출력 | 경험과 환경 변화에 따라 행동 조정 |
| 목표 | 함수의 사양을 충족 | 내재화된 목표를 능동적으로 추구 |

---

## 현대 AI 에이전트: LLM 기반 에이전트

최근의 대규모 언어 모델(LLM) 기반 에이전트는 위의 고전적 정의를 새로운 차원으로 확장합니다. LLM 기반 에이전트는:

- 자연어를 통해 환경을 인식하고 행동을 생성
- Memory, Planning, Reasoning, Reflection, Tool Use를 통합하는 제어 흐름을 실행
- API 호출, 코드 실행, 웹 검색 등 다양한 도구를 활용하여 환경에 작용
- 대화 맥락을 유지하며 시간에 걸쳐 지속적으로 작동

그러나 현재의 LLM 기반 에이전트에는 여전히 도전 과제가 존재합니다. Planning이 종종 취약하여 미묘한 실패를 초래하고, 대규모 도구 선택이 어려우며, 장기 memory와 지속적 학습은 미해결 연구 문제로 남아 있습니다.

---

## 멀티 에이전트 시스템으로의 확장

단일 에이전트의 한계를 극복하기 위해, 여러 에이전트가 협력하는 멀티 에이전트 시스템(Multi-Agent System, MAS)이 연구되어 왔습니다. Jennings, Sycara & Wooldridge의 연구에 따르면, MAS의 핵심 과제는 에이전트 간의 조율(coordination), 협상(negotiation), 그리고 작업 분배(task allocation)입니다. [^5]

멀티 에이전트 시스템에서 에이전트 간의 작업 위임이 정교해질수록, 단순한 [[휴리스틱(Heuristic)|휴리스틱]] 기반 분배를 넘어 동적 역량 평가, 신뢰 기반 매칭, 검증 가능한 작업 완료 등 보다 지능적인 메커니즘이 요구됩니다. 이는 [[지능형 AI 위임(Intelligent AI Delegation)|지능형 위임 프레임워크]]가 다루는 핵심 주제입니다.

---

[^1]: Stuart J. Russell, Peter Norvig. *Artificial Intelligence: A Modern Approach*. Prentice Hall, 1995 (1st ed.), 2020 (4th ed.). Chapter 2. Google Scholar 인용 수 약 59,000회 이상.

[^2]: Michael Wooldridge, Nicholas R. Jennings. "Intelligent Agents: Theory and Practice." *The Knowledge Engineering Review*, Vol. 10, No. 2, pp. 115-152, 1995. 해당 저널에서 역대 가장 많이 인용된 논문.

[^3]: Stan Franklin, Art Graesser. "Is It an Agent, or Just a Program?: A Taxonomy for Autonomous Agents." In *Intelligent Agents III: Agent Theories, Architectures, and Languages*, Lecture Notes in Computer Science, Vol. 1193, Springer, pp. 21-35, 1997. Semantic Scholar 인용 수 약 2,881회.

[^4]: Pattie Maes. "Artificial Life Meets Entertainment: Lifelike Autonomous Agents." *Communications of the ACM*, Vol. 38, No. 11, pp. 108-114, 1995.

[^5]: Nicholas R. Jennings, Katia Sycara, Michael Wooldridge. "A Roadmap of Agent Research and Development." *Autonomous Agents and Multi-Agent Systems*, Vol. 1, No. 1, pp. 7-38, 1998. Semantic Scholar 인용 수 약 2,341회.
