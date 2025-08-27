소프트웨어 개발에서 **단위 테스트(Unit Test)**는 가장 작고 독립적인 코드 단위, 즉 '유닛(Unit)'이 의도한 대로 정확히 작동하는지 검증하는 자동화된 테스트입니다. 마치 건물을 지을 때, 벽돌 하나하나가 규격에 맞게 튼튼하게 만들어졌는지 검사하는 과정과 같습니다. 이 작은 단위들이 모여 견고한 전체 시스템을 이루기 때문입니다.

여기서 '유닛'은  **테스트 대상이 되는 가장 작은 논리적 단위**입니다.

단위 테스트는 개발 사이클의 가장 초기 단계에서 수행되며, 빠르고 지속적인 피드백을 통해 코드의 안정성을 확보하는 핵심적인 역할을 합니다. 이는 [[테스트 주도 개발(TDD)]]과 같은 최신 개발 방법론의 근간이 되기도 합니다.

---

### 좋은 단위 테스트의 조건 (FIRST 원칙)

훌륭한 단위 테스트가 되기 위해서는 다음과 같은 **FIRST** 원칙을 따르는 것이 좋습니다.

- **Fast (빠르게)**: 단위 테스트는 매우 빨라야 합니다. 수백, 수천 개의 테스트가 있더라도 몇 초 안에 완료되어야 개발자가 코드를 수정할 때마다 부담 없이 실행하고 즉각적인 피드백을 받을 수 있습니다.
- **Isolated/Independent (독립적으로)**: 각 테스트는 서로 독립적이어야 하며, 다른 테스트의 결과에 영향을 주어서는 안 됩니다. 실행 순서에 상관없이 항상 동일한 결과를 보장해야 합니다. 또한, 테스트 대상(Unit)은 외부 의존성(데이터베이스(Database), 네트워크(Network), 파일 시스템 등)으로부터 철저히 격리되어야 합니다.
- **Repeatable (반복 가능하게)**: 테스트는 어떤 환경(개발자 노트북, CI 서버 등)에서도 항상 동일한 결과를 내야 합니다. 외부 환경에 의존하면 테스트가 예기치 않게 실패하는 원인이 될 수 있습니다.
- **Self-validating (스스로 검증 가능하게)**: 테스트 결과는 `true` 또는 `false`와 같이 명확하게 나와야 합니다. 로그 파일을 열어보거나 수동으로 결과를 해석해야 한다면 좋은 단위 테스트가 아닙니다. `assert` 구문을 통해 성공과 실패를 자동으로 판별해야 합니다.
- **Timely (시기적절하게)**: 단위 테스트는 테스트할 실제 코드를 작성하기 직전, 또는 직후에 바로 작성하는 것이 가장 효과적입니다. 코드가 복잡해진 후에 테스트를 작성하려고 하면 구조를 바꾸기 어렵고 테스트 작성 자체도 힘들어집니다.

---

### 단위 테스트 vs 통합 테스트

단위 테스트는 종종 [[통합 테스트(Integration Test)]]와 비교됩니다. 둘의 가장 큰 차이점은 **'범위'**와 **'목표'**에 있습니다.

|         |                          |                                  |
| ------- | ------------------------ | -------------------------------- |
| **구분**  | **단위 테스트 (Unit Test)**   | **[[통합 테스트(Integration Test)]]** |
| **범위**  | 단일 메서드나 클래스 등 가장 작은 단위   | 여러 모듈(컴포넌트) 간의 상호작용              |
| **목표**  | 코드 단위의 논리적 정확성 검증        | 모듈 간의 인터페이스 및 데이터 흐름 검증          |
| **의존성** | 외부 의존성을 **격리** (Mock 사용) | 외부 의존성을 **포함**하여 테스트             |
| **속도**  | 매우 빠름                    | 상대적으로 느림                         |
| **피드백** | 즉각적                      | 비교적 느림                           |

단위 테스트가 벽돌 자체의 강도를 시험하는 것이라면, 통합 테스트는 벽돌과 시멘트가 잘 결합되어 튼튼한 벽을 만드는지 확인하는 과정이라고 비유할 수 있습니다. 두 테스트는 서로를 대체하는 관계가 아니라, 상호 보완하며 소프트웨어의 품질을 함께 높이는 역할을 합니다. 더 자세한 내용은 [[단위 테스트 (Unit Test) vs 통합 테스트(Integration Test)]]에서 확인하실 수 있습니다.

---

### Java(JUnit)를 이용한 단위 테스트 예시

Java 진영에서는 JUnit이라는 강력한 테스트 프레임워크를 사용하여 단위 테스트를 작성합니다. 여기서 중요한 개념은 **'격리'**를 위한 [[테스트 더블(Test Double)]]의 사용입니다. 특히 모의 객체(Mock Object)는 외부 의존성을 흉내 내어 테스트 대상 코드만 순수하게 검증할 수 있도록 돕습니다.

`CalculatorService`가 외부 `TaxCalculator`에 의존하여 부가세를 계산하는 간단한 예시를 들어보겠습니다.

```java
// 테스트 대상 클래스
public class CalculatorService {
    private final TaxCalculator taxCalculator; // 외부 의존성

    public CalculatorService(TaxCalculator taxCalculator) {
        this.taxCalculator = taxCalculator;
    }

    // 금액에 부가세를 더한 총액을 반환
    public int calculateTotalPrice(int price) {
        if (price < 0) {
            throw new IllegalArgumentException("금액은 0보다 작을 수 없습니다.");
        }
        double taxRate = taxCalculator.getTaxRate(); // 외부 의존성 메서드 호출
        int tax = (int)(price * taxRate);
        return price + tax;
    }
}
```

이 `CalculatorService`를 테스트할 때, 우리는 실제 `TaxCalculator`의 동작이나 상태에 영향을 받고 싶지 않습니다. 오직 `calculateTotalPrice` 메서드의 논리가 올바른지만 확인하고 싶습니다. 이때 [[Mockito Strict Stubbing]]와 같은 Mocking 프레임워크를 사용합니다.

```java
// JUnit5와 Mockito를 사용한 단위 테스트
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class CalculatorServiceTest {

    @Mock
    private TaxCalculator mockTaxCalculator; // 가짜 TaxCalculator(Mock) 생성

    @InjectMocks
    private CalculatorService calculatorService; // Mock을 주입받을 테스트 대상

    @Test
    void 금액이_양수일_때_총액_계산_성공() {
        // given (준비)
        int price = 10000;
        double taxRate = 0.1;

        // "mockTaxCalculator.getTaxRate()가 호출되면 0.1을 반환하라"고 정의
        when(mockTaxCalculator.getTaxRate()).thenReturn(taxRate);

        // when (실행)
        int totalPrice = calculatorService.calculateTotalPrice(price);

        // then (검증)
        // 10000 + (10000 * 0.1) = 11000
        assertEquals(11000, totalPrice);
    }

    @Test
    void 금액이_음수일_때_예외_발생() {
        // given
        int negativePrice = -100;

        // when & then
        // calculatorService.calculateTotalPrice(-100)를 실행할 때
        // IllegalArgumentException이 발생하는지 확인
        assertThrows(IllegalArgumentException.class, () -> {
            calculatorService.calculateTotalPrice(negativePrice);
        });
    }
}
```

위 테스트 코드에서 `mockTaxCalculator`는 실제 `TaxCalculator`가 아닌, 우리가 원하는 대로 동작하도록 프로그래밍된 가짜 객체입니다. 덕분에 `TaxCalculator`의 내부 로직이나 네트워크 상태와 상관없이 `CalculatorService`의 로직만을 독립적으로, 그리고 빠르게 검증할 수 있습니다.

---
### 벡엔드 단위 테스트

앞서 언급드렸듯, '유닛'은 **테스트 대상이 되는 가장 작은 논리적 단위** 입니다. 벡엔드 개발에서 일반적으로 가장 작은 논리적 단위는 하나의 `HTTP API`로 정의할 수 있습니다. 더 자세한 내용은 [[API 단위 테스트]]를 참고해주세요

---

### 단위 테스트의 가치

- **개발의 자신감**: 코드를 수정하거나 새로운 기능을 추가했을 때, 단위 테스트를 실행하는 것만으로 기존 기능이 깨지지 않았다는 확신(회귀 방지)을 얻을 수 있습니다.
- **살아있는 문서**: 잘 작성된 단위 테스트 코드는 그 자체로 해당 코드의 기능과 사용법을 설명하는 가장 정확한 문서가 됩니다.
- **설계 개선**: 테스트하기 어려운 코드는 보통 설계적으로 문제가 있을 가능성이 높습니다. 단위 테스트를 작성하는 과정은 자연스럽게 결합도(Coupling)는 낮고 응집도(Cohesion)는 높은, 더 나은 설계로 코드를 유도합니다.
- **쉬운 디버깅**: 테스트가 실패하면 문제의 범위가 특정 유닛으로 한정되므로, 버그의 원인을 빠르고 쉽게 찾을 수 있습니다.

---

### 결론

단위 테스트는 단순히 버그를 찾는 행위를 넘어, 소프트웨어의 설계를 개선하고 유지보수 비용을 낮추며, 개발자에게는 안정적인 개발의 발판을 마련해주는 매우 중요한 활동입니다. 비록 처음에는 테스트 코드를 작성하는 시간이 추가로 드는 것처럼 느껴질 수 있지만, 장기적으로는 디버깅과 시스템 안정화에 드는 시간을 극적으로 줄여주어 전체 개발 생산성을 높이는 가장 확실한 투자 중 하나입니다.

---

### 참고 자료

- [Martin Fowler - Unit Test](https://martinfowler.com/bliki/UnitTest.html)
- [JUnit 5 User Guide](https://junit.org/junit5/docs/current/user-guide/)
- [Mockito Documentation](https://site.mockito.org/)