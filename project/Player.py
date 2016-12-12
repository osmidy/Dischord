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
        self.score_mult = 1

        self.health = 100

        self.controller = Leap.Controller()

        self.leftHand = Crosshair()
        self.rightHand = FlameHand()

        self.attacking = False

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

    def get_button(self):
        if not self.rightHand:
            return None
        return self.rightHand.get_button()

    def arm_weapon(self, btn):
        if not self.rightHand:
            return
        self.rightHand.arm_weapon(btn)

    def unarm_weapon(self):
        if not self.rightHand:
            return
        self.rightHand.unarm_weapon()

    def is_attacking(self):
        return self.attacking
        
    def on_update(self, dt):
        if self.controller.is_connected:
            frame = self.controller.frame()
            self.set_hands(frame.hands)
            
            if self.rightHand:
                self.rightHand.set_brightness()
                
                # Update attack state
                hand = self.rightHand.get_hand()
                if not hand:
                    return

                y = hand.palm_normal.y

                if not self.attacking and y >= .95:
                    self.attacking = True
                elif self.attacking and y <= .5:
                    self.attacking = False
            else:
                # Can't be attacking if no right hand
                self.attacking = False

        # Should never be removed from the game
        return True

    def score_up(self):
        self.score += 10 * self.score_mult

    def set_score_mult(self, size):
        self.score_mult = size / 5 + 1

    def get_health(self):
        return self.health

    def decrement_health(self, c=10):
        self.health -= c

