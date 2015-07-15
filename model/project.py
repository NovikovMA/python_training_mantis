# -*- coding: utf-8 -*-
__author__ = 'M.Novikov'

from sys import maxsize                                                     # Максимальное возможное число


# Класс, описывающий объекты - модели проектов Mantis
class Project:

    def __init__(self, id=None, name=None, status=None, inherit_global=None, view_state=None, description=None):
        self.id = id
        self.name = name
        self.status = status
        self.inherit_global = inherit_global
        self.view_state = view_state
        self.description = description

    # Представление в строчном виде
    def __repr__(self):
        return "%s: %s; %s" % (self.id, self.name, self.description)

    # Правило сравнения двух объектов класса между собой
    def __eq__(self, other):
        return (self.id is None or other.id is None or self.id == other.id)\
               and self.name == other.name

    # Вспомогательный метод для сортировки объектов класса по идентификатору
    def id_or_max(self):
        if self.id:
            return int(self.id)
        else:
            return maxsize
