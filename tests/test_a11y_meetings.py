from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import markers
from components.accessibility import ApplyA11yRules as a11y
from pages.meetings import MeetingDetailPage, MeetingsPage


@markers.ember_page
class TestMeetingsLandingPage:
    def test_accessibility(self, driver, session, write_files, exclude_best_practice):
        meetings_page = MeetingsPage(driver)
        meetings_page.goto()
        assert MeetingsPage(driver, verify=True)
        # Click the Register and Upload butttons to reveal the hidden text boxes before
        #     calling axe.
        conference_text = driver.find_element_by_css_selector(
            '[data-test-meetings-list-min-5]'
        )
        meetings_page.scroll_into_view(conference_text)
        meetings_page.register_button.click()
        meetings_page.upload_button.click()
        a11y.run_axe(
            driver,
            session,
            'meetings',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )


@markers.ember_page
class TestMeetingDetailPage:
    def test_accessibility(self, driver, session, write_files, exclude_best_practice):
        """To test the Meeting Detail Page, start at the Meetings Landing Page and then
        scroll down to the meetings list table and click the title link for the first
        meeting in the table to open the detail page for that meeting.
        """
        meetings_page = MeetingsPage(driver)
        meetings_page.goto()
        assert MeetingsPage(driver, verify=True)
        search_bar = driver.find_element_by_css_selector(
            'div[data-test-meetings-list-search]'
        )
        driver.execute_script('arguments[0].scrollIntoView();', search_bar)
        meetings_page.top_meeting_link.click()
        assert MeetingDetailPage(driver, verify=True)
        # wait for project table to be loaded before calling axe
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '[data-test-submissions-list-item-title]')
            )
        )
        a11y.run_axe(
            driver,
            session,
            'mtngdet',
            write_files=write_files,
            exclude_best_practice=exclude_best_practice,
        )
