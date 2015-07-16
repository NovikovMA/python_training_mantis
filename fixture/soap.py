# -*- coding: utf-8 -*-
__author__ = 'M.Novikov'

from model.project import Project                                           # Проекты Mantis
from suds.client import Client                                              # Работа через SOAP
from suds import WebFault                                                   # Разбор ошибок


# Фикстура для работы с протоколом SOAP
class SoapHelper:

    # Создание объектов класса
    def __init__(self, app):
        self.app = app

    # Получение списка проектов
    def get_project_list(self):
        client = Client("http://localhost/mantisbt-1.2.19/api/soap/mantisconnect.php?wsdl") # Подключение к системе Mantis через SOAP
        user = self.app.config["webadmnin"]                                 # Получение данных авторизации
        try:
            soap_projects = client.service.mc_projects_get_user_accessible(user["username"], user["password"])   # Запрос всех проектов доступных пользователю
            return list(map(lambda x: Project(id=x["id"], name=x["name"], description=x["description"]), soap_projects))
        except WebFault:
            return []
