import time

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait



from .base import FunctionalTest

TEST_EMAIL = 'yeahframeoff@mockmyid.com'


class LoginTest(FunctionalTest):

    def switch_to_new_window(self, text_in_title):
        retries = 60
        while retries > 0:
            for handle in self.browser.window_handles:
                self.browser.switch_to.window(handle)
                if text_in_title in self.browser.title:
                    return
            retries -= 1
            time.sleep(0.5)
        self.fail('could not find the window with title "%s"' % text_in_title)

    def wait_for_element_with_id(self, element_id):
        return WebDriverWait(self.browser, timeout=30).until(
            lambda browser: browser.find_element_by_id(element_id),
            'Could not find element with id %s. Page text was:\n%s' %
            (element_id, self.browser.find_element_by_tag_name('body').text)
        )

    def wait_for_page_ready(self, attempts=2):
        attempts -= 1
        for current_attempt in range(attempts + 1):
            try:
                return WebDriverWait(self.browser, timeout=30).until(
                    lambda browser: browser.find_element_by_tag_name('body')
                )
            except StaleElementReferenceException:
                if current_attempt == attempts:
                    raise

    def wait_to_be_logged_out(self):
        self.wait_for_page_ready()
        self.wait_for_element_with_id('id_login')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(TEST_EMAIL, navbar.text)

    def wait_to_be_logged_in(self):
        self.wait_for_page_ready()
        self.wait_for_element_with_id('id_logout')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(TEST_EMAIL, navbar.text)

    def test_login_with_persona(self):
        # User goes to the site, sees the "Sign in"
        # hyperlink for the first time
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_login').click()

        # Persona login box appears
        self.switch_to_new_window("Mozilla Persona")

        # User logs in with his email address
        ## use mockmyid.com for test email
        self.browser.find_element_by_id('authentication_email')\
            .send_keys(TEST_EMAIL)

        self.browser.find_element_by_tag_name('button').click()

        # The Persona window closes
        self.switch_to_new_window('To-Do')

        # User can see that she is logged in
        self.wait_to_be_logged_in()

        # After refreshing the page, user sees that he is still logged in
        self.browser.refresh()
        self.wait_to_be_logged_in()

        # After that user logs out
        self.browser.find_element_by_id('id_logout').click()
        self.wait_to_be_logged_out()

        # # Refreshing the page user reassures that he's really logged out
        self.browser.refresh()
        self.wait_to_be_logged_out()

