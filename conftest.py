# -*- coding: utf-8 -*-
__author__ = 'M.Novikov'

#import importlib
#import jsonpickle                                                           # Работа с файлами формата JSON
import json                                                                 # Работа с файлами формата JSON
import pytest
import os.path                                                              # Работа с файлами и путями к ним
from fixture.application import Application
#from fixture.db import DbFixture                                            # Настройки работы с базой данных
#from fixture.orm import ORMFixture                                          # Работа с базой данных через ORM-подсистему

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


@pytest.fixture
def app(request):
    global fixture
    browser = request.config.getoption("--browser")
    web_config = load_config(request.config.getoption("--target"))["web"]   # Получение данных конфигурации выполнения из файла для работы с Web
    user_config = load_config(request.config.getoption("--target"))["webadmnin"]   # Получение данных конфигурации выполнения из файла для работы с Web
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, base_url=web_config['baseUrl'])
    fixture.session.ensure_login(username=user_config['username'], password=user_config['password'])    # Авторизация пользователя
    return fixture


# Фикстура для работы с базой данных
#@pytest.fixture(scope="session")                                            # Метка использования pytest
#def db(request):
#    db_config = load_config(request.config.getoption("--target"))['db']     # Получение данных конфигурации выполнения из файла для работы с базой данных
#    dbfixture = DbFixture(host=db_config['host'], name=db_config['name'], user=db_config['user'], password=db_config['password'])   # Создание фикстуры работы с базой данных
#    def fin():
#        dbfixture.destroy()                                                 # Уничтожение фикстуры работы с базой данных
#    request.addfinalizer(fin)                                               # Действия при завершении работы с фикстурой
#    return dbfixture


# Фикстура для работы с ORM-подсистемой доступа к базе данных
#@pytest.fixture(scope="session")                                            # Метка использования pytest
#def orm(request):
#    orm_config = load_config(request.config.getoption("--target"))['db']    # Получение данных конфигурации выполнения из файла для работы с базой данных
#    ormfixture = ORMFixture(host=orm_config['host'], name=orm_config['name'], user=orm_config['user'], password=orm_config['password'])   # Создание фикстуры работы с базой данных
#    def fin():
#        ormfixture.destroy()                                                # Уничтожение фикстуры работы с базой данных
#    request.addfinalizer(fin)                                               # Действия при завершении работы с фикстурой
#    return ormfixture


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


# Генератор тестов
#def pytest_generate_tests(metafunc):
#    for fixture in metafunc.fixturenames:
#        if fixture.startswith("data_"):                                     # Имя фикстуры начинается с "data_"
#            testdata = load_from_module(fixture[5:])                        # Загрузка данных из модуля Python-а (файла .py) с заданным имененм
#            metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])
#        elif fixture.startswith("json_"):                                   # Имя фикстуры начинается с "json_"
#            testdata = load_from_json(fixture[5:])                          # Загрузка данных из файла с заданным имененм
#            metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])


# Загрузка данных из модуля Python-а (файла .py) с заданным имененм
#def load_from_module(module):
#    return importlib.import_module("data.%s" % module).testdata             # Получение тестовых данных из указанного модуля


# Загрузка данных из файла с заданным имененм
#def load_from_json(file):
#    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/%s.json" % file)) as f:    # Определение пути к конфигурационному файлу и его открытие
#        return jsonpickle.decode(f.read())                                  # Получение тестовых данных из указанного файла
