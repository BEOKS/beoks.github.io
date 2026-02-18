역방향 가치 전파(Backward Value Propagation)는 미래의 결과를 바탕으로 현재의 결정을 평가하고 수정하는 계획 메커니즘이다. 현재 LLM의 [[Chain-of-Thought(CoT)]] 추론에는 이 능력이 부재하며, 이것이 LLM이 장기 계획(long-horizon planning)에 실패하는 핵심 원인 중 하나이다.

## 개념

역방향 가치 전파의 핵심 아이디어는 역방향 귀납법(backward induction)에서 유래한다. 의사결정 과정의 최종 단계에서 시작하여 각 선행 노드에서의 최적 결정을 재귀적으로 결정하는 방식이다. 이를 통해 전역적으로 지수적일 수 있는 의사결정 공간을 관리 가능한 국소 계산으로 분해할 수 있다.

예를 들어 체스에서, 단순히 "지금 가장 좋아 보이는 수"를 두는 것이 [[탐욕 정책(Greedy Policy)]]이라면, "이 수를 두면 3수 후에 어떤 상황이 되는가?"를 계산하여 현재 수를 결정하는 것이 역방향 가치 전파이다.

## LLM에 부재한 이유

"Why Reasoning Fails to Plan"(arXiv 2601.22311)에 따르면, LLM 기반 에이전트의 장기적 실패는 추론(reasoning)과 계획(planning) 사이의 근본적 격차에서 비롯된다. 일관된 계획에는 세 가지 최소 메커니즘이 필요하다:

1. **명시적 선행 탐색(explicit lookahead)**: 미래 궤적을 시뮬레이션
2. **역방향 가치 전파**: 궤적 수준의 결과를 초기 결정에 전파
3. **제한적 결정(limited commitment)**: 후퇴 가능한 계획 수립

기존 LLM 추론 패러다임은 이 중 최소 하나를 위반한다. CoT와 빔 서치는 명시적 미래 평가와 가치 전파가 없고, Reflexion과 ReAct는 명시적 선행 탐색이 없으며, 강화학습은 온라인 수정이 불가능하다.

## Flare 프레임워크

Flare(Future-aware Lookahead with Reward Estimation)는 Monte Carlo Tree Search(MCTS)를 사용하여 역방향 가치 전파를 구현한 프레임워크이다. 핵심 특징은 다음과 같다:

- 궤적 시뮬레이션을 통해 행동을 장기적 결과로 평가
- 궤적 수준의 피드백을 역방향으로 전파하여 초기 결정을 안내
- 후퇴 지평 방식(receding-horizon scheme)으로 다음 행동에만 결정을 내리고 매 전환 후 재계획

실험 결과, 미래를 인식하는 계획이 장기적 실패를 일관되게 완화하며, 작은 모델이 추론 기반 정책을 사용하는 큰 모델보다 더 나은 성능을 보이는 경우도 있었다.

#### 참고 자료
1. "Why Reasoning Fails to Plan: A Planning-Centric Analysis of Long-Horizon Decision Making in LLM Agents", [arXiv:2601.22311](https://arxiv.org/html/2601.22311)
2. "Tree of Thoughts: Deliberate Problem Solving with Large Language Models", NeurIPS 2023, [Paper](https://proceedings.neurips.cc/paper_files/paper/2023/file/271db9922b8d1f4dd7aaef84ed5ac703-Paper-Conference.pdf)
