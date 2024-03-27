from selenium.webdriver.common.by import By

import settings
from base.locators import ComponentLocator, GroupLocator, Locator
from components.navbars import InstitutionsNavbar
from pages.base import OSFBasePage


class InstitutionsLandingPage(OSFBasePage):
    url = settings.OSF_HOME + "/institutions/"

    # TODO fix insitution typo
    identity = Locator(
        By.CSS_SELECTOR, "div[data-test-insitutions-header]", settings.TIMEOUT
    )

    search_bar = Locator(By.CSS_SELECTOR, ".ember-text-field")

    # Group Locators
    institution_list = GroupLocator(By.CSS_SELECTOR, "div[data-test-institution-name]")

    navbar = ComponentLocator(InstitutionsNavbar)


class BaseInstitutionPage(OSFBasePage):

    base_url = settings.OSF_HOME + "/institutions/"
    url_addition = ""

    def __init__(self, driver, verify=False, institution_id=""):
        self.institution_id = institution_id
        super().__init__(driver, verify)

    @property
    def url(self):
        return self.base_url + self.institution_id + self.url_addition


class InstitutionBrandedPage(BaseInstitutionPage):

    identity = Locator(By.CSS_SELECTOR, "img[data-test-institution-banner]")

    empty_collection_indicator = Locator(
        By.CSS_SELECTOR, "[data-test-search-page-no-results]"
    )

    # Group Locators
    project_list = GroupLocator(
        By.CSS_SELECTOR, "a[data-test-search-result-card-title]"
    )


class InstitutionAdminDashboardPage(BaseInstitutionPage):

    url_addition = "/dashboard"

    identity = Locator(By.CSS_SELECTOR, 'div[data-analytics-scope="Dashboard"]')
    loading_indicator = Locator(By.CSS_SELECTOR, ".ball-scale", settings.LONG_TIMEOUT)
