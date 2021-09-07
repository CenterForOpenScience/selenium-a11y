import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import markers
import settings
from api import osf_api
from components.accessibility import ApplyA11yRules as a11y
from pages.preprints import (
    PreprintDetailPage,
    PreprintDiscoverPage,
    PreprintLandingPage,
    PreprintSubmitPage,
)


class TestPreprintLandingPage:
    def test_accessibility(self, driver, session):
        landing_page = PreprintLandingPage(driver)
        landing_page.goto()
        assert PreprintLandingPage(driver, verify=True)
        a11y.run_axe(driver, session, 'preprints')


class TestPreprintSubmitPage:
    @pytest.mark.skipif(
        not settings.PRODUCTION, reason='This version is only for Production'
    )
    def test_accessibility_prod(self, driver, session, must_be_logged_in):
        """This is a lite version of the Preprint Submit page test just for Production.
        It just navigates to the Submit page without attempting to start a new Preprint.
        """
        submit_page = PreprintSubmitPage(driver)
        submit_page.goto()
        assert PreprintSubmitPage(driver, verify=True)
        a11y.run_axe(driver, session, 'prepsub')

    @markers.dont_run_on_prod
    def test_accessibility_non_prod(
        self, driver, session, project_with_file, must_be_logged_in
    ):
        """This version of the Preprint Submit page test will run on any of the testing
        environments since it creates a fake project with file attached from which a new
        Preprint can be created. We do not want to do this in Production.
        """
        submit_page = PreprintSubmitPage(driver)
        submit_page.goto()
        assert PreprintSubmitPage(driver, verify=True)
        # Start the process of creating a new preprint so that we can get to the point
        #     where we can expand the Basics section before calling axe
        WebDriverWait(driver, 10).until(
            EC.visibility_of(submit_page.select_a_service_help_text)
        )
        submit_page.select_a_service_save_button.click()
        submit_page.upload_from_existing_project_button.click()
        submit_page.upload_project_selector.click()
        submit_page.upload_project_help_text.here_then_gone()
        submit_page.upload_project_selector_project.click()
        submit_page.upload_select_file.click()
        submit_page.upload_file_save_continue.click()
        submit_page.public_available_button.click()
        submit_page.public_data_input.click()
        submit_page.public_data_input.send_keys_deliberately('https://osf.io/')
        submit_page.scroll_into_view(submit_page.preregistration_no_button.element)
        submit_page.preregistration_no_button.click()
        submit_page.preregistration_input.click()
        submit_page.preregistration_input.send_keys_deliberately('QA Testing')
        submit_page.save_author_assertions.click()
        submit_page.basics_abstract_input.click()
        a11y.run_axe(driver, session, 'prepsub')


class TestPreprintDiscoverPage:
    def test_accessibility(self, driver, session):
        # The previous test (Submit page - non prod) may trigger a pop-up alert
        #     messagebox that leaving the page will cause data to not be saved.  At
        #     this point this seems to only be happening with Chrome.  If we get
        #     the alert then we need to accept it before moving on the rest of the
        #     test.
        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present())
            driver.switch_to.alert.accept()
        except TimeoutException:
            pass
        discover_page = PreprintDiscoverPage(driver)
        discover_page.goto()
        assert PreprintDiscoverPage(driver, verify=True)
        discover_page.loading_indicator.here_then_gone()
        a11y.run_axe(driver, session, 'prepdisc')


# TODO: Need to figure out a way to run this test in testing environments - some way
#     to search on the Discover page and guarantee that the search results will be
#     from current environment
@pytest.mark.skipif(
    not settings.PRODUCTION, reason='Cannot test on stagings as they share SHARE'
)
class TestPreprintDetailPage:
    def test_accessibility(self, driver, session):
        discover_page = PreprintDiscoverPage(driver)
        discover_page.goto()
        assert PreprintDiscoverPage(driver, verify=True)
        discover_page.loading_indicator.here_then_gone()
        # click on first entry in search results to open the Preprint Detail page
        discover_page.search_results[0].click()
        detail_page = PreprintDetailPage(driver, verify=True)
        # wait for authors list to fully load so that it doesn't trigger list violation
        detail_page.authors_load_indicator.here_then_gone()
        a11y.run_axe(driver, session, 'prepdet')


class TestBrandedProviders:
    """For all the Branded Providers in each environment we are just going to load the
    landing page since the provider pages should be structured just like the OSF Preprint
    pages which we just tested above. The only real problems that we will be looking for
    are color contrast issues.
    """

    def providers():
        """Return all preprint providers.
        """
        return osf_api.get_providers_list()

    @pytest.fixture(params=providers(), ids=[prov['id'] for prov in providers()])
    def provider(self, request):
        return request.param

    def test_accessibility(self, session, driver, provider):
        landing_page = PreprintLandingPage(driver, provider=provider)
        landing_page.goto()
        assert PreprintLandingPage(driver, verify=True)
        page_name = 'bp_' + provider['id']
        a11y.run_axe(driver, session, page_name)
