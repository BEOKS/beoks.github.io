package hellocucumber

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication

@SpringBootApplication
class CucumberKotlinGradleApplication

fun main(args: Array<String>) {
    runApplication<CucumberKotlinGradleApplication>(*args)
}
