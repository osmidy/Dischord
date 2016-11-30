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
from Background import *
from Foreground import *
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

data = [(0.0,0),(2.0,-250),(4.0,250),(6.0,-125),(10.0,0)]

class E_List(InstructionGroup):
    def __init__(self):
        super(E_List, self).__init__()

        self.enemies = []

    def add(self, obj):
        super(E_List, self).add(obj)
        self.enemies.append(obj)

    def on_update(self, dt):
        print len(self.enemies)
        kill_list = []
        for e in self.enemies:
            if not e.on_update(dt):
                kill_list.append(e) 
        for k in kill_list:
            self.enemies.remove(k)
            self.remove(k)

        return True


class Handler(InstructionGroup):
    def __init__(self):
        super(Handler, self).__init__()
        
        self.audio_controller = AudioController()

        self.time = 0.0
        self.enemy_data = data

        # List of all objects in the game to be drawn
        self.objects = []

        self.enemies = E_List()
        self.background = Background()
        self.foreground = Foreground()
        self.player = Player()
        
        
        self.flames = []


        self.add(self.background)
        self.add(self.enemies)
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

        self.add_enemies(self.time)

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

    def add_enemies(self, time):
        remove_list = []
        for e in self.enemy_data:
            if e[0] <= time:
                E = Enemy(e[1])
                self.enemies.add(E)
                #self.add(E)
                remove_list.append(e)
        for r in remove_list:
            self.enemy_data.remove(r)

    def get_flame(self):
        return self.player.get_flame()

    def add(self, obj):
        super(Handler, self).add(obj)
        self.objects.append(obj)
        
    def remove(self, obj):
        super(Handler, self).remove(obj)
        self.objects.remove(obj)