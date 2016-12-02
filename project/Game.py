from kivy.config import Config
#Config.set('graphics', 'height', '800')
#Config.set('graphics', 'width', '1000')
#Config.set('graphics', 'fullscreen', 'auto')


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

from Handler import *
from AudioController import *

from kivy.core.window import Window
from kivy.clock import Clock as kivyClock
from kivy.uix.label import Label
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.graphics import PushMatrix, PopMatrix, Translate, Scale, Rotate

from random import random, randint, choice
import numpy as np


class Game(BaseWidget):
    def __init__(self):
        super(Game, self).__init__()

        self.handler = Handler()
        self.canvas.add(self.handler)
        self.add_widget(self.handler.get_flame())

        self.HUD = topleft_label()
        self.add_widget(self.HUD)

    def on_touch_down(self, touch):
        pass

    def on_touch_up(self, touch):
        pass

    def on_update(self):
    	self.handler.on_update()
        self.HUD.text = 'Health: %d\n' % self.handler.player.get_health()

run(Game)