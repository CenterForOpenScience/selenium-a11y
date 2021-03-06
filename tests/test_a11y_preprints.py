import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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
    ReviewsDashboardPage,
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
            exclude_best_practice=exclude_best_practice,
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
            exclude_best_practice=exclude_best_practice,
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
            exclude_best_practice=exclude_best_practice,
        )


class TestPreprintDiscoverPage:
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
        discover_page = PreprintDiscoverPage(driver)
        discover_page.goto()
        assert PreprintDiscoverPage(driver, verify=True)
        discover_page.loading_indicator.here_then_gone()
        a11y.run_axe(
            driver,
            session,
            'prepdisc',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )


class TestPreprintDetailPage:
    def test_accessibility(self, driver, session, write_files, exclude_best_practice):
        discover_page = PreprintDiscoverPage(driver)
        discover_page.goto()
        assert PreprintDiscoverPage(driver, verify=True)
        if not settings.PRODUCTION:
            # Since all of the testing environments use the same SHARE server, we need
            # to enter a value in the search input box that will ensure that the results
            # are specific to the current environment.  We can do this by searching for
            # the test environment url in the identifiers metadata field.
            environment_url = settings.OSF_HOME[8:]  # Need to strip out "https://"
            search_text = 'identifiers:"' + environment_url + '"'
            discover_page.search_box.send_keys_deliberately(search_text)
            discover_page.search_box.send_keys(Keys.ENTER)
            if settings.STAGE2:
                # Stage 2 has a lot of old preprint data that is still listed in search
                # results but does not actually have preprint detail pages so we need to
                # sort the results so that the newest preprints are listed first.
                discover_page.sort_button.click()
                discover_page.sort_option_newest_to_oldest.click()
        discover_page.loading_indicator.here_then_gone()
        # click on first entry in search results to open the Preprint Detail page
        discover_page.search_results[0].click()
        detail_page = PreprintDetailPage(driver, verify=True)
        # wait for authors list to fully load so that it doesn't trigger list violation
        detail_page.authors_load_indicator.here_then_gone()
        a11y.run_axe(
            driver,
            session,
            'prepdet',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )


class TestBrandedProviders:
    """For all the Branded Providers in each environment we are just going to load the
    landing page since the provider pages should be structured just like the OSF Preprint
    pages which we just tested above. The only real problems that we will be looking for
    are color contrast issues.
    """

    def providers():
        """Return all preprint providers."""
        return osf_api.get_providers_list()

    @pytest.fixture(params=providers(), ids=[prov['id'] for prov in providers()])
    def provider(self, request):
        return request.param

    def test_accessibility(
        self, session, driver, provider, write_files, exclude_best_practice
    ):
        # As of January 24, 2022, the Engineering Archive ('engrxiv') preprint provider
        # has switched away from using OSF as their preprint service.  Therefore the
        # web page that OSF automatically redirects to is no longer based on the OSF
        # Preprints landing/discover page design.  However, they remain in our active
        # preprint provider list in the OSF api due to legal issues that are still being
        # worked out.  The best guess is that the transition will be completed (and
        # engrxiv removed from the api list) by the end of the first quarter of 2022
        # (i.e. end of March).  So to prevent this test from failing in Production
        # for 'engrxiv' we are going to skip the following steps for this provider.
        if 'engrxiv' not in provider['id']:
            landing_page = PreprintLandingPage(driver, provider=provider)
            landing_page.goto()
            assert PreprintLandingPage(driver, verify=True)
            page_name = 'bp_' + provider['id']
            a11y.run_axe(
                driver,
                session,
                page_name,
                write_files=write_files,
                exclude_best_practice=exclude_best_practice,
            )


# We do not currently have a user setup as an administrator or noderator for any of the
# preprint providers in production
@markers.dont_run_on_prod
class TestPreprintReviewsDashboardPage:
    """To test the Reviews Dashboard page we must login as a user that has been
    setup as an administrator or moderator for at least one of the preprint providers
    that has moderation enabled.
    """

    def test_accessibility(
        self, driver, session, write_files, exclude_best_practice, must_be_logged_in
    ):
        dashboard_page = ReviewsDashboardPage(driver)
        dashboard_page.goto()
        assert ReviewsDashboardPage(driver, verify=True)
        # Wait for list of preprints to load before calling axe
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div._action-body_zlyyw2'))
        )
        a11y.run_axe(
            driver,
            session,
            'revdash',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )


# We do not currently have a user setup as an administrator or noderator for any of the
# preprint providers in production
@markers.dont_run_on_prod
class TestProviderReviewsPages:
    """To test the provider specific Reviews pages we must login as a user that has been
    setup as an administrator or moderator for one of the preprint providers that has
    moderation enabled.  We are using MarXiv as the preprint provider since it exists
    in all testing environments and has the moderation process enabled in each
    environment.
    """

    @pytest.fixture
    def provider(self, driver):
        return osf_api.get_provider(type='preprints', provider_id='marxiv')

    def test_accessibility_reviews_submissions(
        self,
        driver,
        session,
        provider,
        write_files,
        exclude_best_practice,
        must_be_logged_in,
    ):
        submissions_page = ReviewsSubmissionsPage(driver, provider=provider)
        submissions_page.goto()
        assert ReviewsSubmissionsPage(driver, verify=True)
        # Wait for table to load before calling axe
        if submissions_page.no_submissions.absent():
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, '_submission-info_xkm0pa')
                )
            )
        a11y.run_axe(
            driver,
            session,
            'revsub',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
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
        # Wait for table to load before calling axe
        if withdrawals_page.no_requests.absent():
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, '_submission-info_17iwzt')
                )
            )
        a11y.run_axe(
            driver,
            session,
            'revwthdrwls',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
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
        moderators_page.goto()
        assert ReviewsModeratorsPage(driver, verify=True)
        # Wait for moderators list to load before calling axe
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, '_moderator-name_f83dob'))
        )
        a11y.run_axe(
            driver,
            session,
            'revmod',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
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
        # Wait for notifications elements load before calling axe
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'notification-title'))
        )
        a11y.run_axe(
            driver,
            session,
            'revnot',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
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
        a11y.run_axe(
            driver,
            session,
            'revset',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )
