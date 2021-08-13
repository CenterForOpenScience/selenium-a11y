from selenium.webdriver.common.keys import Keys

from components.accessibility import ApplyA11yRules as a11y
from pages.dashboard import DashboardPage
from pages.landing import LandingPage
from pages.login import ForgotPasswordPage
from pages.project import MyProjectsPage
from pages.search import SearchPage


class TestOSFHomePage:
    def test_accessibility(self, driver, session):
        landing_page = LandingPage(driver)
        landing_page.goto()
        assert LandingPage(driver, verify=True)
        a11y.run_axe(driver, session, 'home')


class TestDashboardPage:
    def test_accessibility(self, driver, session, must_be_logged_in):
        dashboard_page = DashboardPage(driver)
        dashboard_page.goto()
        assert DashboardPage(driver, verify=True)
        a11y.run_axe(driver, session, 'dash')


class TestMyProjectsPage:
    def test_accessibility(self, driver, session, must_be_logged_in):
        my_projects_page = MyProjectsPage(driver)
        my_projects_page.goto()
        assert MyProjectsPage(driver, verify=True)
        a11y.run_axe(driver, session, 'myproj')


class TestSearchPage:
    def test_accessibility(self, driver, session):
        search_page = SearchPage(driver)
        search_page.goto()
        assert SearchPage(driver, verify=True)
        # Enter wildcard in search input box and press enter so that we have some search results on the page before
        # running accessibility test
        search_page.search_bar.send_keys('*')
        search_page.search_bar.send_keys(Keys.ENTER)
        search_page.loading_indicator.here_then_gone()
        a11y.run_axe(driver, session, 'search')


class TestForgotPasswordPage:
    def test_accessibility(self, driver, session):
        forgot_password_page = ForgotPasswordPage(driver)
        forgot_password_page.goto()
        assert ForgotPasswordPage(driver, verify=True)
        a11y.run_axe(driver, session, 'frgtpwrd')
