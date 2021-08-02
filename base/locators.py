import settings

from base import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchElementException

class WebElementWrapper:
    """A wrapper for selenium's WebElement. Supports all WebElement attributes
    but adds a few methods to deal with when a WebElement cannot be located.

    :param driver: A selenium WebDriver.
    :param str attribute_name: The attribute name of the locator in its containing class.
    :param locator: An object of the type Locator.
    """
    def __init__(self, driver, attribute_name, locator):
        self.driver = driver
        self.locator = locator
        self.name = attribute_name

    def __getattr__(self, item):
        """If WebElementWrapper does not have an attribute, WebElement attributes are used.

        `self.element` returns a WebElement, if possible, and then searches for the specified
        attribute (`item`) within the WebElement.
        """
        return getattr(self.element, item)

    @property
    def element(self):
        """Return the WebElement directly."""
        return self.locator.get_web_element(self.driver, self.name)

    def present(self):
        """Wait for an element to be visible on page.

        :return: True if element appears. False if timeout.
        """
        try:
            self.element
            return True
        except ValueError:
            return False

    def absent(self):
        """Wait for an element to not be visible on page.

        :return: True if element disappears. False if timeout.
        """
        try:
            WebDriverWait(self.driver, self.locator.timeout).until(
                EC.invisibility_of_element_located(self.locator.location)
            )
            return True
        except TimeoutException:
            return False

    def here_then_gone(self):
        """In theory, wait for an element to appear and then disappear.
        Often used to wait for loading indicators to disappear before
        continuing testing. Appearance is not mandatory as sometimes an
        element may disappear faster than selenium can check for its presence.

        :return: True if element disappears. False if timeout on waiting for disappearance.
        """
        self.present()
        if not self.absent():
            raise ValueError('Element {} is not absent.'.format(self.name))
        return True

    def click_expecting_popup(self, timeout=settings.TIMEOUT):
        """Click an element that opens a new tab/window, switch the driver's
        focus to the newly opened window, maximize it, and close all other windows.

        Use to handle popups no matter what browser you're using
        (some will open tabs some will open windows).

        :param int timeout: How many seconds to wait for the new window to appear.
        """
        og_window = self.driver.current_window_handle

        for window in self.driver.window_handles:
            if window == og_window:
                continue
            self.driver.switch_to.window(window)
            self.driver.close()

        self.driver.switch_to.window(og_window)
        self.driver.maximize_window()
        self.click()

        try:
            WebDriverWait(self.driver, timeout).until(
                EC.number_of_windows_to_be(2))
        except TimeoutException:
            raise ValueError('No new window was opened.')
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.maximize_window()

    def send_keys(self, keys):
        self.element.send_keys(keys)

    def send_keys_deliberately(self, keys):
        """Send keys one at a time to ensure accuracy"""
        for k in keys:
            self.element.send_keys(k)

class BaseLocator:
    """Abstract base class from which all Locator classes inherit.

    Includes the method of how to locate the element (a subclass of selenium By),
    a string that actually identifies the element, and a timeout for how long to wait
    when searching for the element.
    """
    def __init__(self, selector, path, timeout=settings.TIMEOUT):
        self.selector = selector
        self.path = path
        self.location = (selector, path)
        self.timeout = timeout

    def get_element(self, driver, attribute_name):
        """Must be implemented by every Locator subclass. Defines how a locator is used within
         a page (or element). Ultimately is a locator's return value when used in the PageObject model.
         """
        raise NotImplementedError


class Locator(BaseLocator):
    """How to locate a WebElement within a PageObject.

    :param selector: An instance of selenium By. Often `By.CSS_SELECTOR`.
    :param str path: String that uniquely identifies the element, dependant on selector.
    :param int timeout: How many seconds to wait when using a `WebDriverWait` in Locator methods
    most notably `get_web_element`. You may end up waiting longer than your timeout because some
    methods use more than one Wait.
    """
    def get_web_element(self, driver, attribute_name):
        """
        Check if element is on page and visible before returning the selenium
        WebElement. If element is not found or visible raises `ValueError`.

        h/t to seleniumframework.com for the original structure of this method.

        :param driver: A selenium WebDriver.
        :param str attribute_name: The attribute name of the locator in its containing class.
        :return: The WebElement represented by the locator.
        """
        try:
            WebDriverWait(driver, self.timeout).until(
                EC.presence_of_element_located(self.location)
            )
        except(TimeoutException, StaleElementReferenceException):
            raise ValueError('Element {} not present on page. {}'.format(
                attribute_name, driver.current_url)) from None

        try:
            WebDriverWait(driver, self.timeout).until(
                EC.visibility_of_element_located(self.location)
            )
        except(TimeoutException, StaleElementReferenceException):
            raise ValueError('Element {} not visible before timeout. {}'.format(
                attribute_name, driver.current_url)) from None

        try:
            WebDriverWait(driver, self.timeout).until(
                EC.element_to_be_clickable(self.location)
            )
        except(TimeoutException, StaleElementReferenceException):
            raise ValueError('Element {} not clickable before timeout. {}'.format(
                attribute_name, driver.current_url)) from None

        if 'href' in attribute_name:
            try:
                WebDriverWait(driver, self.timeout).until(
                    ec.link_has_href(self.location)
                )
            except(TimeoutException, StaleElementReferenceException):
                raise ValueError('Element {} on page but does not have a href. {}'.format(
                    attribute_name, driver.current_url)) from None
        try:
            return driver.find_element(self.selector, self.path)
        except NoSuchElementException:
            raise ValueError('Element {} was present, but now is gone. {}'.format(
                attribute_name, driver.current_url)) from None

    def get_element(self, driver, attribute_name):
        return WebElementWrapper(driver, attribute_name, self)


class GroupLocator(BaseLocator):
    """How to locate a group of WebElements within a PageObject.

    :param selector: An instance of selenium By.
    :param str path: Identifying string that is shared between the elements
    you are attempting to locate.
    """
    def get_web_elements(self, driver):
        return driver.find_elements(self.selector, self.path)

    def get_element(self, driver, attribute_name=None):
        """Return a list of WebElements. Return empty list if none fitting locator criteria are found."""
        return self.get_web_elements(driver)


class ComponentLocator(Locator):
    """How to locate a Component within a PageObject. Currently, component locators
    are just for namespacing large/discrete sections of PageObjects. In the future,
    theoretically may specifically locate a component WebElement and search for elements
    within that component.

    TODO: Actually use these like a locator, or rename and restructure

    :param component_class: A subclass of BaseElment.
    Note: Currently the parameters selector, path, and timeout don't do anything.
    """
    def __init__(self, component_class, selector=None, path=None, timeout=settings.TIMEOUT):
        super().__init__(selector, path, timeout)
        self.component_class = component_class

    def get_element(self, driver, attribute_name=None):
        return self.component_class(driver)


class BaseElement:
    """Abstract base class from which all Element and eventually Page classes inherit.
    Handles waffled pages, storage of the WebDriver, and returning WebElements when Locators are
    accessed.
    """
    default_timeout = settings.TIMEOUT

    def __new__(cls, *args, **kwargs):
        """Check if an element or page has a waffle version. If waffle is on,
        use the class for the newer waffled version (will have different locators)
        instead of the class initially requested.

        Requires a `waffle_override` dictionary in the BaseElement subclass in the format
        `waffle_override = {<waffle flag>: <BaseElement subclass to use if waffle is on>}`

        :return: Instance of the class in the waffle_override dictionary if waffle flag is true,
        otherwise, instance of the original class on which _new_ was called.
        """
        page = super().__new__(cls)
        if hasattr(cls, 'waffle_override'):
            for waffle_name in cls.waffle_override:
                if waffle_name in settings.EMBER_PAGES:
                    page = super().__new__(cls.waffle_override[waffle_name])
        page.__init__(*args, **kwargs)
        return page

    def __init__(self, driver):
        self.driver = driver

    def verify(self):
        raise NotImplementedError

    def __getattribute__(self, attribute_name):
        """Return the normal expected value from __getattribute__ unless the attribute is a Locator.
        In that case, use the Locator to grab the element it represents from the WebDriver.
        """
        value = object.__getattribute__(self, attribute_name)
        if isinstance(value, BaseLocator):
            return value.get_element(self.driver, attribute_name)
        return value
