import sys
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from unittest import skip

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 


class FunctionalTest(StaticLiveServerTestCase):
    browser_class = webdriver.Opera

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        self.browser = self.browser_class()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        # self.browser.refresh()
        self.browser.quit()

    def restart_browser(self):
        # self.browser.refresh()
        self.browser.quit()
        self.browser = self.browser_class()

    def check_for_rows_in_list_table(self, *needles):
        table = WebDriverWait(self.browser, 4)\
            .until(EC.element_to_be_clickable((By.ID, 'id_list_table')))

        table_rows = table.find_elements_by_tag_name('tr')
        row_texts = {row.text for row in table_rows}
        needles = set(needles)
        self.assertEquals(row_texts & needles, needles)

    def get_element_input_box_locator(self):
        return By.ID, 'id_text'

    def get_element_input_box(self):
        locator = self.get_element_input_box_locator()
        return self.browser.find_element(*locator)

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

    def wait_to_be_logged_out(self, email):
        self.wait_for_page_ready()
        self.wait_for_element_with_id('id_login')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)

    def wait_to_be_logged_in(self, email):
        self.wait_for_page_ready()
        self.wait_for_element_with_id('id_logout')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)
