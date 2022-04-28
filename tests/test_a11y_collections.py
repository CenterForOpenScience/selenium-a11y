import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import markers
from api import osf_api
from components.accessibility import ApplyA11yRules as a11y
from pages.collections import CollectionDiscoverPage, CollectionSubmitPage


@markers.ember_page
class TestCollectionDiscoverPages:
    """This test will load the Discover page for each Collection Provider that exists in
    an environment.
    """

    def providers():
        """Return all collection providers."""
        return osf_api.get_providers_list(type='collections')

    @pytest.fixture(params=providers(), ids=[prov['id'] for prov in providers()])
    def provider(self, request):
        return request.param

    def test_accessibility(
        self, session, driver, provider, write_files, exclude_best_practice
    ):
        discover_page = CollectionDiscoverPage(driver, provider=provider)
        discover_page.goto()
        assert CollectionDiscoverPage(driver, verify=True)
        discover_page.loading_indicator.here_then_gone()
        page_name = 'cp_' + provider['id']
        a11y.run_axe(
            driver,
            session,
            page_name,
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )


@markers.ember_page
class TestCollectionSubmitPage:
    """This test is for the Collection Submit page which is accessed by the "Add to
    Collection" link in the navigation bar of a Collection Provider.  The Collection
    Providers available in each environment are inconsistent.  So we are only accessing
    the Submit page for the Character Lab Collection since this provider exists in every
    environment.
    """

    @pytest.fixture
    def provider(self, driver):
        return osf_api.get_provider(type='collections', provider_id='characterlab')

    def test_accessibility(
        self,
        driver,
        session,
        provider,
        project_with_file,
        write_files,
        exclude_best_practice,
        must_be_logged_in,
    ):
        submit_page = CollectionSubmitPage(driver, provider=provider)
        submit_page.goto()
        assert CollectionSubmitPage(driver, verify=True)
        # Continue process until Project contributors section is expanded before
        #     calling axe
        submit_page.project_selector.click()
        submit_page.project_help_text.here_then_gone()
        submit_page.project_selector_project.click()
        submit_page.project_metadata_save.click()
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '[data-test-project-contributors-list-item-name]')
            )
        )
        a11y.run_axe(
            driver,
            session,
            'collsub',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )
        # Leaving this page without saving causes an alert pop-up in Chrome which will
        # cause the next test run after this one to fail. So we want to trigger the
        # alert here and then accept it.
        submit_page.reload()
        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present())
            driver.switch_to.alert.accept()
        except TimeoutException:
            pass
