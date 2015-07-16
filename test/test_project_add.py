# -*- coding: utf-8 -*-
__author__ = 'M.Novikov'

from model.project import Project                                           # Проекты Mantis
import random                                                               # Случайности
import string                                                               # Строки


# Тест добавления проекта, проверка через пользователький интерфейс
def test_project_add_ui(app):
    project = Project(name=random_string("Project_", 20),description=random_text("Description: ", 100))  # Новый проект
    old_projects = app.project.get_project_list()                           # Список проектов до добавления
    if not project in old_projects:                                         # Проверка наличия проекта в списке
        app.project.create(project)                                         # Добавление проекта
        old_projects.append(project)                                        # Добавление нового проекта в список
    new_projects = app.project.get_project_list()                           # Список проектов после добавления
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)


# Тест добавления проекта, проверка с использование базы данных
def test_project_add_db(app, orm):
    project = Project(name=random_string("Project_", 20),description=random_text("Description: ", 100))  # Новый проект
    old_projects = orm.get_project_list()                                   # Список проектов до добавления
    if not project in old_projects:                                         # Проверка наличия проекта в списке
        app.project.create(project)                                         # Добавление проекта
        old_projects.append(project)                                        # Добавление нового проекта в список
    new_projects = orm.get_project_list()                                   # Список проектов после добавления
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)


# Тест добавления проекта через протокол SOAP
def test_project_add_soap(app):
    project = Project(name=random_string("Project_", 20),description=random_text("Description: ", 100))  # Новый проект
    old_projects = app.soap.get_project_list()                              # Список проектов до добавления
    if not project in old_projects:                                         # Проверка наличия проекта в списке
        app.project.create(project)                                         # Добавление проекта
        old_projects.append(project)                                        # Добавление нового проекта в список
    new_projects = app.soap.get_project_list()                              # Список проектов после добавления
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)


# Получение случайной строки
def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits + " "*10                 # Используемы символы
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])  # Строка


# Получение случайной строки со знаками пунктуации
def random_string_punctuation(prefix, maxlen):
    symbols = string.ascii_letters + string.digits + string.punctuation + " "*10    # Используемы символы
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])  # Строка


# Получение случайного текста
def random_text(prefix, maxlen):
    symbols = string.ascii_letters + string.digits + " "*10 + "\n"*3        # Используемы символы
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])  # Текст


# Получение случайного текста со знаками пунктуации и дополнительными печатными символами
def random_text_printable(prefix, maxlen):
    symbols = string.printable + " "*10 + "\n"*3                            # Используемы символы
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])  # Текст
