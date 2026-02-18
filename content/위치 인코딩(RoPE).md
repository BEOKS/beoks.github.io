RoPE(Rotary Position Embedding, 회전 위치 인코딩)는 트랜스포머 모델에서 토큰의 위치 정보를 인코딩하는 방법론으로, Su et al.(2021)이 제안했다. LLaMA, PaLM, GPT-NeoX 등 대부분의 최신 대형 언어 모델이 채택하고 있다.

## 작동 원리

RoPE는 쿼리(Query)와 키(Key) 벡터를 위치에 따라 회전시켜 상대적 위치 관계를 표현한다. 임베딩 차원을 쌍(pair)으로 묶어 각 쌍을 2D 평면에서 회전시키며, 위치 m에서의 회전각은 `mθ_d`이다. 여기서 θ_d는 차원 d에 따라 결정되는 주파수다.

```
θ_d = base^(-2d/D)     (base = 10,000, D = 전체 차원 수)
```

쿼리와 키의 내적을 계산하면, 결과값이 두 토큰의 상대 위치 차이(m - n)에만 의존하게 된다. 이것이 상대적 위치 인코딩의 핵심이다.

- **고주파 차원**: 짧은 주기로, 인접 토큰 간의 지역적 관계를 포착한다.
- **저주파 차원**: 긴 주기로, 멀리 떨어진 토큰 간의 전역적 관계를 포착한다.

## 긴 문맥에서의 실패: Frequency Collapse

RoPE의 근본적 문제는 훈련 컨텍스트 길이를 초과하면 성능이 급격히 붕괴된다는 것이다. 단순한 성능 저하가 아닌, 완전한 실패로 나타난다.

1. **OOD 회전각 문제**: 훈련 시 보지 못한 위치에 대해 회전각이 분포를 벗어난다. 예를 들어 4K 컨텍스트로 훈련한 모델에서 32K 위치의 회전각은 훈련 분포 밖(OOD)이다.
2. **저주파 차원의 취약성**: 가장 높은 인덱스의 저주파 차원은 훈련 컨텍스트 내에서 한 주기를 완성하지 못한다. 이 차원들은 외삽(extrapolation) 시 가장 심한 영향을 받는다.
3. **위상 붕괴(Phase Collapse)**: 레이어가 깊어질수록 작은 위상 오차가 곱셈적으로 쌓여 어텐션이 완전히 붕괴된다.
4. **정밀도 한계(Precision Wall)**: 극단적으로 긴 시퀀스에서는 FP32 부동소수점 정밀도 한계로 위치 구분 자체가 불가능해진다.

## 해결 시도

- **Base 확대**: base를 10,000에서 500,000으로 확대(LLaMA 3)하여 회전각을 줄인다.
- **YaRN(NTK-aware 보간)**: 고주파는 적게, 저주파는 많이 스케일링하여 보간 압력을 분산한다.
- **Position Interpolation**: 훈련 길이 내로 위치를 압축하여 외삽을 보간으로 전환한다.

그러나 이 기법들도 예측 불가능한 외삽 한계점을 넘으면 성능이 붕괴한다.

#### 참고 자료
1. Su et al. (2021), "RoFormer: Enhanced Transformer with Rotary Position Embedding", [arXiv:2104.09864](https://arxiv.org/abs/2104.09864)
2. "Base of RoPE Bounds Context Length", [arXiv:2405.14591](https://arxiv.org/html/2405.14591v1)
3. "Rotary Positional Embeddings as Phase Modulation", [arXiv:2602.10959](https://arxiv.org/html/2602.10959)
4. "Scaling Laws of RoPE-based Extrapolation", [arXiv:2310.05209](https://arxiv.org/html/2310.05209v2)
