# -*- coding: utf-8 -*-

from robot_core.constants import App, Res

__author__ = "Julien Dubois"
__version__ = "0.1.0"

import os
import threading

from lemapi.activity import Activity
from lemapi.api import get_listener_manager, stop_app, get_audio_player
from lemapi.audio import Mixer
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
        self.mixer = None

        self.init_mixer()
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
                self.mixer.clear()
                self.play_connected_sound()
            else:
                self.view.add_toast("Aucun robot détecté !", \
                    textColor=(0, 0, 0, 255))
                self.mixer.clear()
                self.play_connection_error_sound()
                self.disable_buttons()

        self.view.add_toast("Connection au robot...", textColor=(0, 0, 0, 255))
        self.play_connection_sound()
        threading.Thread(target=connect).start()

    def init_mixer(self):
        ap = get_audio_player()
        self.mixer = Mixer(ap)
        ap.add_mixer(self.mixer)

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

    def play_connection_sound(self):
        ap = get_audio_player()
        sound = ap.get_sound(os.path.join(Res.SOUND_PATH, "connecting.wav"))
        sound.play()
        sound.set_play_count(-1)
        self.mixer.add_sound(sound)

    def play_connected_sound(self):
        ap = get_audio_player()
        sound = ap.get_sound(os.path.join(Res.SOUND_PATH, "connected.wav"))
        sound.play()
        self.mixer.add_sound(sound)

    def play_connection_error_sound(self):
        ap = get_audio_player()
        sound = ap.get_sound(os.path.join(Res.SOUND_PATH, "connection_error.wav"))
        sound.play()
        self.mixer.add_sound(sound)

    def disable_buttons(self):
        self.view.widgets["forward_button"].config(enable=False)
        self.view.widgets["backward_button"].config(enable=False)
        self.view.widgets["right_button"].config(enable=False)
        self.view.widgets["left_button"].config(enable=False)

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
        
        self.mixer.clear()
        get_audio_player().remove_mixer(self.mixer)
        
        super().destroy()
