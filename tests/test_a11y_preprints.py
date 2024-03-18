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
    PreprintLandingPage,
    PreprintSubmitPage,
    ReviewsDashboardPage,
    BrandedPreprintsDiscoverPage,
    ReviewsModeratorsPage,
    ReviewsNotificationsPage,
    ReviewsSettingsPage,
    ReviewsSubmissionsPage,
    ReviewsWithdrawalsPage,
)


class TestPreprintLandingPage:
    def test_accessibility(self, driver, session, write_files, exclude_best_practice):
        landing_page = PreprintLandingPage(driver)
        landing_page.goto()
        assert PreprintLandingPage(driver, verify=True)
        a11y.run_axe(
            driver,
            session,
            'preprints',
            write_files=write_files,
            exclude_best_practice=True,
        )


class TestPreprintSubmitPage:
    @pytest.mark.skipif(
        not settings.PRODUCTION, reason='This version is only for Production'
    )
    def test_accessibility_prod(
        self, driver, session, write_files, exclude_best_practice, must_be_logged_in
    ):
        """This is a lite version of the Preprint Submit page test just for Production.
        It just navigates to the Submit page without attempting to start a new Preprint.
        """
        submit_page = PreprintSubmitPage(driver)
        submit_page.goto()
        assert PreprintSubmitPage(driver, verify=True)
        a11y.run_axe(
            driver,
            session,
            'prepsub',
            write_files=write_files,
            exclude_best_practice=True,
        )

    @markers.dont_run_on_prod
    def test_accessibility_non_prod(
        self,
        driver,
        session,
        project_with_file,
        write_files,
        exclude_best_practice,
        must_be_logged_in,
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
        a11y.run_axe(
            driver,
            session,
            'prepsub',
            write_files=write_files,
            exclude_best_practice=True,
        )


class TestPreprintDetailPage:
    def test_accessibility(self, driver, session, write_files, exclude_best_practice):
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

        # Use api to get the most recent published preprint and then navigate to the
        # detail page for that preprint
        preprint_node = osf_api.get_most_recent_preprint_node_id()
        detail_page = PreprintDetailPage(driver, guid=preprint_node)
        detail_page.goto()
        assert PreprintDetailPage(driver, verify=True)

        a11y.run_axe(
            driver,
            session,
            'prepdet',
            write_files=write_files,
            exclude_best_practice=True,
        )


class TestBrandedProviders:
    """For all the Branded Providers in each environment we are loading both the
    Branded Landing Page and Branded Discover Page.
    """

    def providers():
        """Return all preprint providers."""
        return osf_api.get_providers_list()

    @pytest.fixture(params=providers(), ids=[prov['id'] for prov in providers()])
    def provider(self, request):
        return request.param

    def test_accessibility_landing(
        self, session, driver, provider, write_files, exclude_best_practice
    ):
        if provider['id'] in settings.providers_leaving_OSF:
            pytest.skip()

        landing_page = PreprintLandingPage(driver, provider=provider)
        landing_page.goto()
        assert PreprintLandingPage(driver, verify=True)
        page_name = 'bp_' + provider['id']
        a11y.run_axe(
            driver,
            session,
            page_name,
            write_files=write_files,
            exclude_best_practice=True,
        )

    def test_accessibility_discover(
        self, session, driver, provider, write_files, exclude_best_practice
    ):
        if provider['id'] in settings.providers_leaving_OSF:
            pytest.skip()

        discover_page = BrandedPreprintsDiscoverPage(driver, provider=provider)
        discover_page.goto()
        assert BrandedPreprintsDiscoverPage(driver, verify=True)
        page_name = 'bp_' + provider['id'] + '_disc'
        a11y.run_axe(
            driver,
            session,
            page_name,
            write_files=write_files,
            exclude_best_practice=True,
        )


# We do not currently have a user setup as an administrator or moderator for any of the
# preprint providers in production
@markers.dont_run_on_prod
class TestPreprintReviewsDashboardPage:
    """To test the Reviews Dashboard page we must log in as a user that has been
    set up as an administrator or moderator for at least one of the preprint providers
    that has moderation enabled.
    """

    def test_accessibility(
        self, driver, session, write_files, exclude_best_practice, must_be_logged_in
    ):
        dashboard_page = ReviewsDashboardPage(driver)
        dashboard_page.goto()
        assert ReviewsDashboardPage(driver, verify=True)
        dashboard_page.loading_indicator.here_then_gone()
        a11y.run_axe(
            driver,
            session,
            'revdash',
            write_files=write_files,
            exclude_best_practice=True,
        )


# We do not currently have a user setup as an administrator or moderator for any of the
# preprint providers in production
@markers.dont_run_on_prod
class TestProviderReviewsPages:
    """To test the provider specific Reviews pages we must log in as a user that has been
    set up as an administrator or moderator for one of the preprint providers that has
    moderation enabled.  We are using selpremod as the preprint provider since it exists
    in all testing environments and has the moderation process enabled in each
    environment.
    """

    @pytest.fixture
    def provider(self, driver):
        return osf_api.get_provider(type='preprints', provider_id='selpremod')

    def test_accessibility_reviews_submissions(
        self,
        driver,
        session,
        provider,
        write_files,
        exclude_best_practice,
        must_be_logged_in,
    ):
        # There is a weird routing issue where you have to go to the Reviews Dashboard
        # page first and then you can go to the Reviews Submissions page. If you try to
        # go directly to the Reviews Submissions page first you get redirected back to
        # the Reviews Dashboard page anyway.
        dashboard_page = ReviewsDashboardPage(driver)
        dashboard_page.goto()
        assert ReviewsDashboardPage(driver, verify=True)
        submissions_page = ReviewsSubmissionsPage(driver, provider=provider)
        submissions_page.goto()
        assert ReviewsSubmissionsPage(driver, verify=True)
        submissions_page.loading_indicator.here_then_gone()
        a11y.run_axe(
            driver,
            session,
            'revsub',
            write_files=write_files,
            exclude_best_practice=True,
        )

    def test_accessibility_reviews_withdrawals(
        self,
        driver,
        session,
        provider,
        write_files,
        exclude_best_practice,
        must_be_logged_in,
    ):
        withdrawals_page = ReviewsWithdrawalsPage(driver, provider=provider)
        withdrawals_page.goto()
        assert ReviewsWithdrawalsPage(driver, verify=True)
        withdrawals_page.loading_indicator.here_then_gone()
        a11y.run_axe(
            driver,
            session,
            'revwthdrwls',
            write_files=write_files,
            exclude_best_practice=True,
        )

    def test_accessibility_reviews_moderators(
        self,
        driver,
        session,
        provider,
        write_files,
        exclude_best_practice,
        must_be_logged_in,
    ):
        moderators_page = ReviewsModeratorsPage(driver, provider=provider)
        # TODO: Fix this goto() statement.
        print(
            'Moderators Page URL: {}'.format(moderators_page.url)
        )
        moderators_page.goto()
        assert ReviewsModeratorsPage(driver, verify=True)
        moderators_page.loading_indicator.here_then_gone()
        a11y.run_axe(
            driver,
            session,
            'revmod',
            write_files=write_files,
            exclude_best_practice=1,
        )

    def test_accessibility_reviews_notifications(
        self,
        driver,
        session,
        provider,
        write_files,
        exclude_best_practice,
        must_be_logged_in,
    ):
        notifications_page = ReviewsNotificationsPage(driver, provider=provider)
        notifications_page.goto()
        assert ReviewsNotificationsPage(driver, verify=True)
        notifications_page.loading_indicator.here_then_gone()
        a11y.run_axe(
            driver,
            session,
            'revnot',
            write_files=write_files,
            exclude_best_practice=True,
        )

    def test_accessibility_reviews_settings(
        self,
        driver,
        session,
        provider,
        write_files,
        exclude_best_practice,
        must_be_logged_in,
    ):
        settings_page = ReviewsSettingsPage(driver, provider=provider)
        settings_page.goto()
        assert ReviewsSettingsPage(driver, verify=True)
        settings_page.loading_indicator.here_then_gone()
        a11y.run_axe(
            driver,
            session,
            'revset',
            write_files=write_files,
            exclude_best_practice=True,
        )
