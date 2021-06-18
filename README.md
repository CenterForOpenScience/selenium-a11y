# Selenium A11y

This is the UI test automation for Accessibility Testing of OSF. It uses Selenium WebDriver and Pytest to create tests and the [axe-core](https://github.com/dequelabs/axe-core) test engine to evaluate accessibility rules. 


## Setting up

### Prerequisites


You'll need the webdriver of your choice and Python3.

##### Installing a webdriver:

In order for Selenium to be able to control your local browser, you will need to install [drivers](https://seleniumhq.github.io/selenium/docs/api/py/#drivers) for any browsers in which you desire to run these tests. Start with a driver such as [GekoDriver](https://github.com/mozilla/geckodriver/releases) (firefox) or [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads). (Note: IE is not supported. Safari is only partially supported -- running the tests in Safari is not recommended).

Go to any of the driver links above, install the applicable driver for your system, and move the executable into your *PATH*, e. g., place it in */usr/bin* or */usr/local/bin*.


##### Installing Python3:

For MacOSX users:

```bash
brew install python3
```

For Ubuntu users:

```bash
apt-get install python3

```

It is also suggested you use a virtual environment. After completing the installation of Python3, this can be done with the following commands:

```bash
pip install virtualenv
pip install virtualenvwrapper
mkvirtualenv --python=python3 selenium-a11y
```

### Installing


Now you can install the requirements:

```
pip install -r requirements.txt
```
And you should be good to go!

## Running tests

In order to run the whole test suite simply use pytest:

```bash
pytest

```

You can run specific test classes:

```bash
pytest tests/test_dashboard.py::TestDashboardPage

```


Or specific tests:

```bash
pytest tests/test_dashboard.py::TestDashboardPage::test_institution_logos

```

You can even run tests using custom markers. For example, here's how to run all the OSF smoke tests:

```bash
pytest -m smoke_test

```
See the [pytest documentation](https://docs.pytest.org/en/latest/index.html) for more information on usage.
