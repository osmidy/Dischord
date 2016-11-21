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
import Leap
from Flame import Flame


class Handler(InstructionGroup):
    def __init__(self):
        super(Handler, self).__init__()
        
        self.audio_controller = AudioController()
        
        self.leapController = Leap.Controller()

        self.time = 0.0
        self.initialtime = 3.0

        # List of all objects in the game to be drawn
        self.objects = []
        self.enemy_info = [(0.0, (50.0,0.0,0.0), 0.05, self.audio_controller.play_sfx), (2.0, (50.0,3.14/2,0.0), 0.05, self.audio_controller.play_sfx)]

        self.enemies = []
        self.background = Environment("background")
        self.foreground = Environment("foreground")
        self.leftHand = LeapHand(Color(1, 0, 0))
        self.rightHand = LeapHand(Color(0,0,1))
        
        h = Window.height / 8
        w = Window.width / 12
        self.flame1 = Flame((2*w, h))
        self.flame2 = Flame((6*w, h))
        self.flame3 = Flame((10*w, h))
        
        self.flames = [self.flame1, self.flame2, self.flame3]


        self.add(self.background)
        self.add_enemies_in_range(self.time, self.time+self.initialtime)
        self.add(self.foreground)
        self.add(self.leftHand)
        self.add(self.rightHand)
        self.add(self.flame1); self.add(self.flame2); self.add(self.flame3)
        

        
    def on_update(self):
        dt = kivyClock.frametime
        
        kill_list = []

        for o in self.objects:
            if o.on_update(dt) == False:
                kill_list.append(o)
                
        for o in kill_list:
            self.remove(o)

        self.add_enemies_in_range(self.time+self.initialtime, self.time+self.initialtime+dt)
        
        if self.leapController.is_connected:
            frame = self.leapController.frame()
            self.handleFrame(frame)


        self.time += dt
        
    def handleFrame(self, frame):
        # Remove bublbles, read if visbile
        if self.leftHand.isVisible:
            self.leftHand.set_visible(False)
        if self.rightHand.isVisible:
            self.rightHand.set_visible(False)
        
        hands = frame.hands
        for hand in hands:
            currenthand = self.leftHand if hand.is_left else self.rightHand
            currenthand.set_hand(hand)
            
            self.move_hand(hand, currenthand)
            
            if currenthand.has_flame:
                if hand.grab_strength < .1:
                    currenthand.release_flame()
                else:
                    killed_enemy = self.flame_on_enemy(currenthand.grabbed_flame)
                    if killed_enemy != None:
                        killed_enemy.wasHit(currenthand.grabbed_flame.midi_pitch)
            else:
                for flame in self.flames:
                    if LeapHelper.point_is_hovered(hand, flame.get_pos()) and currenthand.hand_open and hand.grab_strength == 1.0:
                        currenthand.grab_flame(flame)
            
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
                
    ''' Return the enemy we've hit, if any'''
    def flame_on_enemy(self, flame):
        #TODO: make it use cylindrical coordinates
        for e in self.enemies:
            minX, maxX, minY, maxY = e.get_bounding_box()
            x, y = flame.get_pos()
            
            if x >= minX and x <= maxX and y >= minY and y <= maxY:
                return e
                
        return None

    def add_enemies_in_range(self, start, end):
        for e in self.enemy_info:
            if e[0] >= start and e[0] < end:
            	enemy = Enemy(*e)
                self.enemies.append(enemy)
                self.add(enemy)



    def add(self, obj):
        super(Handler, self).add(obj)
        self.objects.append(obj)
        
    def remove(self, obj):
        super(Handler, self).remove(obj)
        self.objects.remove(obj)