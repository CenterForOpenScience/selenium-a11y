from time import sleep

from selenium.webdriver.common.by import By

import settings
from base.locators import BaseElement, GroupLocator, Locator


class EmberCreateProjectModal(BaseElement):

    modal = Locator(By.CLASS_NAME, "modal-dialog")
    create_project_button = Locator(
        By.CSS_SELECTOR, "[data-test-create-project-submit]"
    )
    cancel_button = Locator(By.CSS_SELECTOR, "[data-test-create-project-cancel]")
    title_input = Locator(By.CSS_SELECTOR, "._NewProject__label_fz56y2 input")
    select_all_link = Locator(By.XPATH, '//button[text()="Select all"]')
    remove_all_link = Locator(By.XPATH, '//button[text()="Remove all"]')
    more_arrow = Locator(By.CSS_SELECTOR, 'button[data-analytics-name="Toggle more"]')
    description_input = Locator(By.CLASS_NAME, "project-desc")
    template_dropdown = Locator(By.CLASS_NAME, "ember-power-select-placeholder")

    def institution_selected(self, institution):
        try:
            logo = self.modal.find_element_by_name(institution)
            return "0.25" not in logo.value_of_css_property("opacity")
        except Exception:
            raise ValueError(
                "Institution logo for {} not present in modal".format(institution)
            )


class EmberProjectCreatedModal(BaseElement):

    go_to_project_href_link = Locator(
        By.CSS_SELECTOR, ".modal-dialog a", settings.LONG_TIMEOUT
    )
    keep_working_here_button = Locator(By.CSS_SELECTOR, "button.btn-default")


class EmberProjectList(BaseElement):

    search_input = Locator(By.CSS_SELECTOR, "._quick-search-input_1b28t4 > input")
    top_project_link = Locator(By.CLASS_NAME, "_DashboardItem_17nn6d")
    sort_title_asc_button = Locator(
        By.CSS_SELECTOR,
        '._quick-search-col_1b28t4 ._SortButton_1ifm79 [title~="ascending"]',
    )
    sort_title_dsc_button = Locator(
        By.CSS_SELECTOR,
        '._quick-search-col_1b28t4 ._SortButton_1ifm79 [title~="descending"]',
    )
    sort_date_asc_button = Locator(
        By.CSS_SELECTOR,
        '.col-md-3 ._quick-search-col_1b28t4 ._SortButton_1ifm79 [title~="ascending"]',
    )
    sort_date_dsc_button = Locator(
        By.CSS_SELECTOR,
        '.col-md-3 ._quick-search-col_1b28t4 ._SortButton_1ifm79 [title~="descending"]',
    )
    loading_dashboard_item = Locator(
        By.CLASS_NAME, "_loading-dashboard-item_1b28t4", settings.QUICK_TIMEOUT
    )

    # Group Locators
    project_list_projects = GroupLocator(
        By.CSS_SELECTOR, "._quick-search-table_1b28t4 a"
    )

    def get_nth_project_link(self, n=0):
        if self.loading_dashboard_item.here_then_gone():
            try:
                element = self.project_list_projects[n - 1]
                return element.get_attribute("href")
            except IndexError:
                raise ValueError("Unable to find a project at position {}".format(n))
        raise ValueError("Dashboard page is still loading.")

    def get_list_length(self):
        if self.loading_dashboard_item.here_then_gone():
            return len(self.project_list_projects)
        raise ValueError("Dashboard page is still loading.")


class CreateProjectModal(BaseElement):

    modal = Locator(By.ID, "addProjectFromHome")
    create_project_button = Locator(
        By.CSS_SELECTOR, "#addProject button.btn.btn-success"
    )
    cancel_button = Locator(
        By.CSS_SELECTOR,
        "#addProjectFromHome > div > div > div.modal-footer > button.btn.btn-default",
    )
    title_input = Locator(By.CSS_SELECTOR, ".form-control")
    select_all_link = Locator(By.XPATH, '//a[text()="Select all"]')
    remove_all_link = Locator(By.XPATH, '//a[text()="Remove all"]')
    more_arrow = Locator(
        By.CSS_SELECTOR,
        "#addProjectFromHome > div > div > div.modal-body > div > div.text-muted.pointer",
    )
    description_input = Locator(
        By.CSS_SELECTOR,
        "#addProjectFromHome > div > div > div.modal-body > div > div:nth-child(4) > input",
    )
    template_dropdown = Locator(By.ID, "select2-chosen-2")

    def institution_selected(self, institution):
        try:
            logo = self.modal.find_element(By.NAME, institution)
            return "0.25" not in logo.value_of_css_property("opacity")
        except Exception:
            raise ValueError(
                "Institution logo for {} not present in modal".format(institution)
            )


class ProjectCreatedModal(BaseElement):

    go_to_project_href_link = Locator(
        By.XPATH, '//a[text()="Go to new project"]', settings.LONG_TIMEOUT
    )
    keep_working_here_button = Locator(
        By.CSS_SELECTOR, 'button[data-dismiss="modal"]', settings.TIMEOUT
    )


class CreateCollectionModal(BaseElement):

    modal = Locator(By.CSS_SELECTOR, "#addColl")
    name_input = Locator(By.CSS_SELECTOR, "#addCollInput")
    add_button = Locator(By.CSS_SELECTOR, "#addColl .btn-success")
    cancel_button = Locator(By.CSS_SELECTOR, "#addColl .btn-default")


class DeleteCollectionModal(BaseElement):

    modal = Locator(By.CSS_SELECTOR, "#removeColl")
    delete_button = Locator(By.CSS_SELECTOR, "#removeColl .btn-danger")
    cancel_button = Locator(By.CSS_SELECTOR, "#removeColl .btn-default")


class ProjectList(BaseElement):

    search_input = Locator(By.ID, "searchQuery", settings.LONG_TIMEOUT)
    top_project_link = Locator(
        By.CSS_SELECTOR, "div.quick-search-table > div:nth-child(3) > a:nth-child(1)"
    )
    sort_title_asc_button = Locator(
        By.CSS_SELECTOR,
        "div.quick-search-table > div.row.node-col-headers.m-t-md > div.col-sm-3.col-md-6 > div > button:nth-child(1)",
    )
    sort_title_dsc_button = Locator(
        By.CSS_SELECTOR,
        "div.quick-search-table > div.row.node-col-headers.m-t-md > div.col-sm-3.col-md-6 > div > button:nth-child(2)",
    )
    sort_date_asc_button = Locator(
        By.CSS_SELECTOR,
        "div.quick-search-table > div.row.node-col-headers.m-t-md > div:nth-child(3) > div > span > button:nth-child(1)",
    )
    sort_date_dsc_button = Locator(
        By.CSS_SELECTOR,
        "div.quick-search-table > div.row.node-col-headers.m-t-md > div:nth-child(3) > div > span > button:nth-child(2)",
    )

    # Group Locators
    project_list_projects = GroupLocator(
        By.CSS_SELECTOR, "div.quick-search-table > div:nth-child(3) > a"
    )

    def get_nth_project_link(self, n=0):
        base_selector = "div.quick-search-table > div:nth-child(3) > a:nth-child"
        try:
            selector = "{}({})".format(base_selector, n)
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
            guid = element.get_attribute("href").strip("/")
            return guid
        except Exception:
            raise ValueError("Unable to find a project at position {}".format(n))

    def get_list_length(self):
        sleep(0.4)  # Need sleep to let quicksearch do its thing
        return len(self.project_list_projects)
