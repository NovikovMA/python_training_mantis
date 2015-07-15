# -*- coding: utf-8 -*-
__author__ = 'M.Novikov'


def test_project_add(app):
    assert app.session.is_logged_in_as("administrator")
