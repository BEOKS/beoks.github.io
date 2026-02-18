탐욕 정책(Greedy Policy)은 각 의사결정 단계에서 장기적 결과를 고려하지 않고 현재 시점에서 가장 좋아 보이는 선택을 하는 전략이다. LLM의 맥락에서 이는 [[Chain-of-Thought(CoT)]]를 포함한 추론 방식의 근본적 한계를 설명하는 핵심 개념이다.

## LLM에서의 탐욕 정책

LLM의 토큰 생성은 본질적으로 토큰 수준의 마르코프 결정 과정(MDP)이다. 각 토큰은 이전에 생성된 컨텍스트에만 조건부로 결정되며, 주류 디코딩 방식은 자기회귀적이면서 국소적으로 탐욕적이다. 즉, 단기적 토큰 우도(likelihood)를 최적화한다.

"Why Reasoning Fails to Plan"(arXiv 2601.22311)에 따르면, 이 조합은 국소적 일관성은 유지하지만 전역적 계획은 거의 제공하지 못하여, 종종 중복되거나 표류하는 추론 체인을 만들고 초기 실수를 긴 추론 과정 전체에 전파한다.

## 탐욕 정책의 실패 양상

**되돌릴 수 없는 초기 결정.** 국소 신호에 기반하여 행동을 선택하면, 초기의 결정을 수정하기 어려워져 되돌릴 수 없는 궤적에 갇히게 된다. 이 실패는 계획 지평(planning horizon)이 길어질수록 급격히 악화된다.

**앎과 행함의 격차(Knowing-Doing Gap).** "LLMs are Greedy Agents"(arXiv 2504.16078, 2025) 연구는 LLM이 과제를 해결하는 방법을 "알고" 있으면서도(87%의 정확한 근거 제시) 실제 행동에서는 이를 따르지 못하고 탐욕적 행동을 우선시한다(올바른 근거를 가진 경우에도 64%가 탐욕적 행동)는 것을 발견했다.

## 대안적 접근

탐욕 정책의 한계를 극복하기 위해 Tree-of-Thoughts, Monte Carlo Tree Search(MCTS), 그리고 [[역방향 가치 전파(Backward Value Propagation)]]를 활용하는 Flare 프레임워크 등이 연구되고 있다. 이들은 미래의 결과를 시뮬레이션하여 현재 결정을 수정하는 방식으로 탐욕적 의사결정의 한계를 보완한다.

#### 참고 자료
1. "Why Reasoning Fails to Plan: A Planning-Centric Analysis of Long-Horizon Decision Making in LLM Agents", [arXiv:2601.22311](https://arxiv.org/html/2601.22311)
2. "LLMs are Greedy Agents: Effects of RL", [arXiv:2504.16078](https://arxiv.org/pdf/2504.16078v1)
3. "Chain of Preference Optimization: Improving Chain-of-Thought Reasoning in LLMs", NeurIPS 2024
