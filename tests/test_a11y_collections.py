import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import markers
from api import osf_api
from components.accessibility import ApplyA11yRules as a11y
from pages.collections import (
    CollectionDiscoverPage,
    CollectionModerationAcceptedPage,
    CollectionModerationModeratorsPage,
    CollectionModerationPendingPage,
    CollectionModerationRejectedPage,
    CollectionModerationRemovedPage,
    CollectionModerationSettingsPage,
    CollectionSubmitPage,
)


@markers.ember_page
class TestCollectionDiscoverPages:
    """This test will load the Discover page for each active Collection Provider that
    exists in an environment.
    """

    def providers():
        """Return collection providers to be used in Discover page test. The list of
        collections in some environments (i.e. Staging2) has gotten very long, so a way
        to narrow the list is to set allow_submssions to False in the admin app and we
        can then skip those old testing collections."""
        all_prov = osf_api.get_providers_list(type='collections')
        return [prov for prov in all_prov if prov['attributes']['allow_submissions']]

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


# We do not currently have a user setup as an administrator for any of the collections
# in production
@markers.dont_run_on_prod
@markers.ember_page
class TestModerationPages:
    """To test the Moderation pages we must login as a user that has been setup as an
    administrator or moderator for one of the collection providers that has moderation
    enabled.  We are using the 'selenium' collection since it exists in all testing
    environments and has the moderation process enabled in each environment.
    """

    @pytest.fixture
    def provider(self, driver):
        return osf_api.get_provider(type='collections', provider_id='selenium')

    def test_accessibility_moderation_pending(
        self,
        driver,
        session,
        provider,
        write_files,
        exclude_best_practice,
        must_be_logged_in,
    ):
        pending_page = CollectionModerationPendingPage(driver, provider=provider)
        pending_page.goto()
        assert CollectionModerationPendingPage(driver, verify=True)
        pending_page.loading_indicator.here_then_gone()
        a11y.run_axe(
            driver,
            session,
            'colmodpend',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )

    def test_accessibility_moderation_accepted(
        self,
        driver,
        session,
        provider,
        write_files,
        exclude_best_practice,
        must_be_logged_in,
    ):
        accepted_page = CollectionModerationAcceptedPage(driver, provider=provider)
        accepted_page.goto()
        assert CollectionModerationAcceptedPage(driver, verify=True)
        accepted_page.loading_indicator.here_then_gone()
        a11y.run_axe(
            driver,
            session,
            'colmodacpt',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )

    def test_accessibility_moderation_rejected(
        self,
        driver,
        session,
        provider,
        write_files,
        exclude_best_practice,
        must_be_logged_in,
    ):
        rejected_page = CollectionModerationRejectedPage(driver, provider=provider)
        rejected_page.goto()
        assert CollectionModerationRejectedPage(driver, verify=True)
        rejected_page.loading_indicator.here_then_gone()
        a11y.run_axe(
            driver,
            session,
            'colmodrej',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )

    def test_accessibility_moderation_removed(
        self,
        driver,
        session,
        provider,
        write_files,
        exclude_best_practice,
        must_be_logged_in,
    ):
        removed_page = CollectionModerationRemovedPage(driver, provider=provider)
        removed_page.goto()
        assert CollectionModerationRemovedPage(driver, verify=True)
        removed_page.loading_indicator.here_then_gone()
        a11y.run_axe(
            driver,
            session,
            'colmodrem',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )

    def test_accessibility_moderation_moderators(
        self,
        driver,
        session,
        provider,
        write_files,
        exclude_best_practice,
        must_be_logged_in,
    ):
        moderators_page = CollectionModerationModeratorsPage(driver, provider=provider)
        moderators_page.goto()
        assert CollectionModerationModeratorsPage(driver, verify=True)
        moderators_page.loading_indicator.here_then_gone()
        a11y.run_axe(
            driver,
            session,
            'colmodmods',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )

    def test_accessibility_moderation_settings(
        self,
        driver,
        session,
        provider,
        write_files,
        exclude_best_practice,
        must_be_logged_in,
    ):
        settings_page = CollectionModerationSettingsPage(driver, provider=provider)
        settings_page.goto()
        assert CollectionModerationSettingsPage(driver, verify=True)
        settings_page.loading_indicator.here_then_gone()
        a11y.run_axe(
            driver,
            session,
            'colmodset',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )
