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

from random import random, randint, choice
import numpy as np

import math


class Enemy(InstructionGroup):
    def __init__(self, time, spawn_pos, speed):
        super(Enemy, self).__init__()

        # spawn pos is a 3d coord tuple in cylindrical coords: r,theta,z
        self.pos3D = spawn_pos
        self.pos2D = self.transform()
        self.speed = speed

        self.size = 20

        self.body_color = Color(1,0,0)
        self.add(self.body_color)
        self.body = CRectangle(pos=self.pos2D, size=(self.size, self.size))
        self.add(self.body)

        
    def on_update(self, dt):
        r = self.pos3D[0]
        if r>=0:
            self.pos3D = [r-self.speed, self.pos3D[1], self.pos3D[2]]
            self.pos2D = self.transform()
            
            self.body.set_cpos(self.pos2D)
            self.body.set_csize((self.size,self.size))
        # enemy should move closer in r direction, then call trans funct to get pos2D
        
    # transform 3D cyl coord to screen pos
    def transform(self):
        r = self.pos3D[0]
        theta = self.pos3D[1]
        z = self.pos3D[2]
        r_min = 1.0
        r_max = 45.0
        y_min = 200
        y_max = 300
        theta_min = -math.pi/4
        theta_max = math.pi/4
        x = (-theta*200.0)*r/r_max + Window.width/2
        y = self.map(r, r_min, r_max, y_min, y_max) - theta*(r-r_min)/2
        self.size = self.map(r, r_min, r_max, 200, 20)
        return ( x, y)


    def map(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

