package hellocucumber

import io.cucumber.java.en.Given
import io.cucumber.java.en.When
import io.cucumber.java.en.Then
import org.assertj.core.api.Assertions.assertThat // Make sure you have the AssertJ dependency

// This function would typically go into your main source set (e.g., src/main/kotlin/hellocucumber/FridayLogic.kt)
// For simplicity in this tutorial, it's here.
fun isItFriday(today: String): String {
    // Initially, to make the first scenario pass:
    // return "Nope"
    // Later, to make both pass:
    return if (today == "Friday") "TGIF" else "Nope"
}

class StepDefs {
    private lateinit var today: String
    private lateinit var actualAnswer: String

    // For "Scenario Outline"
    @Given("today is {string}")
    fun today_is(day: String) {
        this.today = day
    }

    // Specific steps for the initial scenarios (will be replaced by the {string} version later)
    // @Given("today is Sunday")
    // fun today_is_Sunday() {
    //     today = "Sunday"
    // }

    // @Given("today is Friday")
    // fun today_is_Friday() {
    //     today = "Friday"
    // }

    @When("I ask whether it's Friday yet")
    fun i_ask_whether_it_s_Friday_yet() {
        actualAnswer = isItFriday(today) // Call our logic function
    }

    @Then("I should be told {string}")
    fun i_should_be_told(expectedAnswer: String) {
        assertThat(actualAnswer).isEqualTo(expectedAnswer)
    }
}