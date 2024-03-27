from urllib.parse import urljoin

import pytest
from selenium.webdriver.common.by import By

import settings
from base.locators import ComponentLocator, GroupLocator, Locator
from components.navbars import PreprintsNavbar
from pages.base import GuidBasePage, OSFBasePage


class BasePreprintPage(OSFBasePage):
    """The base page from which all preprint pages inherit."""

    base_url = settings.OSF_HOME + "/preprints/"
    url_addition = ""
    navbar = ComponentLocator(PreprintsNavbar)

    def __init__(self, driver, verify=False, provider=None):
        self.provider = provider
        if provider:
            self.provider_id = provider["id"]
            self.provider_name = provider["attributes"]["name"]
            self.provider_domain = provider["attributes"]["domain"]

        super().__init__(driver, verify)

    @property
    def url(self):
        """Set the URL based on the provider domain."""
        if self.provider and self.provider_id != "osf":
            if self.provider["attributes"]["domain_redirect_enabled"]:
                return urljoin(self.provider_domain, self.url_addition)
            else:
                return (
                    urljoin(self.base_url, self.provider_id) + "/" + self.url_addition
                )
        return self.base_url + self.url_addition

    def verify(self):
        """Return true if you are on the expected page.
        Checks both the general page identity and the branding.
        """
        if self.provider and self.provider_id != "osf":
            return super().verify() and self.provider_name in self.navbar.title.text
        return super().verify()


class PreprintLandingPage(BasePreprintPage):
    identity = Locator(
        By.CSS_SELECTOR,
        '[data-analytics-scope="preprints landing page"]',
        settings.LONG_TIMEOUT,
    )


class PreprintSubmitPage(BasePreprintPage):
    url_addition = "submit"

    identity = Locator(By.CLASS_NAME, "preprint-submit-header")


class PreprintEditPage(GuidBasePage, BasePreprintPage):
    url_base = urljoin(settings.OSF_HOME, "{guid}")
    url_addition = "/edit"

    identity = Locator(
        By.CSS_SELECTOR, ".m-t-md.preprint-header-preview > p:nth-child(1) > em.m-r-md"
    )
    basics_section = Locator(By.ID, "preprint-form-basics")


class PreprintWithdrawPage(GuidBasePage, BasePreprintPage):
    url_base = urljoin(settings.OSF_HOME, "{guid}")
    url_addition = "/withdraw"

    identity = Locator(
        By.CSS_SELECTOR,
        "section.preprint-form-block.preprint-form-section-withdraw-comment",
    )


@pytest.mark.usefixtures("must_be_logged_in")
class PreprintDiscoverPage(BasePreprintPage):
    base_url = settings.OSF_HOME + "/search?resourceType=Preprint"

    identity = Locator(
        By.CSS_SELECTOR, 'a[data-test-topbar-object-type-link="Preprints"]'
    )
    loading_indicator = Locator(By.CSS_SELECTOR, ".ball-scale")


@pytest.mark.usefixtures("must_be_logged_in")
class BrandedPreprintsDiscoverPage(BasePreprintPage):
    url_addition = "discover"

    identity = Locator(By.CSS_SELECTOR, "[data-test-search-provider-logo]")
    loading_indicator = Locator(By.CSS_SELECTOR, ".ball-scale")


class PreprintDetailPage(GuidBasePage, BasePreprintPage):
    url_base = urljoin(settings.OSF_HOME, "{guid}")
    identity = Locator(
        By.CSS_SELECTOR,
        "[data-test-preprint-header]",
        settings.LONG_TIMEOUT,
    )

    title = Locator(
        By.CSS_SELECTOR, "h1[data-test-preprint-title]", settings.LONG_TIMEOUT
    )
    view_page = Locator(By.ID, "view-page")


class PendingPreprintDetailPage(PreprintDetailPage):
    # This class is for preprints that are pending moderation
    identity = Locator(
        By.ID,
        "preprintTitle",
        settings.LONG_TIMEOUT,
    )

    # This locator needs a data-test-selector from software devs
    title = Locator(By.ID, "preprintTitle", settings.LONG_TIMEOUT)


class ReviewsDashboardPage(OSFBasePage):
    url = settings.OSF_HOME + "/reviews"
    identity = Locator(By.CLASS_NAME, "_reviews-dashboard-header_jdu5ey")
    loading_indicator = Locator(By.CSS_SELECTOR, ".ball-scale")


class BaseReviewsPage(OSFBasePage):
    """The base page from which all preprint provider review pages inherit."""

    base_url = settings.OSF_HOME + "/reviews/preprints/"
    url_addition = ""
    navbar = ComponentLocator(PreprintsNavbar)
    title = Locator(By.CLASS_NAME, "_provider-title_hcnzoe")

    def __init__(self, driver, verify=False, provider=None):
        self.provider = provider
        if provider:
            self.provider_id = provider["id"]
            self.provider_name = provider["attributes"]["name"]

        super().__init__(driver, verify)

    @property
    def url(self):
        """Set the URL based on the provider domain."""
        return urljoin(self.base_url, self.provider_id) + "/" + self.url_addition

    def verify(self):
        """Return true if you are on the expected page.
        Checks both the general page identity and the branding.
        """
        if self.provider:
            return super().verify() and self.provider_name in self.title.text
        return super().verify()


class ReviewsSubmissionsPage(BaseReviewsPage):
    identity = Locator(By.CLASS_NAME, "_reviews-list-heading_k45x8p")
    no_submissions = Locator(
        By.CSS_SELECTOR,
        "div._reviews-list-body_k45x8p > div.text-center.p-v-md._moderation-list-row_xkm0pa",
    )
    loading_indicator = Locator(By.CSS_SELECTOR, ".ball-scale")
    withdrawal_requests_tab = Locator(
        By.CSS_SELECTOR,
        "div._flex-container_hcnzoe > div:nth-child(3) > ul > li:nth-child(2) > a",
    )
    submissions = GroupLocator(By.CSS_SELECTOR, "div._moderation-list-row_xkm0pa")

    def click_submission_row(self, provider_id, preprint_id):
        """Search through the rows of submitted preprints on the Reviews Submissions
        page to find the preprint that has the given preprint_id in its url. When the
        row is found click it to open the Preprint Detail page for that preprint.
        """
        for row in self.submissions:
            url = row.find_element_by_css_selector("a").get_attribute("href")
            node_id = url.split(provider_id + "/", 1)[1]
            if node_id == preprint_id:
                row.click()
                break


class ReviewsWithdrawalsPage(BaseReviewsPage):
    url_addition = "withdrawals"
    identity = Locator(By.CLASS_NAME, "_reviews-list-heading_k45x8p")
    loading_indicator = Locator(By.CSS_SELECTOR, ".ball-scale")


class ReviewsModeratorsPage(BaseReviewsPage):
    url_addition = "/moderators"
    identity = Locator(By.CLASS_NAME, "moderator-list-row")
    loading_indicator = Locator(By.CSS_SELECTOR, ".ball-scale")


class ReviewsNotificationsPage(BaseReviewsPage):
    url_addition = "notifications"
    identity = Locator(By.CLASS_NAME, "_notification-list-heading-container_kchmy0")
    loading_indicator = Locator(By.CSS_SELECTOR, ".ball-scale")


class ReviewsSettingsPage(BaseReviewsPage):
    url_addition = "settings"
    identity = Locator(By.CLASS_NAME, "_reviews-settings_1r3x0j")
    loading_indicator = Locator(By.CSS_SELECTOR, ".ball-scale")


class PreprintPageNotFoundPage(OSFBasePage):
    identity = Locator(By.CSS_SELECTOR, '[data-analytics-scope="404"]')
    page_header = Locator(
        By.CSS_SELECTOR,
        '[data-analytics-scope="404"] > h2',
    )
