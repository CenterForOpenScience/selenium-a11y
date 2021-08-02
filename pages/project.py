import settings

from selenium.webdriver.common.by import By

from api import osf_api
from components.project import FileWidget, LogWidget
from components.dashboard import CreateProjectModal, CreateCollectionModal, DeleteCollectionModal, ProjectCreatedModal
from pages.base import GuidBasePage, OSFBasePage
from base.locators import Locator, ComponentLocator, GroupLocator


class ProjectPage(GuidBasePage):

    identity = Locator(By.CSS_SELECTOR, '#overview > nav#projectSubnav')
    title = Locator(By.ID, 'nodeTitleEditable', settings.LONG_TIMEOUT)
    title_input = Locator(By.CSS_SELECTOR, '.form-inline input')
    title_edit_submit_button = Locator(By.CSS_SELECTOR, '.editable-submit')
    title_edit_cancel_button = Locator(By.CSS_SELECTOR, '.editable-cancel')
    make_public_link = Locator(By.XPATH, '//a[contains(text(), "Make Public")]')
    make_private_link = Locator(By.XPATH, '//a[contains(text(), "Make Private")]')
    confirm_privacy_change_link = Locator(By.XPATH, '//a[text()="Confirm"]')
    cancel_privacy_change_link = Locator(By.XPATH, '//a[text()="Cancel"]')

    # Components
    file_widget = ComponentLocator(FileWidget)
    log_widget = ComponentLocator(LogWidget)

class RequestAccessPage(GuidBasePage):

    identity = Locator(By.CSS_SELECTOR, '#requestAccessPrivateScope')


class MyProjectsPage(OSFBasePage):
    url = settings.OSF_HOME + '/myprojects/'

    identity = Locator(By.CSS_SELECTOR, '.col-xs-8 > h3:nth-child(1)', settings.LONG_TIMEOUT)
    create_project_button = Locator(By.CSS_SELECTOR, '[data-target="#addProject"]')
    create_collection_button = Locator(By.CSS_SELECTOR, '[data-target="#addColl"]')
    first_project = Locator(By.CSS_SELECTOR, 'div[class="tb-tbody-inner"] > div:first-child > div:nth-child(1)')
    first_project_hyperlink = Locator(By.CSS_SELECTOR, 'div[data-rindex="0"] > div:first-child >'
                                                       ' span:last-child > a:first-child')
    first_custom_collection = Locator(By.CSS_SELECTOR, 'li[data-index="4"] span', settings.QUICK_TIMEOUT)
    first_collection_settings_button = Locator(By.CSS_SELECTOR, '.fa-ellipsis-v', settings.QUICK_TIMEOUT)
    first_collection_remove_button = Locator(By.CSS_SELECTOR, '[data-target="#removeColl"]', settings.QUICK_TIMEOUT)

    # Components
    create_collection_modal = ComponentLocator(CreateCollectionModal)
    delete_collection_modal = ComponentLocator(DeleteCollectionModal)
    create_project_modal = ComponentLocator(CreateProjectModal)
    project_created_modal = ComponentLocator(ProjectCreatedModal)


class AnalyticsPage(GuidBasePage):
    base_url = settings.OSF_HOME + '/{guid}/analytics/'

    identity = Locator(By.CSS_SELECTOR, '._Counts_1mhar6')
    private_project_message = Locator(By.CSS_SELECTOR, '._PrivateProject_1mhar6')
    disabled_chart = Locator(By.CSS_SELECTOR, '._Chart_1hff7g _Blurred_1hff7g')


class ForksPage(GuidBasePage):
    base_url = settings.OSF_HOME + '/{guid}/forks/'

    identity = Locator(By.CSS_SELECTOR, '._Forks_1xlord')
    new_fork_button = Locator(By.CSS_SELECTOR, '._Forks__new-fork_1xlord .btn-success')
    create_fork_modal_button = Locator(By.CSS_SELECTOR, '.modal-footer .btn-info')
    cancel_modal_button = Locator(By.CSS_SELECTOR, '.modal-footer .btn-default')
    info_toast = Locator(By.CSS_SELECTOR, '.toast-info')
    fork_link = Locator(By.CSS_SELECTOR, 'a[data-analytics-name="Title"]')
    fork_authors = Locator(By.CSS_SELECTOR, 'div[class="_NodeCard__authors_1i3kzz"]')
    placeholder_text = Locator(By.CSS_SELECTOR, 'div[class="_Forks__placeholder_1xlord"]')

    # Group Locators
    listed_forks = GroupLocator(By.CSS_SELECTOR, '.list-group-item')


class FilesPage(GuidBasePage):
    base_url = settings.OSF_HOME + '/{guid}/files/'

    identity = Locator(By.CSS_SELECTOR, '#treeGrid')
    session = osf_api.get_default_session()
    fangorn_rows = GroupLocator(By.CSS_SELECTOR, '#tb-tbody .fg-file-links')
    fangorn_addons = GroupLocator(By.CSS_SELECTOR, "div[data-level='2']")
    file_action_buttons = GroupLocator(By.CSS_SELECTOR, '#folderRow .fangorn-toolbar-icon')
    delete_modal = Locator(By.CSS_SELECTOR, 'span.btn:nth-child(1)')


"""Note that the class FilesPage in pages/project.py is used for test_project_files.py.
The class FileWidget in components/project.py is used for tests test_file_widget_loads
and test_addon_files_load in test_project.py.
In the future, we may want to put all files tests in one place."""
