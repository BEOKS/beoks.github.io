package com.beoks.cucumberkotlin

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication

@SpringBootApplication
class CucumberKotlinApplication

fun main(args: Array<String>) {
	runApplication<CucumberKotlinApplication>(*args)
}
