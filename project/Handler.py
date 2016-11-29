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
from kivy.core.window import Window
from kivy.clock import Clock as kivyClock
from kivy.uix.label import Label
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.graphics import PushMatrix, PopMatrix, Translate, Scale, Rotate
from kivy.config import Config

from AudioController import *

from random import random, randint, choice
import numpy as np

from leap.LeapHelper import *
from LeapHand import *
from Flame import Flame


class Handler(InstructionGroup):
    def __init__(self):
        super(Handler, self).__init__()
        
        self.audio_controller = AudioController()

        self.time = 0.0
        self.initialtime = 3.0

        # List of all objects in the game to be drawn
        self.objects = []

        self.enemies = []
        self.background = Environment("background")
        self.foreground = Environment("foreground")
        self.player = Player()
        
        
        self.flames = []


        self.add(self.background)
        self.add_enemies_in_range(self.time, self.time+self.initialtime)
        self.add(self.foreground)
        self.add(self.player)        

        
    def on_update(self):
        self.audio_controller.on_update()
        dt = kivyClock.frametime
        
        kill_list = []

        for o in self.objects:
            if o.on_update(dt) == False:
                kill_list.append(o)
                
        for o in kill_list:
            self.remove(o)

        self.crosshair_on_enemy()

        self.add_enemies_in_range(self.time+self.initialtime, self.time+self.initialtime+dt)


        self.time += dt
            
    def move_hand(self, hand, currentHand):
        pos = LeapHelper.position_as_pixels(hand)
        
        def checkBounds(x, y):
            return 0 <= x and x <= Window.width and 0 <= y and y <= Window.height
            
        if not checkBounds(*pos):
            currentHand.release_flame()
            currentHand.set_visible(False)
        else:
            currentHand.set_visible(True)
            currentHand.set_pos(pos)
            
            if not currentHand.isVisible:
                self.objects.add(currentHand)
                currentHand.set_visible(True)
                
    ''' Return the enemies we've hit, if any'''
    def crosshair_on_enemy(self):
        # TODO: find points in some bounding box of the enemy
        pass

    def add_enemies_in_range(self, start, end):
        for e in self.enemies:
            if e[0] >= start and e[0] < end:
            	enemy = Enemy(*e)
                self.enemies.append(enemy)
                self.add(enemy)

    def get_flame(self):
        return self.player.get_flame()

    def add(self, obj):
        super(Handler, self).add(obj)
        self.objects.append(obj)
        
    def remove(self, obj):
        super(Handler, self).remove(obj)
        self.objects.remove(obj)