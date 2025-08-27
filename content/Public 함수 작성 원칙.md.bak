개발자로서 코드를 작성할 때 가장 중요한 것 중 하나는 미래의 사용성을 고려하는 것입니다. 특히 `public` 접근 제어자를 가진 함수들은 다른 개발자들에 의해 재사용될 가능성이 높기 때문에 더욱 신중하게 설계되어야 합니다. 이 글에서는 `public` 함수를 작성할 때 적용해야 할 원칙과 그 근거에 대해 알아보겠습니다.

## Public 함수의 고객은 미래의 개발자들

`public` 함수를 작성할 때 가장 먼저 이해해야 할 것은 이 함수의 "고객"이 누구인지 명확히 하는 것입니다. 여기서 고객이란 함수를 사용하게 될 다른 개발자들을 의미합니다. 이들은:

1. 함수의 내부 구현 세부사항에 대해 깊이 이해하지 못할 수 있습니다.
2. 문서화가 불충분하면 함수의 의도된 사용 방법을 파악하기 어려울 수 있습니다.
3. 함수가 어떤 전제 조건이나 제약 사항을 가지고 있는지 알지 못할 수 있습니다.

따라서 `public` 함수는 이러한 고객들의 실수를 미리 예방할 수 있도록 설계되어야 합니다.

## 방어적 프로그래밍의 필요성

방어적 프로그래밍이란 예상치 못한 입력이나 상태에 대해서도 프로그램이 안정적으로 동작하도록 하는 코딩 방식을 말합니다. `public` 함수에서 방어적 프로그래밍이 특히 중요한 이유는 다음과 같습니다:

1. 함수 호출자가 내부 구현 세부사항을 고려하지 않고 개발합니다.
2. 시간이 지남에 따라 함수의 사용 컨텍스트가 변할 수 있습니다.
3. 함수가 원래 의도한 것과 다른 방식으로 호출될 가능성이 항상 존재합니다.

## 방어적 코딩의 실제 적용

### 1. 파라미터 유효성 검증

```java
/**
 * 사용자 프로필을 업데이트합니다.
 * 
 * @param userId 업데이트할 사용자의 ID
 * @param profileData 업데이트할 프로필 데이터
 * @return 업데이트된 사용자 정보
 * @throws IllegalArgumentException 유효하지 않은 파라미터가 제공된 경우
 */
public User updateUserProfile(Long userId, ProfileData profileData) {
    // 파라미터 유효성 검증
    if (userId == null) {
        throw new IllegalArgumentException("사용자 ID는 null이 될 수 없습니다.");
    }
    
    if (profileData == null) {
        throw new IllegalArgumentException("프로필 데이터는 null이 될 수 없습니다.");
    }
    
    // profileData의 내부 필드들도 검증
    if (profileData.getName() != null && profileData.getName().length() > 100) {
        throw new IllegalArgumentException("이름은 100자를 초과할 수 없습니다.");
    }
    
    // 업데이트 로직 수행
    User user = userRepository.findById(userId)
            .orElseThrow(() -> new ResourceNotFoundException("ID가 " + userId + "인 사용자를 찾을 수 없습니다."));
    
    // 프로필 업데이트 로직
    user.updateProfile(profileData);
    return userRepository.save(user);
}
```

### 2. 불변성(Immutability) 보장

함수에 전달된 객체가 함수 내부에서 변경되지 않도록 보장하는 것이 중요합니다.

```java
/**
 * 주어진 사용자 목록에서 활성 사용자만 필터링합니다.
 * 
 * @param users 필터링할 사용자 목록
 * @return 활성 사용자 목록
 */
public List<User> filterActiveUsers(List<User> users) {
    // 입력 유효성 검증
    if (users == null) {
        return Collections.emptyList(); // null 대신 빈 리스트 반환
    }
    
    // 원본 리스트를 변경하지 않고 새 리스트 생성
    return users.stream()
                .filter(User::isActive)
                .collect(Collectors.toList());
}
```

### 3. 명확한 예외 처리

예외가 발생할 수 있는 상황을 명확히 문서화하고, 적절한 예외를 던지는 것이 중요합니다.

```java
/**
 * 지정된 경로에서 파일을 읽어 내용을 반환합니다.
 * 
 * @param filePath 읽을 파일의 경로
 * @return 파일 내용
 * @throws IllegalArgumentException 파일 경로가 null이거나 비어있는 경우
 * @throws FileNotFoundException 지정된 경로에 파일이 존재하지 않는 경우
 * @throws IOException 파일 읽기 중 오류가 발생한 경우
 */
public String readFile(String filePath) throws IOException {
    // 파라미터 유효성 검증
    if (filePath == null || filePath.trim().isEmpty()) {
        throw new IllegalArgumentException("파일 경로는 null이거나 비어있을 수 없습니다.");
    }
    
    File file = new File(filePath);
    if (!file.exists()) {
        throw new FileNotFoundException("파일을 찾을 수 없습니다: " + filePath);
    }
    
    if (!file.isFile()) {
        throw new IllegalArgumentException("지정된 경로는 파일이 아닙니다: " + filePath);
    }
    
    // 파일 읽기 로직
    try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
        return reader.lines().collect(Collectors.joining(System.lineSeparator()));
    }
}
```

## 중복 검증에 대한 우려

일부 개발자들은 이미 파라미터가 검증된 후에 함수를 호출하는 경우, 중복으로 검증을 하는 것이 비효율적이라고 주장할 수 있습니다. 그러나 이러한 주장에는 몇 가지 문제점이 있습니다.

1. **범위 문제**: 심지어 같은 클래스 내의 `private` 함수들 사이에서도 항상 검증이 보장되지 않습니다. 클래스가 커질수록 한 메서드에서 다른 메서드로의 호출 흐름을 추적하기 어려워집니다.
    
2. **유지보수 문제**: 시간이 지남에 따라 코드가 변경되면서 이전에 수행되던 검증이 제거되거나 수정될 수 있습니다.
    
3. **재사용성 문제**: 함수가 다른 컨텍스트에서 재사용될 때, 이전 컨텍스트에서 수행되던 검증이 새로운 컨텍스트에서는 수행되지 않을 수 있습니다.
    

```java
// 좋지 않은 예:
public void processData(DataObject data) {
    // 검증 없이 바로 사용
    String result = transformData(data);
    saveResult(result);
}

// 좋은 예:
public void processData(DataObject data) {
    if (data == null) {
        throw new IllegalArgumentException("데이터 객체는 null이 될 수 없습니다.");
    }
    
    String result = transformData(data);
    saveResult(result);
}

private String transformData(DataObject data) {
    // 여기서도 null 체크 수행
    if (data == null) {
        throw new IllegalArgumentException("데이터 객체는 null이 될 수 없습니다.");
    }
    
    // 변환 로직
    return data.transform();
}
```

## 성능 고려사항

방어적 코딩이 성능에 미치는 영향은 대부분의 경우 무시할 만한 수준입니다. 기본적인 유효성 검사는 매우 빠르게 수행되며, 이로 인해 발생할 수 있는 버그와 디버깅 비용을 고려하면 그 가치는 더욱 분명해집니다.

특히 성능 최적화 관점에서도, 유효성 검사로 인한 성능 저하보다 잘못된 입력으로 인한 예기치 않은 동작이 더 큰 성능 문제를 일으킬 수 있습니다.

> [!info] 아리안 5 발사 실패 사례
> 1996년 6월 4일, 유럽우주국(ESA)의 **아리안 5** 로켓이 첫 번째 시험 발사에서 폭발하며 실패했습니다. 발사 후 37초 만에 로켓이 공중에서 분해되었고, 약 4억 달러(당시 기준) 상당의 손실을 초래했습니다.
> 사고의 근본 원인은 소프트웨어 코드에서 발생한 **정수 오버플로(Integer Overflow)** 예외처리 부재가 원인이었습니다. 

## 스프링 프레임워크에서의 적용

스프링 프레임워크에서는 방어적 프로그래밍을 지원하는 다양한 기능을 제공합니다.

### 1. Bean Validation API

```java
@RestController
@RequestMapping("/api/users")
public class UserController {

    @PostMapping
    public ResponseEntity<User> createUser(@Valid @RequestBody UserDTO userDTO) {
        // @Valid 애노테이션이 유효성 검증을 자동으로 수행
        // 그러나 서비스 레이어에서도 추가 검증을 수행하는 것이 좋음
        User createdUser = userService.createUser(userDTO);
        return ResponseEntity.status(HttpStatus.CREATED).body(createdUser);
    }
}

@Service
public class UserService {

    public User createUser(UserDTO userDTO) {
        // 추가 비즈니스 로직 검증 수행
        if (userDTO.getRole() == Role.ADMIN && !currentUser.hasAdminCreationPermission()) {
            throw new UnauthorizedException("관리자 사용자를 생성할 권한이 없습니다.");
        }
        
        // 나머지 로직 수행
        // ...
    }
}
```

### 2. Spring의 Assert 유틸리티

```java
import org.springframework.util.Assert;

@Service
public class OrderService {

    public Order createOrder(OrderRequest orderRequest) {
        // Spring의 Assert 유틸리티를 사용한 검증
        Assert.notNull(orderRequest, "주문 요청은 null이 될 수 없습니다.");
        Assert.notEmpty(orderRequest.getItems(), "주문 항목은 비어있을 수 없습니다.");
        
        // 비즈니스 로직 수행
        // ...
    }
}
```

## 결론

`public` 함수를 작성할 때는 항상 방어적으로 접근해야 합니다. 이는 단순히 코드의 견고성을 높이는 것뿐만 아니라, 미래의 개발자들이 함수를 올바르게 사용할 수 있도록 돕는 중요한 실천 방법입니다.

방어적 코딩의 핵심 원칙을 요약하면 다음과 같습니다:

1. 모든 입력 파라미터의 유효성을 철저히 검증합니다.
2. 불변성을 보장하여 예기치 않은 부작용을 방지합니다.
3. 명확한 예외를 던지고 적절히 문서화합니다.
4. 성능보다 안정성을 우선시합니다.

이러한 방어적 프로그래밍 원칙을 따름으로써, 보다 안정적이고 유지보수하기 쉬운 코드를 작성할 수 있으며, 이는 결국 장기적인 개발 생산성 향상으로 이어집니다.