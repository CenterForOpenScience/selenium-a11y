from selenium.webdriver.common.by import By

from base.locators import BaseElement, Locator


class SettingsSideNavigation(BaseElement):
    profile_information_link = Locator(By.XPATH, '//a[text()="Profile information"]')
    account_settings_link = Locator(By.XPATH, '//a[text()="Account settings"]')
    configure_addons_link = Locator(By.XPATH, '//a[text()="Configure add-on accounts"]')
    notifications_link = Locator(By.XPATH, '//a[text()="Notifications"]')
    developer_apps_link = Locator(By.XPATH, '//a[text()="Developer apps"]')
    personal_access_tokens_link = Locator(
        By.XPATH, '//a[text()="Personal access tokens"]'
    )
