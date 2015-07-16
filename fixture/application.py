# -*- coding: utf-8 -*-
__author__ = 'M.Novikov'

from fixture.project import ProjectHelper                                           # Управление проектами Mantis
from fixture.session import SessionHelper
from fixture.soap import SoapHelper                                                 # Работа по протоколу SOAP
from selenium import webdriver


class Application:

    def __init__(self, browser, config):
        if browser == "firefox":
            self.wd = webdriver.Firefox()
        elif browser == "chrome":
            self.wd = webdriver.Chrome()
        elif browser == "ie":
            self.wd = webdriver.Ie()
        else:
            raise ValueError("Unrecognized browser %s" % browser)
        self.project = ProjectHelper(self)
        self.session = SessionHelper(self)
        self.soap = SoapHelper(self)
        self.config = config
        self.base_url = config["web"]['baseUrl']

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
