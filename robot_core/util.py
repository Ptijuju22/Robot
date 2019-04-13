# -*- coding: utf-8 -*-

from robot_core.constants import Res

__author__ = "Julien Dubois"
__version__ = "0.1.0"

import os

from lemapi.api import get_audio_player


def load_sounds():
	print("[Robot] [INFO] [load_sounds] Loading sounds to RAM...")
	ap = get_audio_player()

	for sound in Res.SOUNDS:
		path = os.path.join(Res.SOUND_PATH, sound)
		ap.load_sound(path)