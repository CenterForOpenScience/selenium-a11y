from selenium.webdriver.common.by import By

import settings
from base.locators import ComponentLocator, Locator
from components.generic import SignUpForm
from pages.base import OSFBasePage


class EmberRegisterPage(OSFBasePage):
    url = settings.OSF_HOME + '/register'

    identity = Locator(By.CSS_SELECTOR, '._sign-up-container_19kgff')

    # Components
    sign_up_form = ComponentLocator(SignUpForm)


class RegisterPage(OSFBasePage):

    waffle_override = {'ember_auth_register': EmberRegisterPage}

    url = settings.OSF_HOME + '/register'

    identity = Locator(By.CSS_SELECTOR, '#signUpScope')
