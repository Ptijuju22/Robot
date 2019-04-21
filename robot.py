# -*- coding: utf-8 -*-

from robot_core.activity import Control_activity
from robot_core.constants import App
from robot_core.util import load_images, load_sounds
from robot_core.view import Control_view

__author__ = "Julien Dubois; Melia Conguisti"
__version__ = "0.1.0"

import os

from lemapi.api import start_activity, force_view_update, get_app_path


def main(app_id):
    print("[Robot] [INFO] [main] Starting Robot app")
    App.ID = app_id
    os.chdir(get_app_path())
    load_resources()
    create_control_activity()


def exit():
    pass


def load_resources():
    load_images()
    load_sounds()


def create_control_activity():
    view = Control_view()
    activity = Control_activity(view)
    start_activity(activity)
    force_view_update()
    activity.init_client()
