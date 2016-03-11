import sys
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from unittest import skip

from selenium.webdriver.common.keys import Keys


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
