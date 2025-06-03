안녕하세요, 개발자 여러분! 이 가이드에서는 이미 진행 중이거나 새로 시작하는 Kotlin 기반의 Spring Boot 프로젝트에 [[Cucumber|Cucumber]]를 통합하여 [[행위 주도 개발(BDD)]] 방식의 테스트를 도입하는 구체적인 절차를 단계별로 상세히 안내합니다.

BDD는 개발자와 비개발자 간의 협업을 강화하고, 요구사항을 명확히 하며, 살아있는 문서를 통해 시스템의 행위를 관리할 수 있게 해주는 강력한 개발 방법론입니다. Cucumber는 이러한 BDD를 실현하는 데 사용되는 대표적인 도구입니다. 자, 이제 여러분의 Kotlin Spring Boot 프로젝트에 Cucumber를 차근차근 적용해 봅시다.

## 0단계: 준비물 확인

시작하기 전에 다음 환경이 준비되어 있는지 확인해주세요.

- **Kotlin 및 Spring Boot 프로젝트**: 신규 프로젝트를 생성하거나 기존 프로젝트를 사용합니다.
- **JDK**: Java Development Kit 17 이상을 권장합니다.
- **IntelliJ IDEA**: Kotlin 및 Spring 개발에 최적화된 IDE 사용을 권장합니다. (선택 사항)
- **Gradle**: Kotlin DSL (`build.gradle.kts`)을 사용하는 빌드 환경을 기준으로 설명합니다.

## 1단계: `build.gradle.kts` 의존성 설정

가장 먼저, Cucumber와 Spring Test 관련 라이브러리들을 프로젝트의 `build.gradle.kts` 파일에 추가해야 합니다.
```kotlin
// build.gradle.kts

plugins {
    // ... 기존 플러그인들
    kotlin("jvm") version "1.9.23" // 사용 중인 코틀린 버전
    kotlin("plugin.spring") version "1.9.23" // 스프링 플러그인
    id("org.springframework.boot") version "3.2.5" // 사용 중인 스프링 부트 버전
    // ...
}

// ... group, version 등

repositories {
    mavenCentral()
}

val cucumberVersion = "7.15.0" // 최신 안정 버전 사용 권장

dependencies {
    // Spring Boot
    implementation("org.springframework.boot:spring-boot-starter-web") // 예시: 웹 프로젝트인 경우
    implementation("org.jetbrains.kotlin:kotlin-reflect")
    // ... 기타 애플리케이션 의존성

    // Cucumber
    testImplementation(platform("io.cucumber:cucumber-bom:$cucumberVersion"))
    testImplementation("io.cucumber:cucumber-java")         // Cucumber Core (Kotlin에서도 사용)
    testImplementation("io.cucumber:cucumber-spring")        // Cucumber Spring 통합
    testImplementation("io.cucumber:cucumber-junit-platform-engine") // JUnit 5 연동

    // Spring Boot Test
    testImplementation("org.springframework.boot:spring-boot-starter-test") {
        exclude(group = "org.junit.vintage", module = "junit-vintage-engine") // JUnit 4 제외
    }

    // JUnit 5 (cucumber-junit-platform-engine이 의존하지만, 명시적으로 추가 가능)
    testImplementation("org.junit.platform:junit-platform-suite")
    testImplementation("org.junit.jupiter:junit-jupiter-api") // Optional: for other JUnit 5 tests
}

tasks.withType<Test> {
    useJUnitPlatform()
}
```

**핵심 의존성 설명:**

- `io.cucumber:cucumber-java`: Cucumber의 핵심 Java API입니다. Kotlin은 Java와 상호운용성이 뛰어나므로 이 라이브러리를 사용합니다.
- `io.cucumber:cucumber-spring`: Cucumber가 Spring 컨텍스트를 로드하고 Step Definition 클래스에 의존성을 주입할 수 있도록 지원합니다.
- `io.cucumber:cucumber-junit-platform-engine`: Cucumber 시나리오를 JUnit 5 테스트로 실행할 수 있게 해주는 엔진입니다.


의존성 추가 후에는 반드시 Gradle 프로젝트를 동기화(sync)해주세요. (IntelliJ IDEA에서는 우측 상단 코끼리 아이콘 클릭)

## 2단계: Cucumber 테스트 실행기 (Test Runner) 생성

Cucumber 시나리오를 JUnit Platform을 통해 실행하려면, 특정 어노테이션이 부착된 테스트 실행기 클래스가 필요합니다.

1. `src/test/kotlin` 디렉토리 아래에 애플리케이션의 테스트 루트 패키지(예: `com.example.demo.cucumber`)를 만듭니다.
2. 해당 패키지 내에 `CucumberIntegrationTest.kt` (또는 원하는 이름) 파일을 생성합니다.

```kotlin
// src/test/kotlin/com/example/demo/cucumber/CucumberIntegrationTest.kt
package com.example.demo.cucumber // 애플리케이션의 테스트 패키지에 맞게 수정

import io.cucumber.junit.platform.engine.Constants.GLUE_PROPERTY_NAME
import io.cucumber.junit.platform.engine.Constants.PLUGIN_PROPERTY_NAME
import org.junit.platform.suite.api.ConfigurationParameter
import org.junit.platform.suite.api.IncludeEngines
import org.junit.platform.suite.api.SelectClasspathResource
import org.junit.platform.suite.api.Suite

@Suite
@IncludeEngines("cucumber")
@SelectClasspathResource("features") // src/test/resources/features 디렉토리의 .feature 파일을 찾음
@ConfigurationParameter(key = PLUGIN_PROPERTY_NAME, value = "pretty, json:build/cucumber-reports/cucumber.json")
class CucumberIntegrationTest
```

**어노테이션 설명:**

- `@Suite`: 이 클래스가 JUnit Platform 테스트 스위트임을 나타냅니다.
- `@IncludeEngines("cucumber")`: Cucumber 테스트 엔진을 사용하도록 지정합니다.
- `@SelectClasspathResource("features")`: 클래스패스 상의 `features` 디렉토리에서 `.feature` 파일을 찾도록 지정합니다. 즉, `src/test/resources/features` 에 Feature 파일들을 위치시켜야 합니다.
- `@ConfigurationParameter(key = PLUGIN_PROPERTY_NAME, ...)`: 테스트 결과 출력 포맷을 지정합니다. `pretty`는 콘솔 가독성을 높이고, `json`은 보고서 생성을 위함입니다.

## 3단계: 첫 Feature 파일 작성

이제 실제 시스템의 행위를 정의하는 `.feature` 파일을 작성할 차례입니다.

1. `src/test/resources` 디렉토리 아래에 `features` 라는 새 디렉토리를 만듭니다. (위 `@SelectClasspathResource` 설정과 일치)
2. `features` 디렉토리 안에 `.feature` 확장자를 가진 파일을 생성합니다. 예를 들어, `greeting.feature` 파일을 만들어 보겠습니다.

```gherkin
# src/test/resources/features/greeting.feature
Feature: Greeter Service
  As a user
  I want to receive a personalized greeting
  So that I feel welcomed

  Scenario: Greeting a user with a name
    Given a user named "Alice"
    When the user requests a greeting
    Then the greeting message should be "Hello, Alice!"

  Scenario: Greeting a user without a name
    Given an anonymous user
    When the user requests a greeting
    Then the greeting message should be "Hello, Guest!"
```

이 파일은 [[Gherkin]]이라는 특정 형식을 따릅니다. `Feature`, `Scenario`, `Given`, `When`, `Then` 등의 키워드를 사용하여 사람이 읽기 쉬운 형태로 테스트 케이스를 작성합니다.

## 4단계: Kotlin Step Definition 파일 생성

Feature 파일에 작성된 각 Gherkin Step은 실제 실행될 Kotlin 코드로 연결되어야 합니다. 이 연결 코드를 Step Definition이라고 합니다.

1. 위 `GLUE_PROPERTY_NAME`에서 지정한 패키지(예: `com.example.demo.cucumber.steps`)를 `src/test/kotlin` 아래에 생성합니다.
2. 해당 패키지 안에 Kotlin 파일(예: `GreetingSteps.kt`)을 생성합니다.

```kotlin
// src/test/kotlin/com/example/demo/cucumber/steps/GreetingSteps.kt
package com.example.demo.cucumber.steps

import io.cucumber.java.en.Given
import io.cucumber.java.en.Then
import io.cucumber.java.en.When
import io.cucumber.spring.CucumberContextConfiguration
import org.assertj.core.api.Assertions.assertThat
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.test.context.SpringBootTest
// DemoApplication은 실제 Spring Boot 애플리케이션의 메인 클래스입니다.
// import com.example.demo.DemoApplication
// GreetingService는 테스트 대상 Spring Service (Java로 작성된 예시)입니다.
// import com.example.demo.service.GreetingService

// Spring Boot 애플리케이션 컨텍스트 로드를 위한 설정
// 실제 애플리케이션 클래스를 지정해야 합니다. (예: DemoApplication::class)
// classes 속성은 메인 애플리케이션 클래스나 테스트용 Configuration 클래스를 지정합니다.
@CucumberContextConfiguration
@SpringBootTest // (classes = [DemoApplication::class]) // 실제 Application Class 지정
class GreetingSteps {

    @Autowired
    private lateinit var greetingService: com.example.demo.service.GreetingService // 정식 경로로 GreetingService를 참조

    private var username: String? = null
    private lateinit var actualGreeting: String

    @Given("a user named {string}")
    fun `a user named`(name: String) {
        this.username = name
    }

    @Given("an anonymous user")
    fun `an anonymous user`() {
        this.username = null
    }

    @When("the user requests a greeting")
    fun `the user requests a greeting`() {
        this.actualGreeting = greetingService.getGreeting(this.username)
    }

    @Then("the greeting message should be {string}")
    fun `the greeting message should be`(expectedGreeting: String) {
        assertThat(this.actualGreeting).isEqualTo(expectedGreeting)
    }
}
```

**주요 사항:**

- **`@CucumberContextConfiguration` / `@SpringBootTest`**: 이 어노테이션들이 붙은 클래스를 통해 Cucumber는 Spring 애플리케이션 컨텍스트를 로드합니다. `SpringBootTest`에는 `classes` 속성으로 메인 애플리케이션 클래스 또는 테스트용 설정 클래스를 지정할 수 있습니다. **이 어노테이션은 Step Definition 파일 중 하나에만 위치하면 됩니다.**
- **패키지 위치**: 이 파일은 `CucumberIntegrationTest.kt`의 `GLUE_PROPERTY_NAME`에서 설정한 패키지 (`com.example.demo.cucumber.steps`) 내에 있어야 합니다.
- **어노테이션 (`@Given`, `@When`, `@Then`)**: Gherkin Step의 문자열과 정확히 일치하는 정규 표현식이나 문자열을 어노테이션 값으로 사용합니다. `{string}`과 같은 표현식은 해당 부분의 값을 메서드 파라미터로 전달받습니다.
- **Spring Bean 주입**: `@Autowired`를 사용하여 `GreetingService`와 같은 Spring Bean을 주입받아 테스트에 활용할 수 있습니다. (예시의 `GreetingService`는 사용자의 요청에 따라 Java로 작성된 Spring 컴포넌트입니다.)

## 5단계: 테스트 실행 및 BDD 사이클

이제 모든 설정이 완료되었습니다. 테스트를 실행해 보세요.

- **Gradle 사용**: 터미널에서 `./gradlew test` 명령을 실행합니다.
- **IntelliJ IDEA 사용**:
    - `CucumberIntegrationTest.kt` 파일을 열고 클래스명 옆의 실행 아이콘을 클릭합니다.
    - `.feature` 파일을 열고 시나리오 옆의 실행 아이콘을 클릭하여 개별 시나리오를 실행할 수도 있습니다.

**BDD 사이클 (Red -> Green -> Refactor):**

1. **Red**: 처음에는 `GreetingService` 구현이 없거나 Step Definition이 완벽하지 않아 테스트가 실패할 수 있습니다 (예: `UndefinedStepException`, `NullPointerException` 또는 Assertion 실패).
2. **Green**: `GreetingService.java` 파일을 `src/main/java/com/example/demo/service/`에 만들고, Gherkin 시나리오를 만족하도록 비즈니스 로직을 구현합니다. Step Definition 코드도 정확히 작성합니다. 테스트가 통과되면 녹색불이 켜집니다.
3. **Refactor**: 기능 변경 없이 코드의 구조를 개선합니다. 테스트는 계속 통과해야 합니다.

테스트 실행 후 `build/reports/tests/test/index.html`에서 HTML 형식의 테스트 결과 보고서를 확인할 수 있습니다. Cucumber JSON 리포트(`build/cucumber-reports/cucumber.json`)는 CI 서버 등에서 활용될 수 있습니다.

## 마무리

이것으로 Kotlin으로 작성된 Spring Boot 프로젝트에 Cucumber를 도입하는 기본적인 과정이 마무리되었습니다. Cucumber는 단순히 테스트 코드를 작성하는 것을 넘어, 명확한 요구사항 정의와 팀원 간의 원활한 소통을 돕는 강력한 도구입니다.

처음에는 Gherkin 문법과 Step Definition을 연결하는 과정이 다소 생소할 수 있지만, 몇 번의 연습을 통해 금방 익숙해질 수 있습니다. 이 가이드가 여러분의 BDD 여정에 튼튼한 디딤돌이 되길 바랍니다. 성공적인 Cucumber 도입을 응원합니다!