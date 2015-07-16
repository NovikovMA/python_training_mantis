# -*- coding: utf-8 -*-
__author__ = 'M.Novikov'

import json                                                                 # Работа с файлами формата JSON
import pytest                                                               # Настройка и исполнение тестов
import os.path                                                              # Работа с файлами и путями к ним
from fixture.application import Application
from fixture.orm import ORMFixture                                          # Работа с базой данных через ORM-подсистему

fixture = None
target = None                                                               # Конфигурация запуска тестов


# Получение данных конфигурации выполнения из файла
def load_config(file):
    global target                                                           # Использование общей переменной
    if target is None:                                                      # Если конфигурация не определена
        config_file = file                                                  # Определение пути к конфигурационному файлу
        if not os.path.isfile(config_file):                                 # Если задан не путь к файлу, а, например, только его имя
            config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)    # Определение пути к конфигурационному файлу по умолчанию
        with open(config_file) as f:                                        # Открыть файл, контроль автоматического закрытия после выполнения блока команд
            try:
                target = json.load(f)                                       # Загрузка данных из файла
            except ValueError as ex:                                        # В случае ошибки
                print(ex)                                                   # Вывод информации об ошибке
                target = None                                               # Сбросить данные конфигурации
    return target


# Фикстура для получения конфигурационной информации
@pytest.fixture(scope="session")
def config(request):
    return load_config(request.config.getoption("--target"))                # Содержимое конфигурации в виде словаря


# Фикстура для работы с тестируемым приложение
@pytest.fixture
def app(request, config):
    global fixture
    browser = request.config.getoption("--browser")
    user_config = config["webadmnin"]                                       # Получение данных конфигурации выполнения из файла для работы с Web
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, base_url=config["web"]['baseUrl'])
    fixture.session.ensure_login(username=user_config['username'], password=user_config['password'])    # Авторизация пользователя
    return fixture


# Фикстура для работы с ORM-подсистемой доступа к базе данных
@pytest.fixture(scope="session")                                            # Метка использования pytest
def orm(request, config):
    orm_config = config['db']                                               # Получение данных конфигурации выполнения из файла для работы с базой данных
    ormfixture = ORMFixture(host=orm_config['host'], name=orm_config['name'], user=orm_config['user'], password=orm_config['password'])   # Создание фикстуры работы с базой данных
    def fin():
        ormfixture.destroy()                                                # Уничтожение фикстуры работы с базой данных
    request.addfinalizer(fin)                                               # Действия при завершении работы с фикстурой
    return ormfixture


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.session.ensure_logout()
        fixture.destroy()
    request.addfinalizer(fin)
    return fixture


# Добавление использования параметров из командной строки
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")        # Используемый браузер
    parser.addoption("--target", action="store", default="target.json")     # Конфигурационный файл тестов
