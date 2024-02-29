from urllib.parse import urljoin

import pytest
from selenium.webdriver.common.by import By

import settings
from base.locators import (
    ComponentLocator,
    GroupLocator,
    Locator,
)
from components.navbars import PreprintsNavbar
from pages.base import (
    GuidBasePage,
    OSFBasePage,
)


class BasePreprintPage(OSFBasePage):
    """The base page from which all preprint pages inherit."""

    base_url = settings.OSF_HOME + '/preprints/'
    url_addition = ''
    navbar = ComponentLocator(PreprintsNavbar)

    def __init__(self, driver, verify=False, provider=None):
        self.provider = provider
        if provider:
            self.provider_id = provider['id']
            self.provider_name = provider['attributes']['name']
            self.provider_domain = provider['attributes']['domain']

        super().__init__(driver, verify)

    @property
    def url(self):
        """Set the URL based on the provider domain."""
        if self.provider and self.provider_id != 'osf':
            if self.provider['attributes']['domain_redirect_enabled']:
                return urljoin(self.provider_domain, self.url_addition)
            else:
                return (
                    urljoin(self.base_url, self.provider_id) + '/' + self.url_addition
                )
        return self.base_url + self.url_addition

    def verify(self):
        """Return true if you are on the expected page.
        Checks both the general page identity and the branding.
        """
        if self.provider and self.provider_id != 'osf':
            return super().verify() and self.provider_name in self.navbar.title.text
        return super().verify()


class PreprintLandingPage(BasePreprintPage):
    identity = Locator(
        By.CSS_SELECTOR,
        '[data-analytics-scope="preprints landing page"]',
        settings.LONG_TIMEOUT,
    )
    add_preprint_button = Locator(
        By.CLASS_NAME, '[data-analytics-name="Add a preprint"]', settings.LONG_TIMEOUT
    )
    search_button = Locator(By.CSS_SELECTOR, '[data-analytics-name="Search"]')
    submit_button = Locator(By.CSS_SELECTOR, '[data-test-submit-button]')


class PreprintSubmitPage(BasePreprintPage):
    url_addition = 'submit'

    identity = Locator(By.CLASS_NAME, 'preprint-submit-header')
    select_a_service_help_text = Locator(
        By.CSS_SELECTOR, 'dl[class="dl-horizontal dl-description"]'
    )
    select_a_service_save_button = Locator(
        By.CSS_SELECTOR, '#preprint-form-server button.btn.btn-primary'
    )

    upload_from_existing_project_button = Locator(
        By.XPATH, '//button[text()="Select from an existing OSF project"]'
    )
    upload_project_selector = Locator(
        By.CSS_SELECTOR, 'span[class="ember-power-select-placeholder"]'
    )
    upload_project_selector_input = Locator(
        By.CSS_SELECTOR, 'input[class="ember-power-select-search-input"]'
    )
    upload_project_help_text = Locator(
        By.CSS_SELECTOR, '.ember-power-select-option--search-message'
    )
    upload_project_selector_project = Locator(
        By.CSS_SELECTOR, '.ember-power-select-option'
    )
    upload_select_file = Locator(By.CSS_SELECTOR, '.file-browser-item > a:nth-child(2)')
    upload_file_save_continue = Locator(
        By.CSS_SELECTOR,
        'div[class="p-t-xs pull-right"] > button[class="btn btn-primary"]',
    )

    # Author Assertions
    public_available_button = Locator(
        By.ID, 'hasDataLinksAvailable', settings.QUICK_TIMEOUT
    )
    public_data_input = Locator(
        By.CSS_SELECTOR, '[data-test-multiple-textbox-index] > input'
    )
    preregistration_no_button = Locator(By.ID, 'hasPreregLinksNo')
    preregistration_input = Locator(By.NAME, 'whyNoPrereg')
    save_author_assertions = Locator(
        By.CSS_SELECTOR, '[data-test-author-assertions-continue]'
    )

    basics_license_dropdown = Locator(
        By.CSS_SELECTOR, 'select[class="form-control"]', settings.LONG_TIMEOUT
    )
    basics_tags_section = Locator(By.CSS_SELECTOR, '#preprint-form-basics .tagsinput')
    basics_tags_input = Locator(
        By.CSS_SELECTOR, '#preprint-form-basics .tagsinput input'
    )
    basics_abstract_input = Locator(By.NAME, 'basicsAbstract')
    basics_save_button = Locator(By.CSS_SELECTOR, '#preprint-form-basics .btn-primary')

    first_discipline = Locator(
        By.CSS_SELECTOR, 'ul[role="listbox"] > li:nth-child(2)', settings.QUICK_TIMEOUT
    )
    discipline_save_button = Locator(
        By.CSS_SELECTOR, '#preprint-form-subjects .btn-primary'
    )

    authors_save_button = Locator(
        By.CSS_SELECTOR, '#preprint-form-authors .btn-primary', settings.QUICK_TIMEOUT
    )

    conflict_of_interest_yes = Locator(By.ID, 'coiYes', settings.QUICK_TIMEOUT)
    conflict_of_interest_no = Locator(By.ID, 'coiNo', settings.QUICK_TIMEOUT)
    no_coi_text_box = Locator(
        By.CSS_SELECTOR, '[data-test-has-no-coi]', settings.QUICK_TIMEOUT
    )
    coi_save_button = Locator(By.CSS_SELECTOR, '[data-test-coi-continue]')

    supplemental_create_new_project = Locator(
        By.CSS_SELECTOR,
        'div[class="start"] > div[class="row"] > div:nth-child(2)',
        settings.QUICK_TIMEOUT,
    )
    supplemental_save_button = Locator(
        By.CSS_SELECTOR, '#supplemental-materials .btn-primary'
    )

    create_preprint_button = Locator(
        By.CSS_SELECTOR,
        '.preprint-submit-body .submit-section > div > button.btn.btn-success.btn-md.m-t-md.pull-right',
    )
    modal_create_preprint_button = Locator(
        By.CSS_SELECTOR,
        '.modal-footer button.btn-success:nth-child(2)',
        settings.LONG_TIMEOUT,
    )


class PreprintEditPage(GuidBasePage, BasePreprintPage):
    url_base = urljoin(settings.OSF_HOME, '{guid}')
    url_addition = '/edit'

    identity = Locator(
        By.CSS_SELECTOR, '.m-t-md.preprint-header-preview > p:nth-child(1) > em.m-r-md'
    )
    basics_section = Locator(By.ID, 'preprint-form-basics')
    basics_tags_section = Locator(By.CSS_SELECTOR, '#preprint-form-basics .tagsinput')
    basics_tags_input = Locator(
        By.CSS_SELECTOR, '#preprint-form-basics .tagsinput input'
    )
    basics_save_button = Locator(By.CSS_SELECTOR, '#preprint-form-basics .btn-primary')
    basics_section_changes_saved_indicator = Locator(
        By.CSS_SELECTOR,
        '#preprint-form-basics > header > div.preprint-section-status.pull-right > span.text-success.',
    )
    discipline_section = Locator(By.ID, 'preprint-form-subjects')
    discipline_save_button = Locator(
        By.CSS_SELECTOR, '#preprint-form-subjects .btn-primary'
    )
    authors_save_button = Locator(
        By.CSS_SELECTOR, '#preprint-form-authors .btn-primary', settings.QUICK_TIMEOUT
    )
    return_to_preprint_button = Locator(
        By.CSS_SELECTOR,
        'div.submit-section > div > button.btn.btn-default.btn-md.m-t-md.pull-right',
    )
    withdraw_preprint_button = Locator(
        By.CSS_SELECTOR,
        'div.submit-section > div > button.btn.btn-danger.btn-md.m-t-md.pull-right',
    )

    # Group Locators
    primary_subjects = GroupLocator(
        By.CSS_SELECTOR,
        '#preprint-form-subjects > div > div > div:nth-child(2) > div:nth-child(1) > ul > li',
    )

    def select_primary_subject_by_name(self, subject_name):
        """Select a subject from the first box in the Discipline section (i.e. 'primary'
        subject). This function would need to be modified or another separate function
        created to select from either of the 2 secondary subject boxes.
        """
        for subject in self.primary_subjects:
            if subject.text == subject_name:
                subject.click()
                break


class PreprintWithdrawPage(GuidBasePage, BasePreprintPage):
    url_base = urljoin(settings.OSF_HOME, '{guid}')
    url_addition = '/withdraw'

    identity = Locator(
        By.CSS_SELECTOR,
        'section.preprint-form-block.preprint-form-section-withdraw-comment',
    )
    reason_for_withdrawal_textarea = Locator(By.NAME, 'explanation')
    request_withdrawal_button = Locator(
        By.CSS_SELECTOR,
        'div.submit-section > button.btn.btn-danger.btn-md.m-t-md.pull-right',
    )


@pytest.mark.usefixtures('must_be_logged_in')
class PreprintDiscoverPage(BasePreprintPage):
    base_url = settings.OSF_HOME + '/search?resourceType=Preprint'

    identity = Locator(
        By.CSS_SELECTOR, 'a[data-test-topbar-object-type-link="Preprints"]'
    )
    loading_indicator = Locator(By.CSS_SELECTOR, '.ball-scale')
    search_box = Locator(By.CSS_SELECTOR, 'input[data-test-search-input]')
    sort_button = Locator(By.CSS_SELECTOR, 'div[data-test-topbar-sort-dropdown]')
    sort_option_newest_to_oldest = Locator(
        By.CSS_SELECTOR, '#sortByOptionList > li:nth-child(3) > button'
    )

    # Group Locators
    search_results = GroupLocator(By.CSS_SELECTOR, 'div[data-test-search-result-card]')
    sort_options = GroupLocator(
        By.CSS_SELECTOR, 'ul[class="ember-power-select-options"]'
    )


@pytest.mark.usefixtures('must_be_logged_in')
class BrandedPreprintsDiscoverPage(BasePreprintPage):
    url_addition = 'discover'

    identity = Locator(By.CSS_SELECTOR, '[data-test-search-provider-logo]')
    loading_indicator = Locator(By.CSS_SELECTOR, '.ball-scale')
    search_box = Locator(By.CSS_SELECTOR, 'input[data-test-search-input]')
    sort_button = Locator(By.CSS_SELECTOR, 'div[data-test-topbar-sort-dropdown]')
    sort_option_newest_to_oldest = Locator(
        By.CSS_SELECTOR, '#sortByOptionList > li:nth-child(3) > button'
    )
    no_results = Locator(By.CSS_SELECTOR, 'div[_no-results_fvrbco]')

    # Group Locators
    search_results = GroupLocator(By.CSS_SELECTOR, 'div[data-test-search-result-card]')


class PreprintDetailPage(GuidBasePage, BasePreprintPage):
    url_base = urljoin(settings.OSF_HOME, '{guid}')
    identity = Locator(
        By.CSS_SELECTOR,
        '[data-test-preprint-header]',
        settings.LONG_TIMEOUT,
    )

    title = Locator(
        By.CSS_SELECTOR, 'h1[data-test-preprint-title]', settings.LONG_TIMEOUT
    )
    view_page = Locator(By.ID, 'view-page')
    views_count = Locator(By.CSS_SELECTOR, '[data-test-view-count]')
    downloads_count = Locator(By.CSS_SELECTOR, '[data-test-download-count]')
    download_button = Locator(By.CSS_SELECTOR, '[data-test-download-button]')
    edit_preprint_button = Locator(By.CSS_SELECTOR, 'div[class="edit-preprint-button"]')
    default_citation = Locator(By.CSS_SELECTOR, '[data-test-default-citation="apa"]')

    # Locators for the reviews app preprint detail page
    status = Locator(By.CSS_SELECTOR, 'span._status-badge_7ivjq4')
    status_explanation = Locator(By.CSS_SELECTOR, 'div.status-explanation')
    withdraw_reason = Locator(By.CSS_SELECTOR, '[data-test-withdrawal-justification]')
    make_decision_button = Locator(
        By.CSS_SELECTOR, 'button.btn.dropdown-toggle.btn-success'
    )
    accept_radio_button = Locator(By.CSS_SELECTOR, 'input[value="accepted"]')
    reject_radio_button = Locator(By.CSS_SELECTOR, 'input[value="rejected"]')
    withdraw_radio_button = Locator(By.CSS_SELECTOR, 'input[value="withdrawn"]')
    reason_textarea = Locator(By.CSS_SELECTOR, 'textarea.form-control.ember-text-area')
    submit_decision_button = Locator(By.ID, 'submit-btn')

    # Group Locators
    subjects = GroupLocator(
        By.CSS_SELECTOR,
        '[class="subject-preview"]',
    )
    tags = GroupLocator(By.CSS_SELECTOR, 'div.tag-section.p-t-xs > span')


class PendingPreprintDetailPage(PreprintDetailPage):
    # This class is for preprints that are pending moderation
    identity = Locator(
        By.ID,
        'preprintTitle',
        settings.LONG_TIMEOUT,
    )

    # This locator needs a data-test-selector from software devs
    title = Locator(By.ID, 'preprintTitle', settings.LONG_TIMEOUT)


class ReviewsDashboardPage(OSFBasePage):
    url = settings.OSF_HOME + '/reviews'
    identity = Locator(By.CLASS_NAME, '_reviews-dashboard-header_jdu5ey')
    loading_indicator = Locator(By.CSS_SELECTOR, '.ball-scale')
    provider_group_links = GroupLocator(
        By.CSS_SELECTOR, 'li._provider-links-component_gp8jcl'
    )

    def click_provider_group_link(self, provider_name, link_name):
        """Search through the Provider Groups in the sidebar on the right side of the
        Reviews Dashboard page to find the group with the given provider_name.  When
        the provider group is found, then search through the links in the group for the
        given link_name. Click this link when found.
        """
        for provider_group in self.provider_group_links:
            group_name = provider_group.find_element_by_css_selector(
                'span._provider-name_gp8jcl'
            )
            if provider_name == group_name.text:
                links = provider_group.find_elements_by_css_selector(
                    'ul._provider-links_gp8jcl > li > a'
                )
                for link in links:
                    if link_name in link.text:
                        link.click()
                        break
                break


class BaseReviewsPage(OSFBasePage):
    """The base page from which all preprint provider review pages inherit."""

    base_url = settings.OSF_HOME + '/reviews/preprints/'
    url_addition = ''
    navbar = ComponentLocator(PreprintsNavbar)
    title = Locator(By.CLASS_NAME, '_provider-title_hcnzoe')

    def __init__(self, driver, verify=False, provider=None):
        self.provider = provider
        if provider:
            self.provider_id = provider['id']
            self.provider_name = provider['attributes']['name']

        super().__init__(driver, verify)

    @property
    def url(self):
        """Set the URL based on the provider domain."""
        return urljoin(self.base_url, self.provider_id) + '/' + self.url_addition

    def verify(self):
        """Return true if you are on the expected page.
        Checks both the general page identity and the branding.
        """
        if self.provider:
            return super().verify() and self.provider_name in self.title.text
        return super().verify()


class ReviewsSubmissionsPage(BaseReviewsPage):
    identity = Locator(By.CLASS_NAME, '_reviews-list-heading_k45x8p')
    no_submissions = Locator(
        By.CSS_SELECTOR,
        'div._reviews-list-body_k45x8p > div.text-center.p-v-md._moderation-list-row_xkm0pa',
    )
    loading_indicator = Locator(By.CSS_SELECTOR, '.ball-scale')
    withdrawal_requests_tab = Locator(
        By.CSS_SELECTOR,
        'div._flex-container_hcnzoe > div:nth-child(3) > ul > li:nth-child(2) > a',
    )
    submissions = GroupLocator(By.CSS_SELECTOR, 'div._moderation-list-row_xkm0pa')

    def click_submission_row(self, provider_id, preprint_id):
        """Search through the rows of submitted preprints on the Reviews Submissions
        page to find the preprint that has the given preprint_id in its url. When the
        row is found click it to open the Preprint Detail page for that preprint.
        """
        for row in self.submissions:
            url = row.find_element_by_css_selector('a').get_attribute('href')
            node_id = url.split(provider_id + '/', 1)[1]
            if node_id == preprint_id:
                row.click()
                break


class ReviewsWithdrawalsPage(BaseReviewsPage):
    url_addition = 'withdrawals'
    identity = Locator(By.CLASS_NAME, '_reviews-list-heading_k45x8p')
    loading_indicator = Locator(By.CSS_SELECTOR, '.ball-scale')
    requests = GroupLocator(By.CSS_SELECTOR, 'div._moderation-list-row_17iwzt')

    def click_requests_row(self, provider_id, preprint_id):
        """Search through the rows of requests on the Reviews Withdrawal Requests
        page to find the preprint that has the given preprint_id in its url. When the
        row is found click it to open the Preprint Detail page for that preprint.
        """
        for row in self.requests:
            url = row.find_element_by_css_selector('a').get_attribute('href')
            node_id = url.split(provider_id + '/', 1)[1]
            if node_id == preprint_id:
                row.find_element_by_css_selector('div[title]').click()
                break


class ReviewsModeratorsPage(BaseReviewsPage):
    url_addition = '/moderators'
    identity = Locator(By.CLASS_NAME, 'moderator-list-row')
    loading_indicator = Locator(By.CSS_SELECTOR, '.ball-scale')


class ReviewsNotificationsPage(BaseReviewsPage):
    url_addition = 'notifications'
    identity = Locator(By.CLASS_NAME, '_notification-list-heading-container_kchmy0')
    loading_indicator = Locator(By.CSS_SELECTOR, '.ball-scale')


class ReviewsSettingsPage(BaseReviewsPage):
    url_addition = 'settings'
    identity = Locator(By.CLASS_NAME, '_reviews-settings_1r3x0j')
    loading_indicator = Locator(By.CSS_SELECTOR, '.ball-scale')


class PreprintPageNotFoundPage(OSFBasePage):
    identity = Locator(By.CSS_SELECTOR, '[data-analytics-scope="404"]')
    page_header = Locator(
        By.CSS_SELECTOR,
        '[data-analytics-scope="404"] > h2',
    )