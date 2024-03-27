import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import markers
import settings
from api import osf_api
from components.accessibility import ApplyA11yRules as a11y
from pages.login import safe_login
from pages.registrations import MyRegistrationsPage
from pages.registries import (
    BrandedRegistriesDiscoverPage,
    DraftRegistrationGenericPage,
    DraftRegistrationMetadataPage,
    DraftRegistrationReviewPage,
    RegistrationAddNewPage,
    RegistrationDetailPage,
    RegistrationFileDetailPage,
    RegistrationFileListPage,
    RegistrationMetadataPage,
    RegistrationResourcesPage,
    RegistriesLandingPage,
    RegistriesModerationModeratorsPage,
    RegistriesModerationPendingPage,
    RegistriesModerationSettingsPage,
    RegistriesModerationSubmittedPage,
)


@markers.ember_page
class TestRegistriesLandingPage:
    def test_accessibility(self, driver, session, write_files, exclude_best_practice):
        landing_page = RegistriesLandingPage(driver)
        landing_page.goto()
        assert RegistriesLandingPage(driver, verify=True)
        a11y.run_axe(
            driver,
            session,
            "registries",
            write_files=write_files,
            exclude_best_practice=True,
        )


@markers.ember_page
class TestRegistrationDetailPage:
    """This test is for the Registration Overview Page for a submitted registration."""

    def test_accessibility(self, driver, session, write_files, exclude_best_practice):
        # Use OSF api to get the most recent submitted and approved registration and
        # navigate to its overview page.
        registration_guid = osf_api.get_most_recent_registration_node_id(session)
        registration_page = RegistrationDetailPage(driver, guid=registration_guid)
        registration_page.goto()
        assert RegistrationDetailPage(driver, verify=True)
        registration_page.loading_indicator.here_then_gone()
        a11y.run_axe(
            driver,
            session,
            "regdet",
            write_files=write_files,
            exclude_best_practice=True,
        )


# User with registrations is not setup in production
@markers.dont_run_on_prod
@markers.ember_page
class TestMyRegistrationsPage:
    def test_accessibility(self, driver, session, write_files, exclude_best_practice):
        safe_login(
            driver,
            user=settings.A11Y_REGISTRATIONS_USER,
            password=settings.A11Y_REGISTRATIONS_PASSWORD,
        )
        my_registrations_page = MyRegistrationsPage(driver)
        my_registrations_page.goto()
        assert MyRegistrationsPage(driver, verify=True)
        # Wait for node cards to be visible before calling axe
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test-node-card]"))
        )
        a11y.run_axe(
            driver,
            session,
            "myreg",
            write_files=write_files,
            exclude_best_practice=True,
        )


@markers.ember_page
class TestAddNewRegistrationPage:
    def test_accessibility(
        self, driver, session, write_files, exclude_best_practice, must_be_logged_in
    ):
        add_new_registration_page = RegistrationAddNewPage(driver)
        add_new_registration_page.goto()
        assert RegistrationAddNewPage(driver, verify=True)
        pytest.xfail("aria-command-name issue documented here -> ENG-5354")
        pytest.xfail("link-in-text-block issue documented here -> ENG-5355")
        a11y.run_axe(
            driver,
            session,
            "addnewreg",
            write_files=write_files,
            exclude_best_practice=True,
        )


@pytest.fixture(scope="class")
def log_in_as_user_with_draft_registrations(driver):
    safe_login(
        driver,
        user=settings.A11Y_REGISTRATIONS_USER,
        password=settings.A11Y_REGISTRATIONS_PASSWORD,
    )


# User with registrations is not setup in production
@markers.dont_run_on_prod
class TestSubmittedRegistrationPages:
    @pytest.fixture()
    def my_registrations_page(self, driver, log_in_as_user_with_draft_registrations):
        """Fixture that logs in as a user that already has submitted registrations
        and navigates to the My Registrations page from which the desired registration
        can be selected.
        """
        my_registrations_page = MyRegistrationsPage(driver)
        my_registrations_page.goto()

        # Wait for registration cards to load on page
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test-node-card]"))
        )
        registration_cards = my_registrations_page.registration_cards
        assert registration_cards
        return my_registrations_page

    @markers.ember_page
    def test_accessibility_files_list_page(
        self, driver, session, write_files, exclude_best_practice, my_registrations_page
    ):
        """This test is for checking the accessibility of the Registration File List
        Page of a submitted registration.  First search through the registration cards
        on the Submitted tab of the My Registration Page for the registration that has
        files (searching by registration title).  When you find the desired registration
        get the registration node id from its link and then use the node id to navigate
        to the Files List page for this registration.
        """
        registration_node = my_registrations_page.get_node_id_by_title(
            "Registration With Files for A11y Testing"
        )
        registration_file_list_page = RegistrationFileListPage(
            driver, guid=registration_node
        )
        registration_file_list_page.goto()
        assert RegistrationFileListPage(driver, verify=True)
        # Click the 'Archive of OSF Storage' button to expand the list of files
        registration_file_list_page.file_list_button.click()
        # Wait for file list items to load on page
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[data-test-file-list-item]")
            )
        )
        a11y.run_axe(
            driver,
            session,
            "regfilelist",
            write_files=write_files,
            exclude_best_practice=True,
        )

    @markers.ember_page
    def test_accessibility_file_detail_page(
        self, driver, session, write_files, exclude_best_practice, my_registrations_page
    ):
        """This test is for checking the accessibility of the Registration File Detail
        Page of a submitted registration.  First search through the registration cards
        on the Submitted tab of the My Registration Page for the registration that has
        files (searching by registration title).  When you find the desired registration
        get the registration node id from its link and then use the node id to navigate
        to the Files List page for this registration.  Then click the first file link
        to open the File Detail page for that file.
        """
        registration_node = my_registrations_page.get_node_id_by_title(
            "Registration With Files for A11y Testing"
        )
        registration_file_list_page = RegistrationFileListPage(
            driver, guid=registration_node
        )
        registration_file_list_page.goto()
        assert RegistrationFileListPage(driver, verify=True)
        # Click the 'Archive of OSF Storage' button to expand the list of files
        registration_file_list_page.file_list_button.click()
        # Wait for file list items to load on page
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[data-test-file-list-item]")
            )
        )
        try:
            # Click the first file from the list to open the File Detail page in a new tab
            registration_file_list_page.scroll_into_view(
                registration_file_list_page.first_file_link.element
            )
            registration_file_list_page.first_file_link.click()
            # Wait for the new tab to open - window count should then = 2
            WebDriverWait(driver, 5).until(EC.number_of_windows_to_be(2))
            # Switch focus to the new tab
            driver.switch_to.window(driver.window_handles[1])
            assert RegistrationFileDetailPage(driver)
            # Wait for File Renderer to load
            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "iframe"))
            )
            a11y.run_axe(
                driver,
                session,
                "regfiledet",
                write_files=write_files,
                exclude_best_practice=True,
            )
        finally:
            # Close the second tab that was opened. We do not want subsequent tests to
            # use the second tab.
            driver.close()
            # Switch focus back to the first tab
            driver.switch_to.window(driver.window_handles[0])

    @markers.ember_page
    def test_accessibility_resources_page(
        self, driver, session, write_files, exclude_best_practice, my_registrations_page
    ):
        """This test is for checking the accessibility of the Registration Resources
        Page of a submitted registration.  First search through the registration cards
        on the Submitted tab of the My Registration Page for the registration that has
        resources (searching by registration title).  When you find the desired
        registration get the registration node id from its link and then use the node
        id to navigate to the Resources page for this registration.
        """
        registration_node = my_registrations_page.get_node_id_by_title(
            "Registration With Files for A11y Testing"
        )
        registration_resources_page = RegistrationResourcesPage(
            driver, guid=registration_node
        )
        registration_resources_page.goto()
        assert RegistrationResourcesPage(driver, verify=True)
        # Wait for first resource card to load on page
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[data-test-resource-card-type]")
            )
        )
        a11y.run_axe(
            driver,
            session,
            "regresources",
            write_files=write_files,
            exclude_best_practice=True,
        )

    @markers.ember_page
    def test_accessibility_metadata_page(
        self, driver, session, write_files, exclude_best_practice, my_registrations_page
    ):
        """This test is for checking the accessibility of the Registration Metadata
        Page of a submitted registration.  First search through the registration cards
        on the Submitted tab of the My Registration Page for a specific registration
        (searching by registration title).  When you find the desired registration get
        the registration node id from its link and then use the node id to navigate to
        the Meatadata page for this registration.
        """
        registration_node = my_registrations_page.get_node_id_by_title(
            "Registration With Files for A11y Testing"
        )
        registration_metadata_page = RegistrationMetadataPage(
            driver, guid=registration_node
        )
        registration_metadata_page.goto()
        assert RegistrationMetadataPage(driver, verify=True)
        registration_metadata_page.loading_indicator.here_then_gone()
        a11y.run_axe(
            driver,
            session,
            "regmeta",
            write_files=write_files,
            exclude_best_practice=True,
        )


# User with registrations is not setup in production
@markers.dont_run_on_prod
class TestDraftRegistrationPages:
    @pytest.fixture()
    def my_registrations_page(self, driver, log_in_as_user_with_draft_registrations):
        """Fixture that logs in as a user that already has draft registrations created
        for the various templates/schemas and navigates to the My Registrations page
        from which the desired draft registration type can be selected.
        """
        my_registrations_page = MyRegistrationsPage(driver)
        my_registrations_page.goto()
        my_registrations_page.drafts_tab.click()
        # Wait for draft cards to load on page
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[data-test-draft-registration-card]")
            )
        )
        draft_cards = my_registrations_page.draft_registration_cards
        assert draft_cards
        return my_registrations_page

    @markers.ember_page
    def test_accessibility_metadata_page(
        self, driver, session, write_files, exclude_best_practice, my_registrations_page
    ):
        """This test is for checking the accessibility of the Draft Registration Metadata
        page.  We can just pick the first draft registration that is listed, since the
        Metadata page is the same for all schemas.
        """
        # capture draft id from link url of 1st draft title and use that to go to page
        url = my_registrations_page.draft_registration_title.get_attribute("href")
        draft_id = url.split("drafts/", 1)[1]
        metadata_page = DraftRegistrationMetadataPage(driver, draft_id=draft_id)
        metadata_page.goto()
        assert DraftRegistrationMetadataPage(driver, verify=True)
        a11y.run_axe(
            driver,
            session,
            "drftregmeta",
            write_files=write_files,
            exclude_best_practice=True,
        )

    @markers.ember_page
    def test_accessibility_summary_page(
        self, driver, session, write_files, exclude_best_practice, my_registrations_page
    ):
        """This test is for checking the accessibility of the Draft Registration Summary
        Page which is typically the second page on an Open-Ended Registration template.
        Since the user also has other types of draft registrations, we must search through
        the cards on the Drafts tab of the My Registrations page and find the card for an
        Open-Ended Registration and then capture it's draft id so that we can use it to
        navigate to it's Summary page.
        """
        # Capture the draft id from the first Open-Ended Registration that is listed
        draft_id = my_registrations_page.get_first_draft_id_by_template(
            "Open-Ended Registration"
        )
        summary_page = DraftRegistrationGenericPage(
            driver, draft_id=draft_id, url_addition="1-summary"
        )
        summary_page.goto()
        assert summary_page.page_heading.text == "Summary"
        # Wait for file widget to load before calling axe
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[data-test-files-list-for]")
            )
        )
        a11y.run_axe(
            driver,
            session,
            "drftregsum",
            write_files=write_files,
            exclude_best_practice=True,
        )

    def test_accessibility_study_information_page(
        self, driver, session, write_files, exclude_best_practice, my_registrations_page
    ):
        """This test is for checking the accessibility of the Draft Registration Study
        Information Page which is the second page on a Qualitative Preregistration template.
        Since the user also has other types of draft registrations, we must search through
        the cards on the Drafts tab of the My Registrations page and find the card for a
        Qualitative Preregistration and then capture it's draft id so that we can use it to
        navigate to it's Study Information page.
        """
        # Capture the draft id from the first Qualitative Preregistration that is listed
        draft_id = my_registrations_page.get_first_draft_id_by_template(
            "Qualitative Preregistration"
        )
        study_information_page = DraftRegistrationGenericPage(
            driver, draft_id=draft_id, url_addition="1-study-information"
        )
        study_information_page.goto()
        assert study_information_page.page_heading.text == "Study Information"
        a11y.run_axe(
            driver,
            session,
            "drftregstudy",
            write_files=write_files,
            exclude_best_practice=True,
        )

    def test_accessibility_data_collection_page(
        self, driver, session, write_files, exclude_best_practice, my_registrations_page
    ):
        """This test is for checking the accessibility of the Draft Registration Data
        Collection Page which is the fourth page on a Qualitative Preregistration template.
        Since the user also has other types of draft registrations, we must search through
        the cards on the Drafts tab of the My Registrations page and find the card for a
        Qualitative Preregistration and then capture it's draft id so that we can use it to
        navigate to it's Study Information page.
        """
        # Capture the draft id from the first Qualitative Preregistration that is listed
        draft_id = my_registrations_page.get_first_draft_id_by_template(
            "Qualitative Preregistration"
        )
        data_collection_page = DraftRegistrationGenericPage(
            driver, draft_id=draft_id, url_addition="3-data-collection"
        )
        data_collection_page.goto()
        assert data_collection_page.page_heading.text == "Data Collection"
        a11y.run_axe(
            driver,
            session,
            "drftregdatacol",
            write_files=write_files,
            exclude_best_practice=True,
        )

    def test_accessibility_miscellaneous_page(
        self, driver, session, write_files, exclude_best_practice, my_registrations_page
    ):
        """This test is for checking the accessibility of the Draft Registration
        Miscellaneous Page which is the sixth page on a Qualitative Preregistration
        template.  Since the user also has other types of draft registrations, we must
        search through the cards on the Drafts tab of the My Registrations page and
        find the card for a Qualitative Preregistration and then capture it's draft
        id so that we can use it to navigate to it's Miscellaneous page.
        """
        # Capture the draft id from the first Qualitative Preregistration that is listed
        draft_id = my_registrations_page.get_first_draft_id_by_template(
            "Qualitative Preregistration"
        )
        miscellaneous_page = DraftRegistrationGenericPage(
            driver, draft_id=draft_id, url_addition="5-miscellaneous"
        )
        miscellaneous_page.goto()
        assert miscellaneous_page.page_heading.text == "Miscellaneous"
        a11y.run_axe(
            driver,
            session,
            "drftregmisc",
            write_files=write_files,
            exclude_best_practice=True,
        )

    def test_accessibility_design_plan_page(
        self, driver, session, write_files, exclude_best_practice, my_registrations_page
    ):
        """This test is for checking the accessibility of the Draft Registration Design
        Plan Page which is the third page on an OSF Preregistration template.  Since the
        user also has other types of draft registrations, we must search through the cards
        on the Drafts tab of the My Registrations page and find the card for an OSF
        Preregistration and then capture it's draft id so that we can use it to navigate
        to it's Design Plan page.
        """
        # Capture the draft id from the first OSF Preregistration that is listed
        draft_id = my_registrations_page.get_first_draft_id_by_template(
            "OSF Preregistration"
        )
        design_plan_page = DraftRegistrationGenericPage(
            driver, draft_id=draft_id, url_addition="2-design-plan"
        )
        design_plan_page.goto()
        assert design_plan_page.page_heading.text == "Design Plan"
        # Wait for file widget to load before calling axe
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[data-test-files-list-for]")
            )
        )
        a11y.run_axe(
            driver,
            session,
            "drftregdesign",
            write_files=write_files,
            exclude_best_practice=True,
        )

    def test_accessibility_sampling_plan_page(
        self, driver, session, write_files, exclude_best_practice, my_registrations_page
    ):
        """This test is for checking the accessibility of the Draft Registration Sampling
        Plan Page which is the fourth page on an OSF Preregistration template.  Since the
        user also has other types of draft registrations, we must search through the cards
        on the Drafts tab of the My Registrations page and find the card for an OSF
        Preregistration and then capture it's draft id so that we can use it to navigate
        to it's Design Plan page.
        """
        # Capture the draft id from the first OSF Preregistration that is listed
        draft_id = my_registrations_page.get_first_draft_id_by_template(
            "OSF Preregistration"
        )
        sampling_plan_page = DraftRegistrationGenericPage(
            driver, draft_id=draft_id, url_addition="3-sampling-plan"
        )
        sampling_plan_page.goto()
        assert sampling_plan_page.page_heading.text == "Sampling Plan"
        # Wait for file widget to load before calling axe
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[data-test-files-list-for]")
            )
        )
        a11y.run_axe(
            driver,
            session,
            "drftregsampling",
            write_files=write_files,
            exclude_best_practice=True,
        )

    def test_accessibility_variables_page(
        self, driver, session, write_files, exclude_best_practice, my_registrations_page
    ):
        """This test is for checking the accessibility of the Draft Registration Variables
        Page which is the fifth page on an OSF Preregistration template.  Since the user
        also has other types of draft registrations, we must search through the cards on
        the Drafts tab of the My Registrations page and find the card for an OSF
        Preregistration and then capture it's draft id so that we can use it to navigate
        to it's Variables page.
        """
        # Capture the draft id from the first OSF Preregistration that is listed
        draft_id = my_registrations_page.get_first_draft_id_by_template(
            "OSF Preregistration"
        )
        variables_page = DraftRegistrationGenericPage(
            driver, draft_id=draft_id, url_addition="4-variables"
        )
        variables_page.goto()
        assert variables_page.page_heading.text == "Variables"
        # Wait for file widget to load before calling axe
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[data-test-files-list-for]")
            )
        )
        a11y.run_axe(
            driver,
            session,
            "drftregvariables",
            write_files=write_files,
            exclude_best_practice=True,
        )

    def test_accessibility_analysis_plan_page(
        self, driver, session, write_files, exclude_best_practice, my_registrations_page
    ):
        """This test is for checking the accessibility of the Draft Registration Analysis
        Plan Page which is the sixth page on an OSF Preregistration template.  Since the
        user also has other types of draft registrations, we must search through the cards
        on the Drafts tab of the My Registrations page and find the card for an OSF
        Preregistration and then capture it's draft id so that we can use it to navigate
        to it's Analysis Plan page.
        """
        # Capture the draft id from the first OSF Preregistration that is listed
        draft_id = my_registrations_page.get_first_draft_id_by_template(
            "OSF Preregistration"
        )
        analysis_plan_page = DraftRegistrationGenericPage(
            driver, draft_id=draft_id, url_addition="5-analysis-plan"
        )
        analysis_plan_page.goto()
        assert analysis_plan_page.page_heading.text == "Analysis Plan"
        # Wait for file widget to load before calling axe
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[data-test-files-list-for]")
            )
        )
        a11y.run_axe(
            driver,
            session,
            "drftreganalysis",
            write_files=write_files,
            exclude_best_practice=True,
        )

    def test_accessibility_publication_information_page(
        self, driver, session, write_files, exclude_best_practice, my_registrations_page
    ):
        """This test is for checking the accessibility of the Draft Registration Publication
        Information Page which is the second page on a Registered Report Protocol Preregistration
        template.  Since the user also has other types of draft registrations, we must search
        through the cards on the Drafts tab of the My Registrations page and find the card for
        a Registered Report Protocol Preregistration and then capture it's draft id so that we
        can use it to navigate to it's Publication Information page.
        """
        # Capture the draft id from the first Registered Report Protocol Preregistration
        # that is listed
        draft_id = my_registrations_page.get_first_draft_id_by_template(
            "Registered Report Protocol Preregistration"
        )
        publication_information_page = DraftRegistrationGenericPage(
            driver, draft_id=draft_id, url_addition="1-publication-information"
        )
        publication_information_page.goto()
        assert (
            publication_information_page.page_heading.text == "Publication Information"
        )
        a11y.run_axe(
            driver,
            session,
            "drftregpubinfo",
            write_files=write_files,
            exclude_best_practice=True,
        )

    def test_accessibility_manuscript_page(
        self, driver, session, write_files, exclude_best_practice, my_registrations_page
    ):
        """This test is for checking the accessibility of the Draft Registration Manuscript
        Page which is the second page on a Registered Report Protocol Preregistration template.
        Since the user also has other types of draft registrations, we must search through
        the cards on the Drafts tab of the My Registrations page and find the card for a
        Registered Report Protocol Preregistration and then capture it's draft id so that we
        can use it to navigate to it's Publication Information page.
        """
        # Capture the draft id from the first Registered Report Protocol Preregistration
        # that is listed
        draft_id = my_registrations_page.get_first_draft_id_by_template(
            "Registered Report Protocol Preregistration"
        )
        manuscript_page = DraftRegistrationGenericPage(
            driver, draft_id=draft_id, url_addition="2-manuscript"
        )
        manuscript_page.goto()
        assert manuscript_page.page_heading.text == "Manuscript"
        # Wait for file widget to load before calling axe
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[data-test-files-list-for]")
            )
        )
        a11y.run_axe(
            driver,
            session,
            "drftregmnscrpt",
            write_files=write_files,
            exclude_best_practice=True,
        )

    def test_accessibility_other_page(
        self, driver, session, write_files, exclude_best_practice, my_registrations_page
    ):
        """This test is for checking the accessibility of the Draft Registration Other
        Page which is the fourth page on a Registered Report Protocol Preregistration
        template.  Since the user also has other types of draft registrations, we must
        search through the cards on the Drafts tab of the My Registrations page and find
        the card for an Registered Report Protocol Preregistration and then capture it's
        draft id so that we can use it to navigate to it's Other page.
        """
        # Capture the draft id from the first Registered Report Protocol Preregistration
        # that is listed
        draft_id = my_registrations_page.get_first_draft_id_by_template(
            "Registered Report Protocol Preregistration"
        )
        other_page = DraftRegistrationGenericPage(
            driver, draft_id=draft_id, url_addition="3-other"
        )
        other_page.goto()
        assert other_page.page_heading.text == "Other"
        # Wait for file widget to load before calling axe
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[data-test-files-list-for]")
            )
        )
        a11y.run_axe(
            driver,
            session,
            "drftregother",
            write_files=write_files,
            exclude_best_practice=True,
        )

    def test_accessibility_prereg_template_aspredicted_org_page(
        self, driver, session, write_files, exclude_best_practice, my_registrations_page
    ):
        """This test is for checking the accessibility of the Draft Registration
        Preregistration Template from AsPredicted.org Page which is the second page on
        a Preregistration Template from AsPredicted.org template.  Since the user also
        has other types of draft registrations, we must search through the cards on the
        Drafts tab of the My Registrations page and find the card for a Preregistration
        Template from AsPredicted.org draft and then capture it's draft id so that we
        can use it to navigate to it's Preregistration Template from AsPredicted.org
        page.
        """
        # Capture the draft id from the first Preregistration Template from AsPredicted.org
        # that is listed
        draft_id = my_registrations_page.get_first_draft_id_by_template(
            "Preregistration Template from AsPredicted.org"
        )
        prereg_template_page = DraftRegistrationGenericPage(
            driver,
            draft_id=draft_id,
            url_addition="1-preregistration-template-from-aspredictedorg",
        )
        prereg_template_page.goto()
        assert (
            prereg_template_page.page_heading.text
            == "Preregistration Template from AsPredicted.org"
        )
        a11y.run_axe(
            driver,
            session,
            "drftregasprdct",
            write_files=write_files,
            exclude_best_practice=True,
        )

    def test_accessibility_osf_standard_predata_collection_page(
        self, driver, session, write_files, exclude_best_practice, my_registrations_page
    ):
        """This test is for checking the accessibility of the Draft Registration
        OSF-Standard Pre-Data Collection Registration Page which is the second page on
        an OSF-Standard Pre-Data Collection Registration template.  Since the user also
        has other types of draft registrations, we must search through the cards on the
        Drafts tab of the My Registrations page and find the card for an OSF-Standard
        Pre-Data Collection Registration draft and then capture it's draft id so that
        we can use it to navigate to it's OSF-Standard Pre-Data Collection Registration
        page.
        """
        # Capture the draft id from the first OSF-Standard Pre-Data Collection Registration
        # that is listed
        draft_id = my_registrations_page.get_first_draft_id_by_template(
            "OSF-Standard Pre-Data Collection Registration"
        )
        predata_collection_page = DraftRegistrationGenericPage(
            driver,
            draft_id=draft_id,
            url_addition="1-osf-standard-pre-data-collection-registration",
        )
        predata_collection_page.goto()
        assert (
            predata_collection_page.page_heading.text
            == "OSF-Standard Pre-Data Collection Registration"
        )
        a11y.run_axe(
            driver,
            session,
            "drftregpredata",
            write_files=write_files,
            exclude_best_practice=True,
        )

    def test_accessibility_hypotheses_essential_elements_page(
        self, driver, session, write_files, exclude_best_practice, my_registrations_page
    ):
        """This test is for checking the accessibility of the Draft Registration
        Hypotheses - Essential elements Page which is the second page on a
        Pre-Registration in Social Psychology template.  Since the user also has
        other types of draft registrations, we must search through the cards on the
        Drafts tab of the My Registrations page and find the card for a
        Pre-Registration in Social Psychology draft and then capture it's draft id
        so that we can use it to navigate to it's Hypotheses - Essential elements
        page.
        """
        # Capture the draft id from the first Pre-Registration in Social Psychology
        # that is listed
        draft_id = my_registrations_page.get_first_draft_id_by_template(
            "Pre-Registration in Social Psychology"
        )
        hypotheses_page = DraftRegistrationGenericPage(
            driver,
            draft_id=draft_id,
            url_addition="1-a-hypotheses---essential-elements",
        )
        hypotheses_page.goto()
        assert hypotheses_page.page_heading.text == "A. Hypotheses - Essential elements"
        a11y.run_axe(
            driver,
            session,
            "drftreghypotheses",
            write_files=write_files,
            exclude_best_practice=True,
        )

    def test_accessibility_recommended_elements_page(
        self, driver, session, write_files, exclude_best_practice, my_registrations_page
    ):
        """This test is for checking the accessibility of the Draft Registration
        Recommended elements Page which is the third page on a Pre-Registration in
        Social Psychology template.  Since the user also has other types of draft
        registrations, we must search through the cards on the Drafts tab of the My
        Registrations page and find the card for a Pre-Registration in Social
        Psychology draft and then capture it's draft id so that we can use it to
        navigate to it's Recommended elements page.
        """
        # Capture the draft id from the first Pre-Registration in Social Psychology
        # that is listed
        draft_id = my_registrations_page.get_first_draft_id_by_template(
            "Pre-Registration in Social Psychology"
        )
        recommended_elements_page = DraftRegistrationGenericPage(
            driver,
            draft_id=draft_id,
            url_addition="2-recommended-elements",
        )
        recommended_elements_page.goto()
        assert recommended_elements_page.page_heading.text == "Recommended elements"
        # Wait for file widget to load before calling axe
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[data-test-files-list-for]")
            )
        )
        a11y.run_axe(
            driver,
            session,
            "drftregrecelems",
            write_files=write_files,
            exclude_best_practice=True,
        )

    def test_accessibility_methods_essential_elements_page(
        self, driver, session, write_files, exclude_best_practice, my_registrations_page
    ):
        """This test is for checking the accessibility of the Draft Registration
        Methods - Essential elements Page which is the fourth page on a
        Pre-Registration in Social Psychology template.  Since the user also has
        other types of draft registrations, we must search through the cards on the
        Drafts tab of the My Registrations page and find the card for a
        Pre-Registration in Social Psychology draft and then capture it's draft id
        so that we can use it to navigate to it's Methods - Essential elements page.
        """
        # Capture the draft id from the first Pre-Registration in Social Psychology
        # that is listed
        draft_id = my_registrations_page.get_first_draft_id_by_template(
            "Pre-Registration in Social Psychology"
        )
        methods_page = DraftRegistrationGenericPage(
            driver,
            draft_id=draft_id,
            url_addition="3-b-methods---essential-elements",
        )
        methods_page.goto()
        assert methods_page.page_heading.text == "B. Methods - Essential elements"
        # Wait for file widget to load before calling axe
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[data-test-files-list-for]")
            )
        )
        a11y.run_axe(
            driver,
            session,
            "drftregmethods",
            write_files=write_files,
            exclude_best_practice=True,
        )

    def test_accessibility_analysis_plan_essential_elements_page(
        self, driver, session, write_files, exclude_best_practice, my_registrations_page
    ):
        """This test is for checking the accessibility of the Draft Registration
        Analysis Plan - Essential elements Page which is the sixth page on a
        Pre-Registration in Social Psychology template.  Since the user also has
        other types of draft registrations, we must search through the cards on the
        Drafts tab of the My Registrations page and find the card for a
        Pre-Registration in Social Psychology draft and then capture it's draft id
        so that we can use it to navigate to it's Analysis Plan - Essential elements
        page.
        """
        # Capture the draft id from the first Pre-Registration in Social Psychology
        # that is listed
        draft_id = my_registrations_page.get_first_draft_id_by_template(
            "Pre-Registration in Social Psychology"
        )
        analysis_plan_page = DraftRegistrationGenericPage(
            driver,
            draft_id=draft_id,
            url_addition="5-c-analysis-plan---essential-elements",
        )
        analysis_plan_page.goto()
        assert (
            analysis_plan_page.page_heading.text
            == "C. Analysis plan - Essential elements"
        )
        a11y.run_axe(
            driver,
            session,
            "drftregaplnelems",
            write_files=write_files,
            exclude_best_practice=True,
        )

    def test_accessibility_final_questions_page(
        self, driver, session, write_files, exclude_best_practice, my_registrations_page
    ):
        """This test is for checking the accessibility of the Draft Registration
        Final questions Page which is the eighth page on a Pre-Registration in
        Social Psychology template.  Since the user also has other types of draft
        registrations, we must search through the cards on the Drafts tab of the
        My Registrations page and find the card for a Pre-Registration in Social
        Psychology draft and then capture it's draft id so that we can use it to
        navigate to it's Final questions page.
        """
        # Capture the draft id from the first Pre-Registration in Social Psychology
        # that is listed
        draft_id = my_registrations_page.get_first_draft_id_by_template(
            "Pre-Registration in Social Psychology"
        )
        final_questions_page = DraftRegistrationGenericPage(
            driver, draft_id=draft_id, url_addition="7-final-questions"
        )
        final_questions_page.goto()
        assert final_questions_page.page_heading.text == "Final questions"
        a11y.run_axe(
            driver,
            session,
            "drftregfnlqustns",
            write_files=write_files,
            exclude_best_practice=True,
        )

    def test_accessibility_nature_of_the_effect_page(
        self, driver, session, write_files, exclude_best_practice, my_registrations_page
    ):
        """This test is for checking the accessibility of the Draft Registration
        The Nature of the Effect Page which is the second page on a Replication
        Recipe (Brandt et al., 2013): Pre-Registration template.  Since the user
        also has other types of draft registrations, we must search through the
        cards on the Drafts tab of the My Registrations page and find the card
        for a Replication Recipe (Brandt et al., 2013): Pre-Registration draft
        and then capture it's draft id so that we can use it to navigate to it's
        The Nature of the Effect page.
        """
        # Capture the draft id from the first Replication Recipe (Brandt et al., 2013):
        # Pre-Registration that is listed
        draft_id = my_registrations_page.get_first_draft_id_by_template(
            "Replication Recipe (Brandt et al., 2013): Pre-Registration"
        )
        nature_effect_page = DraftRegistrationGenericPage(
            driver, draft_id=draft_id, url_addition="1-the-nature-of-the-effect"
        )
        nature_effect_page.goto()
        assert nature_effect_page.page_heading.text == "The Nature of the Effect"
        a11y.run_axe(
            driver,
            session,
            "drftregnateff",
            write_files=write_files,
            exclude_best_practice=True,
        )

    def test_accessibility_designing_replication_study_page(
        self, driver, session, write_files, exclude_best_practice, my_registrations_page
    ):
        """This test is for checking the accessibility of the Draft Registration
        Designing the Replication Study Page which is the third page on a Replication
        Recipe (Brandt et al., 2013): Pre-Registration template.  Since the user also
        has other types of draft registrations, we must search through the cards on
        the Drafts tab of the My Registrations page and find the card for a
        Replication Recipe (Brandt et al., 2013): Pre-Registration draft and then
        capture it's draft id so that we can use it to navigate to it's Designing
        the Replication Study page.
        """
        # Capture the draft id from the first Replication Recipe (Brandt et al., 2013):
        # Pre-Registration that is listed
        draft_id = my_registrations_page.get_first_draft_id_by_template(
            "Replication Recipe (Brandt et al., 2013): Pre-Registration"
        )
        design_study_page = DraftRegistrationGenericPage(
            driver, draft_id=draft_id, url_addition="2-designing-the-replication-study"
        )
        design_study_page.goto()
        assert design_study_page.page_heading.text == "Designing the Replication Study"
        a11y.run_axe(
            driver,
            session,
            "drftregdesrepstdy",
            write_files=write_files,
            exclude_best_practice=True,
        )

    def test_accessibility_documenting_differences_page(
        self, driver, session, write_files, exclude_best_practice, my_registrations_page
    ):
        """This test is for checking the accessibility of the Draft Registration
        Documenting Differences between the Original and Replication Study Page which
        is the fourth page on a Replication Recipe (Brandt et al., 2013):
        Pre-Registration template.  Since the user also has other types of draft
        registrations, we must search through the cards on the Drafts tab of the My
        Registrations page and find the card for a Replication Recipe (Brandt et al.,
        2013): Pre-Registration draft and then capture it's draft id so that we can
        use it to navigate to it's Documenting Differences between the Original and
        Replication Study page.
        """
        # Capture the draft id from the first Replication Recipe (Brandt et al., 2013):
        # Pre-Registration that is listed
        draft_id = my_registrations_page.get_first_draft_id_by_template(
            "Replication Recipe (Brandt et al., 2013): Pre-Registration"
        )
        documenting_differences_page = DraftRegistrationGenericPage(
            driver,
            draft_id=draft_id,
            url_addition="3-documenting-differences-between-the-original-and-replication-study",
        )
        documenting_differences_page.goto()
        assert (
            documenting_differences_page.page_heading.text
            == "Documenting Differences between the Original and Replication Study"
        )
        a11y.run_axe(
            driver,
            session,
            "drftregdocdiff",
            write_files=write_files,
            exclude_best_practice=True,
        )

    def test_accessibility_analysis_replication_evaluation_page(
        self, driver, session, write_files, exclude_best_practice, my_registrations_page
    ):
        """This test is for checking the accessibility of the Draft Registration
        Analysis and Replication Evaluation Page which is the fifth page on a
        Replication Recipe (Brandt et al., 2013): Pre-Registration template.  Since
        the user also has other types of draft registrations, we must search through
        the cards on the Drafts tab of the My Registrations page and find the card
        for a Replication Recipe (Brandt et al., 2013): Pre-Registration draft and
        then capture it's draft id so that we can use it to navigate to it's Analysis
        and Replication Evaluation page.
        """
        # Capture the draft id from the first Replication Recipe (Brandt et al., 2013):
        # Pre-Registration that is listed
        draft_id = my_registrations_page.get_first_draft_id_by_template(
            "Replication Recipe (Brandt et al., 2013): Pre-Registration"
        )
        analysis_replication_eval_page = DraftRegistrationGenericPage(
            driver,
            draft_id=draft_id,
            url_addition="4-analysis-and-replication-evaluation",
        )
        analysis_replication_eval_page.goto()
        assert (
            analysis_replication_eval_page.page_heading.text
            == "Analysis and Replication Evaluation"
        )
        a11y.run_axe(
            driver,
            session,
            "drftregrepeval",
            write_files=write_files,
            exclude_best_practice=True,
        )

    def test_accessibility_registering_replication_attempt_page(
        self, driver, session, write_files, exclude_best_practice, my_registrations_page
    ):
        """This test is for checking the accessibility of the Draft Registration
        Registering the Replication Attempt Page which is the second page on a
        Replication Recipe (Brandt et al., 2013): Post-Completion template.  Since
        the user also has other types of draft registrations, we must search through
        the cards on the Drafts tab of the My Registrations page and find the card
        for a Replication Recipe (Brandt et al., 2013): Post-Completion draft and
        then capture it's draft id so that we can use it to navigate to it's
        Registering the Replication Attempt page.
        """
        # Capture the draft id from the first Replication Recipe (Brandt et al., 2013):
        # Post-Completion that is listed
        draft_id = my_registrations_page.get_first_draft_id_by_template(
            "Replication Recipe (Brandt et al., 2013): Post-Completion"
        )
        registering_replication_page = DraftRegistrationGenericPage(
            driver,
            draft_id=draft_id,
            url_addition="1-registering-the-replication-attempt",
        )
        registering_replication_page.goto()
        assert (
            registering_replication_page.page_heading.text
            == "Registering the Replication Attempt"
        )
        a11y.run_axe(
            driver,
            session,
            "drftregrepatt",
            write_files=write_files,
            exclude_best_practice=True,
        )

    def test_accessibility_reporting_replication_page(
        self, driver, session, write_files, exclude_best_practice, my_registrations_page
    ):
        """This test is for checking the accessibility of the Draft Registration
        Reporting the Replication Page which is the second page on a Replication Recipe
        (Brandt et al., 2013): Post-Completion template.  Since the user also has other
        types of draft registrations, we must search through the cards on the Drafts
        tab of the My Registrations page and find the card for a Replication Recipe
        (Brandt et al., 2013): Post-Completion draft and then capture it's draft id
        so that we can use it to navigate to it's Reporting the Replication page.
        """
        # Capture the draft id from the first Replication Recipe (Brandt et al., 2013):
        # Post-Completion that is listed
        draft_id = my_registrations_page.get_first_draft_id_by_template(
            "Replication Recipe (Brandt et al., 2013): Post-Completion"
        )
        reporting_replication_page = DraftRegistrationGenericPage(
            driver,
            draft_id=draft_id,
            url_addition="2-reporting-the-replication",
        )
        reporting_replication_page.goto()
        assert (
            reporting_replication_page.page_heading.text == "Reporting the Replication"
        )
        a11y.run_axe(
            driver,
            session,
            "drftregreprep",
            write_files=write_files,
            exclude_best_practice=True,
        )

    def test_accessibility_data_description_page(
        self, driver, session, write_files, exclude_best_practice, my_registrations_page
    ):
        """This test is for checking the accessibility of the Draft Registration
        Data Description Page which is the third page on a Secondary Data
        Preregistration template.  Since the user also has other types of draft
        registrations, we must search through the cards on the Drafts tab of the My
        Registrations page and find the card for a Secondary Data Preregistration
        draft and then capture it's draft id so that we can use it to navigate to
        it's Data Description page.
        """
        # Capture the draft id from the first Secondary Data Preregistration that
        # is listed
        draft_id = my_registrations_page.get_first_draft_id_by_template(
            "Secondary Data Preregistration"
        )
        data_description_page = DraftRegistrationGenericPage(
            driver,
            draft_id=draft_id,
            url_addition="2-data-description",
        )
        data_description_page.goto()
        assert data_description_page.page_heading.text == "Data Description"
        # Wait for file widget to load before calling axe
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[data-test-files-list-for]")
            )
        )
        a11y.run_axe(
            driver,
            session,
            "drftregdatadesc",
            write_files=write_files,
            exclude_best_practice=True,
        )

    def test_accessibility_knowledge_of_data_page(
        self, driver, session, write_files, exclude_best_practice, my_registrations_page
    ):
        """This test is for checking the accessibility of the Draft Registration
        Knowledge of Data Page which is the fifth page on a Secondary Data
        Preregistration template.  Since the user also has other types of draft
        registrations, we must search through the cards on the Drafts tab of the My
        Registrations page and find the card for a Secondary Data Preregistration
        draft and then capture it's draft id so that we can use it to navigate to
        it's Knowledge of Data page.
        """
        # Capture the draft id from the first Secondary Data Preregistration that
        # is listed
        draft_id = my_registrations_page.get_first_draft_id_by_template(
            "Secondary Data Preregistration"
        )
        data_knowledge_page = DraftRegistrationGenericPage(
            driver,
            draft_id=draft_id,
            url_addition="4-knowledge-of-data",
        )
        data_knowledge_page.goto()
        assert data_knowledge_page.page_heading.text == "Knowledge of Data"
        a11y.run_axe(
            driver,
            session,
            "drftregknowdata",
            write_files=write_files,
            exclude_best_practice=True,
        )

    @markers.ember_page
    def test_accessibility_review_page(
        self, driver, session, write_files, exclude_best_practice, my_registrations_page
    ):
        """This test is for checking the accessibility of the Draft Registration Review
        Page which is the final page of any template.  In this case we are using an OSF
        Preregistration draft registration since it is one of the longer templates and
        therefore more data is displayed on the review page.  Since the user also has
        other types of draft registrations, we must search through the cards on the
        Drafts tab of the My Registrations page and find the card for an OSF
        Preregistration and then capture it's draft id so that we can use it to navigate
        to it's Other page.
        """
        # Capture the draft id from the first OSF Preregistration that is listed
        draft_id = my_registrations_page.get_first_draft_id_by_template(
            "OSF Preregistration"
        )
        review_page = DraftRegistrationReviewPage(driver, draft_id=draft_id)
        review_page.goto()
        assert DraftRegistrationReviewPage(driver, verify=True)
        a11y.run_axe(
            driver,
            session,
            "drftregreview",
            write_files=write_files,
            exclude_best_practice=True,
        )


class TestBrandedRegistrationsProviders:
    def providers():
        """Return all registration providers."""
        return osf_api.get_providers_list(type="registrations")

    @pytest.fixture(params=providers(), ids=[prov["id"] for prov in providers()])
    def provider(self, request):
        return request.param

    def test_accessibility(
        self, session, driver, provider, write_files, exclude_best_practice
    ):
        # # Test for all providers except OSF and assessment
        if provider["id"] in settings.non_branded_registries:
            pytest.skip()

        discover_page = BrandedRegistriesDiscoverPage(driver, provider=provider)
        discover_page.goto()
        assert BrandedRegistriesDiscoverPage(driver, verify=True)
        discover_page.loading_indicator.here_then_gone()
        page_name = "br_" + provider["id"]
        a11y.run_axe(
            driver,
            session,
            page_name,
            write_files=write_files,
            exclude_best_practice=True,
        )


# We do not currently have a user setup as an administrator for any of the registries
# in production
@markers.dont_run_on_prod
@markers.ember_page
class TestModerationPages:
    """To test the Moderation pages we must login as a user that has been setup as an
    administrator for one of the registry providers that has moderation enabled.  We
    are using the egap registry since it exists in all testing environments and has the
    moderation process enabled in each environment.
    """

    @pytest.fixture
    def provider(self, driver):
        return osf_api.get_provider(provider_id="egap")

    def test_accessibility_moderation_submitted(
        self,
        driver,
        session,
        provider,
        write_files,
        exclude_best_practice,
        must_be_logged_in,
    ):
        submitted_page = RegistriesModerationSubmittedPage(driver, provider=provider)
        submitted_page.goto()
        assert RegistriesModerationSubmittedPage(driver, verify=True)
        # Wait for registration table to load before calling axe
        if submitted_page.no_registrations_message.absent():
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "[data-test-registration-list-card]")
                )
            )
        a11y.run_axe(
            driver,
            session,
            "regmodsub",
            write_files=write_files,
            exclude_best_practice=True,
        )

    def test_accessibility_moderation_pending(
        self,
        driver,
        session,
        provider,
        write_files,
        exclude_best_practice,
        must_be_logged_in,
    ):
        pending_page = RegistriesModerationPendingPage(driver, provider=provider)
        pending_page.goto()
        assert RegistriesModerationPendingPage(driver, verify=True)
        # Wait for registration table to load before calling axe
        if pending_page.no_registrations_message.absent():
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "[data-test-registration-list-card]")
                )
            )
        a11y.run_axe(
            driver,
            session,
            "regmodpend",
            write_files=write_files,
            exclude_best_practice=True,
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
        moderators_page = RegistriesModerationModeratorsPage(driver, provider=provider)
        moderators_page.goto()
        assert RegistriesModerationModeratorsPage(driver, verify=True)
        # Wait for moderators table to load before calling axe
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[data-test-moderator-row]")
            )
        )
        a11y.run_axe(
            driver,
            session,
            "regmodmod",
            write_files=write_files,
            exclude_best_practice=True,
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
        settings_page = RegistriesModerationSettingsPage(driver, provider=provider)
        settings_page.goto()
        assert RegistriesModerationSettingsPage(driver, verify=True)
        # Wait for notifications list to load before calling axe
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[data-test-subscription-list-row]")
            )
        )
        a11y.run_axe(
            driver,
            session,
            "regmodset",
            write_files=write_files,
            exclude_best_practice=True,
        )
