# Architecture of Selenium A11y

## important areas
- `pages/`
    - describes the app using the "page object" pattern
    - each `Page` class:
        - represents a specific page of the app
        - has a set of `Locator`s for locating controls on the page
- `components/`
    - like page objects but each describes a component, a repeated piece of functionality
- `tests/`
    - all the accessibility tests for OSF
    - interacts with the web app via the page objects from `pages/`
    - pytest markers used to divide tests into test suites
        - see `pytest.ini` for the current set of markers
- `api/`
    - reusable utilities for interacting with the OSF api
