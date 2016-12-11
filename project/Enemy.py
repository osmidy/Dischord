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

from MusicHelper import *

from random import random, randint, choice
import numpy as np

import math
D = 1000

class Enemy(InstructionGroup):
    def __init__(self, spawn_x, key = Notes.C, chord = Chords.MAJOR_FIVE, speed=None, audio_callback=None, hurt_player_callback=None):
        super(Enemy, self).__init__()

        # pos3D is 3D cartesian coords
        self.pos3D = [spawn_x,0,-D]

        # pos2D is for actual position on screen
        self.pos2D = self.convert_to_pos2D(self.pos3D)

        self.size = np.array((200,400))

        if speed:
            self.speed = speed
        else:
            self.speed = 1.0

        self.hurt_player_callback = hurt_player_callback


        #---------#
        # Visuals #
        #---------#

        self.color = Color(1,0.1,0.1)
        s = self.size*self.scale_with_z()
        self.cbrect = CBRectangle( cbpos=(self.pos2D[0],self.pos2D[1]), cbsize=(s[0],s[1]) )
        self.add(self.color)
        self.add(self.cbrect)

        # If currently targeted by crosshair
        self.is_targeted = False

        self.is_dead = False

        

        # TODO: list of textures for different animation states
        # TODO: eventually replace with textures
        # self.texture = Image(source='find_a_picture.png').texture
        # self.rect = Rectangle(texture=self.texture, pos=(0,0), size=(100,100))

        #---------------#
        # Audio & Music #
        #---------------#

        self.correctPitches = MusicHelper.get_proper_chord(key, chord)
        self.dissonantPitches, self.correctionIndex = MusicHelper.get_dissonant_chord(self.correctPitches)

        self.audio_callback = audio_callback

    def lit(self):
        self.color.rgb = (0.1,0.1,1)

    def un_lit(self):
        self.color.rgb = (1,0.1,0.1)

        
    def on_update(self, dt):
        if self.is_dead:
            return False

        if self.pos3D[2] < 0:
            s = dt*self.speed*50
            self.change3D(0, 0, s)
        else:
            self.hurt_player_callback(5)
            return False

        return True

    # Called when a crosshair first hovers over an enemy
    def on_target(self):
        if (self.is_targeted):
            return

        if self.audio_callback:
            self.audio_callback(self.dissonantPitches)

    # Called immediately before dying when an enemy is hit by a player
    # Return True if successfully killed by the player, else False
    def on_hit(self, pitch):
        comparisonPitches = self.dissonantPitches[:self.correctionIndex] + [pitch] + self.dissonantPitches[self.correctionIndex:]

        pitches = None
        killed = False
        if comparisonPitches == self.correctPitches:
            pitches = self.correctPitches
            self.is_dead = True
            killed = True
        else:
            pitches = comparisonPitches

        if self.audio_callback:
            self.audio_callback(pitches)

        return killed
        

    def set_is_targeted(self, val):
        self.is_targeted = val

    def get_is_targeted(self):
        return self.is_targeted

    def change3D(self, a, b, c):
        self.pos3D = (self.pos3D[0] + a, self.pos3D[1] + b, self.pos3D[2] + c)
        self.pos2D = self.convert_to_pos2D(self.pos3D)
        self.cbrect.cbpos = self.pos2D
        s = self.size*self.scale_with_z()
        self.cbrect.size = (s[0],s[1])


    def scale_with_z(self, z=None):
        if z == None:
            z = self.pos3D[2]
        #D = 500.0   # D should be the abs value of most negative z for enemies to spawn at
        # note: z is negative for values in the field for enemies, with player at z=0
        #return 2*z/(3*D) + 1.0
        Y = Window.height*0.6
        # magic numbers, as far as the eye can see!!! ignore magic numbers below!!!! :D
        return self.map(-Y/(D*D) * (z+D)*(z+D) + Y, 0.0, D/(D*12.7/5000), 1.0, 1/10)

    def convert_to_pos2D(self, pos3D):
        #D = 500.0
        Y = Window.height*0.6
        X = Window.width
        x = pos3D[0]
        y = pos3D[1]
        z = pos3D[2]

        j = -Y/(D*D) * (z+D)*(z+D) + Y
        c = self.map(j, 0, Y, 1, 1/3)
        i = self.map(x+X/2, 0, X, X/2*(1-c), X/2*(1+c))

        return (i,j)


    def map(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

