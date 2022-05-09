from selenium.webdriver.common.by import By

import settings
from base.locators import ComponentLocator, Locator
from components.generic import SignUpForm
from components.navbars import EmberNavbar
from pages.base import OSFBasePage


class LandingPage(OSFBasePage):
    identity = Locator(By.CSS_SELECTOR, '._heroHeader_1qc5dv', settings.LONG_TIMEOUT)

    loading_indicator = Locator(By.CSS_SELECTOR, '.ball-scale')

    # Components
    navbar = ComponentLocator(EmberNavbar)
    sign_up_form = ComponentLocator(SignUpForm)


class LegacyLandingPage(OSFBasePage):
    waffle_override = {'ember_home_page': LandingPage}

    identity = Locator(By.CSS_SELECTOR, '._heroHeader_1qc5dv')


class RegisteredReportsLandingPage(OSFBasePage):
    url = settings.OSF_HOME + '/rr/'

    identity = Locator(By.CSS_SELECTOR, '.reg-landing-page-logo')
