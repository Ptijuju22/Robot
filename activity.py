# -*- coding: utf-8 -*-

__author__ = "Julien Dubois; Melia Conguisti"
__version__ = "0.1.0"

from lemapi.activity import Activity
from lemapi.api import get_listener_manager
from lemapi.event import Event


class Control_activity(Activity):
    def __init__(self):
        self.clicked = {
            "forward": False,
            "backward": False,
            "left": False,
            "right": False
            }

        self.init_events()

    def init_events(self):
        lm = get_listener_manager()
        event = Event(self.button_return, "forward")
        self.view.widgets["forward_button"].onClickEvents.append(event)
        event = Event(self.button_return, "backward")
        self.view.widgets["backward_button"].onClickEvents.append(event)
        event = Event(self.button_return, "left")
        self.view.widgets["left_button"].onClickEvents.append(event)
        event = Event(self.button_return, "right")
        self.view.widgets["right_button"].onClickEvents.append(event)

    def button_return(self, hovered, clicked, middle_clicked, right_clicked, \
        direction):

        if self.clicked[direction]
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
        pass

    def forward(self):
        pass

    def backward(self):
        pass

    def left(self):
        pass

    def right(self):
        pass
