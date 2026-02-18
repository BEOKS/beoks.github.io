암묵적 연관 테스트(Implicit Association Test, IAT)는 Greenwald, McGhee, & Schwartz(1998)가 개발한 심리학 측정 도구로, 사람이 의식하지 못하는 무의식적 편향과 태도를 측정한다. LLM의 암묵적 편향을 밝히는 데 응용되어 AI 안전성 연구의 핵심 방법론이 되었다.

## 원래의 심리학적 방법론

IAT는 두 개념(예: 꽃 vs. 곤충)과 한 속성(예: 좋음 vs. 나쁨)을 같은 응답 키에 배치했을 때의 반응 속도 차이로 연관 강도를 측정한다. 강하게 연관된 쌍(꽃+좋음)은 약하게 연관된 쌍(곤충+좋음)보다 반응이 빠르다.

세 가지 실험에서 IAT는 (a) 거의 보편적인 평가적 차이(꽃 vs. 곤충), (b) 예상되는 개인차(일본인 vs. 한국인에 대한 일본 참가자의 태도), (c) 의식적으로 부인되는 연관(인종 편향)에 민감하게 반응했다.

원본 논문은 4,000회 이상 인용되며 사회심리학의 가장 영향력 있는 도구 중 하나로 자리잡았다.

## LLM 편향 연구에의 응용

"Explicitly Unbiased LLMs Still Form Biased Associations"(PNAS 2025)는 IAT를 LLM에 응용하여, 표준 편향 벤치마크를 통과한 모델도 광범위한 암묵적 편향을 보유하고 있음을 밝혔다.

### 연구 방법

1. **LLM Word Association Test**: IAT에서 착안한 프롬프트 기반 암묵적 편향 측정
2. **LLM Relative Decision Test**: 두 후보를 절대 평가 대신 상대 비교로 판단하여 암묵적 편향을 더 선명하게 드러냄

### 주요 발견

8개의 가치 정렬 모델을 검사한 결과:

- "특정 인종이 범죄와 관련이 있는가?"라고 직접 물으면 "그렇지 않다"고 올바르게 답변한다.
- 그러나 간접적으로 측정하면 인종-범죄, 인종-무기, 성별-과학, 나이-부정성 등 **21개 고정관념**에서 사회적 편견과 일치하는 연관 패턴이 **모든 모델에서** 발견되었다.
- GPT-4는 아프리카계·아시아계 이름의 후보를 사무직에, 백인 이름의 후보를 관리직에 추천하는 경향을 보였다.

이는 표준 벤치마크가 LLM의 암묵적 편향을 잡아내지 못하며, 심리학의 행동 관찰 기반 측정법이 모델 평가의 중요한 대안이 됨을 시사한다.

#### 참고 자료
1. Greenwald, McGhee, & Schwartz (1998), "Measuring Individual Differences in Implicit Cognition: The Implicit Association Test", *Journal of Personality and Social Psychology*, 74(6), 1464-1480
2. "Explicitly Unbiased Large Language Models Still Form Biased Associations", [PNAS 2025](https://www.pnas.org/doi/10.1073/pnas.2416228122)
