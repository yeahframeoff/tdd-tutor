from .base import FunctionalTest
from selenium import webdriver
from unittest import skip

from selenium.webdriver.common.keys import Keys


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # User foes to the home page and tries to submit
        # an empty item. Hits enter on the empty input box
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        # The home page refreshes, and there is an error message saying
        # that list items cannot be blank
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        # The user tries again with some text for the item, and that works
        self.browser.find_element_by_id('id_new_item').send_keys('Buy milk' + Keys.ENTER)
        self.check_for_rows_in_list_table('#1: Buy milk')

        # Now, he decides to submit a blank item again
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        # She receives a similar warning on the list page
        self.check_for_rows_in_list_table('#1: Buy milk')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        # And he fixes it by inputting some text in
        self.fail("Write the test!")
        self.browser.find_element_by_id('id_new_item').send_keys('Make tea' + Keys.ENTER)
        self.check_for_rows_in_list_table('#1: Buy milk', '#2: Make tea')
