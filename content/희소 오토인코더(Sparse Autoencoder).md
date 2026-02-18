희소 오토인코더(Sparse Autoencoder, SAE)는 LLM의 내부 작동을 이해하기 위해 사용되는 기계적 해석 가능성(mechanistic interpretability) 도구이다. Anthropic이 2023~2024년에 걸쳐 개발하고 확장하여 Claude 3 Sonnet 내부에서 수천만 개의 해석 가능한 특징(feature)을 식별하는 데 성공했다.

## 배경: 다의성 문제

LLM의 개별 뉴런은 의미적으로 무관한 여러 맥락에서 활성화되는 다의성(polysemanticity)을 보인다. 이는 신경망이 뉴런 수보다 더 많은 특징을 중첩(superposition)이라는 메커니즘을 통해 표현하기 때문이다. 이로 인해 개별 뉴런만으로는 모델이 내부적으로 무엇을 하는지 이해하기 어렵다.

## 작동 원리

SAE는 희소 사전 학습(sparse dictionary learning) 알고리즘의 일종이다.

1. **인코더**: 모델의 활성화를 학습된 선형 변환과 ReLU 비선형성을 통해 고차원 공간으로 매핑한다. 이 고차원 층의 단위가 "특징"이다.
2. **디코더**: 모델의 활성화를 재구성하려고 시도한다.
3. **희소성 제약**: L1 정규화 페널티가 특징 활성화의 희소성을 유도하여, 주어진 입력에 대해 극소수의 특징만 활성화된다.

훈련이 완료되면, SAE는 모델의 활성화를 "특징 방향"(디코더 가중치)의 선형 조합으로 근사 분해한다. 어떤 토큰이든 소수의 활성 특징으로 "설명"된다.

## Scaling Monosemanticity (Templeton et al., 2024)

Anthropic의 "Towards Monosemanticity"(2023)가 소규모 1층 트랜스포머에서 SAE의 가능성을 입증한 후, "Scaling Monosemanticity"(2024)에서 이를 Claude 3 Sonnet에 성공적으로 확장했다. 주요 발견은 다음과 같다:

- **수천만 개의 특징 발견**: "골든 게이트 브리지", "코드 버그" 같은 구체적 개념부터 추상적 개념까지 다양한 특징 식별
- **다국어·다중모달 특징**: 발견된 특징이 매우 추상적이어서 여러 언어와 모달리티에 걸쳐 일반화
- **안전 관련 특징**: 기만, 아첨(sycophancy), 편향, 위험한 콘텐츠와 관련된 특징 관찰
- **특징 조향(Feature Steering)**: "골든 게이트 브리지" 특징의 활성도를 증폭시키면, Claude가 모든 대화를 골든 게이트 브리지와 연결짓는 행동을 보임. 이는 특징이 해당 개념을 인과적으로 인코딩하고 있다는 증거

## 한계

SAE는 모델의 단일 잔여 층(residual layer)에만 적용되며, 모델 전체의 층 간 상호작용은 포착하지 못한다. 또한 일부 비평가들은 특징이 높은 활성화 수준에서는 특정 개념과 대응하지만, 중간 수준의 활성화에서는 해당 개념과 무관한 경우가 많다고 지적했다.

#### 참고 자료
1. "Towards Monosemanticity: Decomposing Language Models With Dictionary Learning", Anthropic (2023), [Link](https://transformer-circuits.pub/2023/monosemantic-features)
2. Templeton et al. (2024), "Scaling Monosemanticity: Extracting Interpretable Features from Claude 3 Sonnet", [Link](https://transformer-circuits.pub/2024/scaling-monosemanticity/)
