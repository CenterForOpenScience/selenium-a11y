import settings

from selenium.webdriver.common.by import By

from base.locators import Locator
from pages.base import OSFBasePage


class SupportPage(OSFBasePage):
    url = settings.OSF_HOME + '/support'

    identity = Locator(By.CSS_SELECTOR, '._Support_15i3vw', settings.LONG_TIMEOUT)
