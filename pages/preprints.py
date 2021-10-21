from urllib.parse import urljoin

import pytest
from selenium.webdriver.common.by import By

import settings
from base.locators import ComponentLocator, GroupLocator, Locator
from components.navbars import PreprintsNavbar
from pages.base import GuidBasePage, OSFBasePage


class BasePreprintPage(OSFBasePage):
    """The base page from which all preprint pages inherit.
    """

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
        """Set the URL based on the provider domain.
        """
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
        By.CSS_SELECTOR, '.ember-application .preprint-header', settings.LONG_TIMEOUT
    )
    add_preprint_button = Locator(
        By.CLASS_NAME, 'preprint-submit-button', settings.LONG_TIMEOUT
    )
    search_button = Locator(By.CSS_SELECTOR, '.preprint-search .btn-default')
    submit_navbar = Locator(By.CSS_SELECTOR, '.branded-nav > :nth-child(2)')
    submit_button = Locator(By.CSS_SELECTOR, '.btn.btn-success')


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

    conflict_of_interest = Locator(By.ID, 'coiNo', settings.QUICK_TIMEOUT)
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


@pytest.mark.usefixtures('must_be_logged_in')
class PreprintDiscoverPage(BasePreprintPage):
    url_addition = 'discover'

    identity = Locator(By.ID, 'share-logo')
    loading_indicator = Locator(By.CSS_SELECTOR, '.ball-scale')

    # Group Locators
    search_results = GroupLocator(By.CSS_SELECTOR, '.search-result h4 > a')
    no_results = GroupLocator(By.CSS_SELECTOR, '.search-results-section .text-muted')


class PreprintDetailPage(GuidBasePage, BasePreprintPage):
    url_base = urljoin(settings.OSF_HOME, '{guid}')

    identity = Locator(By.ID, 'preprintTitle', settings.LONG_TIMEOUT)
    title = Locator(By.ID, 'preprintTitle', settings.LONG_TIMEOUT)
    view_page = Locator(By.ID, 'view-page')
    authors_load_indicator = Locator(By.CSS_SELECTOR, '.comma-list > .ball-pulse')


class ReviewsDashboardPage(OSFBasePage):
    url = settings.OSF_HOME + '/reviews'
    identity = Locator(By.CLASS_NAME, '_reviews-dashboard-header_jdu5ey')


class BaseReviewsPage(OSFBasePage):
    """The base page from which all preprint provider review pages inherit.
    """

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
        """Set the URL based on the provider domain.
        """
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


class ReviewsWithdrawalsPage(BaseReviewsPage):
    url_addition = 'withdrawals'
    identity = Locator(By.CLASS_NAME, '_reviews-list-heading_k45x8p')
    no_requests = Locator(
        By.CSS_SELECTOR,
        'div._reviews-list-body_k45x8p > div.text-center.p-v-md._moderation-list-row_xkm0pa',
    )


class ReviewsModeratorsPage(BaseReviewsPage):
    url_addition = 'moderators'
    identity = Locator(By.CLASS_NAME, 'moderator-list-row')


class ReviewsNotificationsPage(BaseReviewsPage):
    url_addition = 'notifications'
    identity = Locator(By.CLASS_NAME, '_notification-list-heading-container_kchmy0')


class ReviewsSettingsPage(BaseReviewsPage):
    url_addition = 'settings'
    identity = Locator(By.CLASS_NAME, '_reviews-settings_1r3x0j')
