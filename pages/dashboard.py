from selenium.webdriver.common.by import By

import components.dashboard as components
import settings
from base.locators import ComponentLocator, Locator
from components.navbars import EmberNavbar
from pages.base import OSFBasePage


class DashboardPage(OSFBasePage):
    url = settings.OSF_HOME + "/dashboard/"

    identity = Locator(
        By.CSS_SELECTOR, 'div[data-analytics-scope="Dashboard"]', settings.LONG_TIMEOUT
    )
    loading_indicator = Locator(By.CSS_SELECTOR, ".ball-scale")
    create_project_button = Locator(
        By.CSS_SELECTOR,
        "[data-test-create-project-modal-button]",
        settings.LONG_TIMEOUT,
    )
    collections_link = Locator(By.CSS_SELECTOR, "a[data-test-products-collections]")
    registries_link = Locator(By.CSS_SELECTOR, "a[data-test-products-registries]")
    institutions_link = Locator(By.CSS_SELECTOR, "a[data-test-products-institutions]")
    preprints_link = Locator(By.CSS_SELECTOR, "a[data-test-products-preprints]")
    view_meetings_button = Locator(
        By.CSS_SELECTOR, 'a[data-analytics-name="meetings_button"]'
    )
    view_preprints_button = Locator(
        By.CSS_SELECTOR, 'a[data-analytics-name="preprints_button"]'
    )
    first_noteworthy_project = Locator(
        By.CSS_SELECTOR, "[data-test-noteworthy-project]", settings.LONG_TIMEOUT
    )

    # Components
    navbar = ComponentLocator(EmberNavbar)
    create_project_modal = ComponentLocator(components.EmberCreateProjectModal)
    project_created_modal = ComponentLocator(components.EmberProjectCreatedModal)
    project_list = ComponentLocator(components.EmberProjectList, settings.LONG_TIMEOUT)
