import pytest
from faker import Faker

import settings

from api import osf_api
from pythosf import client
from pages.login import logout, safe_login
from pages.project import ProjectPage
from utils import launch_driver


@pytest.fixture(scope='session')
def session():
    return client.Session(api_base_url=settings.API_DOMAIN, auth=(settings.USER_ONE, settings.USER_ONE_PASSWORD))

@pytest.fixture(scope='session', autouse=True)
def check_credentials(session):
    # TODO: Add future check for USER_TWO
    try:
        osf_api.current_user(session)
    except Exception:
        pytest.exit('Your user credentials are incorrect.')

@pytest.fixture(scope='session')
def driver():
    driver = launch_driver()
    yield driver
    driver.quit()

@pytest.fixture(scope='session')
def fake():
    return Faker()

@pytest.fixture(scope='session', autouse=True)
def waffled_pages(session):
    settings.EMBER_PAGES = osf_api.waffled_pages(session)

@pytest.fixture(scope='session', autouse=True)
def hide_cookie_banner(driver):
    """Set the cookieconsent cookie so that that cookie banner doesn't show up
    (as it can obscure other UI elements).
     Note: If we ever want to test that banner will need to stop this cookie from being set.
    """
    driver.get(settings.OSF_HOME)
    driver.add_cookie({'name': 'osf_cookieconsent', 'value': '1', 'domain': '.osf.io'})

@pytest.fixture(scope='class', autouse=True)
def default_logout(driver):
    logout(driver)

@pytest.fixture(scope='class')
def must_be_logged_in(driver):
    safe_login(driver)

@pytest.fixture(scope='class')
def must_be_logged_in_as_user_two(driver):
    safe_login(driver, user=settings.USER_TWO, password=settings.USER_TWO_PASSWORD)

@pytest.fixture(scope='class')
def delete_user_projects_at_setup(session):
    osf_api.delete_all_user_projects(session=session)

@pytest.fixture
def default_project(session):
    """Creates a new project through the api and returns it. Deletes the project at the end of the test run.
     If PREFERRED_NODE is set, returns the APIDetail of preferred node.
     """
    if settings.PREFERRED_NODE:
        yield osf_api.get_node(session)
    else:
        project = osf_api.create_project(session, title='OSF Test Project')
        yield project
        project.delete()

@pytest.fixture
def default_project_page(driver, default_project):
    return ProjectPage(driver, guid=default_project.id)

@pytest.fixture
def public_project(session):
    if settings.PRODUCTION:
        raise ValueError('You should not create public projects on production!')
    project = osf_api.create_project(session, title='OSF Test Project', public=True)
    yield project
    project.delete()

@pytest.fixture
def project_with_file(session, default_project):
    """Returns a project with a file.
    Returns PREFERRED_NODE if it is set.
    """
    if settings.PREFERRED_NODE:
        osf_api.get_existing_file(session)
    else:
        osf_api.upload_fake_file(session, default_project)
    return default_project
