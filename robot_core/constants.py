# -*- coding: utf-8 -*-

__author__ = "Julien Dubois"
__version__ = "0.1.0"


class App:
    ID = 0
    SERVER_ADDRESS = "10.3.141.1"
    SERVER_PORT = 41520
    CONNECTION_TIMEOUT = 10

class Res:
	SOUND_PATH = "data/sounds/"
	SOUNDS = (
		"connected.wav",
		"connecting.wav",
		"connection_error.wav"
	)
	IMAGE_PATH = "data/images/"
	IMAGES = (
		"connected.png",
		"disconnected.png",
		"wifi_0.png",
		"wifi_1.png",
		"wifi_2.png",
		"wifi_3.png"
	)