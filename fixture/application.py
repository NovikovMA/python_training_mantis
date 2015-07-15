# -*- coding: utf-8 -*-
__author__ = 'M.Novikov'

#from fixture.address import AddressHelper
#from fixture.group import GroupHelper
from fixture.session import SessionHelper
from selenium import webdriver


class Application:

    def __init__(self, browser, base_url):
        if browser == "firefox":
            self.wd = webdriver.Firefox()
        elif browser == "chrome":
            self.wd = webdriver.Chrome()
        elif browser == "ie":
            self.wd = webdriver.Ie()
        else:
            raise ValueError("Unrecognized browser %s" % browser)
        self.session = SessionHelper(self)
        #self.address = AddressHelper(self)
        #self.group = GroupHelper(self)
        self.base_url = base_url

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False

    # Открыть программу в окне браузера
    def open_home_page(self):
        wd = self.wd
        wd.get(self.base_url)

    def destroy(self):
        self.wd.quit()
