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



class Environment(InstructionGroup):
    def __init__(self, gtype):
        super(Environment, self).__init__()

        self.type = gtype

        if gtype == "foreground":
       		self.color = Color(0.7, 0.6, 0.28)
       		self.rect = Rectangle(pos=(0,100), size=(Window.width, 100))
        elif gtype == "background":
            self.color = Color(0.2, 0.6, 0.28)
            self.rect = Rectangle(pos=(0,0), size=(Window.width, 500))

        self.add(self.color)
        self.add(self.rect)


        
    def on_update(self, dt):
        pass
