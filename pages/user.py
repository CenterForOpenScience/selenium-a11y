from selenium.webdriver.common.by import By

import settings
from api import osf_api
from base.locators import ComponentLocator, GroupLocator, Locator
from components.user import SettingsSideNavigation
from pages.base import GuidBasePage, OSFBasePage


class UserProfilePage(GuidBasePage):
    user = osf_api.current_user()

    def __init__(self, driver, verify=False, guid=user.id):
        super().__init__(driver, verify, guid)

    # TODO: Reconsider using a component here (and using component locators correctly)
    identity = Locator(By.CLASS_NAME, 'profile-fullname', settings.LONG_TIMEOUT)
    no_public_projects_text = Locator(By.CSS_SELECTOR, '#publicProjects .help-block')
    no_public_components_text = Locator(
        By.CSS_SELECTOR, '#publicComponents .help-block'
    )
    edit_profile_link = Locator(By.CSS_SELECTOR, '#edit-profile-settings')

    # TODO: Seperate out by component if it becomes necessary
    loading_indicator = Locator(By.CSS_SELECTOR, '.ball-pulse')

    # Group Locators
    public_projects = GroupLocator(By.CSS_SELECTOR, '#publicProjects .list-group-item')
    public_components = GroupLocator(
        By.CSS_SELECTOR, '#publicComponents .list-group-item'
    )
    quickfiles = GroupLocator(By.CSS_SELECTOR, '#quickFiles .list-group-item')


class BaseUserSettingsPage(OSFBasePage):
    url = settings.OSF_HOME + '/settings/'

    identity = Locator(By.ID, 'profileSettings')

    # Components
    side_navigation = ComponentLocator(SettingsSideNavigation)


class ProfileInformationPage(BaseUserSettingsPage):
    url = settings.OSF_HOME + '/settings/'

    identity = Locator(By.CSS_SELECTOR, 'div[id="profileSettings"]')
    middle_name_input = Locator(
        By.CSS_SELECTOR, '#names > div > form > div:nth-child(5) > input'
    )
    save_button = Locator(
        By.CSS_SELECTOR,
        '#names > div > form > div.p-t-lg.p-b-lg > button.btn.btn-success',
    )
    update_success = Locator(By.CSS_SELECTOR, '.text-success')
    social_tab_link = Locator(By.LINK_TEXT, 'Social')
    employment_tab_link = Locator(By.LINK_TEXT, 'Employment')
    education_tab_link = Locator(By.LINK_TEXT, 'Education')


class AccountSettingsPage(BaseUserSettingsPage):
    url = settings.OSF_HOME + '/settings/account/'

    identity = Locator(
        By.CSS_SELECTOR, 'div[data-analytics-scope="Connected emails panel"]'
    )


class ConfigureAddonsPage(BaseUserSettingsPage):
    url = settings.OSF_HOME + '/settings/addons/'

    identity = Locator(By.CSS_SELECTOR, '#configureAddons')


class NotificationsPage(BaseUserSettingsPage):
    url = settings.OSF_HOME + '/settings/notifications/'

    identity = Locator(By.CSS_SELECTOR, '#notificationSettings')
    loading_indicator = Locator(By.CSS_SELECTOR, '.ball-scale', settings.LONG_TIMEOUT)


class EmberDeveloperAppsPage(BaseUserSettingsPage):
    url = settings.OSF_HOME + '/settings/applications/'

    identity = Locator(By.CSS_SELECTOR, '[data-test-create-app-link]')


class DeveloperAppsPage(BaseUserSettingsPage):
    waffle_override = {'ember_user_settings_apps_page': EmberDeveloperAppsPage}

    url = settings.OSF_HOME + '/settings/applications/'

    identity = Locator(By.CSS_SELECTOR, 'div[data-analytics-scope="Developer apps"')


class CreateDeveloperAppPage(BaseUserSettingsPage):
    url = settings.OSF_HOME + '/settings/applications/create'

    identity = Locator(By.CSS_SELECTOR, '[data-test-developer-app-name]')


class EmberPersonalAccessTokenPage(BaseUserSettingsPage):
    url = settings.OSF_HOME + '/settings/tokens/'

    identity = Locator(By.CSS_SELECTOR, '[data-test-create-token-link]')


class PersonalAccessTokenPage(BaseUserSettingsPage):
    waffle_override = {'ember_user_settings_tokens_page': EmberPersonalAccessTokenPage}

    url = settings.OSF_HOME + '/settings/tokens/'

    identity = Locator(By.CSS_SELECTOR, 'a[data-analytics-name="Personal access"]')


class CreatePersonalAccessTokenPage(BaseUserSettingsPage):
    url = settings.OSF_HOME + '/settings/tokens/create'

    identity = Locator(By.CSS_SELECTOR, '[data-test-token-name]')
