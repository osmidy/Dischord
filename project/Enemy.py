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
from kivy.uix.image import Image
from kivy.clock import Clock as kivyClock
from kivy.uix.label import Label
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.graphics import PushMatrix, PopMatrix, Translate, Scale, Rotate
from kivy.config import Config

from MusicHelper import *
from TonalFlowChart import *

from random import random, randint, choice
import numpy as np

import math
D = 1000
d = 30

class Note_Display(InstructionGroup):
    def __init__(self, key, chord, x_center, y_top):
        super(Note_Display, self).__init__()

        self.key = key

        # Group of midi pitches
        self.chord = chord

        self.num_notes = len(chord)
        #d = 40
        x = np.linspace(x_center-d,x_center+d,self.num_notes)

        self.notes = []
        for i in xrange(self.num_notes):
            chordName = MusicHelper.get_scale_name(key, self.chord[i])
            texture = self.get_texture(chordName)
            self.add( CBRectangle(texture=texture, cbpos=(x[i],y_top+5), cbsize=(25,25)) )

    def add(self, note):
        super(Note_Display, self).add(note)
        self.notes.append(note)

    def get_texture(self, name):
        #implement choosing proper image from chord/notes (how do I do this?)
        return Image(source="../data/" + name + ".png").texture

    def on_update(self, dt, x_center, y_top):
        #d = 40
        x = np.linspace(x_center-d,x_center+d,self.num_notes)
        for i in xrange(len(self.notes)):
            self.notes[i].cbpos = ( x[i], y_top+5 )
            self.notes[i].cbsize = ( 25, 25 )


class Enemy(InstructionGroup):
    def __init__(self, spawn_x, key = Notes.C, speed=1.0, audio_callback=None, hurt_player_callback=None, dmg_rect_on_hit_callback=None, add_sound=None, remove_sound=None):
        super(Enemy, self).__init__()

        self.time = 0.0
        self.anim_switch_time = 0.270
        self.anim_time = self.anim_switch_time
        self.anim_frame = 0

        # pos3D is 3D cartesian coords
        self.pos3D = [spawn_x,0,-D]

        # pos2D is for actual position on screen
        self.pos2D = self.convert_to_pos2D(self.pos3D)

        self.size = np.array((200,380))*Window.height/600

        self.speed = speed

        # Callback Functions
        self.hurt_player_callback = hurt_player_callback
        self.dmg_rect_on_hit_callback = dmg_rect_on_hit_callback

        #---------#
        # Visuals #
        #---------#

        self.texture = Image(source='../data/ogre.png').texture
        self.textures = []
        self.texture_a = self.texture.get_region(0,435,107,145);
        self.textures.append(self.texture_a)
        self.texture_b = self.texture.get_region(107,435,107,145);
        self.textures.append(self.texture_b)
        self.texture_c = self.texture.get_region(215,435,107,145);
        self.textures.append(self.texture_c)
        self.texture_d = self.texture.get_region(322,435,107,145);
        self.textures.append(self.texture_d)


        s = self.size*self.scale_with_z()
        self.cbrect = CBRectangle(texture=self.textures[self.anim_frame], cbpos=(self.pos2D[0],self.pos2D[1]), cbsize=(s[0],s[1]))
        self.color = Color(0.65,0.65,0.65)
        self.add(self.color)
        self.add(self.cbrect)

        # self.color = Color(1,0.1,0.1)
        # s = self.size*self.scale_with_z()
        # self.cbrect = CBRectangle( cbpos=(self.pos2D[0],self.pos2D[1]), cbsize=(s[0],s[1]) )
        # self.add(self.color)
        # self.add(self.cbrect)

        # If currently targeted by crosshair
        self.is_targeted = False

        self.is_dead = False
        

        # TODO: list of textures for different animation states
        # TODO: eventually replace with textures
        # self.texture = Image(source='../data/find_a_picture.png').texture
        # self.rect = Rectangle(texture=self.texture, pos=(0,0), size=(100,100))

        #---------------#
        # Audio & Music #
        #---------------#

        self.key = key
        self.chord = Chord(key)
        self.dissonantPitches = self.chord.pitches

        # Assigned when this Enemy is killed
        self.resolvedPitches = []

        #TODO: these are example pitches; we need to add the pitches from the notes of chord...
        self.seq = add_sound((69,74,78))

        # Note Display
        self.ND = Note_Display(key, self.dissonantPitches, self.pos2D[0], self.pos2D[1]+s[1])
        self.add(self.ND)

        # Callback Functions
        self.audio_callback = audio_callback
        self.add_sound = add_sound
        self.remove_sound = remove_sound

    def lit(self):
        self.color.rgb = (0.4,0.4,1)

    def un_lit(self):
        self.color.rgb = (0.65,0.65,0.65)
        
    def on_update(self, dt):
        self.time += dt

        # Check if enemy is dead, and return false immediately if so
        if self.is_dead:
            self.remove_sound(self.seq)
            print "dead"
            return False

        # Animate the Enemy's frames
        self.anim_time -= dt
        if self.anim_time <= 0.0:
            self.anim_time = self.anim_switch_time + self.anim_time
            self.anim_frame += 1
            self.cbrect.texture = self.textures[self.anim_frame%len(self.textures)]

        # Move Enemy down toward the player
        if self.pos3D[2] < 0:
            s = dt*self.speed*30
            self.change3D(0, 0, s)
        else:
            self.hurt_player_callback(5)
            self.dmg_rect_on_hit_callback()
            self.is_dead = True

        # Move Note Display to follow enemy
        s = self.size*self.scale_with_z()
        self.ND.on_update( dt, self.pos2D[0], self.pos2D[1]+s[1] )

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
        # Sub in the pitch for the note is closest to in the chord
        minDist = float("inf")
        minPitch = None
        for chordPitch in self.dissonantPitches:
            dist = abs(pitch - chordPitch)
            if dist < minDist:
                minDist = dist
                minPitch = chordPitch

        idx = self.dissonantPitches.index(minPitch)
        comparisonPitches = list(self.dissonantPitches)
        comparisonPitches[idx] = minPitch

        playbackPitches = comparisonPitches
        killed = False

        if Chord.is_valid_chord(self.key, comparisonPitches):
            self.resolvedPitches = comparisonPitches
            self.is_dead = True
            killed = True

        if self.audio_callback:
            self.audio_callback(playbackPitches)

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
            #print z
        #D = 500.0   # D should be the abs value of most negative z for enemies to spawn at
        # note: z is negative for values in the field for enemies, with player at z=0
        #return 2*z/(3*D) + 1.0
        Y = Window.height*0.68
        # magic numbers, as far as the eye can see!!! ignore magic numbers below!!!! :D
        #return self.map(-Y/(D*D) * (z+D)*(z+D) + Y, 0.0, D/(D*12.7/5000), 1.0, 1/10)
        s = np.power(1.002,z)
        #print s
        return s

    def convert_to_pos2D(self, pos3D):
        #D = 500.0
        Y = Window.height*0.68
        X = Window.width
        x = pos3D[0]
        y = pos3D[1]
        z = pos3D[2]

        #j = -Y/(D*D) * (z+D)*(z+D) + Y
        j = Y - Y*np.power(1.002,z)
        c = self.map(j, 0, Y, 1, 1/3)
        i = self.map(x+X/2, 0, X, X/2*(1-c), X/2*(1+c))

        return (i,j)


    def map(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

