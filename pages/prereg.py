from selenium.webdriver.common.by import By

import settings
from base.locators import Locator
from pages.base import OSFBasePage


class PreregLandingPage(OSFBasePage):
    url = settings.OSF_HOME + '/prereg/'

    identity = Locator(
        By.CSS_SELECTOR, 'body > div.watermarked > div > div > h1 > img'
    )  # TODO: Ignore bad locator - will change in emberization
    start_prereg_button = Locator(
        By.CSS_SELECTOR,
        'body > div.watermarked > div > div > div.row.hidden-xs > table > tbody > tr:nth-child(1) > td:nth-child(1) > div',
    )
    continue_draft_button = Locator(
        By.CSS_SELECTOR,
        'body > div.watermarked > div > div > div.row.hidden-xs > table > tbody > tr:nth-child(1) > td:nth-child(2) > div',
    )
    register_existing_project_button = Locator(
        By.CSS_SELECTOR,
        'body > div.watermarked > div > div > div.row.hidden-xs > table > tbody > tr:nth-child(1) > td:nth-child(3) > div',
    )
    new_prereg_input = Locator(By.CSS_SELECTOR, '#newPrereg > input')
