package hellocucumber

import io.cucumber.junit.platform.engine.Constants
import org.junit.platform.suite.api.ConfigurationParameter
import org.junit.platform.suite.api.IncludeEngines
import org.junit.platform.suite.api.SelectClasspathResource
import org.junit.platform.suite.api.Suite

@Suite
@IncludeEngines("cucumber")
@SelectClasspathResource("hellocucumber") // Tells Cucumber to look for features in src/test/resources/hellocucumber
@ConfigurationParameter(key = Constants.PLUGIN_PROPERTY_NAME, value = "pretty, json:build/cucumber-report/cucumber.json") // "pretty" for console output, json for reports
class RunCucumberTest