# -*- coding: utf-8 -*-
__author__ = 'M.Novikov'

from model.project import Project                                           # Проекты Mantis
import re                                                                   # Регулярные выражения


# Фикстура для работы с проектами Mantis
class ProjectHelper:

    # Создание объектов класса
    def __init__(self, app):
        self.app = app

    # Переход к списку проектов
    def open_project_page(self):
        wd = self.app.wd                                                    # Получение доступа к web-драйверу
        if not (wd.current_url.endswith("manage_proj_page.php") and len(wd.find_elements_by_link_text("Manage Projects")) == 0):    # При отсутсвии строки поиска
            wd.find_element_by_link_text("Manage").click()                  # Переход к странице управления
            wd.find_element_by_link_text("Manage Projects").click()         # Переход к управлению проектами

    # Проверка и изменение текстовых полей формы ввода
    def change_text_value(self, field_name, text):
        wd = self.app.wd                                                    # Получение доступа к web-драйверу
        if text is not None:                                                # Если изменяемое значение не пустое
            wd.find_element_by_name(field_name).click()                     # Выбрать поле
            wd.find_element_by_name(field_name).clear()                     # Очистить поле
            wd.find_element_by_name(field_name).send_keys(text)             # Заполнить поле новым значение параметра

    # Заполнение параметров проекта
    def fill_project_form(self, project):
        self.change_text_value("name", project.name)                        # Наименование проекта
        self.change_text_value("description", project.description)          # Описание проекта

    # Создание нового проекта
    def create(self, new_project):
        wd = self.app.wd                                                    # Получение доступа к web-драйверу
        self.open_project_page()                                            # Переход к списку проектов
        wd.find_element_by_css_selector("td.form-title > form > input.button-small").click()    # Запуск добавления нового пректа
        self.fill_project_form(new_project)                                 # Заполнение параметров проекта
        wd.find_element_by_css_selector("input.button").click()             # Подтверждение введенных данных
        self.project_cache = None                                           # Сброс сохраненного ранее списка проектов

    # Выбор проекта по порядковому номеру
    def select_by_index(self, index):
        wd = self.app.wd                                                    # Получение доступа к web-драйверу
        wd.find_elements_by_xpath("//table[3]/tbody/tr")[index+2].find_element_by_tag_name("a").click()

    # Удаление проекта по порядковому номеру
    def delete_by_index(self, index):
        wd = self.app.wd                                                    # Получение доступа к web-драйверу
        self.open_project_page()                                            # Переход к списку проектов
        self.select_by_index(index)                                         # Выбор проекта по порядковому номеру
        wd.find_element_by_css_selector("form > input.button").click()      # Удаление проекта
        wd.find_element_by_css_selector("input.button").click()             # Подтверждение удаления
        self.project_cache = None                                           # Сброс сохраненного ранее списка проектов

    project_cache = None                                                    # Список проектов

    # Получение списка проектов
    def get_project_list(self):
        if self.project_cache is None:                                      # При отсутствии списка групп
            wd = self.app.wd                                                # Получение доступа к web-драйверу
            self.open_project_page()                                        # Переход к списку проектов
            self.project_cache = []                                         # Изначально список проектов пустой
            tbody = wd.find_elements_by_xpath("//table[3]/tbody/tr")        # Таблица проектов
            for row in tbody[2:]:                                           # Перебор всех элементов списка на странице
                cells = row.find_elements_by_tag_name("td")                 # Получение списка ячеек строки таблицы проектов
                href = cells[0].find_element_by_tag_name("a").get_attribute("href")
                id = re.search("\d+$", href).group(0)                       # Идентификатор проекта
                name = cells[0].find_element_by_tag_name("a").text          # Получение названия проекта
                description = cells[4].text                                 # Получение описания проекта
                self.project_cache.append(Project(id=id, name=name, description=description))  # Добавление в список проектов
        return list(self.project_cache)                                     # Список проектов

    # Проверка наличия проекта в списке
    def is_project_on_list(self, project):
        return project in self.get_project_list()

    def count(self):
        wd = self.app.wd                                                    # Получение доступа к web-драйверу
        self.open_project_page()                                            # Переход к списку проектов
        return len(wd.find_elements_by_xpath("//table[3]/tbody/tr")) - 2    # Колическво возможных к выбору элементов списка
