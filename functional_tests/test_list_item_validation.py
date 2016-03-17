from .base import FunctionalTest
from selenium import webdriver
from unittest import skip

from selenium.webdriver.common.keys import Keys


class ItemValidationTest(FunctionalTest):

    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')

    def test_cannot_add_empty_list_items(self):
        # User foes to the home page and tries to submit
        # an empty item. Hits enter on the empty input box
        self.browser.get(self.server_url)
        self.get_element_input_box().send_keys(Keys.ENTER)

        # The home page refreshes, and there is an error message saying
        # that list items cannot be blank
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        # The user tries again with some text for the item, and that works
        self.get_element_input_box().send_keys('Buy milk' + Keys.ENTER)
        self.check_for_rows_in_list_table('#1: Buy milk')

        # Now, he decides to submit a blank item again
        self.get_element_input_box().send_keys(Keys.ENTER)
        # She receives a similar warning on the list page
        self.check_for_rows_in_list_table('#1: Buy milk')
        error = self.get_error_element()
        self.assertEqual(error.text, "You can't have an empty list item")

        # And he fixes it by inputting some text in
        # self.fail("Write the test!")
        self.get_element_input_box().send_keys('Make tea' + Keys.ENTER)
        self.check_for_rows_in_list_table('#1: Buy milk', '#2: Make tea')

    def test_cannot_add_duplicate_items(self):
        # User goes to the same home page and starts a new list
        self.browser.get(self.server_url)
        self.get_element_input_box().send_keys('Cook waffles' + Keys.ENTER)
        self.check_for_rows_in_list_table('#1: Cook waffles')

        # ACCIDENTALLY LOL, accidentally user tries to enter a duplicate item
        self.get_element_input_box().send_keys('Cook waffles' + Keys.ENTER)

        # Sees a helpful error message 
        self.check_for_rows_in_list_table('#1: Cook waffles')
        error = self.get_error_element()
        self.assertEqual(error.text, "You've already got this in your list")

    def test_error_messaages_are_cleared_on_input(self):
        # User starts a new list in a way that causes a validation error
        self.browser.get(self.server_url)
        self.get_element_input_box().send_keys(Keys.ENTER)
        error = self.get_error_element()
        self.assertTrue(error.is_displayed())

        # user starts typing in the input box to clear the error
        self.get_element_input_box().send_keys('a')

        # users is pleased to see that error message dissapears
        error = self.get_error_element()
        self.assertFalse(error.is_displayed())
