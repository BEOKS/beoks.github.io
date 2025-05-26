
Spring Bean Validation의 공용 사용은 애플리케이션 전반에 걸쳐 일관된 비즈니스 로직을 적용할 때 매우 효과적인 접근 방식입니다. 예를 들어 여러 곳에서 사용되는 유효성 검증 로직이 있을 때, 이를 하나의 Bean으로 정의하고 공유함으로써 유지보수성을 크게 향상시킬 수 있습니다.

## Bean으로 정의하는 유효성 검증 로직

유효성 검증 요구사항이 "모든 에디터는 2MB까지 입력할 수 있도록 제한" 같은 경우, 이를 Bean으로 관리하면 요구사항 변경 시 한 곳만 수정해도 모든 곳에 변경사항이 적용됩니다.

### 커스텀 유효성 검증기 구현하기

먼저 커스텀 유효성 검증기를 구현해 보겠습니다.

```java
import javax.validation.Constraint;
import javax.validation.Payload;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Target({ElementType.FIELD, ElementType.METHOD, ElementType.PARAMETER})
@Retention(RetentionPolicy.RUNTIME)
@Constraint(validatedBy = EditorSizeValidator.class)
public @interface EditorSize {
    String message() default "에디터 입력 크기가 제한을 초과하였습니다";
    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};
}
```

그리고 이 어노테이션을 처리할 유효성 검증기 클래스를 Bean으로 등록합니다:

```java
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import javax.validation.ConstraintValidator;
import javax.validation.ConstraintValidatorContext;

@Component
public class EditorSizeValidator implements ConstraintValidator<EditorSize, String> {
    
    // 설정에서 제한 값을 주입받아 사용
    @Value("${editor.max.size:2097152}") // 기본값 2MB (바이트 단위)
    private int maxSize;
    
    // 유효성 검증 방식(바이트 또는 글자수)
    @Value("${editor.validation.type:byte}")
    private String validationType;

    @Override
    public boolean isValid(String value, ConstraintValidatorContext context) {
        if (value == null) {
            return true; // null 값은 @NotNull 등 다른 어노테이션으로 처리
        }
        
        if ("byte".equals(validationType)) {
            return value.getBytes().length <= maxSize;
        } else if ("char".equals(validationType)) {
            return value.length() <= maxSize;
        }
        
        // 기본적으로 바이트 검사
        return value.getBytes().length <= maxSize;
    }
}
```

### 설정 값 관리

편리한 관리를 위해 설정 값을 properties 또는 yaml 파일에서 관리합니다:

```yaml
# application.yml
editor:
  max:
    size: 2097152 # 2MB (바이트 단위)
  validation:
    type: byte # byte 또는 char
```

### 유효성 검증 Bean 사용하기

이제 도메인 클래스나 DTO에서 이 커스텀 어노테이션을 사용할 수 있습니다:

```java
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class ContentDto {
    private String title;
    
    @EditorSize
    private String content;
    
    // 기타 필드들...
}
```

## 설정 변경을 위한 전략

요구사항이 "바이트가 아닌 글자수로 제한 조건을 변경"과 같이 바뀌는 경우, 설정 파일만 수정하면 됩니다:

```yaml
# 변경된 application.yml
editor:
  max:
    size: 1000 # 최대 1000자
  validation:
    type: char # 글자수 기준으로 변경
```

이렇게 하면 애플리케이션 내 모든 `@EditorSize` 어노테이션이 바이트 대신 글자수를 기준으로 유효성 검증을 수행하게 됩니다.

## 유효성 검증 로직 확장하기

보다 복잡한 검증 로직이 필요할 때는 Bean이 다른 Bean을 주입받아 사용할 수 있습니다:

```java
@Component
public class EditorSizeValidator implements ConstraintValidator<EditorSize, String> {
    
    @Value("${editor.max.size:2097152}")
    private int maxSize;
    
    @Value("${editor.validation.type:byte}")
    private String validationType;
    
    private final ContentSanitizer sanitizer;
    
    public EditorSizeValidator(ContentSanitizer sanitizer) {
        this.sanitizer = sanitizer;
    }

    @Override
    public boolean isValid(String value, ConstraintValidatorContext context) {
        if (value == null) {
            return true;
        }
        
        // 컨텐츠 전처리 (태그 제거 등)
        String sanitizedValue = sanitizer.sanitize(value);
        
        if ("byte".equals(validationType)) {
            return sanitizedValue.getBytes().length <= maxSize;
        } else if ("char".equals(validationType)) {
            return sanitizedValue.length() <= maxSize;
        }
        
        return sanitizedValue.getBytes().length <= maxSize;
    }
}
```

## 유효성 검증 로직 테스트

Spring Bean으로 구현된 유효성 검증 로직은 단위 테스트를 통해 검증할 수 있습니다:

```java
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.TestPropertySource;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
@TestPropertySource(properties = {
    "editor.max.size=10",
    "editor.validation.type=char"
})
public class EditorSizeValidatorTest {
    
    @Autowired
    private EditorSizeValidator validator;
    
    @Test
    public void testCharValidation() {
        assertTrue(validator.isValid("1234567890", null));
        assertFalse(validator.isValid("12345678901", null));
    }
    
    @Test
    public void testNullValue() {
        assertTrue(validator.isValid(null, null));
    }
}
```

## 실무에서의 활용 사례

Spring Bean을 공용으로 사용하는 패턴은 다양한 상황에서 활용할 수 있습니다:

1. **공통 비즈니스 로직**: 여러 컨트롤러나 서비스에서 사용되는 비즈니스 로직
2. **유효성 검증**: 다양한 입력 필드에 적용되는 검증 규칙
3. **데이터 변환 로직**: 다양한 형태의 데이터를 표준화하는 변환 로직
4. **보안 처리**: 권한 검사, 데이터 암호화 등의 보안 관련 로직

## 결론

Spring Bean을 공용으로 사용하여 유효성 검증 로직을 관리하면 다음과 같은 이점이 있습니다:

1. **일관성**: 애플리케이션 전체에 동일한 검증 규칙 적용
2. **유지보수성**: 요구사항 변경 시 한 곳만 수정하면 전체 적용
3. **테스트 용이성**: 검증 로직을 독립적으로 테스트 가능
4. **확장성**: 기존 Bean을 확장하거나 조합하여 새로운 기능 구현 가능
