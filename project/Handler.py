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
from MusicHelper import *
from AudioController import *
from leap.LeapHelper import *
from LeapHand import *
from Flame import Flame

from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.clock import Clock as kivyClock
from kivy.uix.label import Label
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.graphics import PushMatrix, PopMatrix, Translate, Scale, Rotate
from kivy.config import Config

from random import random, randint, choice
import numpy as np


data = [(0.0,0),(2.0,-250),(4.0,250),(6.0,-400),(10.0,0)]
#data = [(0.0,0)]

class E_List(InstructionGroup):
    def __init__(self):
        super(E_List, self).__init__()

        self.enemies = []

    def add(self, obj):
        super(E_List, self).insert(0,obj)
        self.enemies.insert(0,obj)

    def on_update(self, dt):
        kill_list = []
        for e in self.enemies:
            if not e.on_update(dt):
                kill_list.append(e) 
        for k in kill_list:
            self.enemies.remove(k)
            self.remove(k)

        return True

class ProgressionManager(InstructionGroup):
    def __init__(self):
        super(ProgressionManager, self).__init__()

        # list of tuples: (chord, display_rect)
        self.progression = []
        super(ProgressionManager, self).add(Color(0.6,0.6,0.8))

    def add(self, chord):
        x = 50 + len(self.progression)*50
        y = Window.height - 87
        txt = self.get_chord_texture(chord)
        display_rect = Rectangle( texture=txt, pos=(x,y) , size=(45,45) )
        tup = (chord, display_rect)
        super(ProgressionManager, self).add(display_rect)
        self.progression.append(tup)

    def clear(self):
        for c in self.progression:
            super(ProgressionManager, self).remove(c[1])
        self.progression[:] = []

    def get_chord_texture(self, chord):
        data_path = "../data_path/"

        #get string with name of chord
        name = data_path + chord.get_chord_name()
        if name.isupper():
            return Image(source=name+'.png').texture
        else:
            return Image(source=name.upper()+'_.png').texture

    def on_update(self, dt):
        return True

class Damage_Rect(InstructionGroup):
    def __init__(self):
        super(Damage_Rect, self).__init__()

        self.was_hit = False
        self.isfading = False

        self.damage_rect = Rectangle(pos=(0,0), size=(Window.width,Window.height))
        self.damage_color = Color(rgba=(1,0,0,0.0))

        self.add(self.damage_color)
        self.add(self.damage_rect)

    def on_hit(self):
        self.was_hit = True

    def flash_rect(self, inc):
        a = self.damage_color.rgba[3]
        if a >= 0.55:
            self.was_hit = False
            self.isfading = True
        elif a <= 0.0:
            self.damage_color.rgba = (1,0,0,0.0)
            self.isfading = False

        if self.was_hit:
            self.damage_color.rgba = (1, 0, 0, a+inc*2)
        else:
            self.damage_color.rgba = (1, 0, 0, a-inc)

    def on_update(self, dt):
        if self.was_hit or self.isfading:
            self.flash_rect(0.07)

        return True



class Handler(InstructionGroup):
    def __init__(self):
        super(Handler, self).__init__()
        
        self.audio_controller = None

        self.time = 0.0
        self.enemy_data = data

        # Handles and displays progressions near top of screen
        self.PM = ProgressionManager()

        # Displays Damage rectangle when player is hit
        self.dmg_rect = Damage_Rect()

        # List of all objects in the game to be drawn
        self.objects = []

        # References to game elements interacted with
        self.target = None

        self.enemies = E_List()
        self.background = Background()
        self.foreground = Foreground()
        self.player = Player()

        # Add Instruction Groups to self
        self.add(self.background)
        self.add(self.enemies)
        self.add(self.foreground)
        self.add(self.player)
        self.add(self.PM)
        self.add(self.dmg_rect)


    def include_audio(self, audio_controller):
        self.audio_controller = audio_controller
        
    def on_update(self):
        self.audio_controller.on_update()

        dt = kivyClock.frametime
        
        kill_list = []

        for o in self.objects:
            if o.on_update(dt) == False:
                kill_list.append(o)
                
        for o in kill_list:
            self.remove(o)

        # Reset any disabled buttons if valid to do so
        if not self.player.is_attacking():
            for btn in self.foreground.buttons:
                btn.enable()

        self.crosshair_on_enemy()

        self.select_button()
        self.try_fire()

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
                
    def crosshair_on_enemy(self):
        # TODO: find points in some bounding box of the enemy
        crosshair = self.player.leftHand.get_pos()
        del_x = crosshair[0] - Window.width/2
        del_y = crosshair[1]
        A = (Window.width/2, -10000) # 
        B = (Window.width/2 + 3*del_x, 3*del_y)

        self.target = None
        sorted_enemies = sorted(self.enemies.enemies, key = lambda x: x.cbrect.pos[1])
        
        for e in sorted_enemies:
            x = e.cbrect.pos[0]
            y = e.cbrect.pos[1]
            w = e.cbrect.size[0]
            h = e.cbrect.size[1]

            pts = [(x,y),(x+w,y),(x+w,y+h),(x,y+h),(x,y)]
            cont = False

            for i in xrange(3):
                C = pts[i]
                D = pts[i+1]

                if self.intersect(A,B,C,D):
                    e.lit()
                    e.on_target()
                    e.set_is_targeted(True)
                    self.target = e
                    cont = True
                    break
            if cont:
                break

        for e in sorted_enemies:
            if e != self.target:
                e.un_lit()
                e.set_is_targeted(False)

    def select_button(self):
        if self.player.is_attacking():
            return

        flame = self.get_flame()
        if flame == None:
            return

        flameX = flame.emitter_x
        flameY = flame.emitter_y

        for btn in self.foreground.buttons:
            if not btn.is_enabled:
                continue

            x1, y1, x2, y2 = btn.get_boundaries()

            if x1 <= flameX and flameX <= x2 and y1 <= flameY and flameY <= y2:
                self.player.arm_weapon(btn)
                active_button = btn
                return


    def try_fire(self):
        if self.player.is_attacking() and self.target:
            flame = self.get_flame()
            active_button = self.player.get_button()
            
            if not active_button:
                return

            note = active_button.get_note()
            self.target.on_hit(note.get_pitch())
            active_button.disable()
            self.player.unarm_weapon()

    def ccw(self, A,B,C):
        return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

    # Return true if line segments AB and CD intersect
    def intersect(self, A,B,C,D):
        return self.ccw(A,C,D) != self.ccw(B,C,D) and self.ccw(A,B,C) != self.ccw(A,B,D)


    def add_enemies(self, time):
        remove_list = []
        for e in self.enemy_data:
            if e[0] <= time:
                E = Enemy(e[1], audio_callback=self.play_enemy_sound, hurt_player_callback=self.player.decrement_health, dmg_rect_on_hit_callback=self.dmg_rect.on_hit)
                self.enemies.add(E)
                remove_list.append(e)
                
        for r in remove_list:
            self.enemy_data.remove(r)

    def play_enemy_sound(self, pitches):
        for pitch in pitches:
            self.audio_controller.play_sfx(pitch)

    def get_flame(self):
        return self.player.get_flame()

    def add(self, obj):
        super(Handler, self).add(obj)
        self.objects.append(obj)
        
    def remove(self, obj):
        super(Handler, self).remove(obj)
        self.objects.remove(obj)