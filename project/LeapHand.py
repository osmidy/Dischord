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

from leap.LeapHelper import *
import Leap

'''
Class for view of hand positions, as well as
the data backing the view
'''

class LeapHand(InstructionGroup):
    def __init__(self, color):
        super(LeapHand, self).__init__()
        
        self.pos = (0, 0)
        
        self.controller = Leap.Controller()
        
        # Indicate if hand is seen on canvas
        self.isVisible = False
        
        # Data model from a Leap controller
        self.hand = None
        
        self.color = color
        self.add(self.color)
        
        self.has_flame = False
        self.hand_open = True
        self.grabbed_flame = None
        
        self.cursor = CEllipse(cpos = self.pos, size = (40, 40))
        self.add(self.cursor)

    def on_update(self, dt):
        pass
        
    def update_state(self):
        pass
    
    def set_pos(self, pos):
        self.pos = pos
        self.cursor.set_cpos(pos)
        
        self.move_flame()
            
    def move_flame(self):
        if self.has_flame:
            self.grabbed_flame.set_pos(self.pos)
            
    def grab_flame(self, flame):
        if not self.has_flame:
            self.grabbed_flame = flame
            self.has_flame = True
            self.hand_open = False
            self.grabbed_flame.set_pos(self.pos)
            
    def release_flame(self):
        if self.has_flame:
            self.grabbed_flame.reset_pos()
            self.has_flame = False
            self.grabbed_flame = None
            self.hand_open = True
            
    def set_hand(self, hand):
        self.hand = hand
        
    def set_visible(self, val):
        self.isVisible = val
        
        if self.isVisible:
            self.add(self.color)
            self.add(self.cursor)
        else:
            self.remove(self.cursor)
            self.remove(self.color)
            self.hand = None