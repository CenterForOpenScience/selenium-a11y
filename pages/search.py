from selenium.webdriver.common.by import By

import settings
from base.locators import GroupLocator, Locator
from pages.base import OSFBasePage


class SearchPage(OSFBasePage):
    url = settings.OSF_HOME + "/search/"

    identity = Locator(By.CSS_SELECTOR, 'div[data-analytics-scope="Search page main"]')
    search_input = Locator(
        By.CSS_SELECTOR, ".ember-text-field.ember-view._search-input_fvrbco"
    )
    search_button = Locator(By.CSS_SELECTOR, "button[data-test-search-submit]")
    loading_indicator = Locator(By.CSS_SELECTOR, ".ball-scale")

    # Group Locators
    search_results = GroupLocator(By.CSS_SELECTOR, ".search-result")
