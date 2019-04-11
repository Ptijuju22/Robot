# -*- coding: utf-8 -*-

from robot_code.constants import App

__author__ = "Julien Dubois"
__version__ = "0.1.0"

import threading

from lemapi.activity import Activity
from lemapi.api import get_listener_manager, stop_app
from lemapi.event_manager import Event
from lemapi.network import Client, Wifi
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
        self.old_network = ""

        self.init_events()

    def init_client(self):
        def connect():
            self.old_network = Wifi.get_current_ssid()
            Wifi.add_network("LemRobotHotspot", "m3liaR0b0t")
            Wifi.connect("LemRobotHotspot")

            self.client = Client(App.SERVER_ADDRESS, App.SERVER_PORT)
            if self.client.connect(App.CONNECTION_TIMEOUT):
                self.view.add_toast("Connection établie !", \
                    textColor=(0, 0, 0, 255))
            else:
                self.view.add_toast("Aucun robot détecté !", \
                    textColor=(0, 0, 0, 255))

        self.view.add_toast("Connection au robot...", \
            textColor=(0, 0, 0, 255))
        threading.Thread(target=connect).start()

    def init_events(self):
        lm = self.listener_manager

        event = Event(self.send_move, "forward")
        self.view.widgets["forward_button"].clickEvents.append(event)
        lm.km.add_key_down_event(event, K_UP)
        lm.cm.add_joy_up_event(event)

        event = Event(self.send_move, "backward")
        self.view.widgets["backward_button"].clickEvents.append(event)
        lm.km.add_key_down_event(event, K_DOWN)
        lm.cm.add_joy_down_event(event)

        event = Event(self.send_move, "left")
        self.view.widgets["left_button"].clickEvents.append(event)
        lm.km.add_key_down_event(event, K_LEFT)
        lm.cm.add_joy_left_event(event)

        event = Event(self.send_move, "right")
        self.view.widgets["right_button"].clickEvents.append(event)
        lm.km.add_key_down_event(event, K_RIGHT)
        lm.cm.add_joy_right_event(event)

        event = Event(self.send_move, "stop")
        self.view.widgets["forward_button"].endClickEvents.append(event)
        self.view.widgets["backward_button"].endClickEvents.append(event)
        self.view.widgets["left_button"].endClickEvents.append(event)
        self.view.widgets["right_button"].endClickEvents.append(event)
        self.view.widgets["quit_button"].endClickEvents.append(event)
        lm.km.add_key_down_event(event, K_UP)
        lm.km.add_key_down_event(event, K_DOWN)
        lm.km.add_key_down_event(event, K_LEFT)
        lm.km.add_key_down_event(event, K_RIGHT)
        lm.cm.add_joy_dead_event(event)

        event = Event(stop_app)
        self.view.widgets["quit_button"].endClickEvents.append(event)
        lm.km.add_key_down_event(event, K_ESCAPE)
        lm.cm.add_button_pressed_event(event, "button_b")


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
        Wifi.connect(self.old_network)
        super().destroy()
