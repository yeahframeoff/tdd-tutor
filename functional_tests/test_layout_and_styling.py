from .base import FunctionalTest
from selenium import webdriver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 


class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        # User goes to the home page
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        # User notices the input box is nicely centered
        inputbox = self.get_element_input_box()
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
        inputbox.send_keys('testing\n')
        inputbox = WebDriverWait(self.browser, 4)\
            .until(EC.element_to_be_clickable(self.get_element_input_box_locator()))
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
