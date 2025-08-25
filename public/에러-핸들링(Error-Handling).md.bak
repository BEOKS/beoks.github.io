소프트웨어 개발에서 에러 핸들링은 안정적이고 견고한 애플리케이션을 만드는 데 필수적인 요소입니다. 적절한 에러 처리는 프로그램이 예상치 못한 상황에서도 우아하게 대응하고, 디버깅을 용이하게 하며, 사용자 경험을 향상시킵니다. 이 글에서는 자바 개발자를 위한 에러와 예외 처리의 기본 개념부터 고급 기법까지 체계적으로 살펴보겠습니다.
## 에러와 예외의 기본 개념

자바에서는 프로그램 실행 중 발생할 수 있는 문제를 크게 에러(Error)와 예외(Exception) 두 가지로 분류합니다.

### 에러(Error)

에러는 일반적으로 시스템 레벨의 심각한 문제를 나타내며, 애플리케이션 코드에서 처리하기 어렵거나 불가능한 상황을 의미합니다.

주요 특징:

- JVM이나 하드웨어 관련 문제에서 발생
- 대부분 복구 불가능한 상황
- 애플리케이션에서 잡아서 처리하지 않음
- `java.lang.Error` 클래스의 하위 클래스

예시:

- `OutOfMemoryError`: 메모리 부족
- `StackOverflowError`: 스택 메모리 초과
- `NoClassDefFoundError`: 클래스 정의를 찾을 수 없음

### 예외(Exception)

예외는 프로그램 실행 중 발생하는 예상 가능한(또는 예상치 못한) 경우를 나타내며, 애플리케이션 코드에서 처리할 수 있습니다.

주요 특징:

- 프로그램 로직 실행 중 발생하는 문제
- 적절한 처리를 통해 복구 가능한 경우가 많음
- `try-catch` 구문으로 잡아서 처리할 수 있음
- `java.lang.Exception` 클래스의 하위 클래스

## 자바의 예외 계층 구조

자바의 모든 예외와 에러는 `Throwable` 클래스를 상속합니다. 이 계층 구조는 예외 처리 방식을 결정하는 데 중요한 역할을 합니다.

```mermaid
classDiagram
    Throwable <|-- Error
    Throwable <|-- Exception
    Exception <|-- RuntimeException
    Exception <|-- IOException
    Exception <|-- SQLException
    RuntimeException <|-- NullPointerException
    RuntimeException <|-- ArrayIndexOutOfBoundsException
    RuntimeException <|-- IllegalArgumentException
    
    class Throwable {
        +String message
        +Throwable cause
        +printStackTrace()
        +getMessage()
        +getCause()
    }
    
    class Error {
        +OutOfMemoryError
        +StackOverflowError
        +NoClassDefFoundError
    }
    
    class Exception {
        +checked exceptions
    }
    
    class RuntimeException {
        +unchecked exceptions
    }
```

### 체크 예외(Checked Exception)

체크 예외는 컴파일 시점에 처리 여부를 검사하는 예외입니다. 개발자는 이러한 예외를 명시적으로 처리하거나 메서드 시그니처에 선언해야 합니다.

주요 특징:

- `Exception` 클래스를 직접 상속하는 하위 클래스들
- 컴파일러가 예외 처리 여부를 강제함
- 메서드에서 발생 가능한 체크 예외는 반드시 `throws` 절에 선언되어야 함

예시:

- `IOException`: 입출력 작업 중 발생하는 예외
- `SQLException`: 데이터베이스 액세스 관련 예외
- `ClassNotFoundException`: 클래스를 찾을 수 없을 때 발생하는 예외

```java
public void readFile(String path) throws IOException {
    BufferedReader reader = new BufferedReader(new FileReader(path));
    // 파일 읽기 로직
    reader.close();
}
```

### 언체크 예외(Unchecked Exception)

언체크 예외는 컴파일 시점에 처리 여부를 검사하지 않는 예외입니다. `RuntimeException`과 그 하위 클래스들이 여기에 해당합니다.

주요 특징:

- `RuntimeException` 클래스의 하위 클래스들
- 컴파일러가 예외 처리를 강제하지 않음
- 명시적인 처리나 선언이 필요 없음
- 주로 프로그래밍 오류를 나타냄

예시:

- `NullPointerException`: 널 참조를 역참조할 때 발생
- `ArrayIndexOutOfBoundsException`: 배열 인덱스가 범위를 벗어날 때 발생
- `IllegalArgumentException`: 메서드에 부적절한 인수를 전달했을 때 발생

```java
public int divide(int a, int b) {
    // ArithmeticException은 언체크 예외이므로 명시적 선언 불필요
    return a / b;  // b가 0이면 ArithmeticException 발생
}
```

## 예외 처리 메커니즘

자바는 예외를 처리하기 위한 다양한 메커니즘을 제공합니다.

### try-catch-finally

가장 기본적인 예외 처리 방법은 `try-catch-finally` 블록을 사용하는 것입니다.

```java
try {
    // 예외가 발생할 수 있는 코드
    FileReader file = new FileReader("file.txt");
    // 파일 처리 로직
} catch (FileNotFoundException e) {
    // FileNotFoundException 처리
    System.err.println("파일을 찾을 수 없습니다: " + e.getMessage());
} catch (IOException e) {
    // IOException 처리
    System.err.println("파일 읽기 중 오류 발생: " + e.getMessage());
} finally {
    // 예외 발생 여부와 관계없이 항상 실행되는 코드
    // 주로 리소스 정리에 사용
    if (file != null) {
        try {
            file.close();
        } catch (IOException e) {
            System.err.println("파일 닫기 실패: " + e.getMessage());
        }
    }
}
```

### try-with-resources

Java 7부터 도입된 `try-with-resources` 구문은 `AutoCloseable` 인터페이스를 구현한 리소스를 자동으로 닫아주는 기능을 제공합니다.

```java
try (FileReader file = new FileReader("file.txt");
     BufferedReader reader = new BufferedReader(file)) {
    // 파일 처리 로직
    String line = reader.readLine();
    // 추가 로직
} catch (IOException e) {
    System.err.println("파일 처리 중 오류: " + e.getMessage());
}
// 리소스는 자동으로 닫힘
```

이 방식의 장점:

- 코드가 간결해짐
- 리소스 누수(resource leak) 방지
- 예외가 발생해도 리소스가 안전하게 닫힘

### 멀티 catch

Java 7부터는 여러 예외를 하나의 catch 블록에서 처리할 수 있는 멀티 catch 구문을 지원합니다.

```java
try {
    // 예외 발생 가능 코드
} catch (FileNotFoundException | SQLException e) {
    // 두 예외를 동일한 방식으로 처리
    System.err.println("파일 또는 DB 오류: " + e.getMessage());
}
```

### 예외 전파(Exception Propagation)

예외가 발생하면 해당 예외는 콜 스택을 따라 상위 메서드로 전파됩니다. 적절한 catch 블록을 만나기 전까지 이 과정은 계속됩니다.

```java
public void method3() {
    int[] arr = new int[5];
    arr[10] = 50;  // ArrayIndexOutOfBoundsException 발생
}

public void method2() {
    method3();  // 예외가 method2로 전파됨
}

public void method1() {
    try {
        method2();  // 예외가 method1으로 전파됨
    } catch (ArrayIndexOutOfBoundsException e) {
        System.out.println("배열 인덱스 오류 처리");
    }
}
```

## 효과적인 예외 처리 전략

효과적인 예외 처리는 애플리케이션의 안정성과 유지보수성을 크게 향상시킵니다.

### 예외의 적절한 계층 설계

애플리케이션의 도메인에 맞는 예외 계층을 설계하는 것이 중요합니다.

```java
// 기본 애플리케이션 예외
public class ApplicationException extends Exception {
    public ApplicationException(String message) {
        super(message);
    }
    
    public ApplicationException(String message, Throwable cause) {
        super(message, cause);
    }
}

// 비즈니스 로직 예외
public class BusinessException extends ApplicationException {
    public BusinessException(String message) {
        super(message);
    }
}

// 데이터 액세스 예외
public class DataAccessException extends ApplicationException {
    public DataAccessException(String message, Throwable cause) {
        super(message, cause);
    }
}
```

이러한 계층적 접근 방식의 장점:

- 예외의 분류가 명확해짐
- 특정 유형의 예외만 선택적으로 처리 가능
- 일관된 예외 처리 전략 구현 가능

### 예외 변환(Exception Translation)

하위 레벨의 예외를 상위 레벨의 추상화된 예외로 변환하는 것이 유용할 수 있습니다.

```java
public User findUserById(Long id) throws UserNotFoundException {
    try {
        return userRepository.findById(id);
    } catch (SQLException e) {
        // 하위 레벨 예외를 의미 있는 비즈니스 예외로 변환
        throw new UserNotFoundException("ID가 " + id + "인 사용자를 찾을 수 없습니다", e);
    }
}
```

예외 변환의 이점:

- 추상화 계층 유지: 상위 계층은 하위 계층의 구현 세부 사항을 알 필요가 없음
- 의미 있는 컨텍스트 제공: 비즈니스 로직에 맞는 예외 메시지와 정보 제공
- 예외 처리의 일관성 유지

### 원인 체인(Cause Chain)

예외를 변환할 때는 원래 예외를 원인(cause)으로 포함하는 것이 중요합니다.

```java
try {
    // 코드
} catch (SQLException e) {
    throw new DataAccessException("데이터베이스 접근 중 오류 발생", e);
}
```

이를 통해:

- 원래 발생한 예외의 정보를 보존할 수 있음
- 디버깅 시 전체 예외 체인을 추적할 수 있음
- 상세한 오류 정보를 로깅할 수 있음

### 실패 원자성(Failure Atomicity)

메서드가 예외를 던지는 경우, 객체의 상태를 호출 전과 동일하게 유지해야 합니다. 이것을 '실패 원자성'이라고 합니다.

```java
public void transferMoney(Account from, Account to, BigDecimal amount) 
        throws InsufficientFundsException {
    
    BigDecimal originalFromBalance = from.getBalance();
    
    try {
        // 출금 계좌에서 금액 차감
        from.withdraw(amount);
        
        // 입금 계좌에 금액 추가 (예외 발생 가능)
        to.deposit(amount);
    } catch (Exception e) {
        // 예외 발생 시 출금 계좌 상태 복원
        from.setBalance(originalFromBalance);
        throw e; // 예외 다시 던지기
    }
}
```

실패 원자성을 보장하는 방법:

- 연산 전에 객체 상태 저장
- 실패 시 원래 상태로 복원
- 트랜잭션 사용
- 불변 객체 활용

## 커스텀 예외 설계하기

애플리케이션에 특화된 커스텀 예외를 설계하는 것은 명확한 오류 처리와 비즈니스 로직 표현에 도움이 됩니다.

### 커스텀 예외 생성 지침

1. **의미 있는 이름 사용**: 예외 이름이 문제를 명확하게 설명해야 함
2. **적절한 상위 클래스 선택**: 체크 예외나 언체크 예외 중 적절한 것 선택
3. **충분한 컨텍스트 제공**: 문제 해결에 도움이 되는 정보 포함
4. **직렬화 가능성 고려**: 분산 환경에서 사용할 경우 `Serializable` 구현

### 커스텀 예외 예시

```java
public class OrderNotFoundException extends RuntimeException {
    private final Long orderId;
    
    public OrderNotFoundException(Long orderId) {
        super("주문 ID: " + orderId + "를 찾을 수 없습니다");
        this.orderId = orderId;
    }
    
    public Long getOrderId() {
        return orderId;
    }
}
```

### 체크 예외 vs 언체크 예외 선택 기준

**체크 예외가 적합한 경우**:

- 호출자가 예외를 복구할 수 있을 때
- 호출자에게 예외 처리를 강제하고 싶을 때
- 비즈니스 로직의 일부로서 예외적 상황을 표현할 때

**언체크 예외가 적합한 경우**:

- 프로그래밍 오류를 나타낼 때
- 복구가 불가능하거나 불필요할 때
- 예외 선언이 메서드 시그니처를 지나치게 복잡하게 만들 때
- 대부분의 클라이언트가 예외를 처리할 필요가 없을 때

## 스프링 프레임워크의 예외 처리

스프링 프레임워크는 예외 처리를 위한 다양한 메커니즘을 제공합니다.

### @ExceptionHandler

컨트롤러 내에서 발생하는 특정 예외를 처리하기 위한 메서드를 지정할 수 있습니다.

```java
@Controller
public class UserController {
    
    @GetMapping("/users/{id}")
    public User getUser(@PathVariable Long id) {
        // 사용자 조회 로직 - 사용자가 없으면 예외 발생
        if (userNotFound) {
            throw new UserNotFoundException(id);
        }
        return user;
    }
    
    @ExceptionHandler(UserNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleUserNotFound(UserNotFoundException ex) {
        ErrorResponse error = new ErrorResponse("USER_NOT_FOUND", ex.getMessage());
        return new ResponseEntity<>(error, HttpStatus.NOT_FOUND);
    }
}
```

### @ControllerAdvice와 @RestControllerAdvice

여러 컨트롤러에 걸쳐 전역적으로 예외를 처리하려면 `@ControllerAdvice`나 `@RestControllerAdvice`를 사용합니다.

```java
@RestControllerAdvice
public class GlobalExceptionHandler {
    
    @ExceptionHandler(UserNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleUserNotFound(UserNotFoundException ex) {
        ErrorResponse error = new ErrorResponse("USER_NOT_FOUND", ex.getMessage());
        return new ResponseEntity<>(error, HttpStatus.NOT_FOUND);
    }
    
    @ExceptionHandler(DataIntegrityException.class)
    public ResponseEntity<ErrorResponse> handleDataIntegrity(DataIntegrityException ex) {
        ErrorResponse error = new ErrorResponse("DATA_INTEGRITY_ERROR", ex.getMessage());
        return new ResponseEntity<>(error, HttpStatus.CONFLICT);
    }
    
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGenericException(Exception ex) {
        ErrorResponse error = new ErrorResponse("INTERNAL_ERROR", "서버 내부 오류가 발생했습니다");
        return new ResponseEntity<>(error, HttpStatus.INTERNAL_SERVER_ERROR);
    }
}
```

### 스프링의 예외 변환

스프링은 기술 특화적인 예외를 추상화된 예외로 자동 변환하는 메커니즘을 제공합니다.

```java
// 스프링 데이터 JPA 예외 변환 설정
@Configuration
public class PersistenceConfig {
    
    @Bean
    public PersistenceExceptionTranslationPostProcessor exceptionTranslation() {
        return new PersistenceExceptionTranslationPostProcessor();
    }
}
```

이 설정으로 JPA나 JDBC의 저수준 예외가 스프링의 `DataAccessException` 계층으로 변환됩니다.

### ResponseStatusException

Spring 5부터는 `ResponseStatusException`을 사용하여 HTTP 상태 코드를 직접 지정할 수 있습니다.

```java
@GetMapping("/users/{id}")
public User getUser(@PathVariable Long id) {
    return userRepository.findById(id)
        .orElseThrow(() -> new ResponseStatusException(
            HttpStatus.NOT_FOUND, "ID가 " + id + "인 사용자를 찾을 수 없습니다"));
}
```

이 방식의 장점:

- 간단한 예외 처리를 위한 보일러플레이트 코드 감소
- 특정 엔드포인트에 대한 맞춤형 예외 처리 가능
- 커스텀 예외 클래스 생성 필요성 감소
## 에러 코드
에러 코드에 대한 상세 설명은 [[에러코드]]를 참고해주세요