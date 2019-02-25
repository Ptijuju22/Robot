# -*- coding: utf-8 -*-

from robot_code.globals import App

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

        self.init_events()

    def init_client(self):
        self.client = Client(App.SERVER_ADDRESS, App.SERVER_PORT)
        connected = self.client.connect()

    def init_events(self):
        lm = get_listener_manager()
        event = Event(self.send_move, "forward")
        self.view.widgets["forward_button"].clickEvents.append(event)
        event = Event(self.send_move, "backward")
        self.view.widgets["backward_button"].clickEvents.append(event)
        event = Event(self.send_move, "left")
        self.view.widgets["left_button"].clickEvents.append(event)
        event = Event(self.send_move, "right")
        self.view.widgets["right_button"].clickEvents.append(event)

        event = Event(self.send_move, "stop")
        self.view.widgets["forward_button"].endClickEvents.append(event)
        self.view.widgets["backward_button"].endClickEvents.append(event)
        self.view.widgets["left_button"].endClickEvents.append(event)
        self.view.widgets["right_button"].endClickEvents.append(event)
        self.view.widgets["quit_button"].endClickEvents.append(event)
        
        event = Event(stop_app)
        self.view.widgets["quit_button"].endClickEvents.append(event)

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
