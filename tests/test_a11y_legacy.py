from components.accessibility import ApplyA11yRules as a11y

from pages import (
    search,
    project,
    login,
    user,
)

class TestProjectFiles:

    def test_accessibility(self, driver, session, must_be_logged_in):
        page = project.FilesPage(driver, guid='tcyeb')
        page.goto()
        assert project.FilesPage(driver, verify=True)
        a11y.run_axe(driver, session, 'project_files')

class TestUserProfile:

    def test_accessibility(self, driver, session, must_be_logged_in):
        page = user.UserProfilePage(driver)
        page.goto()
        assert user.UserProfilePage(driver, verify=True)
        a11y.run_axe(driver, session, 'user_profile')

class TestSearchPage:

    def test_accessibility(self, driver, session, must_be_logged_in):
        page = search.SearchPage(driver)
        page.goto()
        assert search.SearchPage(driver, verify=True)
        a11y.run_axe(driver, session, 'search')

class TestMyProjectsPage:

    def test_accessibility(self, driver, session, must_be_logged_in):
        page = project.MyProjectsPage(driver)
        page.goto()
        assert project.MyProjectsPage(driver, verify=True)
        a11y.run_axe(driver, session, 'my_projects')

class TestForgotPasswordPage:

    def test_accessibility(self, driver, session, must_be_logged_in):
        page = login.ForgotPasswordPage(driver)
        page.goto()
        assert login.ForgotPasswordPage(driver, verify=True)
        a11y.run_axe(driver, session, 'forgot_password')

class TestProjectOverviewPage:

    def test_accessibility(self, driver, session, must_be_logged_in):
        page = project.ProjectPage(driver, guid='tcyeb')
        page.goto()
        assert project.ProjectPage(driver, verify=True)
        a11y.run_axe(driver, session, 'project')

