from time import sleep

from selenium.webdriver.common.by import By

import settings
from base.locators import BaseElement, Locator


class SignUpForm(BaseElement):
    name_input = Locator(By.NAME, "fullName")
    email_one_input = Locator(By.NAME, "email1")
    email_two_input = Locator(By.NAME, "email2")
    password_input = Locator(By.NAME, "password")
    terms_of_service_checkbox = Locator(By.NAME, "acceptedTermsOfService")
    sign_up_button = Locator(By.CSS_SELECTOR, "[data-test-sign-up-button]")
    registration_success = Locator(
        By.CSS_SELECTOR, ".ext-success", settings.LONG_TIMEOUT
    )

    def click_recaptcha(self):
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
        # only click the captcha checkbox if it isn't already checked
        if (
            Locator(By.ID, "recaptcha-anchor")
            .get_element(self.driver, "recaptcha-anchor")
            .get_attribute("aria-checked")
            == "false"
        ):
            Locator(By.CSS_SELECTOR, ".recaptcha-checkbox-border").get_element(
                self.driver, "capcha"
            ).click()
        self.driver.switch_to.default_content()
        sleep(2)
