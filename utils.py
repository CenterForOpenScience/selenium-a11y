from selenium import webdriver

import settings


def launch_driver(driver_name=settings.DRIVER, desired_capabilities=None):
    """Create and configure a WebDriver.
    Args:
        driver_name : Name of WebDriver to use
        desired_capabilities : Desired browser specs
    """

    try:
        driver_cls = getattr(webdriver, driver_name)
    except AttributeError:
        driver_cls = getattr(webdriver, settings.DRIVER)

    if driver_name == 'Remote':
        if desired_capabilities is None:
            desired_capabilities = settings.DESIRED_CAP
        command_executor = 'http://{}:{}@hub.browserstack.com:80/wd/hub'.format(
            settings.BSTACK_USER, settings.BSTACK_KEY
        )
        # DeprecationWarning: Please use FirefoxOptions to set browser profile
        from selenium.webdriver import FirefoxProfile

        ffp = FirefoxProfile()
        # Set the default download location [0=Desktop, 1=Downloads, 2=Specified location]
        ffp.set_preference('browser.download.folderList', 2)
        # Specify the download directory
        ffp.set_preference('browser.download.dir', 'Users/Public/Downloads')
        # Disable the OS-level pop-up modal
        ffp.set_preference('browser.download.manager.showWhenStarting', False)
        ffp.set_preference('browser.helperApps.alwaysAsk.force', False)
        # Specify the file types supported by the download
        ffp.set_preference(
            'browser.helperApps.neverAsk.saveToDisk',
            'text/plain, application/octet-stream, application/binary, text/csv, application/csv, '
            'application/excel, text/comma-separated-values, text/xml, application/xml',
        )
        driver = driver_cls(
            command_executor=command_executor,
            desired_capabilities=desired_capabilities,
            browser_profile=ffp,
        )
    elif driver_name == 'Chrome' and settings.HEADLESS:
        from selenium.webdriver.chrome.options import Options

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('window-size=1200x600')
        driver = driver_cls(chrome_options=chrome_options)
    elif driver_name == 'Chrome' and not settings.HEADLESS:
        from selenium.webdriver.chrome.options import Options

        chrome_options = Options()
        # disable w3c for local testing
        chrome_options.add_experimental_option('w3c', False)
        preferences = {'download.default_directory': ''}
        chrome_options.add_experimental_option('prefs', preferences)
        driver = driver_cls(chrome_options=chrome_options)
    elif driver_name == 'Firefox' and not settings.HEADLESS:
        from selenium.webdriver import FirefoxProfile

        ffp = FirefoxProfile()
        # Set the default download location [0=Desktop, 1=Downloads, 2=Specified location]
        ffp.set_preference('browser.download.folderList', 1)
        ffp.set_preference('browser.download.manager.showWhenStarting', False)
        ffp.set_preference('browser.helperApps.alwaysAsk.force', False)
        ffp.set_preference(
            'browser.helperApps.neverAsk.saveToDisk',
            'text/plain, application/octet-stream, application/binary, text/csv, application/csv, '
            'application/excel, text/comma-separated-values, text/xml, application/xml',
        )
        driver = driver_cls(firefox_profile=ffp)
    else:
        driver = driver_cls()

    driver.maximize_window()
    return driver


def find_current_browser(driver):
    current_browser = driver.desired_capabilities.get('browserName')
    return current_browser
