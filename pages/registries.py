from urllib.parse import urljoin

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

import settings
from base.locators import ComponentLocator, GroupLocator, Locator
from components.navbars import RegistriesNavbar
from pages.base import GuidBasePage, OSFBasePage


class BaseRegistriesPage(OSFBasePage):
    base_url = settings.OSF_HOME + '/registries/'
    url_addition = ''
    navbar = ComponentLocator(RegistriesNavbar)

    def __init__(self, driver, verify=False, provider=None):
        self.provider = provider
        if provider:
            self.provider_id = provider['id']
            self.provider_name = provider['attributes']['name']

        super().__init__(driver, verify)

    @property
    def url(self):
        """Set the URL based on the provider"""
        if self.provider and self.provider_id != 'osf':
            return urljoin(self.base_url, self.provider_id) + '/' + self.url_addition
        return self.base_url + self.url_addition


class RegistriesLandingPage(BaseRegistriesPage):
    identity = Locator(
        By.CSS_SELECTOR, '._RegistriesHeader_3zbd8x', settings.LONG_TIMEOUT
    )
    search_box = Locator(By.ID, 'search')


class RegistriesDiscoverPage(BaseRegistriesPage):
    url_addition = 'discover'

    identity = Locator(
        By.CSS_SELECTOR, 'div[data-analytics-scope="Registries Discover page"]'
    )
    search_box = Locator(By.ID, 'search')
    loading_indicator = Locator(By.CSS_SELECTOR, '.ball-scale', settings.LONG_TIMEOUT)
    osf_filter = Locator(
        By.CSS_SELECTOR, '[data-test-source-filter-id$="OSF Registries"]'
    )

    # Group Locators
    search_results = GroupLocator(
        By.CSS_SELECTOR, '._RegistriesSearchResult__Title_1wvii8'
    )

    def get_first_non_withdrawn_registration(self):
        for result in self.search_results:
            try:
                result.find_element_by_class_name('label-default')
            except NoSuchElementException:
                return result.find_element_by_css_selector(
                    '[data-test-result-title-id]'
                )


class BaseSubmittedRegistrationPage(GuidBasePage):
    base_url = settings.OSF_HOME
    url_addition = ''

    @property
    def url(self):
        return self.base_url + '/' + self.guid + '/' + self.url_addition


class RegistrationDetailPage(BaseSubmittedRegistrationPage):
    """This is the Registration Overview Page"""

    identity = Locator(By.CSS_SELECTOR, '[data-test-registration-title]')
    loading_indicator = Locator(By.CSS_SELECTOR, '.ball-scale', settings.LONG_TIMEOUT)


class RegistrationFileListPage(BaseSubmittedRegistrationPage):
    url_addition = 'files'
    identity = Locator(By.CSS_SELECTOR, '[data-test-file-providers-list]')
    file_list_button = Locator(By.CSS_SELECTOR, '[data-test-file-list-link]')
    loading_indicator = Locator(By.CSS_SELECTOR, '.ball-scale')
    first_file_link = Locator(By.CSS_SELECTOR, '[data-analytics-name="Open file"]')


class RegistrationFileDetailPage(GuidBasePage):
    identity = Locator(By.CSS_SELECTOR, '[data-test-file-renderer')


class RegistrationResourcesPage(BaseSubmittedRegistrationPage):
    url_addition = 'resources'
    identity = Locator(By.CSS_SELECTOR, '[data-test-add-resource-section]')


class RegistrationAddNewPage(BaseRegistriesPage):
    url_addition = 'new'
    identity = Locator(
        By.CSS_SELECTOR, 'form[data-test-new-registration-form]', settings.LONG_TIMEOUT
    )

    @property
    def url(self):
        """Have to override the url for the Add New Page since this page does
        include 'osf' in the url for OSF Registries
        """
        if self.provider is None:
            self.provider_id = 'osf'
        return urljoin(self.base_url, self.provider_id) + '/' + self.url_addition


class RegistriesModerationSubmittedPage(BaseRegistriesPage):
    url_addition = 'moderation/submitted'
    identity = Locator(By.CSS_SELECTOR, '[data-test-submissions-type]')
    no_registrations_message = Locator(
        By.CSS_SELECTOR, '[data-test-registration-list-none]'
    )


class RegistriesModerationPendingPage(BaseRegistriesPage):
    url_addition = 'moderation/pending'
    identity = Locator(By.CSS_SELECTOR, '[data-test-submissions-type]')
    no_registrations_message = Locator(
        By.CSS_SELECTOR, '[data-test-registration-list-none]'
    )


class RegistriesModerationModeratorsPage(BaseRegistriesPage):
    url_addition = 'moderation/moderators'
    identity = Locator(By.CSS_SELECTOR, '[data-test-moderator-row]')


class RegistriesModerationSettingsPage(BaseRegistriesPage):
    url_addition = 'moderation/settings'
    identity = Locator(By.CSS_SELECTOR, '[data-test-subscription-list]')


class BaseRegistrationDraftPage(BaseRegistriesPage):
    base_url = settings.OSF_HOME + '/registries/drafts/'
    url_addition = ''

    def __init__(self, driver, verify=False, draft_id=''):
        self.draft_id = draft_id
        super().__init__(driver, verify)

    @property
    def url(self):
        return self.base_url + self.draft_id + '/' + self.url_addition


class DraftRegistrationMetadataPage(BaseRegistrationDraftPage):
    url_addition = 'metadata'
    identity = Locator(
        By.CSS_SELECTOR, 'div[data-test-metadata-title]', settings.LONG_TIMEOUT
    )


class DraftRegistrationGenericPage(BaseRegistrationDraftPage):
    def __init__(self, driver, verify=False, draft_id='', url_addition=''):
        self.draft_id = draft_id
        self.url_addition = url_addition
        super().__init__(driver, verify, draft_id)

    identity = Locator(
        By.CSS_SELECTOR, 'div[data-analytics-scope="Registries"]', settings.LONG_TIMEOUT
    )
    page_heading = Locator(By.CSS_SELECTOR, 'h2[data-test-page-heading]')


class DraftRegistrationReviewPage(BaseRegistrationDraftPage):
    url_addition = 'review'
    identity = Locator(
        By.CSS_SELECTOR,
        '[data-test-toggle-anchor-nav-button]',
        settings.LONG_TIMEOUT,
    )
