import sys
sys.path.append('..')
from common.core import *
from common.gfxutil import *
from common.audio import *
from common.mixer import *
from common.note import *
from common.wavegen import *
from common.wavesrc import *

from common.kivyparticle import ParticleSystem

from kivy.core.window import Window
from kivy.clock import Clock as kivyClock
from kivy.uix.label import Label
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.graphics import PushMatrix, PopMatrix, Translate, Scale, Rotate

from leap.LeapHelper import *

from random import random, randint, choice
import numpy as np


# part 1
class MainWidget(BaseWidget) :
    c_major_pitches = [72, 74, 76, 77, 79, 81, 83, 84]
    num_octaves = 3
    
    hsv_luminosity_factor = .3
    # hsv values in roy g biv in reverse order. last value refers to red for next octave
    roygbiv_hsv = [(0, 1, .41), (18./360, 1, .567), (50./360, 1, .565), (106./360, 1, .433), \
                    (229./360, .846, .433), (260./360, 1, .2), (285./360, 1, .133), (285./360, 1, .1)]
    # reverse standard roygbiv
    roygbiv_hsv = roygbiv_hsv[::-1]
    
    def __init__(self):
        super(MainWidget, self).__init__()
        self.info = topleft_label()
        self.add_widget(self.info)

        self.objects = AnimGroup()
        self.canvas.add(self.objects)
        
        # Audio framework init
        self.audio = Audio(2)
        self.note_duration = 1.0
        self.duration_step = 0.2
        
        # global mixer for all objects within the scope of this widget
        self.mixer = Mixer()
        self.audio.set_generator(self.mixer)
        
        self.leftHandBubble = HandBubble((20, 20), 20, Color(1, 0, 0))
        self.rightHandBubble = HandBubble((20, 20), 20, Color(1, 1, 0))
        self.centerMarker = HandBubble((Window.width / 2, Window.height / 2), 30, Color(0, 0, 1))
        self.objects.add(self.leftHandBubble); self.objects.add(self.rightHandBubble); self.objects.add(self.centerMarker)
        
        # Mock flames
        h = Window.height / 8
        w = Window.width / 12
        self.flame1 = Flame((2*w, h), 25, Color(1, .65, 0))
        self.flame2 = Flame((6*w, h), 25, Color(1, .65, 0))
        self.flame3 = Flame((10*w, h), 25, Color(1, .65, 0))
        self.objects.add(self.flame1); self.objects.add(self.flame2); self.objects.add(self.flame3)
        
        self.flames = [self.flame1, self.flame2, self.flame3]
        
        self.timbre = "sine"
        self.timbre_map = {"sine": NoteGenerator.sine, "square": NoteGenerator.square, "sawtooth": NoteGenerator.saw, \
                            "triangle": NoteGenerator.tri, "steelpan": NoteGenerator.square}
                            
        self.segments = {"sine": 40, "square": 4, "sawtooth": 5, "triangle": 3, "steelpan": 10}
        
        self.leapController = Leap.Controller()
        self.leapController.set_policy(Leap.Controller.POLICY_IMAGES) # allow access to images
        
    def on_touch_down(self, touch) :
        # init Bubble settings
        pos = touch.pos
        
        # generate note and color
        (noteGen, color) = self.make_note(*pos)
        
        radius = 20 * noteGen.duration
        
        self.mixer.add(noteGen)
        
        self.objects.add(Bubble(pos, radius, color, self.mixer, self.segments[self.timbre], self.note_duration))

    def on_update(self):
        self.objects.on_update()
        self.audio.on_update()

        self.info.text = str(Window.mouse_pos)
        self.info.text += '\nfps:%d' % kivyClock.get_fps()
        self.info.text += '\nobjects:%d' % len(self.objects.objects)
        
        self.info.text += "\nNote duration: %.1fs [Toggle with up/down]" % self.note_duration
        self.info.text += "\nTimbre: %s [Toggle with s]" % self.timbre
        
        if self.leapController.is_connected:
            frame = self.leapController.frame()
            self.handleFrame(frame)
        
    def handleFrame(self, frame):
        # Remove bubbles; re-add later if appropriate hand is present
        self.objects.remove(self.leftHandBubble)
        self.objects.remove(self.rightHandBubble)
        self.leftHandBubble.isDrawn = False
        self.rightHandBubble.isDrawn = False
        
        hands = frame.hands
        
        for hand in hands:
            handBubble = self.leftHandBubble if hand.is_left else self.rightHandBubble
            if not handBubble.isDrawn:
                self.objects.add(handBubble)
                handBubble.isDrawn = True
            handPos = self.move_hand(hand, handBubble)
            
            if handBubble.has_flame:
                if hand.grab_strength < .1:
                    handBubble.release_flame()
            else:
                for flame in self.flames:
                    if LeapHelper.point_is_hovered(hand, flame.get_pos()) and handBubble.handOpen and hand.grab_strength == 1.0:
                        # TODO: in actual code, make sure flames know original pos, track grab
                        handBubble.grab_flame(flame)
            
    
    def move_hand(self, hand, handBubble):
        pos = LeapHelper.position_as_pixels(hand)
        
        def checkBounds(x, y):
            return 0 <= x and x <= Window.width and 0 <= y and y <= Window.height
            
        if not checkBounds(*pos):
            handBubble.release_flame()
            self.objects.remove(handBubble)
            handBubble.isDrawn = True
        else:
            if hand.is_left:
                self.leftHandBubble.set_pos(pos)
            else:
                self.rightHandBubble.set_pos(pos)
        return pos
    
    def on_key_down(self, keycode, modifiers):
    
        if keycode[1] == 's':
            self.toggle_timbre()
        if keycode[1] == "up":
            self.note_duration += self.duration_step
        if keycode[1] == "down" and self.note_duration >= 2 * self.duration_step: # Mult. by two to account for floating point (im)precision
            self.note_duration -= self.duration_step
        
    def make_note(self, x, y):
    
        # Chosoe pitch based on horizontal position
        pitchIndex = int( (1.0 * x) / Window.width * 8 )
        
        # Choose octave based on vertical position. num_octaves octaves are supported
        center_y = Window.height / 2.0
        band_size = 1.0 * Window.height / self.num_octaves
        
        octave_delta = 0
        if self.num_octaves % 2 != 0 and y < center_y:
            octave_delta = int((y - (center_y + band_size / 2)) / band_size)
        elif self.num_octaves % 2 != 0 and y >= center_y:
            octave_delta = int((y - (center_y - band_size / 2)) / band_size)
        else:
            octave_delta = int((y - center_y) / band_size)
        pitch_delta = octave_delta * 12

        pitch = self.c_major_pitches[pitchIndex] + pitch_delta
        gain = 1.0
        duration = self.note_duration
        
        hsv_val = (self.roygbiv_hsv[pitchIndex][0], self.roygbiv_hsv[pitchIndex][1], \
                    self.roygbiv_hsv[pitchIndex][2] * self.hsv_luminosity_factor ** -octave_delta)
        
        color = Color(*hsv_val, mode="hsv")
        
        timbre = self.timbre_map[self.timbre]
        
        return (NoteGenerator(pitch, gain, duration, harmonics = timbre), color)
        
    def toggle_timbre(self):
        keys_list = sorted(self.timbre_map.keys())
        i = keys_list.index(self.timbre)
            
        i += 1
        if i >= len(keys_list):
            i = 0
        self.timbre = keys_list[i]


class Bubble(InstructionGroup):
    def __init__(self, pos, r, color, mixer, segments = 40, duration=1.5):
        super(Bubble, self).__init__()

        center_x = Window.width/2
        center_y = Window.height/2
        
        # Duration of the bubble animation and its corresponding note
        self.duration = duration
        
        # pointer to a global mixer object
        self.mixer = mixer

        self.color = color
        self.add(self.color)
    
        self.shape = CEllipse(cpos = pos, size = (2*r, 2*r), segments = segments)
        self.add(self.shape)

        self.radius_anim = KFAnim((0, r), (.1, 2*r), (self.duration, 0))
        self.pos_anim = KFAnim((0, pos[0], pos[1]), (self.duration, pos[0], Window.height + r))

        self.time = 0
        self.on_update(0)

    def on_update(self, dt):
        # animate radius
        rad = self.radius_anim.eval(self.time)
        self.shape.csize = (2*rad, 2*rad)

        # animate position
        pos = self.pos_anim.eval(self.time)
        self.shape.cpos = pos

        # advance time
        self.time += dt
        # continue flag
        return self.radius_anim.is_active(self.time)
        
class HandBubble(InstructionGroup):
    def __init__(self, pos, r, color, segments = 40, duration=1.5):
        super(HandBubble, self).__init__()

        center_x = Window.width/2
        center_y = Window.height/2
        
        self.isDrawn = True # Is it currently visible on the canvas?
        
        self.pos = pos
        
        self.has_flame = False
        self.grabbed_flame = None
        self.handOpen = True
        
        # Duration of the bubble animation and its corresponding note
        self.duration = duration
        
        self.color = color
        self.add(self.color)
    
        self.shape = CEllipse(cpos = pos, size = (2*r, 2*r), segments = segments)
        self.add(self.shape)

        self.time = 0
        self.on_update(0)

    def on_update(self, dt):
        pass
        
    def set_pos(self, pos):
        self.pos = pos
        self.shape.set_cpos(pos)
        
        if self.has_flame:
            self.move_flame()
        
    def get_pos(self):
        return self.pos
        
    def move_flame(self):
        if self.has_flame:
            self.grabbed_flame.set_pos(self.pos)
            
    def grab_flame(self, flame):
        if not self.has_flame:
            self.grabbed_flame = flame
            self.has_flame = True
            self.grabbed_flame.set_pos(self.pos)
            self.handOpen = False
            
    def release_flame(self):
        if self.has_flame:
            self.grabbed_flame.reset_pos()
            self.has_flame = False
            self.grabbed_flame = None
            self.handOpen = True
        
class Flame(InstructionGroup):
    def __init__(self, pos, r, color, segments = 40, duration=1.5):
        super(Flame, self).__init__()

        center_x = Window.width/2
        center_y = Window.height/2
        
        self.pos = pos
        self.original_pos = pos
        
        # Duration of the bubble animation and its corresponding note
        self.duration = duration
        
        self.color = color
        self.add(self.color)
    
        self.shape = CEllipse(cpos = pos, size = (2*r, 2*r), segments = segments)
        self.add(self.shape)

        self.time = 0
        self.on_update(0)

    def on_update(self, dt):
        pass
        
    def set_pos(self, pos):
        self.pos = pos
        self.shape.set_cpos(pos)
        
    def reset_pos(self):
        self.pos = self.original_pos
        self.shape.set_cpos(self.pos)
        
    def get_pos(self):
        return self.pos
        
run(eval('MainWidget'))