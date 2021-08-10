from selenium.webdriver.common.by import By

import settings
from base.locators import GroupLocator, Locator
from pages.base import OSFBasePage


class SearchPage(OSFBasePage):
    url = settings.OSF_HOME + '/search/'

    identity = Locator(By.ID, 'searchPageFullBar')
    search_bar = Locator(By.ID, 'searchPageFullBar')
    loading_indicator = Locator(By.CSS_SELECTOR, '.ball-scale')

    # Group Locators
    search_results = GroupLocator(By.CSS_SELECTOR, '.search-result')
