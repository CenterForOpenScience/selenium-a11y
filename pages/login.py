from selenium.webdriver.common.by import By

import settings
from base.exceptions import LoginError
from base.locators import Locator, GroupLocator
from pages.base import BasePage, OSFBasePage


class LoginPage(BasePage):
    url = settings.OSF_HOME + '/login'

    identity = Locator(By.ID, 'loginForm', settings.LONG_TIMEOUT)
    username_input = Locator(By.ID, 'username')
    password_input = Locator(By.ID, 'password')
    submit_button = Locator(By.NAME, 'submit')
    remember_me_checkbox = Locator(By.ID, 'rememberMe')
    institutional_login_button = Locator(By.ID, 'instnLogin')
    orcid_login_button = Locator(By.ID, 'orcidlogin')

    if 'localhost:5000' in settings.OSF_HOME:
        submit_button = Locator(By.ID, 'submit')
        identity = Locator(By.ID, 'login')

    def error_handling(self):
        if '/login' not in self.driver.current_url:
            raise LoginError('Already logged in')

    def submit_login(self, user, password):
        self.username_input.send_keys(user)
        if ('localhost:5000' not in settings.OSF_HOME):
            self.password_input.send_keys(password)
            if self.remember_me_checkbox.is_selected():
                self.remember_me_checkbox.click()
        self.submit_button.click()


class InstitutionalLoginPage(BasePage):
    url = settings.OSF_HOME + '/login?campaign=institution'

    identity = Locator(By.CSS_SELECTOR, '#institutionSelect')
    dropdown_options = GroupLocator(By.CSS_SELECTOR, '#institutionSelect option')


def login(driver, user=settings.USER_ONE, password=settings.USER_ONE_PASSWORD):
    login_page = LoginPage(driver)
    login_page.goto()
    login_page.submit_login(user, password)


def safe_login(driver, user=settings.USER_ONE, password=settings.USER_ONE_PASSWORD):
    """Raise a LoginError if login fails.
    """
    login(driver, user=user, password=password)
    if not OSFBasePage(driver).is_logged_in():
        raise LoginError('Login failed')


def logout(driver):
    """Log the user out.
    """
    driver.get(settings.OSF_HOME + '/logout/')
