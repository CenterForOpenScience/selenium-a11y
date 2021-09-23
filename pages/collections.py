from urllib.parse import urljoin

from selenium.webdriver.common.by import By

import settings
from base.locators import Locator
from pages.base import OSFBasePage


class BaseCollectionPage(OSFBasePage):
    """The base page from which all collection pages inherit.
    """

    base_url = settings.OSF_HOME + '/collections/'
    url_addition = ''

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


class CollectionDiscoverPage(BaseCollectionPage):
    url_addition = 'discover'

    identity = Locator(By.CSS_SELECTOR, 'div[data-test-provider-branding]')
    loading_indicator = Locator(By.CSS_SELECTOR, '.ball-scale')


class CollectionSubmitPage(BaseCollectionPage):
    url_addition = 'submit'

    identity = Locator(By.CSS_SELECTOR, 'div[data-test-collections-submit-sections]')
    project_selector = Locator(
        By.CSS_SELECTOR, 'span[class="ember-power-select-placeholder"]'
    )
    project_help_text = Locator(
        By.CSS_SELECTOR, '.ember-power-select-option--search-message'
    )
    project_selector_project = Locator(By.CSS_SELECTOR, '.ember-power-select-option')
    project_metadata_save = Locator(
        By.CSS_SELECTOR, '[data-test-project-metadata-save-button]'
    )
