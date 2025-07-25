**"리팩토링은 소프트웨어의 겉보기 동작은 그대로 유지한 채, 내부 구조를 개선하여 더 이해하기 쉽고 수정하기 쉽게 만드는 과정이다."**

이 말은 리팩토링의 대가 마틴 파울러(Martin Fowler)가 그의 저서에서 내린 정의입니다. 여기서 핵심은 **'겉보기 동작(기능)은 바꾸지 않는다'**는 점입니다. 리팩토링은 버그를 수정하거나 새로운 기능을 추가하는 행위가 아닙니다. 오직 코드의 내부 구조, 즉 설계와 가독성을 개선하여 소프트웨어의 건강 상태를 좋게 만드는 체질 개선 활동과 같습니다.

시간이 지나면서 소프트웨어는 계속해서 변경되고 확장됩니다. 이 과정에서 초기 설계의 우아함은 점차 사라지고, 코드는 복잡해지며 이해하기 어려워집니다. 이러한 '썩어가는(decay)' 코드는 결국 버그의 온상이 되고 새로운 기능을 추가하기 어렵게 만듭니다. 리팩토링은 이러한 소프트웨어의 엔트로피 증가를 막고, 지속 가능한 개발을 가능하게 하는 필수적인 활동입니다.

---

### 왜 리팩토링을 해야 할까?

리팩토링은 단지 코드를 '예쁘게' 만드는 작업이 아닙니다. 다음과 같은 명확하고 실질적인 목표를 가집니다.

1. **가독성 향상 (코드 이해 촉진)**: 잘 짜인 코드는 주석보다 더 명확하게 의도를 드러냅니다. 리팩토링을 통해 복잡한 로직을 단순화하고, 변수와 메서드의 이름을 명확히 하여 동료 개발자가 코드를 이해하는 시간을 단축시킵니다.
2. **유지보수 용이성 증대**: 설계가 개선된 코드는 버그를 찾기가 더 쉽고, 새로운 기능을 추가하거나 기존 기능을 수정하는 것이 훨씬 간단해집니다. 이는 장기적인 개발 비용 절감으로 이어집니다.
3. **버그 발생 가능성 감소**: 복잡하고 꼬인 코드는 잠재적인 버그를 숨기기 좋습니다. 리팩토링을 통해 코드 구조를 명확히 하면 논리적인 허점이 드러나고, 버그가 발생할 여지를 줄일 수 있습니다.
4. **개발 속도 향상**: 단기적으로는 리팩토링에 시간이 드는 것처럼 보이지만, 장기적으로는 잘 정리된 코드 베이스 위에서 개발하는 것이 훨씬 빠릅니다. '나중에 고치자'는 생각으로 쌓아둔 [[기술 부채(Technical Debt)]]는 결국 개발 속도를 저해하는 가장 큰 원인이 됩니다.

---

### 리팩토링은 언제 해야 할까?

리팩토링을 위한 특별한 시간을 따로 마련하기보다는, 개발 과정에 자연스럽게 녹여내는 것이 가장 이상적입니다.

- **[[테스트 주도 개발(TDD)]]의 Refactor 단계에서**: TDD의 'Red-Green-Refactor' 사이클 자체가 리팩토링을 내재하고 있습니다. 기능 구현(Green) 후 즉시 코드를 개선(Refactor)하는 것이 가장 좋은 습관입니다.
- **기능 추가 전/후에**: 새로운 기능을 추가하기 전에, 관련 코드를 리팩토링하여 기능 추가를 더 쉽게 만들 수 있습니다. 또한, 기능 추가 후에 새로 작성된 코드를 다듬는 과정도 필요합니다.
- **[[코드 스멜(Code Smell)]]을 발견했을 때**: 코드를 읽다가 무언가 '나쁜 냄새'가 난다고 느껴질 때가 바로 리팩토링의 신호입니다. 긴 메서드, 거대한 클래스, 중복된 코드 등이 대표적인 코드 스멜입니다.
- **코드 리뷰 중에**: 동료의 코드를 리뷰하면서 더 나은 구조를 제안하고 함께 개선해 나가는 과정에서 리팩토링을 수행할 수 있습니다.

---

### 리팩토링의 기본 예시: 메서드 추출 (Extract Method)

가장 대표적이고 자주 사용되는 리팩토링 기법 중 하나인 '메서드 추출'을 통해 리팩토링의 개념을 살펴보겠습니다.

**리팩토링 전 (Before)**

아래 코드는 주문 금액을 계산하면서 고객에게 보낼 청구 내역을 출력하는 로직을 가지고 있습니다. 한 메서드 안에 너무 많은 책임이 섞여 있습니다.

```java
public class Order {
    private List<Double> amounts;
    private String customerName;

    // ... 생성자 및 다른 메서드

    public void printOwing() {
        // 1. 배너 출력
        System.out.println("*************************");
        System.out.println("***** Customer Owes *****");
        System.out.println("*************************");

        // 2. 총액 계산
        double outstanding = 0.0;
        for (Double amount : amounts) {
            outstanding += amount;
        }

        // 3. 세부 정보 출력
        System.out.println("name: " + customerName);
        System.out.println("amount: " + outstanding);
    }
}
```

**리팩토링 후 (After)**

각각의 역할을 별도의 private 메서드로 추출하여 `printOwing` 메서드의 가독성과 재사용성을 높였습니다.

```java
public class Order {
    private List<Double> amounts;
    private String customerName;

    // ... 생성자 및 다른 메서드

    public void printOwing() {
        printBanner();
        double outstanding = calculateOutstanding();
        printDetails(outstanding);
    }

    private void printBanner() {
        System.out.println("*************************");
        System.out.println("***** Customer Owes *****");
        System.out.println("*************************");
    }

    private double calculateOutstanding() {
        // Java Stream API를 사용하여 더 간결하게 표현
        return amounts.stream().mapToDouble(Double::doubleValue).sum();
    }

    private void printDetails(double outstanding) {
        System.out.println("name: " + customerName);
        System.out.println("amount: " + outstanding);
    }
}
```

리팩토링 후, `printOwing` 메서드는 이제 전체 작업의 흐름을 명확하게 보여주는 요약본처럼 기능합니다. 각 세부 구현은 잘 명명된 private 메서드 안에 캡슐화되어 있어 코드를 이해하기가 훨씬 쉬워졌습니다. 기능은 전혀 바뀌지 않았지만, 코드의 품질은 극적으로 향상되었습니다.

이 외에도 다양한 [[리팩토링 기법]]이 존재합니다.

---

### 안전한 리팩토링의 전제 조건: 테스트 코드

리팩토링을 할 때 가장 중요한 것은 **실수로 기존 기능을 망가뜨리지 않는 것**입니다. 어떻게 이를 보장할 수 있을까요? 바로 **자동화된 테스트 코드**입니다.

리팩토링을 시작하기 전에 반드시 해당 코드의 동작을 검증하는 [[단위 테스트(Unit Test)]]나 [[통합 테스트(Integration Test)]]가 갖춰져 있어야 합니다. 테스트 코드는 리팩토링 과정에서 의도치 않은 변경이 발생했을 때 즉시 우리에게 알려주는 든든한 안전망 역할을 합니다.

**리팩토링의 과정**

1. 리팩토링할 코드에 대한 테스트 코드가 있는지 확인한다. (없다면 먼저 작성한다!)
2. 테스트를 실행하여 모두 통과하는지 확인한다. (Green 상태)
3. 코드를 조금씩 리팩토링한다.
4. 다시 테스트를 실행하여 여전히 모두 통과하는지 확인한다.
5. 위 3~4번 과정을 반복한다.

테스트가 없다면, 리팩토링은 '정리'가 아니라 '고장'을 유발하는 위험한 도박이 될 수 있습니다.

---

### 결론

리팩토링은 일회성 이벤트가 아니라, 코드를 작성하는 내내 지속되어야 하는 습관이자 문화입니다. 깨끗하고 건강한 코드는 팀의 생산성을 높이고, 예측 불가능한 버그를 줄이며, 변화하는 비즈니스 요구사항에 민첩하게 대응할 수 있는 힘을 줍니다. 지금 당장 눈앞의 코드를 조금 더 명확하게, 조금 더 단순하게 만들 수 없는지 고민해보는 것, 그것이 바로 위대한 소프트웨어를 만드는 리팩토링의 첫걸음입니다.

---

### 참고 자료

- 리팩토링 2판 (Refactoring: Improving the Design of Existing Code, 2nd Edition) - 마틴 파울러
- 클린코드 (Clean Code) - 로버트 C. 마틴
- sourcemaking.com - Refactoring