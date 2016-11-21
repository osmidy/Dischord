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



class Player(InstructionGroup):
    def __init__(self):
        super(Player, self).__init__()

        self.body_color = Color(1,1,1)
        self.add(self.body_color)
        self.body = Rectangle(pos=(Window.width/2-20,0), size=(40,40))
        self.add(self.body)

        
    def on_update(self, dt):
        pass
        # enemy should move closer in r direction
        
