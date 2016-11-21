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


class Flame(InstructionGroup):
    def __init__(self, pos):
        super(Flame, self).__init__()
        
        # TODO: This will be a particle. Use circle for MS1
        self.pos = pos
        self.orignal_pos = pos
        
        # TODO: make these args, label flame with note
        self.midi_pitch = 60
        self.note_name = "C"
        
        self.color = Color(1, .65, 0) # Orange
        self.add(self.color)
        
        self.circle = CEllipse(cpos = pos, size = (50, 50)) # radius = 25
        self.add(self.circle)
        self.color = Color(0,0,0)
        
        
    def on_update(self, dt):
        pass
        
    def set_pos(self, pos):
        self.pos = pos
        self.circle.set_cpos(pos)
        
    def reset_pos(self):
        self.pos = self.orignal_pos
        self.circle.set_cpos(self.pos)
        
    def get_pos(self):
        return self.pos