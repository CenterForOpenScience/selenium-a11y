from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import markers
from api import osf_api
from components.accessibility import ApplyA11yRules as a11y
from pages.project import (
    AddonsPage,
    AnalyticsPage,
    ContributorsPage,
    FilesPage,
    FileViewPage,
    ForksPage,
    ProjectPage,
    RegistrationsPage,
    RequestAccessPage,
    SettingsPage,
    WikiPage,
)


@markers.legacy_page
class TestProjectPage:
    def test_accessibility(
        self,
        driver,
        session,
        default_project,
        write_files,
        exclude_best_practice,
        must_be_logged_in,
    ):
        """For the Project Overview page test we are creating a new dummy test project
        and then deleting it after we have finished unless we are running in Production,
        then we are using a Preferred Node from the environment settings file.
        """
        project_page = ProjectPage(driver, guid=default_project.id)
        project_page.goto()
        assert ProjectPage(driver, verify=True)
        # wait until file widget has fully loaded so that we can ensure that all sections
        # of project page have fully loaded before applying a11y rules
        project_page.file_widget.loading_indicator.here_then_gone()
        a11y.run_axe(
            driver,
            session,
            'project',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )


@markers.legacy_page
class TestFilesPage:
    def test_accessibility(
        self,
        driver,
        session,
        project_with_file,
        write_files,
        exclude_best_practice,
        must_be_logged_in,
    ):
        """For the Project Files page test we are creating a new dummy test project and
        then deleting it after we have finished unless we are running in Production, then
        we are using a Preferred Node from the environment settings file.
        """
        files_page = FilesPage(driver, guid=project_with_file.id)
        files_page.goto()
        files_page.loading_indicator.here_then_gone()
        assert FilesPage(driver, verify=True)
        a11y.run_axe(
            driver,
            session,
            'prjFiles',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )


@markers.legacy_page
class TestFileViewPage:
    def test_accessibility(
        self,
        driver,
        session,
        project_with_file,
        write_files,
        exclude_best_practice,
        must_be_logged_in,
    ):
        """For the File View page test we are creating a new dummy test project and
        then deleting it after we have finished unless we are running in Production,
        then we are using a Preferred Node from the environment settings file.
        """
        files_page = FilesPage(driver, guid=project_with_file.id)
        files_page.goto()
        files_page.loading_indicator.here_then_gone()
        # Wait until fangorn has loaded at least one of the files in the tree
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#tb-tbody div[data-level="3"]')
            )
        )
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located(
                (By.CSS_SELECTOR, '#tb-tbody .fa-refresh')
            )
        )
        for file in files_page.fangorn_rows:
            # open the first text file you find
            if '.txt' in file.text:
                file.click()
                break
        file_view_page = FileViewPage(driver, verify=True)
        # wait for file navigation menu and iframe to load before running axe
        file_view_page.file_nav_loading_indicator.here_then_gone()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'mfrIframe'))
        )
        a11y.run_axe(
            driver,
            session,
            'fileView',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )


@markers.legacy_page
class TestWikiPage:
    def test_accessibility(
        self,
        driver,
        session,
        default_project,
        write_files,
        exclude_best_practice,
        must_be_logged_in,
    ):
        """For the Wiki page test we are creating a new dummy test project and then
        deleting it after we have finished unless we are running in Production, then
        we are using a Preferred Node from the environment settings file.
        """
        wiki_page = WikiPage(driver, guid=default_project.id)
        wiki_page.goto()
        assert WikiPage(driver, verify=True)
        a11y.run_axe(
            driver,
            session,
            'prjWiki',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )


@markers.ember_page
class TestAnalyticsPage:
    def test_accessibility(
        self,
        driver,
        session,
        default_project,
        write_files,
        exclude_best_practice,
        must_be_logged_in,
    ):
        """For the Analytics page test we are creating a new dummy test project and
        then deleting it after we have finished unless we are running in Production,
        then we are using a Preferred Node from the environment settings file.
        """
        analytics_page = AnalyticsPage(driver, guid=default_project.id)
        analytics_page.goto()
        assert AnalyticsPage(driver, verify=True)
        # wait until analytics graphs load
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.keen-dataviz-stage'))
        )
        a11y.run_axe(
            driver,
            session,
            'prjAnlytcs',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )


@markers.ember_page
class TestRegistrationsPage:
    def test_accessibility(
        self,
        driver,
        session,
        default_project,
        write_files,
        exclude_best_practice,
        must_be_logged_in,
    ):
        """For the Registrations page test we are creating a new dummy test project
        and then deleting it after we have finished unless we are running in Production,
        then we are using a Preferred Node from the environment settings file.
        """
        registrations_page = RegistrationsPage(driver, guid=default_project.id)
        registrations_page.goto()
        assert RegistrationsPage(driver, verify=True)
        # wait until Registration cards are loaded if there are any
        registrations_page.first_registration_title.present()
        a11y.run_axe(
            driver,
            session,
            'prjReg',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )


@markers.legacy_page
class TestContributorsPage:
    def test_accessibility(
        self,
        driver,
        session,
        default_project,
        write_files,
        exclude_best_practice,
        must_be_logged_in,
    ):
        """For the Contributors page test we are creating a new dummy test project
        and then deleting it after we have finished unless we are running in Production,
        then we are using a Preferred Node from the environment settings file.
        """
        contributors_page = ContributorsPage(driver, guid=default_project.id)
        contributors_page.goto()
        assert ContributorsPage(driver, verify=True)
        a11y.run_axe(
            driver,
            session,
            'prjCntrb',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )


@markers.legacy_page
class TestAddonsPage:
    def test_accessibility(
        self,
        driver,
        session,
        default_project,
        write_files,
        exclude_best_practice,
        must_be_logged_in,
    ):
        """For the Add-ons page test we are creating a new dummy test project and then
        deleting it after we have finished unless we are running in Production, then we
        are using a Preferred Node from the environment settings file.
        """
        addons_page = AddonsPage(driver, guid=default_project.id)
        addons_page.goto()
        assert AddonsPage(driver, verify=True)
        a11y.run_axe(
            driver,
            session,
            'prjAddons',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )


@markers.legacy_page
class TestSettingsPage:
    def test_accessibility(
        self,
        driver,
        session,
        default_project,
        write_files,
        exclude_best_practice,
        must_be_logged_in,
    ):
        """For the Settings page test we are creating a new dummy test project and
        then deleting it after we have finished unless we are running in Production,
        then we are using a Preferred Node from the environment settings file.
        """
        settings_page = SettingsPage(driver, guid=default_project.id)
        settings_page.goto()
        settings_page.email_notifications_loading_indicator.here_then_gone()
        assert SettingsPage(driver, verify=True)
        a11y.run_axe(
            driver,
            session,
            'prjSttngs',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )


@markers.ember_page
@markers.dont_run_on_prod
class TestForksPage:
    def test_accessibility(
        self,
        driver,
        session,
        default_project,
        write_files,
        exclude_best_practice,
        must_be_logged_in,
    ):
        """For the Forks page test we are creating a new dummy test project and
        then deleting it after we have finished - also deleting the new fork that
        is created
        """
        forks_page = ForksPage(driver, guid=default_project.id)
        forks_page.goto()
        assert ForksPage(driver, verify=True)
        # create a new fork so that we can make sure that data display is a11y compliant
        forks_page.new_fork_button.click()
        forks_page.create_fork_modal_button.click()
        forks_page.info_toast.present()
        forks_page.reload()
        forks_page.verify()
        forks_page.fork_authors.present()
        assert len(forks_page.listed_forks) == 1
        # clean-up leftover fork
        fork_guid = forks_page.fork_link.get_attribute('data-test-node-title')
        osf_api.delete_project(session, fork_guid, None)
        a11y.run_axe(
            driver,
            session,
            'prjForks',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )


@markers.legacy_page
class TestRequestAccessPage:
    def test_accessibility(
        self,
        driver,
        session,
        default_project_page,
        write_files,
        exclude_best_practice,
        must_be_logged_in_as_user_two,
    ):
        """For the Request Access page test we are creating a new dummy test project
        and then deleting it after we have finished unless we are running in Production,
        then we are using a Preferred Node from the environment settings file.
        """
        default_project_page.goto(expect_redirect_to=RequestAccessPage)
        assert RequestAccessPage(driver, verify=True)
        a11y.run_axe(
            driver,
            session,
            'prjReqAcc',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )
