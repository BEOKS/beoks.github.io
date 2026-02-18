구성적 일반화(Compositional Generalization)란 알려진 구성 요소들을 새로운 방식으로 조합해 한 번도 보지 못한 복합 과제를 처리하는 능력이다. 인간 언어와 사고의 핵심 특성이며, LLM이 진정한 이해에 도달하기 위한 필수 조건으로 여겨진다.

## LLM의 구성 능력 평가

"Do Large Language Models Have Compositional Ability?"(arXiv 2024)는 LLM의 구성적 일반화 능력을 체계적으로 평가했다.

- **단순한 합성 과제**(서로 다른 입력 부분에 독립적인 규칙 적용): LLM이 일정한 구성적 능력을 보이며, 모델 크기를 키우면 향상된다.
- **복잡한 다단계 추론 과제**: 성능이 떨어지며, **모델 크기를 키워도 개선이 없다.** 이것이 핵심적인 한계이다.

예를 들어 LLM은 "X의 수도는?"과 "Y국의 통화는?"이라는 각각의 질문에는 정확히 답할 수 있다. 그러나 "X의 수도에서 사용되는 통화는?"처럼 두 지식을 결합해야 하는 질문에서는 성능이 급격히 떨어진다.

## 구성을 통한 OOD 일반화

Song, Xu, & Zhong(2025)의 "Out-of-Distribution Generalization via Composition"(PNAS)은 트랜스포머가 훈련 분포를 벗어난(OOD) 새 과제를 어떻게 처리하는지 메커니즘 수준에서 분석했다.

### 핵심 발견

- **OOD 일반화와 구성은 서로 연결되어 있다.** 트랜스포머의 두 자기 어텐션 레이어를 합성(composition)함으로써 OOD 일반화가 달성된다.
- **"공통 다리 표현 가설(Common Bridge Representation Hypothesis)"**: 임베딩 공간의 공유된 잠재 부분 공간이 초기 레이어와 후기 레이어를 연결하는 다리 역할을 한다.
- 이 부분 공간 정렬이 갑작스럽게 나타나는 현상은 LLM의 능력 창발(emergent abilities)과 맥을 같이 한다.

### 함의

테스트 데이터에 구성적 구조가 있으면 Few-shot이나 Zero-shot 일반화가 가능하지만, 구성적 구조가 없는 진정한 새로운 과제에서는 일반화가 실패한다. [[Chain-of-Thought(CoT)]] 프롬프팅의 효과도 과제의 구성적 구조를 명시적으로 활용하기 때문이다.

#### 참고 자료
1. "Do Large Language Models Have Compositional Ability?", [arXiv:2407.15720](https://arxiv.org/abs/2407.15720)
2. Song, Xu, & Zhong (2025), "Out-of-Distribution Generalization via Composition", [PNAS](https://www.pnas.org/doi/10.1073/pnas.2417182122)
