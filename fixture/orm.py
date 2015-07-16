# -*- coding: utf-8 -*-
__author__ = 'M.Novikov'

from model.project import Project                                           # Проекты Mantis
from pony.orm import *                                                      # Работа с базой данных
from pymysql.converters import decoders                                     # Преобразование данных


class ORMFixture:

    db = Database()

    # Структура объектов, привязываемых к базе данных
    class ORMProject(db.Entity):                                            # Проект Mantis
        _table_ = "mantis_project_table"                                    # Наименование связываемой таблицы базы данных
        id = PrimaryKey(int, column="id")                                   # Идентификатор
        name = Optional(str, column="name")                                 # Название
        description = Optional(str, column="description")                   # Описание

    # Создание фикстуры работы с базой данных
    def __init__(self, host, name, user, password):
        self.db.bind("mysql", host=host, database=name, user=user, password=password, conv=decoders)    # Подключение к базе данных с разрешением преобразования данных в извесные форматы
        self.db.generate_mapping()                                          # Сопоставление объектов класса и таблиц базы данных
        #sql_debug(True)                                                     # Вывод формируемых sql-запросов в консоль

    # Уничтожение фикстуры работы с базой данных
    def destroy(self):
        pass

    # Преобразование объектов ORMGroup (текущий формат) к формату объектов model (общий формат)
    def convert_project_to_model(self, projects):
        def convert(project):                                              # Преобразование одного ORM-объекта проекта Mantis в формат модели проекта Mantis
            return Project(id=project.id, name=project.name, description=project.description)
        return list(map(convert, projects))                                # Преобразованный список проектов

    # Получение списка проектов
    @db_session                                                             # Метка выполнения функции в рамках единой сессии
    def get_project_list(self):
        return self.convert_project_to_model(select(p for p in ORMFixture.ORMProject))  # Получение (запрос к базе) списка проектов
