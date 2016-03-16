from .base import FunctionalTest
from selenium import webdriver

from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get(self.server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.get_element_input_box()
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item',
        )

        # She types "Buy tomates" into a text box (Edith's hobby
        # is tying fly-fishing lures)
        inputbox.send_keys('Buy tomatoes')


        # When she hits enter, the page updates, she is taken to a new URL,
        # and now the page lists "1: Buy peacock feathers" 
        # as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        eidth_list_url = self.browser.current_url
        self.assertRegex(eidth_list_url, '/lists/.+')
        self.check_for_rows_in_list_table('#1: Buy tomatoes')

        # There is still a text box inviting her to add another item. She
        # enters "Use tomatoes for whatever" (Edith is very methodical)
        inputbox = self.get_element_input_box()
        inputbox.send_keys('Use tomatoes for whatever')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        self.check_for_rows_in_list_table('#1: Buy tomatoes',
                                          '#2: Use tomatoes for whatever')

        # Now a new user, Dave, opens the site

        ## we have new browser session here to make sure there is no
        ## info of previous user

        self.restart_browser()

        # Dave visits the gome page. No sign of previous user
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy tomatoes', page_text)
        self.assertNotIn('Use tomatoes for whatever', page_text)

        # Dave starts a new list by entering a new item
        inputbox = self.get_element_input_box()
        inputbox.send_keys('Go to gym')
        inputbox.send_keys(Keys.ENTER)

        # Dave gets his own unique url
        dave_list_url = self.browser.current_url
        self.assertRegex(dave_list_url, '/lists/.+')
        self.assertNotEqual(eidth_list_url, dave_list_url)

        # Again, there is no sign of previous user
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy tomatoes', page_text)
        self.assertNotIn('Use tomatoes for whatever', page_text)
        self.assertIn('Go to gym', page_text)

        # Satisfied, users quit

        self.browser.quit()
