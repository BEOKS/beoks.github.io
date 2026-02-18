안전성 정렬(Safety Alignment)이란 대형 언어 모델(LLM)이 인간의 의도와 가치에 부합하여 동작하도록 훈련하는 기법의 총칭이다. 단순히 언어 능력을 높이는 사전 학습(pre-training)과 달리, 정렬 과정은 모델이 유용하고, 무해하며, 정직하게(Helpful, Harmless, Honest) 반응하도록 행동 방식 자체를 교정한다.

## 핵심 기법

### RLHF (Reinforcement Learning from Human Feedback)

Ouyang et al.(2022)이 InstructGPT에서 확립한 3단계 파이프라인으로, 현재 산업 표준이다.

1. **지도 미세조정(SFT)**: 인간이 직접 작성한 고품질 예시 데이터로 모델을 미세조정한다.
2. **보상 모델 훈련**: 인간 평가자가 모델 출력 쌍에 선호도를 매기면, 이를 학습한 보상 모델(Reward Model)이 만들어진다.
3. **강화 학습 최적화**: PPO(Proximal Policy Optimization)로 보상 모델의 점수를 극대화하도록 언어 모델을 최적화한다.

가장 충격적인 결과는 13억 파라미터의 InstructGPT가 1,750억 파라미터의 GPT-3보다 인간 평가에서 선호되었다는 점이다. 모델 규모가 아닌 정렬 품질이 실용적 성능을 결정할 수 있음을 보여준다.

### Constitutional AI (헌법적 AI)

Anthropic이 개발한 방법으로, "AI는 사람을 속여서는 안 된다"와 같은 명시적 원칙들의 집합(헌법)을 만들고, AI 스스로 이 원칙에 따라 자신의 출력을 비판하고 수정한다. 이를 RLAIF(Reinforcement Learning from AI Feedback)라고 부르며, 인간 어노테이터 의존도를 획기적으로 줄인다.

### DPO (Direct Preference Optimization)

Rafailov et al.(2023)이 제안한 기법으로, 최적의 RLHF 정책이 닫힌 형식(closed form)으로 유도될 수 있다는 수학적 통찰에 기반한다. 별도의 보상 모델 없이 선호 데이터에서 직접 언어 모델을 최적화하여, 복잡한 강화 학습 파이프라인을 제거한다.

## 근본적 취약점: 얕은 정렬

Qi et al.(2024)의 "Safety Alignment Should Be Made More Than Just a Few Tokens Deep"은 현재 안전성 정렬의 가장 심각한 구조적 문제를 체계적으로 분석했다. 핵심 발견은 다음과 같다.

현재 LLM의 안전성은 출력의 **첫 몇 개 토큰에만 집중**되어 있다. 정렬된 모델과 정렬되지 않은 기반 모델의 차이는 "죄송합니다, 저는 그 요청을 도와드릴 수 없습니다"라는 서두를 생성하느냐 마느냐에 가깝다. 일단 첫 토큰이 거부가 아닌 방향으로 유도되면, 이후 생성은 비정렬 모델과 사실상 동일하다.

이 구조적 취약성은 다음과 같은 공격들을 설명한다:

- **Adversarial Suffix Attack**: 프롬프트 뒤에 특수 문자열을 붙여 초기 토큰 생성을 유도
- **Prefilling Attack**: API에서 모델의 응답 서두를 직접 채워 안전 거부 응답을 건너뜀
- **Fine-tuning Attack**: 소수의 해로운 데이터로 미세조정하면 정렬이 무너짐
- **Decoding Parameter Attack**: 온도(temperature)나 샘플링 방식 변경만으로 안전 동작 우회

## 정렬 세금(Alignment Tax)

RLHF는 특정 NLP 벤치마크 성능을 저하시키는 부작용이 있다. 안전성과 유용성 사이의 트레이드오프가 존재하며, 이를 "정렬 세금"이라 부른다.

#### 참고 자료
1. Ouyang et al. (2022), "Training Language Models to Follow Instructions with Human Feedback", NeurIPS 2022, [arXiv:2203.02155](https://arxiv.org/abs/2203.02155)
2. Bai et al. (2022), "Constitutional AI: Harmlessness from AI Feedback", [arXiv:2212.08073](https://arxiv.org/abs/2212.08073)
3. Rafailov et al. (2023), "Direct Preference Optimization", [arXiv:2305.18290](https://arxiv.org/abs/2305.18290)
4. Qi et al. (2024), "Safety Alignment Should Be Made More Than Just a Few Tokens Deep", [arXiv:2406.05946](https://arxiv.org/abs/2406.05946)
