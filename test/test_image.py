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
from kivy.graphics.texture import Texture
from kivy.uix.image import Image

from random import random, randint, choice
import numpy as np


# part 1
class MainWidget1(BaseWidget) :
    def __init__(self):
        super(MainWidget1, self).__init__()
        
        #Setup Graphics
        self.objects = []

        #self.canvas.add(self.objects)

        self.texture = Image(source='moon.png').texture

        #self.texture.blit_buffer()
        #self.add_widget(self.texture)


        self.rect = CRectangle(texture=self.texture, cpos=(Window.width/2,Window.height/2), csize=(512,512))

        self.canvas.add(self.rect)



    def on_update(self):
        #self.objects.on_update()
        pass


run(MainWidget1)