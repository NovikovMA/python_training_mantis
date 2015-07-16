# -*- coding: utf-8 -*-
__author__ = 'M.Novikov'


class SessionHelper:

    def __init__(self, app):
        self.app = app

    # Авторизация пользователя
    def login(self, username, password):
        wd = self.app.wd                                                    # Получение доступа к web-драйверу
        self.app.open_home_page()                                           # Открыть программу в окне браузера
        wd.find_element_by_name("username").click()                         # Выбор поля ввода логина
        wd.find_element_by_name("username").clear()                         # Очистка поля ввода логина
        wd.find_element_by_name("username").send_keys(username)             # Ввод логина
        wd.find_element_by_name("password").click()                         # Выбор поля ввода пароля
        wd.find_element_by_name("password").clear()                         # Очистка поля ввода пароля
        wd.find_element_by_name("password").send_keys(password)             # Ввод пароля
        wd.find_element_by_css_selector('input[type="submit"]').click()     # Подтверждение авторизации

    # Выход из программы
    def logout(self):
        wd = self.app.wd                                                    # Получение доступа к web-драйверу
        wd.find_element_by_link_text("Logout").click()                      # Выход из учетной записи

    def is_logged_in(self):
        wd = self.app.wd                                                    # Получение доступа к web-драйверу
        return len(wd.find_elements_by_link_text("Logout")) > 0             # Проверка наличия кнопки (ссылки) выхода

    def is_logged_in_as(self, username):
        return self.get_logged_user() == username

    def get_logged_user(self):
        wd = self.app.wd
        return wd.find_element_by_css_selector("td.login-info-left span").text

    def ensure_login(self, username, password):
        if self.is_logged_in():                                             # Если пользователь авторизован
            if self.is_logged_in_as(username):                              # Если пользователь авторизован не под своим именем
                return
            else:
                self.logout()
        self.login(username, password)                                      # Авторизация пользователя

    def ensure_logout(self):
        if self.is_logged_in():
            self.logout()
