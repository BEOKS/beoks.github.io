기호 접지 문제(Symbol Grounding Problem)는 컴퓨터 시스템의 기호(symbol)가 어떻게 실세계의 대상과 연결되어 의미를 가질 수 있는지에 대한 근본적 질문이다. Stevan Harnad(1990)가 처음 명명하고 정식화했으며, LLM 시대에 다시 핵심적인 쟁점으로 부상했다.

## 핵심 문제

전통적 AI 시스템에서 기호는 다른 기호에 의해서만 정의된다. 사전에서 모르는 단어의 뜻을 찾으면 또 다른 단어들로 설명되어 있고, 그 단어들의 뜻을 다시 찾으면 또 다른 단어들이 나오는 순환적 구조와 같다. Harnad는 이 순환에서 벗어나 기호가 실세계 경험에 "접지(grounding)"되어야 진정한 의미를 가질 수 있다고 주장했다.

ChatGPT가 비에 대한 에세이를 완벽하게 쓸 수 있지만, 실제로 비를 경험한 적은 없다. 기계에게 단어는 맥락적 경험 없이 여전히 기호에 불과하다.

## 벡터 접지 문제

Mollo & Millière(2025)는 "The Vector Grounding Problem"에서 고전적 기호 접지 문제를 LLM의 맥락으로 재정립했다. LLM은 이산적 기호 대신 연속적 벡터를 사용하지만, 이 차이가 접지 문제를 해결하지는 못한다. LLM은 "기호의 회전목마" 대신 "숫자의 회전목마"에 갇혀 있을 뿐이며, 벡터 성분들 역시 세계와 연결되어 있지 않고 다른 기호들과 연결되어 있다.

다만, 같은 논문에서 저자들은 LLM이 참조적 접지(referential grounding)의 두 조건을 충족할 수 있다고 주장하기도 한다: (1) 세계와의 적절한 인과-정보적 관계, (2) 이 정보를 전달하는 기능을 부여한 선택의 역사. 이는 다중감각이나 신체화 없이도 가능하다는 입장이다.

## 멀티모달 LLM의 시도와 한계

비전-언어 모델(VLM)은 언어를 시각 등 다른 모달리티와 연결하여 접지 문제를 해결하려 한다. 그러나 "Do Multimodal Large Language Models and Humans Ground Language Similarly?"(MIT Press, Computational Linguistics 2024)의 실험에서, 멀티모달 LLM은 일부 암묵적 감각운동 특징에는 민감하지만 다른 것들에는 민감하지 않으며, 인간의 접지 효과를 완전히 설명하지 못했다.

Frontiers in Systems Neuroscience(2025)는 다중감각과 신체화가 접지 문제의 해결에 필요조건도 충분조건도 아닐 수 있다고 지적하며, 언어가 먼저 별도로 학습된 후 다른 모달리티와 나중에 연결되는 현재의 구조적 한계를 강조했다.

## 함의 이해의 실패

기호 접지의 부재는 LLM이 단어의 물리적·감각적 함의(implication)를 이해하지 못하는 문제로 이어진다. "뜨거운"이라는 단어를 처리할 때, 인간은 화상의 위험, 손을 뗄 수 없을 때의 공포, 뜨거운 물체의 열전도 같은 풍부한 함의를 즉각적으로 활성화한다. LLM에게 "뜨거운"은 "차가운"의 반의어이자 "위험한", "뜨겁다"와 자주 공기(co-occur)하는 통계적 이웃일 뿐이다.

### 감각운동 표상의 근본적 결핍

"Large language models without grounding recover non-sensorimotor but not sensorimotor features of human concepts"(Nature Human Behaviour 2025)는 약 4,442개 어휘 개념에 대해 인간과 LLM(GPT-4, PaLM, Gemini 포함)의 내부 표상을 비교했다. 핵심 발견은 다음과 같다:

- LLM은 추상적·비감각운동적 영역(예: "민주주의", "우정")에서는 인간과 유사한 표상을 보였다.
- 그러나 감각 영역으로 갈수록 유사도가 체계적으로 감소했고, **운동(motor) 차원에서는 유사도가 거의 0에 수렴**했다.
- 시각 학습이 추가된 멀티모달 모델은 시각 관련 차원에서 일부 개선을 보였으나, 감각운동 차원의 근본적 결핍은 해결하지 못했다.

연구진은 이를 "대형 언어 모델은 장미의 향기를 맡거나, 꽃잎을 만지거나, 들판을 걸을 수 없다. 이러한 경험 없이는 꽃이 무엇인지 그 풍부함 속에서 표현할 수 없다"고 요약했다.

### 물리적 함의 추론의 실패

이 표상 격차는 실용적 과제에서 구체적인 실패로 나타난다.

"MacGyver: Are Large Language Models Creative Problem Solvers?"(NAACL 2024)는 1,600개 이상의 실세계 문제에서 LLM의 창의적 문제 해결 능력을 평가했다. GPT-4조차 효율적 해결책을 제시한 비율은 **18.9%**에 불과했고, 제안된 해결책의 **37.5%는 물리적으로 불가능**했다. LLM은 도구의 물리적 속성(질량, 강도, 온도)과 그로 인한 행동 가능성(어포던스)을 연결하지 못했다.

"Exploring Failure Cases in Multimodal Reasoning About Physical Dynamics"(AAAI 2024)에서는 모델이 개별 물체의 속성("원기둥은 둥글다", "유리는 깨지기 쉽다")은 알고 있으면서도, 이를 조합하여 다단계 물리적 상호작용을 추론하는 데는 체계적으로 실패했다. 원자적 지식은 존재하지만, 이를 물리적으로 일관된 추론으로 구성하는 능력이 결여된 것이다.

#### 참고 자료
1. Harnad, S. (1990), "The Symbol Grounding Problem", *Physica D*, 42, 335-346
2. Mollo & Millière (2025), "The Vector Grounding Problem", [arXiv:2304.01481](https://arxiv.org/html/2304.01481v2)
3. "Do Multimodal Large Language Models and Humans Ground Language Similarly?", [MIT Press](https://direct.mit.edu/coli/article/50/4/1415/123786)
4. "Will multimodal large language models ever achieve deep understanding of the world?", [Frontiers 2025](https://www.frontiersin.org/journals/systems-neuroscience/articles/10.3389/fnsys.2025.1683133/full)
5. Xu et al. (2025), "Large language models without grounding recover non-sensorimotor but not sensorimotor features of human concepts", [Nature Human Behaviour](https://www.nature.com/articles/s41562-025-02203-8)
6. Tian et al. (2024), "MacGyver: Are Large Language Models Creative Problem Solvers?", [NAACL 2024](https://aclanthology.org/2024.naacl-long.297/)
7. Ghaffari & Krishnaswamy (2024), "Exploring Failure Cases in Multimodal Reasoning About Physical Dynamics", [arXiv:2402.15654](https://arxiv.org/abs/2402.15654)
