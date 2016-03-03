from selenium import webdriver
from django.test import LiveServerTestCase

from selenium.webdriver.common.keys import Keys


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Opera()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_rows_in_list_table(self, *needles):
        table = self.browser.find_element_by_id('id_list_table')
        table_rows = table.find_elements_by_tag_name('tr')
        row_texts = [row.text for row in table_rows]
        for needle in needles:
            self.assertIn(needle, row_texts)


    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item',
        )

        # She types "Buy tomates" into a text box (Edith's hobby
        # is tying fly-fishing lures)
        inputbox.send_keys('Buy tomatoes')


        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)

        self.check_for_rows_in_list_table('#1: Buy tomatoes')

        # There is still a text box inviting her to add another item. She
        # enters "Use tomatoes for whatever" (Edith is very methodical)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use tomatoes for whatever')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        self.check_for_rows_in_list_table('#1: Buy tomatoes',
                                          '#2: Use tomatoes for whatever')

        # Edith wonders whether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.

        self.fail('Finish the test!')
        # She visits that URL - her to-do list is still there.

        # Satisfied, she goes back to sleep

        self.browser.quit()
