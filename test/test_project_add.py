# -*- coding: utf-8 -*-
__author__ = 'M.Novikov'

from model.project import Project                                           # Проекты Mantis


# Добавление проекта, проверка через пользователький интерфейс
def test_project_add_ui(app):
    project = Project(name="Test project",description="Description test project.")  # Новый проект
    old_projects = app.project.get_project_list()                           # Список проектов до добавления
    if not app.project.is_project_on_list(project):                         # Проверка наличия проекта в списке
        app.project.create(project)                                         # Добавление проекта
        old_projects.append(project)                                        # Добавление нового проекта в список
    new_projects = app.project.get_project_list()                           # Список проектов после добавления
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)

# Добавление проекта, проверка с использование базы данных
def test_project_add_db():
    pass
