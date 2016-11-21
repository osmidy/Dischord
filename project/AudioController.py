import sys
sys.path.append('..')
from common.core import *
from common.audio import *
from common.mixer import *
from common.wavegen import *
from common.wavesrc import *
from common.gfxutil import *
from common.kivyparticle import ParticleSystem

from common.note import *

from kivy.uix.label import Label
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.graphics import PushMatrix, PopMatrix, Translate, Scale, Rotate
from kivy.clock import Clock as kivyClock

import re
import random
import numpy as np
import bisect


class AudioController(object):
    def __init__(self):
        super(AudioController, self).__init__()
        self.audio = Audio(2)
        self.mixer = Mixer()
        self.audio.set_generator(self.mixer)


    # start / stop the song
    def toggle(self):
        pass

    # mute / unmute the solo track
    def set_mute(self, mute):
        pass

    # play a sound-fx (miss sound)
    def play_sfx(self, note):
        # play note
        self.mixer.add(NoteGenerator(note, 0.2, 0.2, harmonics = ((1., 1/2., 1/3., 1/4., 1/5., 1/6., 1/7., 1/8., 1/9.))))

    # needed to update audio
    def on_update(self):
        self.audio.on_update()
