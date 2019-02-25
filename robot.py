# -*- coding: utf-8 -*-

from robot_code.activities import Control_activity
from robot_code.globals import App
from robot_code.views import Control_view

__author__ = "Julien Dubois; Melia Conguisti"
__version__ = "0.1.0"

from lemapi.api import start_activity, force_view_update


def main(app_id):
    print("[Robot] [INFO] [main] Starting Robot app")
    App.ID = app_id
    create_control_activity()


def exit():
    pass


def create_control_activity():
    view = Control_view()
    activity = Control_activity(view)
    start_activity(activity)
    force_view_update()
    activity.init_client()
