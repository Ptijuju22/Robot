# -*- coding: utf-8 -*-

from robot_code.constants import App

__author__ = "Julien Dubois"
__version__ = "0.1.0"

import threading

from lemapi.activity import Activity
from lemapi.api import get_listener_manager, stop_app
from lemapi.event_manager import Event
from lemapi.network import Client
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_UP, K_ESCAPE


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
        def connect():
            self.client = Client(App.SERVER_ADDRESS, App.SERVER_PORT)
            if self.client.connect():
                self.view.add_toast("Connection établie !")
            else:
                self.view.add_toast("Aucun robot détecté !")

        self.view.add_toast("Connection au robot...")
        threading.Thread(target=connect).start()

    def init_events(self):
        lm = get_listener_manager()

        event = Event(self.send_move, "forward")
        self.view.widgets["forward_button"].clickEvents.append(event)
        lm.km.add_key_down_event(event, K_UP)
        event = Event(self.send_move, "backward")
        self.view.widgets["backward_button"].clickEvents.append(event)
        lm.km.add_key_down_event(event, K_DOWN)
        event = Event(self.send_move, "left")
        self.view.widgets["left_button"].clickEvents.append(event)
        lm.km.add_key_down_event(event, K_LEFT)
        event = Event(self.send_move, "right")
        self.view.widgets["right_button"].clickEvents.append(event)
        lm.km.add_key_down_event(event, K_RIGHT)

        event = Event(self.on_joy_motion)
        lm.cm.add_joy_motion_event(event)

        event = Event(self.send_move, "stop")
        self.view.widgets["forward_button"].endClickEvents.append(event)
        self.view.widgets["backward_button"].endClickEvents.append(event)
        self.view.widgets["left_button"].endClickEvents.append(event)
        self.view.widgets["right_button"].endClickEvents.append(event)
        self.view.widgets["quit_button"].endClickEvents.append(event)

        event = Event(stop_app)
        self.view.widgets["quit_button"].endClickEvents.append(event)

    def on_joy_motion(self, x, y, old_x, old_y):
        if abs(x) > abs(y):
            if x >= 0.1:
                if old_x < 0.1:
                    self.send_move("right")
            elif x <= -0.1:
                if old_x > -0.1:
                    self.send_move("left")
            elif old_x >= 0.1 or old_x <= -0.1:
                self.send_move("stop")
        else:
            if y >= 0.1:
                if old_y < 0.1:
                    self.send_move("forward")
            elif y <= -0.1:
                if old_y > -0.1:
                    self.send_move("backward")
            elif old_y >= 0.1 or old_y <= -0.1:
                self.send_move("stop")

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
