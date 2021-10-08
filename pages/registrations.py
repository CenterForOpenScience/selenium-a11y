from selenium.webdriver.common.by import By

import settings
from base.locators import GroupLocator, Locator
from pages.base import OSFBasePage


class MyRegistrationsPage(OSFBasePage):
    url = settings.OSF_HOME + '/registries/my-registrations/'
    identity = Locator(
        By.CSS_SELECTOR, 'div[data-analytics-scope="My Registrations page"]'
    )

    drafts_tab = Locator(By.CSS_SELECTOR, '[data-test-my-registrations-nav="drafts"]')
    no_drafts_message = Locator(By.CSS_SELECTOR, 'p[data-test-draft-list-no-drafts]')
    draft_registration_title = Locator(
        By.CSS_SELECTOR, 'a[data-analytics-name="view_registration"]'
    )

    submissions_tab = Locator(By.XPATH, '//a[text()="Submitted"]')
    no_submissions_message = Locator(
        By.CSS_SELECTOR, 'p[data-test-draft-list-no-registrations]'
    )
    public_registration_title = Locator(By.CSS_SELECTOR, 'a[data-test-node-title]')

    create_a_registration_button = GroupLocator(
        By.XPATH, '//button[text()="Create a registration"]'
    )

    draft_registration_cards = GroupLocator(
        By.CSS_SELECTOR, 'div[data-test-draft-registration-card]'
    )

    def get_first_draft_id_by_template(self, template_name):
        for draft_card in self.draft_registration_cards:
            template = draft_card.find_element_by_css_selector('[data-test-form-type]')
            if template_name in template.text:
                url = draft_card.find_element_by_css_selector(
                    'a[data-analytics-name="view_registration"]'
                ).get_attribute('href')
                draft_id = url.split('drafts/', 1)[1]
                return draft_id
