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
from kivy.uix.image import Image
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Rectangle, Bezier
from kivy.graphics import PushMatrix, PopMatrix, Translate, Scale, Rotate
from kivy.graphics.texture import Texture
from kivy.config import Config

from MusicHelper import Note, Notes

from random import random, randint, choice
import numpy as np


class Wall(InstructionGroup):
	def __init__(self):
		super(Wall, self).__init__()

		self.texture = Image(source='../data/stonewall2_edited.png').texture
		self.rect = Rectangle( texture=self.texture, pos=(0,0), size=(Window.width,Window.height*0.2) )
		self.add(Color(0.2,0.15,0.15))
		self.add(self.rect)

	def on_update(self, dt):
		pass

class Button(InstructionGroup):
    def __init__(self, y, h, color, note = Notes.B):
        super(Button, self).__init__()

        self.color = color

        # Set alpha
        alpha_lvl = 0.5
        self.enabled_color = Color(rgba=(color.rgb[0], color.rgb[1], color.rgb[2], alpha_lvl))
        self.disabled_color = Color(rgba=(0.5, 0.5, 0.5, alpha_lvl))

        self.add(self.color)

        self.crrect = CRRectangle( crpos=(Window.width, y), crsize=(50, h) )
        self.add(self.crrect)

        self.note = note
        self.is_enabled = True

        self.note_texture = self.get_note_texture(note)
        self.text_crrect = CRRectangle( texture=self.note_texture, crpos=(Window.width, y), crsize=(50, 50) )
        self.add(Color(1,1,1))
        self.add(self.text_crrect)

    def get_boundaries(self):
        lowerX, lowerY = self.crrect.pos
        upperX = lowerX + self.crrect.get_crsize()[0]
        upperY = lowerY + self.crrect.get_crsize()[1]

        return lowerX, lowerY, upperX, upperY

    def get_note(self):
        return self.note

    def get_note_texture(self, note):
        name = note.get_name()
        return Image(source='../data/'+name+'.png').texture

    def enable(self):
        self.is_enabled = True
        n = self.enabled_color.rgba
        self.color.rgba = (n[0],n[1],n[2],n[3])
        # TODO: get new note, make note text visible

    def disable(self):
        self.is_enabled = False
        n = self.disabled_color.rgba
        self.color.rgba = (n[0],n[1],n[2],n[3])
        # TODO: make note text invisible, set note to None

    def on_update(self, dt):
        pass


class Foreground(InstructionGroup):
    def __init__(self, key):
        super(Foreground, self).__init__()

        w = Window.width
        h = Window.height

        # Draw Wall
        self.wall = Wall()
        self.add(self.wall)

        # key of game
        self.key = key

        # Draw Buttons
        self.buttons = []
        num_buttons = 4
        height = Window.height*0.6
        h = height/num_buttons

        button_y_positions = np.linspace(Window.height-height -  h/2, Window.height-h/2  , num_buttons)

        # rygb from top to bottom (so, ordered bgyr here)
        colors = [(.22, .22, 1.), (.22, 1., .22), (1., 1., .22), (1., .22, .22)]

        for i in xrange(num_buttons):
            notes = Note.get_notes_in_key(self.key)
            note = choice(notes)
            b = Button(button_y_positions[i], h-5, Color(*colors[i]), note=note)
            self.buttons.append(b)
            self.add(b)

    def on_update(self, dt):
        # As of now, should never be removed
        return True
