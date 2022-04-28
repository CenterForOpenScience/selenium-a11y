import re

from selenium.webdriver.common.keys import Keys

import markers
import settings
from components.accessibility import ApplyA11yRules as a11y
from components.email_access import EmailAccess
from pages.dashboard import DashboardPage
from pages.landing import LandingPage
from pages.login import ForgotPasswordPage, ResetPasswordPage
from pages.project import MyProjectsPage
from pages.register import RegisterPage
from pages.search import SearchPage
from pages.support import SupportPage


@markers.ember_page
class TestOSFHomePage:
    def test_accessibility(self, driver, session, write_files, exclude_best_practice):
        landing_page = LandingPage(driver)
        landing_page.goto()
        assert LandingPage(driver, verify=True)
        a11y.run_axe(
            driver,
            session,
            'home',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )


@markers.ember_page
class TestDashboardPage:
    def test_accessibility(
        self, driver, session, write_files, exclude_best_practice, must_be_logged_in
    ):
        dashboard_page = DashboardPage(driver)
        dashboard_page.goto()
        assert DashboardPage(driver, verify=True)
        a11y.run_axe(
            driver,
            session,
            'dash',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )


@markers.legacy_page
class TestMyProjectsPage:
    def test_accessibility(
        self, driver, session, write_files, exclude_best_practice, must_be_logged_in
    ):
        my_projects_page = MyProjectsPage(driver)
        my_projects_page.goto()
        assert MyProjectsPage(driver, verify=True)
        my_projects_page.empty_collection_indicator.present()
        a11y.run_axe(
            driver,
            session,
            'myproj',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )


@markers.ember_page
class TestRegisterPage:
    def test_accessibility(self, driver, session, write_files, exclude_best_practice):
        register_page = RegisterPage(driver)
        register_page.goto()
        assert RegisterPage(driver, verify=True)
        a11y.run_axe(
            driver,
            session,
            'signup',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )


@markers.legacy_page
class TestSearchPage:
    def test_accessibility(self, driver, session, write_files, exclude_best_practice):
        search_page = SearchPage(driver)
        search_page.goto()
        assert SearchPage(driver, verify=True)
        # Enter wildcard in search input box and press enter so that we have some search
        #     results on the page before running accessibility test
        search_page.search_bar.send_keys('*')
        search_page.search_bar.send_keys(Keys.ENTER)
        search_page.loading_indicator.here_then_gone()
        a11y.run_axe(
            driver,
            session,
            'search',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )


@markers.ember_page
class TestSupportPage:
    def test_accessibility(self, driver, session, write_files, exclude_best_practice):
        support_page = SupportPage(driver)
        support_page.goto()
        assert SupportPage(driver, verify=True)
        a11y.run_axe(
            driver,
            session,
            'support',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )


@markers.legacy_page
class TestForgotPasswordPage:
    def test_accessibility(self, driver, session, write_files, exclude_best_practice):
        forgot_password_page = ForgotPasswordPage(driver)
        forgot_password_page.goto()
        assert ForgotPasswordPage(driver, verify=True)
        a11y.run_axe(
            driver,
            session,
            'frgtpwrd',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )


@markers.legacy_page
# For the next test we have only set up test users with IMAP enabled email address in
#     the testing environments.
@markers.dont_run_on_prod
class TestResetPasswordPage:
    def test_accessibility(self, driver, session, write_files, exclude_best_practice):
        # First go to Forgot Password page and enter email address and click Reset
        #     Password button
        forgot_password_page = ForgotPasswordPage(driver)
        forgot_password_page.goto()
        assert ForgotPasswordPage(driver, verify=True)
        forgot_password_page.email_input.send_keys(settings.IMAP_EMAIL)
        forgot_password_page.reset_password_button.click()
        # Loop until the new email arrives in the inbox
        email_count = 0
        loop_counter = 0
        while email_count == 0:
            # Retrieve count of UNSEEN email messages from inbox
            email_count = EmailAccess.get_count_of_unseen_emails_by_imap(
                settings.IMAP_HOST,
                settings.IMAP_EMAIL,
                settings.IMAP_EMAIL_PASSWORD,
            )
            # To prevent an endless loop waiting for the email
            loop_counter += 1
            if loop_counter == 60:
                raise Exception(
                    'No unseen emails. Verify that Reset Password email was sent.'
                )
                break

        # Only proceed with accessibility check if there is an email
        if email_count > 0:
            # Next we need to retrieve the email that was sent by OSF and get the link to
            #     the Reset Password page
            email_body = EmailAccess.get_latest_email_body_by_imap(
                settings.IMAP_HOST,
                settings.IMAP_EMAIL,
                settings.IMAP_EMAIL_PASSWORD,
                'Inbox',
                'SUBJECT',
                'Reset Password',
            )
            # Search through the email body text and find the reset password link
            match = re.search('/resetpassword/' + '.{42}', str(email_body))
            # Need to remove any literal carriage returns or line breaks from matched string
            reset_URL = match.group(0).replace('=\\r\\n', '')
            assert match is not None
            # Reconstruct the full url for the reset password link and navigate to it
            driver.get(settings.OSF_HOME + reset_URL)
            assert ResetPasswordPage(driver, verify=True)
            # Finally run axe to check accessibility
            a11y.run_axe(
                driver,
                session,
                'resetpwrd',
                write_files=write_files,
                exclude_best_practice=exclude_best_practice,
            )
