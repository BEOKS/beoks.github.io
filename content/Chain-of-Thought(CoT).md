Chain-of-Thought(CoT)는 Wei et al.(2022)이 제안한 프롬프팅 기법으로, LLM에게 "단계별로 생각하라(Let's think step by step)"고 지시하여 중간 추론 과정을 명시적으로 생성하게 하는 방법이다.

## 작동 원리

일반적인 프롬프팅에서 LLM은 질문을 받으면 바로 답을 생성한다. CoT는 이와 달리 모델이 암묵적 확률 분포 계산을 명시적인 논리 체인으로 변환하도록 유도한다. 각 단계는 이전 단계를 조건으로 다음 토큰을 생성하는 자기회귀적(autoregressive) 과정이며, 이를 통해 복잡한 문제를 더 작은 하위 문제로 분해하는 효과를 얻는다.

예를 들어, "로저는 테니스 공 5개를 가지고 있다. 2캔을 더 샀고, 각 캔에는 3개가 들어있다. 총 몇 개인가?"라는 문제에서 CoT는 다음과 같이 작동한다:
- 1단계: 로저는 처음에 5개를 가지고 있다
- 2단계: 2캔 × 3개 = 6개를 추가로 구매했다
- 3단계: 5 + 6 = 11개

## 한계

CoT는 유용하지만 근본적 한계가 존재한다.

**눈덩이 효과(Snowball Effect).** 다단계 추론에서 초기 단계의 오류가 후속 단계로 전파되며 누적된다. Frontiers in AI(2025) 연구에 따르면 긴 추론 체인에서 특정 유형의 환각이 시간이 지남에 따라 복합적으로 증가한다.

**환각 탐지 방해.** arXiv:2506.17088 연구는 CoT가 환각 빈도를 줄이는 데는 도움이 되지만, 동시에 환각을 탐지하는 데 사용되는 핵심 신호를 가려버린다는 트레이드오프를 발견했다.

**[[탐욕 정책(Greedy Policy)]]으로서의 한계.** CoT는 각 단계에서 국소적으로 가장 그럴듯한 다음 단계를 선택하는 탐욕적 방식으로 작동한다. 장기적 결과를 고려하여 초기 결정을 수정하는 [[역방향 가치 전파(Backward Value Propagation)]]가 불가능하다.

**모델 크기 의존성.** 자기 반성(self-reflection)을 통한 환각 완화는 70B 파라미터 이상의 대형 모델에서만 효과적이며, 소형 모델에서는 오히려 오류를 증가시킨다.

#### 참고 자료
1. Wei et al. (2022), "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models", NeurIPS 2022
2. "Chain-of-Thought Prompting Obscures Hallucination Cues in Large Language Models", [arXiv:2506.17088](https://arxiv.org/abs/2506.17088)
3. "Why Reasoning Fails to Plan", [arXiv:2601.22311](https://arxiv.org/html/2601.22311)
4. "Survey and analysis of hallucinations in LLMs", [Frontiers in AI 2025](https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2025.1622292/full)
