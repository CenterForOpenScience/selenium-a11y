from selenium.webdriver.common.by import By

import settings
from base.locators import Locator
from pages.base import BasePage


class COSDonatePage(BasePage):
    url = 'https://www.cos.io/about/support-cos'

    # This meta tag is unique to the donate page but cannot be verified as a 'visible' locator
    # See https://github.com/cos-qa/osf-selenium-tests/blob/b7f3f21376b7d6f751993cdcffea9262856263e3/base/locators.py#L157-L163
    identity = Locator(
        By.XPATH,
        '//meta[@name="cos:id" and @content="donate-page"]',
        settings.LONG_TIMEOUT,
    )
