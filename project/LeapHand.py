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
Model for data from hand positions.  Methods are interfaces which
child classes should implement as needed.
'''

class LeapHand(InstructionGroup):
    def __init__(self):
        super(LeapHand, self).__init__()
        
        self.pos = (0, 0)
        
        # Indicate if hand is seen on canvas
        self.isVisible = False
        
        # Data model from a Leap controller
        self.hand = None

    def on_update(self, dt):
        pass
        
    def update_state(self):
        pass
    
    def set_pos(self, pos):
        self.pos = pos
            
    def set_hand(self, hand):
        self.hand = hand
        
    def set_visible(self, val):
        self.isVisible = val

        if not self.isVisible:
            self.hand = None