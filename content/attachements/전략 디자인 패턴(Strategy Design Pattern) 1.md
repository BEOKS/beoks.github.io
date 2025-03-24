**전략 패턴(Strategy Pattern)**은 객체의 행동을 변경해야 할 때, 해당 행동을 별도의 클래스로 정의하고 필요할 때 교체할 수 있도록 만드는 디자인 패턴이다. 즉, **동일한 문제를 해결하는 여러 알고리즘(전략)을 정의하고, 실행 시점에서 이를 선택할 수 있도록** 한다.

---

## 🔹 전략 패턴의 핵심 개념

1. **상속이 아닌 "구성(Composition)"을 활용**하여 동작을 캡슐화한다.
2. **행동(알고리즘)을 인터페이스로 추상화**하고, 이를 구현한 여러 전략(Concrete Strategy)을 정의한다.
3. **실행 중 전략을 쉽게 변경할 수 있도록 설계**하여 유연성을 높인다.

---

## 🔹 구조 (UML)

```plaintext
┌──────────────────────┐
│     Context         │
│  (전략을 사용)      │
│ ┌────────────────┐ │
│ │ Strategy       │ │
│ │ (인터페이스)   │ │
│ └────────────────┘ │
│   strategy:Strategy │
│ ┌────────────────┐ │
│ │ setStrategy()  │ │
│ │ execute()      │ │
└──────────────────────┘
         ▲
         │
 ┌────────────────┐  ┌────────────────┐
 │ StrategyA      │  │ StrategyB      │
 │ (구체적인 전략) │  │ (구체적인 전략) │
 │ execute() 구현 │  │ execute() 구현 │
 └────────────────┘  └────────────────┘
```

---

## 🔹 예제 코드 (TypeScript)

### 🎯 1. 전략 인터페이스 정의

```typescript
interface Strategy {
  execute(a: number, b: number): number;
}
```

### 🎯 2. 구체적인 전략 클래스 구현

```typescript
class AddStrategy implements Strategy {
  execute(a: number, b: number): number {
    return a + b;
  }
}

class MultiplyStrategy implements Strategy {
  execute(a: number, b: number): number {
    return a * b;
  }
}
```

### 🎯 3. 컨텍스트(Context) 클래스 구현

```typescript
class Calculator {
  private strategy: Strategy;

  constructor(strategy: Strategy) {
    this.strategy = strategy;
  }

  setStrategy(strategy: Strategy) {
    this.strategy = strategy;
  }

  calculate(a: number, b: number): number {
    return this.strategy.execute(a, b);
  }
}
```

### 🎯 4. 실행 코드

```typescript
const calculator = new Calculator(new AddStrategy());
console.log(calculator.calculate(5, 3)); // 8 (덧셈)

calculator.setStrategy(new MultiplyStrategy());
console.log(calculator.calculate(5, 3)); // 15 (곱셈)
```

---

## 🔹 전략 패턴을 사용하는 이유

✅ **유연성 증가** - 실행 중 전략을 변경할 수 있음  
✅ **코드 재사용성 증가** - 알고리즘을 별도의 클래스로 분리하여 재사용 가능  
✅ **OCP(개방-폐쇄 원칙) 준수** - 기존 코드를 수정하지 않고 새로운 전략을 추가 가능  
✅ **유지보수 용이** - 각 전략을 독립적으로 수정 가능

---

## 🔹 전략 패턴이 유용한 경우

- **여러 알고리즘을 런타임에 변경해야 할 때**
    - 예: 정렬 알고리즘(버블 정렬, 퀵 정렬 등) 선택
- **if-else 또는 switch문이 너무 많을 때**
    - 예: 결제 방식(신용카드, 페이팔, 애플페이 등) 처리
- **클래스가 특정 행동에 따라 여러 버전이 필요할 때**
    - 예: AI의 행동 패턴(공격적 AI, 방어적 AI)

---

## 🔹 전략 패턴 vs 상태 패턴(State Pattern)

전략 패턴과 상태 패턴은 비슷하지만 차이점이 있다.

|비교 항목|전략 패턴 (Strategy)|상태 패턴 (State)|
|---|---|---|
|목적|알고리즘(전략) 변경|객체의 상태 변경|
|상태 변화|외부에서 직접 변경|내부적으로 변경|
|변경 방식|사용자가 직접 설정|객체 내부에서 상태 변화|

💡 **전략 패턴**은 특정 기능(알고리즘)을 변경하는 것이고,  
💡 **상태 패턴**은 객체의 상태에 따라 행동이 변하는 것이다.

---

## 🔹 마무리

전략 패턴은 **"동작을 객체화하여 유연성을 높이는"** 패턴이다.  
특히 **"조건문이 많아지는 문제를 해결"**하고, **"알고리즘을 쉽게 교체할 수 있도록 설계"**하는 데 유용하다.  
TypeScript, Java, Python 등 다양한 언어에서 활용 가능하며, SOLID 원칙 중 **OCP(개방-폐쇄 원칙)**을 잘 준수하는 패턴이다.