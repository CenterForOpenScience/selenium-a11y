from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import markers
import settings
from api import osf_api
from components.accessibility import ApplyA11yRules as a11y
from pages.project import (
    AddonsPage,
    AnalyticsPage,
    ContributorsPage,
    FilesPage,
    FileViewPage,
    ForksPage,
    MetadataPage,
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


@markers.ember_page
class TestMetadataPage:
    def test_accessibility(
        self,
        driver,
        session,
        default_project,
        write_files,
        exclude_best_practice,
        must_be_logged_in,
    ):
        """For the Project Metadata page test we are creating a new dummy test project
        and then deleting it after we have finished unless we are running in Production,
        then we are using a Preferred Node from the environment settings file.
        """
        metadata_page = MetadataPage(driver, guid=default_project.id)
        metadata_page.goto()
        assert MetadataPage(driver, verify=True)
        metadata_page.loading_indicator.here_then_gone()
        a11y.run_axe(
            driver,
            session,
            'prjMeta',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )


@markers.ember_page
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
        # Wait until at least one of the files in the list is present
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test-select-file]'))
        )
        assert FilesPage(driver, verify=True)
        a11y.run_axe(
            driver,
            session,
            'prjFiles',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )


@markers.ember_page
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
        try:
            files_page = FilesPage(driver, guid=project_with_file.id)
            files_page.goto()
            # Wait until at least one of the files in the list is present
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '[data-test-select-file]')
                )
            )
            for file in files_page.file_rows:
                # open the first text file you find
                if '.txt' in file.text:
                    file.click()
                    break
            # Wait for the new tab to open - window count should then = 2
            WebDriverWait(driver, 5).until(EC.number_of_windows_to_be(2))
            # Switch focus to the new tab
            driver.switch_to.window(driver.window_handles[1])
            assert FileViewPage(driver, verify=True)
            # wait for iframe to load before running axe
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '#mfrIframeParent'))
            )
            a11y.run_axe(
                driver,
                session,
                'fileView',
                write_files=write_files,
                exclude_best_practice=exclude_best_practice,
            )
        finally:
            # Close the second tab that was opened. We do not want subsequent tests to
            # use the second tab.
            driver.close()
            # Switch focus back to the first tab
            driver.switch_to.window(driver.window_handles[0])


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
        then we are using a Preferred Node from the environment settings file.  Also
        if not running in Production, then we are creating a draft registration that
        will appear on the Draft Registrations tab of the Project Registrations page.
        """
        registrations_page = RegistrationsPage(driver, guid=default_project.id)
        registrations_page.goto()
        assert RegistrationsPage(driver, verify=True)
        if not settings.PRODUCTION:
            # First get the list of allowed registration schemas for OSF in a name and
            # id pair list. Then loop through the list to pull out just the id for the
            # Open-Ended Registration schema. We'll need this schema id to create the
            # draft.
            schema_list = osf_api.get_registration_schemas_for_provider(
                provider_id='osf'
            )
            for schema in schema_list:
                if schema[0] == 'Open-Ended Registration':
                    schema_id = schema[1]
                    break
            # Use the api to create a draft registration for the temporary project
            osf_api.create_draft_registration(
                session, node_id=default_project.id, schema_id=schema_id
            )
            # Reload the page so that the draft is visible on the Drafts tab
            registrations_page.reload()
            registrations_page.draft_registrations_tab.click()
            registrations_page.draft_registration_card.click()
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
