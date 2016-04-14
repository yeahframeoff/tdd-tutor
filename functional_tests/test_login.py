import time

from selenium.webdriver.support.wait import WebDriverWait

from .base import FunctionalTest


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
        return WebDriverWait(self.browser, timeout=10).until(
            lambda browser: browser.find_element_by_id(element_id)
        )

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
            .send_keys('yeahframeoff@mockmyid.com')

        self.browser.find_element_by_tag_name('button').click()

        # The Persona window closes
        self.switch_to_new_window('To-Do')

        # User can see that she is logged in
        self.wait_for_element_with_id('id_logout')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn('yeahframeoff@mockmyid.com', navbar.text)
