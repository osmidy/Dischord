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
from kivy.config import Config

import Leap
from Crosshair import *
from FlameHand import *

from random import random, randint, choice
import numpy as np

import math

'''
Representation of the player's interactions with the game,
as well as his current standing (score, etc.)
'''
class Player(InstructionGroup):
    def __init__(self):
        super(Player, self).__init__()

        self.score = 0

        self.health = 100

        self.controller = Leap.Controller()

        self.leftHand = Crosshair()
        self.rightHand = FlameHand()

        self.add(self.leftHand)
        self.add(self.rightHand)

    def set_hands(self, hands):
        # TODO: handle overlapping of enemy (in Handler)
        for hand in hands:
            pos = LeapHelper.position_as_pixels(hand)
            
            if hand.is_left:
                self.leftHand.set_hand(hand)
                self.leftHand.set_pos(pos)
            else:
                self.rightHand.set_hand(hand)
                self.rightHand.set_pos(pos)

    def get_flame(self):
        return self.rightHand.flameParticle
        
    def on_update(self, dt):
        if self.controller.is_connected:
            frame = self.controller.frame()
            self.set_hands(frame.hands)

        # Should never be removed from the game
        return True

    def score_up(self):
        self.score += 10

    def get_health(self):
        return self.health

