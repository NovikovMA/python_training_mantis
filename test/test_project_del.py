# -*- coding: utf-8 -*-
__author__ = 'M.Novikov'

from model.project import Project                                           # Проекты Mantis
from random import randrange                                                # Случайности
import random                                                               # Случайности


# Тест удаления проекта, проверка через пользователький интерфейс
def test_project_del_ui(app):
    if app.project.count() == 0:                                            # Проверка наличия хотя бы одного проекта в списке
        app.project.create(Project(name="Test project",description="Description test project."))    # Добавление нового проекта
    old_projects = app.project.get_project_list()                           # Список проектов до удалени
    index = randrange(len(old_projects))                                    # Получение случайного порядкового номера
    app.project.delete_by_index(index)                                      # Удаление проекта
    new_projects = app.project.get_project_list()                           # Список проектов после удаления
    old_projects[index:index+1] = []                                        # Удаление проекта из списка
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)


# Тест удаления проекта, проверка с использование базы данных
def test_project_del_db(app, orm):
    if len(orm.get_project_list()) == 0:                                    # Проверка наличия хотя бы одного проекта в списке
        app.project.create(Project(name="Test project",description="Description test project."))    # Добавление нового проекта
    old_projects = orm.get_project_list()                                   # Список проектов до удалени
    project = random.choice(old_projects)                                   # Получение случайного порядкового номера
    app.project.delete_by_id(project.id)                                    # Удаление проекта
    new_projects = orm.get_project_list()                                   # Список проектов после удаления
    old_projects.remove(project)                                            # Удаление проекта из списка
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)
