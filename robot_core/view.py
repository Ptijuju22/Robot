# -*- coding: utf-8 -*-

from robot_core.constants import Res

__author__ = "Julien Dubois"
__version__ = "0.1.0"

import os

from lemapi.api import get_gui
from lemapi.view import View
from lemapi.widget import Button, Image_widget


class Control_view(View):
    def __init__(self):
        super().__init__()
        self.animation_index = 0

    def init_widgets(self):
        w, h = get_gui().get_size()
        tk = {"textColor": (0, 0, 0, 255)}
        image_path = os.path.join(Res.IMAGE_PATH, "wifi_0.png")

        self.add_widget("forward_button", Button, (w * 0.5, h * 0.25), \
            size=(w * 0.25, h * 0.25), anchor=(0, 0), text="Avancer", \
            textKwargs=tk)
        self.add_widget("backward_button", Button, (w * 0.5, h * 0.75), \
            size=(w * 0.25, h * 0.25), anchor=(0, 0), text="Reculer", \
            textKwargs=tk)
        self.add_widget("left_button", Button, (w * 0.25, h * 0.5), \
            size=(w * 0.25, h * 0.25), anchor=(0, 0), text="Gauche", \
            textKwargs=tk)
        self.add_widget("right_button", Button, (w * 0.75, h * 0.5), \
            size=(w * 0.25, h * 0.25), anchor=(0, 0), text="Droite", \
            textKwargs=tk)
        self.add_widget("quit_button", Button, (w * 0.5, h * 0.5), \
            size=(w * 0.2, h * 0.2), anchor=(0, 0), text="Quitter", \
            textKwargs=tk)
        
        self.add_widget("connection_image", Image_widget, (w*0.05, h*0.05), \
            image_path, size=(h*0.1, h*0.1))

    def update(self):
        get_gui().draw_background_color((255, 255, 255))
        super().update()

    def update_connection_animation(self):
        self.animation_index = (self.animation_index + 1) % 4
        image_names = ("wifi_0.png", "wifi_1.png", "wifi_2.png", "wifi_3.png")
        path = os.path.join(Res.IMAGE_PATH, image_names[self.animation_index])
        self.widgets["connection_image"].change_image(path)

    def set_connected_image(self, connected):
        if connected:
            path = os.path.join(Res.IMAGE_PATH, "connected.png")
        else:
            path = os.path.join(Res.IMAGE_PATH, "disconnected.png")
        self.widgets["connection_image"].change_image(path)

    def disable_buttons(self):
        self.widgets["forward_button"].config(enable=False)
        self.widgets["backward_button"].config(enable=False)
        self.widgets["right_button"].config(enable=False)
        self.widgets["left_button"].config(enable=False)

    def enable_buttons(self):
        self.widgets["forward_button"].config(enable=True)
        self.widgets["backward_button"].config(enable=True)
        self.widgets["right_button"].config(enable=True)
        self.widgets["left_button"].config(enable=True)