# -*- coding: utf-8 -*-

from globals import App

__author__ = "Julien Dubois; Melia Conguisti"
__version__ = "0.1.0"

from lemapi.activity import Activity
from lemapi.api import get_listener_manager
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

        event = Event(self.stop_move)
        self.view.widgets["forward_button"].clickEvents.append(event)
        self.view.widgets["backward_button"].clickEvents.append(event)
        self.view.widgets["left_button"].clickEvents.append(event)
        self.view.widgets["right_button"].clickEvents.append(event)

    def button_return(self, hovered, clicked, middle_clicked, right_clicked, \
        direction):

        if self.clicked[direction]:
            if not clicked:
                self.clicked[direction] = False
                self.stop_move()
        elif clicked:
            self.clicked[direction] = True

            if direction == "forward":
                self.forward()
            elif direction == "backward":
                self.backward()
            elif direction == "left":
                self.left()
            else:
                self.right()

    def stop_move(self):
        if self.client:
            if self.client.connected:
                self.client.send_data("stop")

    def forward(self):
        if self.client:
            if self.client.connected:
                self.client.send_data("forward")

    def backward(self):
        if self.client:
            if self.client.connected:
                self.client.send_data("backward")

    def left(self):
        if self.client:
            if self.client.connected:
                self.client.send_data("left")

    def right(self):
        if self.client:
            if self.client.connected:
                self.client.send_data("right")

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
