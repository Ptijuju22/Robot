# -*- coding: utf-8 -*-

__author__ = "Julien Dubois"
__version__ = "0.1.0"

from lemapi.api import get_gui
from lemapi.view import View
from lemapi.widget import Button


class Control_view(View):
    def init_widgets(self):
        w, h = get_gui().get_size()
        tk = {"textColor": (0, 0, 0, 255)}
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

    def update(self):
        get_gui().draw_background_color((255, 255, 255))
        super().update()
