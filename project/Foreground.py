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
from kivy.uix.image import Image
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Rectangle, Bezier
from kivy.graphics import PushMatrix, PopMatrix, Translate, Scale, Rotate
from kivy.graphics.texture import Texture
from kivy.config import Config

from random import random, randint, choice
import numpy as np


class Wall(InstructionGroup):
	def __init__(self):
		super(Wall, self).__init__()

		self.texture = Image(source='stonewall2_edited.png').texture
		self.rect = Rectangle( texture=self.texture, pos=(0,0), size=(Window.width,Window.height*0.2) )
		self.add(Color(0.2,0.15,0.15))
		self.add(self.rect)

	def on_update(self, dt):
		pass

class Foreground(InstructionGroup):
    def __init__(self):
        super(Foreground, self).__init__()

        w = Window.width
        h = Window.height

        # Draw Wall
        self.wall = Wall()
        self.add(self.wall)

        
    def on_update(self, dt):
        # As of now, should never be removed
        return True