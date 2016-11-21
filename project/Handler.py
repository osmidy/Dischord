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

from Enemy import *
from Environment import *
from Player import *
from LeapHand import *

from kivy.core.window import Window
from kivy.clock import Clock as kivyClock
from kivy.uix.label import Label
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.graphics import PushMatrix, PopMatrix, Translate, Scale, Rotate
from kivy.config import Config

from random import random, randint, choice
import numpy as np



class Handler(InstructionGroup):
    def __init__(self):
        super(Handler, self).__init__()

        self.time = 0.0
        self.initialtime = 3.0

        # List of all objects in the game to be drawn
        self.objects = []
        self.enemy_info = [(0.0, (50.0,0.0,0.0), 0.05), (2.0, (50.0,3.14/2,0.0), 0.05)]

        self.enemies = []
        self.player = LeapHand()
        self.background = Environment("background")
        self.foreground = Environment("foreground")

        


        self.add(self.background)
        self.add_enemies_in_range(self.time, self.time+self.initialtime)
        self.add(self.foreground)
        self.add(self.player)
        

        
    def on_update(self):
    	dt = kivyClock.frametime

    	for o in self.objects:
    		o.on_update(dt)

        self.add_enemies_in_range(self.time+self.initialtime, self.time+self.initialtime+dt)


        self.time += dt

    def add_enemies_in_range(self, start, end):
        for e in self.enemy_info:
            if e[0] >= start and e[0] < end:
            	enemy = Enemy(*e)
                self.enemies.append(enemy)
                self.add(enemy)



    def add(self, obj):
        super(Handler, self).add(obj)
        self.objects.append(obj)