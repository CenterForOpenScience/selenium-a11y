import re
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import markers
import settings
from api import osf_api
from components.accessibility import ApplyA11yRules as a11y
from components.email_access import EmailAccess
from pages.dashboard import DashboardPage
from pages.landing import LandingPage
from pages.login import ForgotPasswordPage, ResetPasswordPage
from pages.project import MyProjectsPage
from pages.quickfiles import QuickfileDetailPage, QuickfilesPage
from pages.register import RegisterPage
from pages.search import SearchPage
from pages.support import SupportPage


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


class TestMyQuickFilesPage:
    def test_accessibility(self, driver, session, must_be_logged_in):
        """ The Quick Files Page may or may not have any files listed depending on the
        current user. Users in the testing environment probably will, but the Production
        user may not.
        """
        quickfiles_page = QuickfilesPage(driver)
        quickfiles_page.goto()
        quickfiles_page.loading_indicator.here_then_gone()
        assert QuickfilesPage(driver, verify=True)
        a11y.run_axe(driver, session, 'quickfiles')


# For this next test we are uploading a text file to the user's Quick Files page so we
#     don't want to run this in Production.
@markers.dont_run_on_prod
class TestMyQuickFileDetailPage:
    def test_accessibility(self, driver, session, must_be_logged_in):
        osf_api.upload_single_quickfile(session)
        quickfiles_page = QuickfilesPage(driver)
        quickfiles_page.goto()
        quickfiles_page.loading_indicator.here_then_gone()
        # click on title of file in table to open the Quick File Detail page
        quickfiles_page.file_titles[0].click()
        assert QuickfileDetailPage(driver, verify=True)
        # wait for mfr iframe to be visible before running axe
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'mfrIframeParent'))
        )
        a11y.run_axe(driver, session, 'qfiledet')


class TestRegisterPage:
    def test_accessibility(self, driver, session):
        register_page = RegisterPage(driver)
        register_page.goto()
        assert RegisterPage(driver, verify=True)
        a11y.run_axe(driver, session, 'signup')


class TestSearchPage:
    def test_accessibility(self, driver, session):
        search_page = SearchPage(driver)
        search_page.goto()
        assert SearchPage(driver, verify=True)
        # Enter wildcard in search input box and press enter so that we have some search
        #     results on the page before running accessibility test
        search_page.search_bar.send_keys('*')
        search_page.search_bar.send_keys(Keys.ENTER)
        search_page.loading_indicator.here_then_gone()
        a11y.run_axe(driver, session, 'search')


class TestSupportPage:
    def test_accessibility(self, driver, session):
        support_page = SupportPage(driver)
        support_page.goto()
        assert SupportPage(driver, verify=True)
        a11y.run_axe(driver, session, 'support')


class TestForgotPasswordPage:
    def test_accessibility(self, driver, session):
        forgot_password_page = ForgotPasswordPage(driver)
        forgot_password_page.goto()
        assert ForgotPasswordPage(driver, verify=True)
        a11y.run_axe(driver, session, 'frgtpwrd')


# For the next test we have only set up test users with IMAP enabled email address in
#     the testing environments.
@markers.dont_run_on_prod
class TestResetPasswordPage:
    def test_accessibility(self, driver, session):
        # first go to Forgot Password page and enter email address and click Reset
        #     Password button
        forgot_password_page = ForgotPasswordPage(driver)
        forgot_password_page.goto()
        assert ForgotPasswordPage(driver, verify=True)
        forgot_password_page.email_input.send_keys(settings.IMAP_EMAIL)
        forgot_password_page.reset_password_button.click()
        # wait for the email to actually be sent
        time.sleep(10)
        # next we need to retrieve the email that was sent by OSF and get the link to
        #     the Reset Password page
        email_body = EmailAccess.get_latest_email_body_by_imap(
            settings.IMAP_HOST,
            settings.IMAP_EMAIL,
            settings.IMAP_EMAIL_PASSWORD,
            'Inbox',
            'SUBJECT',
            'Reset Password',
        )
        # search through the email body text and find the reset password link
        match = re.search('/resetpassword/' + '.{42}', str(email_body))
        # need to remove any literal carriage returns or line breaks from matched string
        reset_URL = match.group(0).replace('=\\r\\n', '')
        assert match is not None
        # reconstruct the full url for the reset password link and navigate to it
        driver.get(settings.OSF_HOME + reset_URL)
        assert ResetPasswordPage(driver, verify=True)
        # finally run axe to check accessibility
        a11y.run_axe(driver, session, 'resetpwrd')
