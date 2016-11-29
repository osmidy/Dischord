import sys
sys.path.append('..')
from common.core import *
from common.gfxutil import *
from common.audio import *
from common.mixer import *
from common.note import *
from common.wavegen import *
from common.wavesrc import *
from common.writer import *

from kivy.core.window import Window
from kivy.clock import Clock as kivyClock
from kivy.uix.label import Label
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.graphics import PushMatrix, PopMatrix, Translate, Scale, Rotate
from kivy.config import Config

from random import random, randint, choice
import numpy as np

import math


class Enemy(InstructionGroup):
    def __init__(self, spawn_pos, speed, audio_callback=None):
        super(Enemy, self).__init__()

        # pos is 3D cartesian coords
        self.pos = spawn_pos

        # list of textures for different animation states
        # TODO: eventually replace with textures
        self.textures = []
        self.textures.append(Texture())



        
    def on_update(self, dt):
        pass


    def map(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

