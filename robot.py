# -*- coding: utf-8 -*-

from activity import Control_activity
from globals import App
from view import Control_view

__author__ = "Julien Dubois; Melia Conguisti"
__version__ = "0.1.0"

from lemapi.api import start_activity


def main(app_id):
    App.app_id = app_id
    create_control_activity()


def exit():
    pass


def create_control_activity():
    view = Control_view()
    activity = Control_activity(view)
    start_activity(activity)
