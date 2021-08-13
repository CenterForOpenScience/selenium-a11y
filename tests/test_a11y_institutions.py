import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import markers
from api import osf_api
from components.accessibility import ApplyA11yRules as a11y
from pages.institutions import (
    InstitutionAdminDashboardPage,
    InstitutionBrandedPage,
    InstitutionsLandingPage,
)


class TestInstitutionsLandingPage:
    def test_accessibility(self, driver, session):
        landing_page = InstitutionsLandingPage(driver)
        landing_page.goto()
        assert InstitutionsLandingPage(driver, verify=True)
        a11y.run_axe(driver, session, 'institutions')


class TestBrandedInstitutionPages:
    """ Test the Branded Institution Page for each institution in the environment. Use the osf api to get
    the list of institution ids and then load each branded iinstitution page and run the axe test engine.
    """

    def institutions():
        """ Return all institution ids.
        """
        return osf_api.get_all_institutions(data_type='ids')

    @pytest.fixture(params=institutions())
    def institution(self, request):
        return request.param

    def test_accessibility(self, driver, session, institution):
        institution_page = InstitutionBrandedPage(driver, institution_id=institution)
        institution_page.goto()
        assert InstitutionBrandedPage(driver, verify=True)
        # first check if the collection is empty - this may often be the case in the test environments
        if institution_page.empty_collection_indicator.absent():
            # wait for projects table to start loading before calling axe
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '#tb-tbody > div > div > div.tb-row')
                )
            )
        page_name = 'bi_' + institution
        a11y.run_axe(driver, session, page_name)


# Can't run this is Production since I don't have admin access to any institutions in Production
@markers.dont_run_on_prod
class TestInstitutionAdminDashboardPage:
    def test_accessibility(self, driver, session, must_be_logged_in):
        """ Test using the COS admin dahsboard page - user must already be setup as an admin for the
        COS institution in each environment through the OSF admin app.
        """
        dashboard_page = InstitutionAdminDashboardPage(driver, institution_id='cos')
        dashboard_page.goto()
        assert InstitutionAdminDashboardPage(driver, verify=True)
        dashboard_page.loading_indicator.here_then_gone()
        a11y.run_axe(driver, session, 'biadmindash')
