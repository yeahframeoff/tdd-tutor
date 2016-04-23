import time


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
        self.wait_to_be_logged_in(email=TEST_EMAIL)

        # After refreshing the page, user sees that he is still logged in
        self.browser.refresh()
        self.wait_to_be_logged_in(email=TEST_EMAIL)

        # After that user logs out
        self.browser.find_element_by_id('id_logout').click()
        self.wait_to_be_logged_out(email=TEST_EMAIL)

        # # Refreshing the page user reassures that he's really logged out
        self.browser.refresh()
        self.wait_to_be_logged_out(email=TEST_EMAIL)

