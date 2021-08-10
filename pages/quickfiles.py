from selenium.webdriver.common.by import By

import settings
from api import osf_api
from base.locators import ComponentLocator, GroupLocator, Locator
from components.dashboard import EmberCreateProjectModal, EmberProjectCreatedModal
from components.navbars import EmberNavbar
from pages.base import GuidBasePage, OSFBasePage


class BaseQuickfilesPage(OSFBasePage):

    navbar = ComponentLocator(EmberNavbar)


class QuickfilesPage(BaseQuickfilesPage, GuidBasePage):
    """Main page for a user's quickfiles. Take's a user's guid, but defaults to USER_ONE's if a guid isn't given.
    """

    base_url = settings.OSF_HOME + '/{guid}/quickfiles/'
    user = osf_api.current_user()

    def __init__(self, driver, verify=False, guid=user.id):
        super().__init__(driver, verify, guid)

    identity = Locator(By.ID, 'quickfiles-dropzone')
    loading_indicator = Locator(By.CSS_SELECTOR, '.ball-scale')
    upload_button = Locator(By.CSS_SELECTOR, 'button[data-analytics-name="Upload"]')
    share_button = Locator(By.CSS_SELECTOR, '[data-test-share-dialog-button]')
    download_button = Locator(By.CSS_SELECTOR, '[data-test-download-button]')
    download_as_zip_button = Locator(By.CSS_SELECTOR, '[data-test-download-zip-button]')
    view_button = Locator(By.CSS_SELECTOR, '[data-test-view-button]')
    help_button = Locator(By.CSS_SELECTOR, '[data-test-info-button]')
    filter_button = Locator(By.CSS_SELECTOR, '[data-test-filter-button]')
    rename_button = Locator(By.CSS_SELECTOR, '[data-test-rename-file-button]')
    delete_button = Locator(By.CSS_SELECTOR, '[data-test-delete-file-button]')
    move_button = Locator(By.CSS_SELECTOR, '[data-test-move-button]')

    filter_input = Locator(By.CSS_SELECTOR, '[data-test-filter-input]')
    filter_close_button = Locator(By.CSS_SELECTOR, '[data-test-close-filter]')
    generic_modal = Locator(By.CSS_SELECTOR, '.modal-title')
    help_modal_close_button = Locator(
        By.CSS_SELECTOR, '[data-test-close-current-modal]'
    )
    share_popover = Locator(By.CSS_SELECTOR, '[data-test-file-share-copyable-text]')
    move_create_new_project_button = Locator(
        By.CSS_SELECTOR, '[data-test-ps-new-project-button]'
    )
    move_existing_project_button = Locator(
        By.CSS_SELECTOR, '[data-test-ps-existing-project-button]'
    )
    move_modal_close_button = Locator(
        By.CSS_SELECTOR, '[data-test-move-to-project-modal-close-button]'
    )
    confirm_delete_button = Locator(
        By.CSS_SELECTOR, '[data-test-delete-file-confirm-button]'
    )
    flash_message = Locator(By.CSS_SELECTOR, '.flash-message')
    rename_input = Locator(By.CSS_SELECTOR, '[data-test-rename-field="rename"]')
    rename_save_button = Locator(By.CSS_SELECTOR, '[data-test-save-rename]')
    rename_close_button = Locator(By.CSS_SELECTOR, '[data-test-close-rename]')

    # Group Locators
    files = GroupLocator(By.CSS_SELECTOR, '._file-browser-item_1v8xgw')
    file_titles = GroupLocator(By.CSS_SELECTOR, '[data-test-file-item-link]')

    # Components
    create_project_modal = ComponentLocator(EmberCreateProjectModal)
    project_created_modal = ComponentLocator(EmberProjectCreatedModal)


class QuickfileDetailPage(BaseQuickfilesPage, GuidBasePage):
    identity = Locator(By.CSS_SELECTOR, 'div[data-analytics-scope="File detail"]')

    delete_button = Locator(By.CSS_SELECTOR, '[data-test-delete-button]')
    download_button = Locator(By.CSS_SELECTOR, '[data-test-download-button]')
    share_button = Locator(By.CSS_SELECTOR, '[data-test-share-button]')
    view_button = Locator(By.CSS_SELECTOR, 'button[data-analytics-name="View"]')
    edit_button = Locator(By.CSS_SELECTOR, 'button[data-analytics-name="Edit"]')
    revisions_button = Locator(By.CSS_SELECTOR, '[data-test-revisions-tab]')
    filter_button = Locator(By.CSS_SELECTOR, '[data-test-filter-button]')
