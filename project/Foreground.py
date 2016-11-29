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
from kivy.graphics import Color, Ellipse, Rectangle, Bezier
from kivy.graphics import PushMatrix, PopMatrix, Translate, Scale, Rotate
from kivy.config import Config

from random import random, randint, choice
import numpy as np



class Foreground(InstructionGroup):
    def __init__(self):
        super(Foreground, self).__init__()

        w = Window.width
        h = Window.height

        # Draw Wall
        # TODO: use a wall texture (find image online) instead of a solid brown color
        self.wall_color = Color(0.5,0.3,0.1)
        self.wall_rect = Rectangle(pos=(0,0), size=(w,h*0.2))
        self.add(self.wall_color
        self.add(self.wall_rect)

        
    def on_update(self, dt):
        pass
