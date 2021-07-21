import pytest
import settings

from api import osf_api

from components.accessibility import ApplyA11yRules as a11y

from pages.preprints import (
    PreprintLandingPage,
    PreprintSubmitPage,
    PreprintDiscoverPage,
    PreprintDetailPage
)


class TestPreprintLandingPage:

    def test_accessibility(self, driver, session):
        landing_page = PreprintLandingPage(driver)
        landing_page.goto()
        assert PreprintLandingPage(driver, verify=True)
        a11y.run_axe(driver, session, 'preprints')


class TestPreprintSubmitPage:

    def test_accessibility(self, driver, session, must_be_logged_in):
        submit_page = PreprintSubmitPage(driver)
        submit_page.goto()
        assert PreprintSubmitPage(driver, verify=True)
        a11y.run_axe(driver, session, 'prepsub')


class TestPreprintDiscoverPage:

    def test_accessibility(self, driver, session):
        discover_page = PreprintDiscoverPage(driver)
        discover_page.goto()
        assert PreprintDiscoverPage(driver, verify=True)
        discover_page.loading_indicator.here_then_gone()
        a11y.run_axe(driver, session, 'prepdisc')


# TODO: Need to figure out a way to run this test in testing environments - some way to search on the
# Discover page and guarantee that the search results will be from current environment
@pytest.mark.skipif(not settings.PRODUCTION, reason='Cannot test on stagings as they share SHARE')
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
    """ For all the Branded Providers in each environment we are just going to load the landing page since the
    provider pages should be structured just like the OSF Preprint pages which we just tested above. The only
    real problems that we will be looking for is color contrast issues.
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
