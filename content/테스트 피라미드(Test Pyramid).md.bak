소프트웨어를 개발할 때, 우리가 작성한 코드가 의도대로 정확하게 동작하는지 어떻게 보장할 수 있을까요? 바로 **테스트**를 통해서입니다. 하지만 모든 테스트가 동일한 가치를 가지는 것은 아니며, 효율적인 테스트 전략을 수립하는 것은 매우 중요합니다. **테스트 피라미드(Test Pyramid)** 는 바로 이러한 고민에 대한 훌륭한 해답을 제시하는 전략적 프레임워크입니다.

테스트 피라미드는 [[테스트 자동화(Test Automation)]] 전략을 시각적으로 표현한 모델로, 2009년 마이크 콘(Mike Cohn)에 의해 대중화되었습니다. 이 모델의 핵심은 **테스트 스위트를 여러 계층으로 나누고, 각 계층의 테스트 양을 다르게 가져감으로써 효율성과 안정성을 모두 확보하는 것**입니다.

피라미드라는 이름에서 알 수 있듯이, 아래로 갈수록 테스트의 개수가 많아지고 위로 갈수록 적어지는 구조를 가집니다.

코드 스니펫

```mermaid
graph TD
    subgraph 테스트 피라미드
        E2E_Test(E2E 테스트)
        Integration_Test(통합 테스트)
        Unit_Test(단위 테스트)
    end
    
    style Unit_Test fill:#9f9,stroke:#333,stroke-width:2px
    style Integration_Test fill:#ff9,stroke:#333,stroke-width:2px
    style E2E_Test fill:#f99,stroke:#333,stroke-width:2px

    Unit_Test --> Integration_Test
    Integration_Test --> E2E_Test
```

이 구조는 각 테스트 유형의 특징과 직접적인 관련이 있습니다. 피라미드의 하단에 위치한 테스트는 실행 속도가 빠르고, 비용이 저렴하며, 격리된 환경에서 실행되어 안정적입니다. 반면, 상단으로 갈수록 실행 속도가 느려지고, 비용이 비싸지며, 여러 외부 요인에 의해 실패할 확률이 높아집니다.

---

## 테스트 피라미드의 계층별 상세 설명

테스트 피라미드는 일반적으로 세 가지 주요 계층으로 구성됩니다.

### 1. 단위 테스트 (Unit Tests)

피라미드의 가장 넓은 기반을 형성하는 것은 **단위 테스트**입니다.

- **목표**: 코드의 가장 작은 단위(예: 메서드, 함수, 클래스)가 독립적으로 정확하게 동작하는지를 검증합니다.
- **특징**:
    - **신속성**: 실행 속도가 매우 빠릅니다. 수천 개의 테스트도 몇 초 안에 완료될 수 있습니다.
    - **격리성**: 다른 컴포넌트나 외부 시스템(데이터베이스, 네트워크 등)으로부터 완전히 격리된 상태에서 실행됩니다. 의존성은 `[[Mocking]]`을 통해 가짜 객체로 대체됩니다.
    - **높은 안정성**: 외부 요인의 영향을 받지 않으므로 테스트 결과가 일관적입니다.
- **역할**: 개발자에게 가장 빠르고 즉각적인 피드백을 제공하여 버그를 조기에 발견하고, 코드 리팩토링에 대한 자신감을 부여합니다.

자세한 내용은 [[단위 테스트(Unit Test)]] 노트를 참고해주세요.

### 2. 통합 테스트 (Integration Tests)

피라미드의 중간 계층은 **통합 테스트**입니다.

- **목표**: 여러 개의 모듈, 컴포넌트, 또는 서비스가 함께 연동될 때 발생하는 문제를 검증합니다.
- **특징**:
    - **중간 속도**: 단위 테스트보다는 느리지만, E2E 테스트보다는 빠릅니다.
    - **연동성**: 실제 데이터베이스, 파일 시스템, 또는 다른 마이크로서비스와의 상호작용을 테스트합니다.
    - **상대적 불안정성**: 외부 시스템의 상태에 따라 테스트가 실패할 수 있습니다.
- **역할**: 단위 테스트만으로는 발견할 수 없는, 컴포넌트 간의 인터페이스나 데이터 흐름에서 발생하는 오류를 찾아냅니다. 예를 들어, 서비스 계층과 데이터 접근 계층(Repository)이 올바르게 상호작용하는지 확인합니다.

자세한 내용은 [[통합 테스트(Integration Test)]] 노트를 참고해주세요.

### 3. E2E 테스트 (End-to-End Tests)

피라미드의 가장 좁은 최상층은 **E2E(End-to-End) 테스트**입니다. 종종 UI 테스트라고도 불립니다.

- **목표**: 실제 사용자의 시나리오를 그대로 시뮬레이션하여, 전체 시스템이 처음부터 끝까지 올바르게 동작하는지를 검증합니다.
- **특징**:
    - **느린 속도**: 실제 애플리케이션을 구동하고 UI를 조작하므로 실행 시간이 매우 깁니다.
    - **높은 비용**: 작성하고 유지보수하는 데 많은 노력이 필요합니다. 작은 UI 변경에도 테스트가 쉽게 깨질 수 있습니다(Brittle).
    - **최고의 신뢰도**: 이 테스트가 통과하면, 사용자의 핵심 기능이 정상적으로 작동한다는 강한 확신을 가질 수 있습니다.
- **역할**: 시스템 전체의 비즈니스 흐름과 사용자 경험을 최종적으로 보증합니다. 따라서 가장 중요한 핵심 기능(예: '로그인 후 상품 주문')에 대해서만 제한적으로 작성해야 합니다.

자세한 내용은 [[E2E 테스트(End-to-End Test)]] 노트를 참고해주세요.

---

## 왜 테스트 피라미드를 따라야 할까요?

테스트 피라미드 전략을 채택하면 다음과 같은 명확한 이점을 얻을 수 있습니다.

1. **빠른 피드백 루프**: 대부분의 테스트가 빠른 단위 테스트로 구성되므로, 개발자는 코드 변경 후 즉시 결과를 확인하고 문제를 수정할 수 있습니다. 이는 [[테스트 주도 개발(TDD)]]과 같은 애자일 개발 방식에서 특히 중요합니다.
2. **높은 ROI (투자 대비 수익)**: 단위 테스트는 작성 비용이 저렴하고 버그를 조기에 발견하여 수정 비용을 절감시켜주므로 가장 높은 ROI를 제공합니다.
3. **안정적인 테스트 스위트**: 불안정한 E2E 테스트의 수를 최소화하고 안정적인 단위 테스트에 집중함으로써, 테스트가 비기능적인 외부 요인으로 실패하는 경우를 줄일 수 있습니다. 이는 테스트 결과에 대한 신뢰도를 높입니다.
4. **유지보수 용이성**: 범위가 작고 명확한 단위 테스트는 문제가 발생했을 때 원인을 특정하기 쉽습니다. 반면, 복잡한 E2E 테스트는 실패 원인을 분석하는 데 많은 시간이 소요될 수 있습니다.

---

## 흔히 저지르는 실수: 테스트 아이스크림 콘

테스트 피라미드를 무시하고 반대의 전략을 취하는 경우, **아이스크림 콘(Ice Cream Cone)** 이라는 안티패턴에 빠지게 됩니다.

코드 스니펫

```mermaid
graph TD
    subgraph 아이스크림 콘 안티패턴
        Unit_Test(단위 테스트)
        Integration_Test(통합 테스트)
        Manual_Test(수동/E2E 테스트)
    end
    
    style Manual_Test fill:#f99,stroke:#333,stroke-width:2px
    style Integration_Test fill:#ff9,stroke:#333,stroke-width:2px
    style Unit_Test fill:#9f9,stroke:#333,stroke-width:2px

    Manual_Test --> Integration_Test
    Integration_Test --> Unit_Test
```

이는 대부분의 테스트를 느리고 불안정한 E2E 테스트나 수동 테스트에 의존하고, 단위 테스트는 거의 작성하지 않는 형태입니다. 이러한 구조는 다음과 같은 심각한 문제를 야기합니다.

- **느린 피드백**: 테스트 실행에 몇 시간씩 걸려 개발 속도를 저해합니다.
- **높은 유지보수 비용**: UI가 변경될 때마다 수많은 테스트 코드를 수정해야 합니다.
- **불안정한 빌드**: 테스트가 자주 실패하여 CI/CD 파이프라인이 멈추고, 팀은 점차 테스트 결과를 불신하게 됩니다.

이러한 문제에 대한 자세한 내용은 [[테스트 안티패턴(Test Anti-Patterns)]]에서 확인하실 수 있습니다.

---

## 스프링(Spring) 애플리케이션 예시

스프링 프레임워크 환경에서 테스트 피라미드를 어떻게 적용할 수 있는지 간단한 예시로 살펴보겠습니다.

### 단위 테스트 예시 (Service Layer)

`OrderService`의 특정 로직을 다른 의존성 없이 테스트합니다. `PaymentClient`는 `[[Mocking]]`을 통해 가짜 객체로 대체합니다.

```java
// JUnit 5, Mockito 사용
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;
import static org.assertj.core.api.Assertions.assertThat;

@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

    @InjectMocks
    private OrderService orderService; // 테스트 대상 클래스

    @Mock
    private PaymentClient paymentClient; // Mock 처리할 의존성

    @Mock
    private OrderRepository orderRepository; // Mock 처리할 의존성

    @Test
    void 주문이_성공하면_결제가_요청된다() {
        // given
        long orderId = 1L;
        Order order = new Order(orderId, "Test Item", 10000);
        when(orderRepository.findById(orderId)).thenReturn(java.util.Optional.of(order));
        when(paymentClient.requestPayment(10000)).thenReturn(true); // 결제 성공 시나리오

        // when
        boolean result = orderService.processOrder(orderId);

        // then
        assertThat(result).isTrue();
        verify(paymentClient).requestPayment(10000); // paymentClient의 requestPayment가 호출되었는지 검증
    }
}
```

### 통합 테스트 예시 (Controller Layer)

실제 서블릿 컨테이너를 모킹하여 컨트롤러의 요청-응답 전체 과정을 테스트합니다. 서비스나 리포지토리 계층은 실제 스프링 빈을 사용하거나 테스트용 빈으로 대체할 수 있습니다.

```java
// Spring Boot Test, MockMvc 사용
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;

@SpringBootTest
@AutoConfigureMockMvc
class OrderControllerTest {

    @Autowired
    private MockMvc mockMvc; // HTTP 요청을 시뮬레이션

    @Test
    void 올바른_주문_요청시_성공적으로_처리된다() throws Exception {
        // given
        String orderRequestJson = "{\"itemName\":\"Spring Book\",\"quantity\":1}";

        // when & then
        mockMvc.perform(post("/api/orders")
                .contentType(MediaType.APPLICATION_JSON)
                .content(orderRequestJson))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.orderStatus").value("SUCCESS"));
    }
}
```

E2E 테스트는 Selenium, Cypress, Playwright와 같은 별도의 도구를 사용하여 실제 브라우저를 구동해 애플리케이션 UI부터 데이터베이스까지 전체 흐름을 테스트하게 됩니다.

---

## 결론

**테스트 피라미드는 절대적인 규칙이라기보다는, 테스트 스위트의 건강 상태를 진단하고 균형 잡힌 테스트 포트폴리오를 구축하기 위한 매우 효과적인 지침**입니다. 견고하고 신뢰할 수 있는 소프트웨어를 더 빠르고 효율적으로 제공하고 싶다면, 테스트 피라미드 전략을 이해하고 팀의 상황에 맞게 적용하는 것이 중요합니다.

가장 중요한 것은 피라미드의 기반을 이루는 **단위 테스트에 가장 많은 노력을 기울이는 것**입니다. 이를 통해 개발의 모든 단계에서 자신감을 갖고 제품을 만들어나갈 수 있을 것입니다.

## 참고 자료

- [Martin Fowler - Test Pyramid](https://martinfowler.com/bliki/TestPyramid.html)
- [Mike Cohn - The Forgotten Layer of the Test Automation Pyramid](https://www.mountaingoatsoftware.com/blog/the-forgotten-layer-of-the-test-automation-pyrami%3C/3%3Ed)
- [Google Testing Blog - Just Say No to More End-to-End Tests](https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html%3C/4%3E)