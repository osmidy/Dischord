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


class Moon(InstructionGroup):
	def __init__(self):
		super(Moon, self).__init__()

		self.texture = Image(source='moon.png').texture
		self.rect = CRectangle(texture=self.texture, cpos=(Window.width/2,Window.height-70), csize=(64,64))

		# TODO: maybe also draw a letter (signifying key of level) onto the moon


	def on_update(self,dt):
		# moon should move across the sky as level progresses
		pass

class Sun(InstructionGroup):
	def __init__(self):
		super(Sun, self).__init__()
		pass

	def on_update(self,dt):
		pass

class Backdrop(InstructionGroup):
	def __init__(self):
		super(Backdrop, self).__init__()

		self.texture = Image(source='forest.png').texture
		self.rect = Rectangle(texture=self.texture, pos=(0,Window.height*0.6), size=(Window.width,Window.height*0.4))

		# TODO: add functionality to have different, interchangeable backdrops


	def on_update(self,dt):
		# moon should move across the sky as level progresses
		pass


class Background(InstructionGroup):
    def __init__(self):
        super(Background, self).__init__()

        w = Window.width
        h = Window.height

        # Draw Ground and Sky Rectangles
        self.ground_color = Color(0.1,1.0,0.2)
        self.ground_rect = Rectangle(pos=(0,0), size=(w,h*0.6))
        self.add(self.ground_color)
        self.add(self.ground_rect)

        self.sky_color = Color(0.0,0.0,0.3)
        self.sky_rect = Rectangle(pos=(0,h*0.6), size=(w,h-h*0.6))
        self.add(self.sky_color)
        self.add(self.sky_rect)

        # Draw Sun and Moon
        self.moon = Moon()
        self.add(self.moon)
        #self.sun = Sun()	# TODO: add sun functionality as well
        #self.add(self.sun)


        # Draw backdrop
        self.backdrop = Backdrop()      
        self.add(self.backdrop) 

        
    def on_update(self, dt):
        pass

