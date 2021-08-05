from selenium.webdriver.common.by import By

import settings
from base.exceptions import LoginError
from base.locators import GroupLocator, Locator
from pages.base import BasePage, OSFBasePage


class LoginPage(BasePage):
    url = settings.OSF_HOME + '/login'

    identity = Locator(By.ID, 'loginForm', settings.LONG_TIMEOUT)
    username_input = Locator(By.ID, 'username')
    password_input = Locator(By.ID, 'password')
    login_error_message = Locator(By.CLASS_NAME, 'login-error-inline')
    submit_button = Locator(By.NAME, 'submit')
    remember_me_checkbox = Locator(By.ID, 'rememberMe')
    institutional_login_button = Locator(By.ID, 'instnLogin')
    orcid_login_button = Locator(By.ID, 'orcidlogin')
    osf_home_link = Locator(By.CSS_SELECTOR, '.navbar-link')
    sign_up_button = Locator(By.ID, 'osfRegister')
    reset_password_link = Locator(By.LINK_TEXT, 'Reset password')
    need_help_link = Locator(By.LINK_TEXT, 'Need help signing in?')
    cos_footer_link = Locator(By.LINK_TEXT, 'Center for Open Science')
    terms_of_use_footer_link = Locator(By.LINK_TEXT, 'Terms of Use')
    privacy_policy_footer_link = Locator(By.LINK_TEXT, 'Privacy Policy')
    status_footer_link = Locator(By.LINK_TEXT, 'Status')

    if 'localhost:5000' in settings.OSF_HOME:
        submit_button = Locator(By.ID, 'submit')
        identity = Locator(By.ID, 'login')

    def error_handling(self):
        if '/login' not in self.driver.current_url:
            raise LoginError('Already logged in')

    def submit_login(self, user, password):
        self.username_input.send_keys(user)
        if 'localhost:5000' not in settings.OSF_HOME:
            self.password_input.send_keys(password)
            if self.remember_me_checkbox.is_selected():
                self.remember_me_checkbox.click()
        self.submit_button.click()


class Login2FAPage(BasePage):

    identity = Locator(By.ID, 'totploginForm')
    username_input = Locator(By.ID, 'username')
    oneTimePassword_input = Locator(By.ID, 'oneTimePassword')
    login_error_message = Locator(By.CLASS_NAME, 'login-error-inline')
    verify_button = Locator(By.NAME, 'submit')
    cancel_link = Locator(By.LINK_TEXT, 'Cancel')
    need_help_link = Locator(By.LINK_TEXT, 'Need help signing in?')


class LoginToSPage(BasePage):

    identity = Locator(By.ID, 'tosloginForm')
    terms_of_use_link = Locator(By.LINK_TEXT, 'Terms of Use')
    privacy_policy_link = Locator(By.LINK_TEXT, 'Privacy Policy')
    tos_checkbox = Locator(By.ID, 'termsOfServiceChecked')
    continue_button = Locator(By.ID, 'primarySubmitButton')
    cancel_link = Locator(By.LINK_TEXT, 'Cancel and go back to OSF')


class InstitutionalLoginPage(BasePage):
    url = settings.OSF_HOME + '/login?campaign=institution'

    identity = Locator(By.CSS_SELECTOR, '#institutionSelect')
    institution_dropdown = Locator(By.ID, 'institutionSelect')
    sign_in_button = Locator(By.ID, 'institutionSubmit')
    osf_home_link = Locator(By.CSS_SELECTOR, '.navbar-link')
    sign_up_button = Locator(By.ID, 'osfRegister')
    cant_find_institution_link = Locator(By.LINK_TEXT, "I can't find my institution")
    need_help_link = Locator(By.LINK_TEXT, 'Need help signing in?')
    sign_in_with_osf_link = Locator(By.LINK_TEXT, 'Sign in with your OSF account')
    cos_footer_link = Locator(By.LINK_TEXT, 'Center for Open Science')
    terms_of_use_footer_link = Locator(By.LINK_TEXT, 'Terms of Use')
    privacy_policy_footer_link = Locator(By.LINK_TEXT, 'Privacy Policy')
    status_footer_link = Locator(By.LINK_TEXT, 'Status')

    dropdown_options = GroupLocator(By.CSS_SELECTOR, '#institutionSelect option')


class InstitutionForgotPasswordPage(BasePage):
    url = settings.OSF_HOME + '/forgotpassword-institution/'

    identity = Locator(By.ID, 'forgotPasswordForm')


class ForgotPasswordPage(BasePage):
    url = settings.OSF_HOME + '/forgotpassword/'

    identity = Locator(By.ID, 'forgotPasswordForm')


class UnsupportedInstitutionLoginPage(BasePage):
    url = settings.CAS_DOMAIN + '/login?campaign=unsupportedinstitution'

    identity = Locator(By.ID, 'osfUnsupportedInstitutionLogin')
    set_password_button = Locator(By.NAME, 'submit')


class GenericCASPage(BasePage):
    url = settings.CAS_DOMAIN

    identity = Locator(By.CLASS_NAME, 'login-error-card')
    navbar_brand = Locator(By.CLASS_NAME, 'cas-brand-text')
    auto_redirect_message = Locator(
        By.CSS_SELECTOR,
        '#content > div > section > section.text-without-mdi.text-center.text-bold.text-large.margin-large-vertical.title',
    )
    status_message = Locator(
        By.CSS_SELECTOR, '#content > div > section > section.card-message > h2'
    )
    error_detail = Locator(
        By.CSS_SELECTOR, '#content > div > section > section.card-message > pre'
    )


class CASAuthorizationPage(BasePage):
    url = settings.CAS_DOMAIN + '/oauth2/authorize'

    identity = Locator(By.CLASS_NAME, 'login-section')
    navbar_brand = Locator(By.CLASS_NAME, 'cas-brand-text')
    status_message = Locator(
        By.CSS_SELECTOR, '#content > div > section > section.card-message > h2'
    )
    allow_button = Locator(By.ID, 'allow')
    deny_button = Locator(By.ID, 'deny')


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
