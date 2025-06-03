plugins {
    kotlin("jvm") version "1.9.25"
    kotlin("plugin.spring") version "1.9.25"
    id("org.springframework.boot") version "3.5.0"
    id("io.spring.dependency-management") version "1.1.7"
}

group = "hellocucumber"
version = "0.0.1-SNAPSHOT"

val cucumberVersion = "7.11.2" // From cucumber-bom in the tutorial
val junitVersion = "5.9.2"     // From junit-bom in the tutorial
val kotlinTestVersion = "1.9.25" // From kotlin.version in the tutorial, or match your Kotlin plugin

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(17)
    }
}

repositories {
    mavenCentral()
}

dependencies {
    implementation("org.springframework.boot:spring-boot-starter")
    implementation("org.jetbrains.kotlin:kotlin-reflect")
    testImplementation("org.springframework.boot:spring-boot-starter-test")
    testImplementation("org.jetbrains.kotlin:kotlin-test-junit5")
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")

    // Kotlin Standard Library (usually included by the kotlin("jvm") plugin)
    //implementation("org.jetbrains.kotlin:kotlin-stdlib-jdk8") // Or just kotlin-stdlib

    // Cucumber Dependencies
    testImplementation(platform("io.cucumber:cucumber-bom:$cucumberVersion"))
    testImplementation("io.cucumber:cucumber-java") // Cucumber core for Java/Kotlin
    testImplementation("io.cucumber:cucumber-junit-platform-engine") // For running with JUnit Platform

    // JUnit 5 Dependencies (for the test runner and assertions)
    testImplementation(platform("org.junit:junit-bom:$junitVersion"))
    testImplementation("org.junit.platform:junit-platform-suite")
    //testImplementation("org.junit.jupiter:junit-jupiter") // Not strictly needed if platform-suite pulls it in, but good to be explicit

    // Kotlin Test (optional, but good for unit testing Kotlin code)
    //testImplementation("org.jetbrains.kotlin:kotlin-test:$kotlinTestVersion")

    // AssertJ for fluent assertions (as used in the tutorial's StepDefs)
    testImplementation("org.assertj:assertj-core:3.25.3") // Use a recent version
}

kotlin {
    compilerOptions {
        freeCompilerArgs.addAll("-Xjsr305=strict")
    }
}

tasks.withType<Test> {
    useJUnitPlatform()
}
