from selenium.webdriver.common.by import By

import markers
import settings
from components.accessibility import ApplyA11yRules as a11y
from pages.login import (
    CASAuthorizationPage,
    GenericCASPage,
    InstitutionalLoginPage,
    InstitutionForgotPasswordPage,
    Login2FAPage,
    LoginPage,
    LoginToSPage,
    UnsupportedInstitutionLoginPage,
    login,
)


class TestCASLoginPage:
    def test_accessibility(self, driver, session, write_files, exclude_best_practice):
        login_page = LoginPage(driver)
        login_page.goto()
        assert LoginPage(driver, verify=True)
        a11y.run_axe(
            driver,
            session,
            "login",
            write_files=write_files,
            exclude_best_practice=True,
        )


@markers.dont_run_on_prod
class TestLogin2FAPage:
    """This test logs in as a user with 2 Factor Authentication enabled. After entering
    their login credentials as normal the user is then directed to a 2 Factor Authentication
    page.
    """

    def test_accessibility(self, driver, session, write_files, exclude_best_practice):
        login(
            driver, user=settings.CAS_2FA_USER, password=settings.CAS_2FA_USER_PASSWORD
        )
        assert Login2FAPage(driver, verify=True)
        a11y.run_axe(
            driver,
            session,
            "login2FA",
            write_files=write_files,
            exclude_best_practice=True,
        )


@markers.dont_run_on_prod
class TestLoginToSPage:
    """This test logs in as a user that has not accepted the OSF Terms of Service.  After
    entering their login credentials as normal the user is then directed to a Terms of
    Service acceptance page.
    """

    def test_accessibility(self, driver, session, write_files, exclude_best_practice):
        login(
            driver, user=settings.CAS_TOS_USER, password=settings.CAS_TOS_USER_PASSWORD
        )
        assert LoginToSPage(driver, verify=True)
        a11y.run_axe(
            driver,
            session,
            "loginToS",
            write_files=write_files,
            exclude_best_practice=True,
        )


class TestInstitutionalLoginPage:
    def test_accessibility(self, driver, session, write_files, exclude_best_practice):
        institution_login_page = InstitutionalLoginPage(driver)
        institution_login_page.goto()
        assert InstitutionalLoginPage(driver, verify=True)
        a11y.run_axe(
            driver,
            session,
            "i9nlogin",
            write_files=write_files,
            exclude_best_practice=True,
        )


class TestPreselectedInstitutionLoginPage:
    def test_accessibility(self, driver, session, write_files, exclude_best_practice):
        preselectUrl = (
            settings.CAS_DOMAIN
            + "/login?campaign=institution&institutionId=nd&service="
            + settings.OSF_HOME
            + "/login/?next="
            + settings.OSF_HOME
            + "/"
        )
        driver.get(preselectUrl)
        assert driver.find_element(By.CSS_SELECTOR, "#institutionSelect").get_property(
            "disabled"
        )
        a11y.run_axe(
            driver,
            session,
            "i9npresel",
            write_files=write_files,
            exclude_best_practice=True,
        )


class TestUnsupportedInstitutionLoginPage:
    def test_accessibility(self, driver, session, write_files, exclude_best_practice):
        unsupported_institution_page = UnsupportedInstitutionLoginPage(driver)
        unsupported_institution_page.goto()
        assert UnsupportedInstitutionLoginPage(driver, verify=True)
        a11y.run_axe(
            driver,
            session,
            "unsupi9n",
            write_files=write_files,
            exclude_best_practice=True,
        )


class TestInstitutionForgotPasswordPage:
    """Test the Forgot Password page that is reached from the Unsupported Institution
    Login Page. This Forgot Password page is different from the other Forgot Password
    page in OSF.
    """

    def test_accessibility(self, driver, session, write_files, exclude_best_practice):
        unsupported_institution_page = UnsupportedInstitutionLoginPage(driver)
        unsupported_institution_page.goto()
        assert UnsupportedInstitutionLoginPage(driver, verify=True)
        # click the Set a password button to be redirtected to the Institution specific
        # Forgot Password page. Don't need to first enter an email address.
        unsupported_institution_page.set_password_button.click()
        assert InstitutionForgotPasswordPage(driver, verify=True)
        a11y.run_axe(
            driver,
            session,
            "i9nfrgtpswrd",
            write_files=write_files,
            exclude_best_practice=True,
        )


class TestGenericCASExceptionPage:
    def test_accessibility(self, driver, session, write_files, exclude_best_practice):
        """Test the Service not authorized exception page by having an invalid service in the url"""
        driver.get(settings.CAS_DOMAIN + "/login?service=https://noservice.osf.io/")
        assert GenericCASPage(driver, verify=True)
        a11y.run_axe(
            driver,
            session,
            "genCASExcept",
            write_files=write_files,
            exclude_best_practice=True,
        )


@markers.dont_run_on_prod
class TestCASOauthAuthorizationPage:
    def test_accessibility(
        self, driver, session, write_files, exclude_best_practice, must_be_logged_in
    ):
        """Test the CAS Oauth Authorization page by building an authorization url using
        the required parameters and then navigating to that url. No need to complete the
        authorization process since we just want to evaluate the authorization page for
        accessibility compliance.
        """
        client_id = settings.DEVAPP_CLIENT_ID
        redirect_uri = "https://www.google.com/"
        requested_scope = (
            "osf.nodes.metadata_read osf.nodes.access_read osf.nodes.data_read"
        )
        authorization_url = (
            settings.CAS_DOMAIN
            + "/oauth2/authorize?response_type=code&client_id="
            + client_id
            + "&redirect_uri="
            + redirect_uri
            + "&scope="
            + requested_scope
            + "&access_type=online"
        )
        # navigate to the authorization url in the browser
        driver.get(authorization_url)
        assert CASAuthorizationPage(driver, verify=True)
        a11y.run_axe(
            driver,
            session,
            "CASOauth",
            write_files=write_files,
            exclude_best_practice=True,
        )
