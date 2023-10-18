import pytest

import markers
from components.accessibility import ApplyA11yRules as a11y
from pages.user import (
    AccountSettingsPage,
    ConfigureAddonsPage,
    CreateDeveloperAppPage,
    CreatePersonalAccessTokenPage,
    EmberDeveloperAppsPage,
    EmberPersonalAccessTokenPage,
    NotificationsPage,
    ProfileInformationPage,
    UserProfilePage,
)


@markers.legacy_page
class TestUserProfilePage:
    def test_accessibility(
        self, driver, session, write_files, exclude_best_practice, must_be_logged_in
    ):
        profile_page = UserProfilePage(driver)
        profile_page.goto()
        assert UserProfilePage(driver, verify=True)
        pytest.xfail("Link-in-text-block issue documented here -> ENG-4875")
        a11y.run_axe(
            driver,
            session,
            'usrProf',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )


@markers.legacy_page
class TestUserSettingsProfileInformationPage:
    @pytest.fixture()
    def profile_information_page(self, driver, must_be_logged_in):
        profile_information_page = ProfileInformationPage(driver)
        profile_information_page.goto()
        return profile_information_page

    def test_accessibility_name_tab(
        self,
        driver,
        session,
        write_files,
        exclude_best_practice,
        profile_information_page,
    ):
        """Test Name Tab (default) of User Settings Profile Information Page"""
        assert ProfileInformationPage(driver, verify=True)
        a11y.run_axe(
            driver,
            session,
            'usrSetPrfName',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )

    def test_accessibility_social_tab(
        self,
        driver,
        session,
        write_files,
        exclude_best_practice,
        profile_information_page,
    ):
        """Test Social Tab of User Settings Profile Information Page"""
        # Running Axe in the previous step leaves you at the bottom of the page, so we
        # need to scroll back up to the Social tab link before we can click it and then
        # run Axe again.
        profile_information_page.scroll_into_view(
            profile_information_page.social_tab_link.element
        )
        profile_information_page.social_tab_link.click()
        assert ProfileInformationPage(driver, verify=True)
        a11y.run_axe(
            driver,
            session,
            'usrSetPrfSoc',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )

    def test_accessibility_employment_tab(
        self,
        driver,
        session,
        write_files,
        exclude_best_practice,
        profile_information_page,
    ):
        """Test Employment Tab of User Settings Profile Information Page"""
        # Running Axe in the previous step leaves you at the bottom of the page, so we
        # need to scroll back up to the Employment tab link before we can click it and then
        # run Axe again.
        profile_information_page.scroll_into_view(
            profile_information_page.employment_tab_link.element
        )
        profile_information_page.employment_tab_link.click()
        assert ProfileInformationPage(driver, verify=True)
        pytest.xfail("Label issue documented here -> ENG-3062")
        a11y.run_axe(
            driver,
            session,
            'usrSetPrfEmp',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )

    def test_accessibility_education_tab(
        self,
        driver,
        session,
        write_files,
        exclude_best_practice,
        profile_information_page,
    ):
        """Test Education Tab of User Settings Profile Information Page"""
        # Running Axe in the previous step leaves you at the bottom of the page, so we
        # need to scroll back up to the Education tab link before we can click it and then
        # run Axe again.
        profile_information_page.scroll_into_view(
            profile_information_page.education_tab_link.element
        )
        profile_information_page.education_tab_link.click()
        assert ProfileInformationPage(driver, verify=True)
        pytest.xfail("Label issue documented here -> ENG-3062")
        a11y.run_axe(
            driver,
            session,
            'usrSetPrfEd',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )


@markers.ember_page
class TestUserSettingsAccountSettingsPage:
    def test_accessibility(
        self, driver, session, write_files, exclude_best_practice, must_be_logged_in
    ):
        account_settings_page = AccountSettingsPage(driver)
        account_settings_page.goto()
        assert AccountSettingsPage(driver, verify=True)
        a11y.run_axe(
            driver,
            session,
            'usrSetAccnt',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )


@markers.legacy_page
class TestUserSettingsConfigureAddonsPage:
    def test_accessibility(
        self, driver, session, write_files, exclude_best_practice, must_be_logged_in
    ):
        configure_addons_page = ConfigureAddonsPage(driver)
        configure_addons_page.goto()
        assert ConfigureAddonsPage(driver, verify=True)
        a11y.run_axe(
            driver,
            session,
            'usrSetAddons',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )


@markers.legacy_page
class TestUserSettingsNotificationsPage:
    def test_accessibility(
        self, driver, session, write_files, exclude_best_practice, must_be_logged_in
    ):
        notifications_page = NotificationsPage(driver)
        notifications_page.goto()
        assert NotificationsPage(driver, verify=True)
        # wait for Notification Preferences section to finish loading
        notifications_page.loading_indicator.here_then_gone()
        pytest.xfail("Label issue documented here -> ENG-3074"
                     "Color-contrast issue documented here -> ENG-3075")
        a11y.run_axe(
            driver,
            session,
            'usrSetNtfctns',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )


@markers.ember_page
class TestUserSettingsDeveloperAppsPage:
    def test_accessibility(
        self, driver, session, write_files, exclude_best_practice, must_be_logged_in
    ):
        developer_apps_page = EmberDeveloperAppsPage(driver)
        developer_apps_page.goto()
        assert EmberDeveloperAppsPage(driver, verify=True)
        a11y.run_axe(
            driver,
            session,
            'usrSetDevApp',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )


@markers.ember_page
class TestUserSettingsCreateDeveloperAppPage:
    def test_accessibility(
        self, driver, session, write_files, exclude_best_practice, must_be_logged_in
    ):
        create_dev_app_page = CreateDeveloperAppPage(driver)
        create_dev_app_page.goto()
        assert CreateDeveloperAppPage(driver, verify=True)
        a11y.run_axe(
            driver,
            session,
            'usrSetCrtDevApp',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )


@markers.ember_page
class TestUserSettingsPersonalAccessTokensPage:
    def test_accessibility(
        self, driver, session, write_files, exclude_best_practice, must_be_logged_in
    ):
        personal_access_tokens_page = EmberPersonalAccessTokenPage(driver)
        personal_access_tokens_page.goto()
        assert EmberPersonalAccessTokenPage(driver, verify=True)
        a11y.run_axe(
            driver,
            session,
            'usrSetPAT',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )


@markers.ember_page
class TestUserSettingsCreatePersonalAccessTokenPage:
    def test_accessibility(
        self, driver, session, write_files, exclude_best_practice, must_be_logged_in
    ):
        create_personal_access_tokens_page = CreatePersonalAccessTokenPage(driver)
        create_personal_access_tokens_page.goto()
        assert CreatePersonalAccessTokenPage(driver, verify=True)
        a11y.run_axe(
            driver,
            session,
            'usrSetCrtPAT',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )
