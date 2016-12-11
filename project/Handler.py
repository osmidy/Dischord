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


class Handler(InstructionGroup):
    def __init__(self):
        super(Handler, self).__init__()
        
        self.audio_controller = AudioController()

        self.time = 0.0
        self.enemy_data = data

        # List of all objects in the game to be drawn
        self.objects = []

        # References to game elements interacted with
        self.target = None
        self.active_button = None

        self.enemies = E_List()
        self.background = Background()
        self.foreground = Foreground()
        self.player = Player()

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

        # Reset any disabled buttons if valid to do so
        if self.active_button and not self.active_button.is_enabled and not self.player.is_attacking():
            self.active_button.enable()

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
        A = (Window.width/2, -200)
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
                flame.arm_weapon(btn)
                self.active_button = btn
                return


    def try_fire(self):
        if self.player.is_attacking() and self.target:
            flame = self.get_flame()
            self.active_button = flame.get_button()
            
            if not active_button:
                return

            note = active_button.get_note()
            self.target.on_hit(note.get_pitch())
            self.active_button.disable()
            flame.unarm_weapon()

    def ccw(self, A,B,C):
        return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

    # Return true if line segments AB and CD intersect
    def intersect(self, A,B,C,D):
        return self.ccw(A,C,D) != self.ccw(B,C,D) and self.ccw(A,B,C) != self.ccw(A,B,D)


    def add_enemies(self, time):
        remove_list = []
        for e in self.enemy_data:
            if e[0] <= time:
                E = Enemy(e[1], audio_callback = self.play_enemy_sound, hurt_player_callback = self.player.decrement_health)
                self.enemies.add(E)
                #self.add(E)
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