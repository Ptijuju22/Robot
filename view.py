# -*- coding: utf-8 -*-

__author__ = "Julien Dubois; Melia Conguisti"
__version__ = "0.1.0"

from lemapi.api import get_gui
from lemapi.view import View
from lemapi.widget import Button


class Control_view(View):
    def init_widgets(self):
        w, h = get_gui().get_size()
        self.add_widget("forward_button", Button, (w * 0.5, h * 0.25), \
            size=(w * 0.25, h * 0.25), anchor=(0, 0), text="Avancer")
        self.add_widget("backward_button", Button, (w * 0.5, h * 0.75), \
            size=(w * 0.25, h * 0.25), anchor=(0, 0), text="Reculer")
        self.add_widget("left_button", Button, (w * 0.25, h * 0.5), \
            size=(w * 0.25, h * 0.25), anchor=(0, 0), text="Gauche")
        self.add_widget("right_button", Button, (w * 0.75, h * 0.5), \
            size=(w * 0.25, h * 0.25), anchor=(0, 0), text="Droite")
