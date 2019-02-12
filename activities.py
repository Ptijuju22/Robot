# -*- coding: utf-8 -*-

from globals import App

__author__ = "Julien Dubois; Melia Conguisti"
__version__ = "0.1.0"

from lemapi.activity import Activity
from lemapi.api import get_listener_manager, stop_app
from lemapi.event_manager import Event
from lemapi.network import Client


class Control_activity(Activity):
    def __init__(self, view):
        super().__init__(view)

        self.clicked = {
            "forward": False,
            "backward": False,
            "left": False,
            "right": False
            }
        self.client = None

        self.init_client()
        self.init_events()

    def init_client(self):
        self.client = Client(App.SERVER_ADDRESS, App.SERVER_PORT)
        connected = self.client.connect()

    def init_events(self):
        lm = get_listener_manager()
        event = Event(self.button_return, "forward")
        self.view.widgets["forward_button"].stateEvents.append(event)
        event = Event(self.button_return, "backward")
        self.view.widgets["backward_button"].stateEvents.append(event)
        event = Event(self.button_return, "left")
        self.view.widgets["left_button"].stateEvents.append(event)
        event = Event(self.button_return, "right")
        self.view.widgets["right_button"].stateEvents.append(event)

        event = Event(stop_app)
        self.view.widgets["quit_button"].clickEvents.append(event)

    def button_return(self, hovered, clicked, middle_clicked, right_clicked, \
        direction):

        if self.clicked[direction]:
            if not clicked:
                self.clicked[direction] = False
                self.send_move("stop")
        elif clicked:
            self.clicked[direction] = True
            self.send_move(direction)

    def send_move(self, move):
        if self.client:
            if self.client.connected:
                self.client.send_msg(move)

    def sleep(self):
        if self.client:
            self.client.disconnect()
        super().sleep()

    def wakeup(self):
        if self.client:
            self.client.connect()
        super().wakeup()

    def destroy(self):
        if self.client:
            self.client.disconnect()
        super().destroy()
