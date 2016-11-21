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

Config.set('input', 'leapfinger', 'leapfinger')

# part 1
class MainWidget(BaseWidget) :
    def __init__(self):
        super(MainWidget, self).__init__()
        ar = np.array([69,71,73,76,80])
        am = np.array([69,71,72,76,79])
        aa = np.array([69,71,72,77,79])

        self.arpeggios = np.concatenate((ar-24,ar-12,ar,ar+12,ar+24), axis=0)
        self.arpeggios_m = np.concatenate((am-24,am-12,am,am+12,am+24), axis=0)
        self.arpeggios_a = np.concatenate((aa-24,aa-12,aa,aa+12,aa+24), axis=0)

        self.arpeggio = 'major'

        self.MIN_SIZE = 0.5
        self.MAX_SIZE = 40.0

        self.W = Window.width
        self.H = Window.height

        self.timbre = 'sine'
        self.duration = 2.0
        self.gain = 0.1
        self.gain_multi = 1.3

        self.spawn_buf = 0
        self.spawn_delay = 8

        #Setup Graphics
        self.objects = AnimGroup()
        self.canvas.add(self.objects)

        self.info = topleft_label()
        self.add_widget(self.info)

        #Setup Audio
        self.writer = AudioWriter('data') # for debugging audio output
        self.audio = Audio(2, self.writer.add_audio)

        self.mixer = Mixer()
        self.audio.set_generator(self.mixer)

    def on_touch_move(self, touch):
        if ('pos' in touch.profile) or ('pos3d' in touch.profile):
            print "yeaaaa"
        if touch.grab_current is self:
            print "yeaaaa"

        print touch
        if self.spawn_buf <= 0:
            self.make_bubble(touch)
            self.spawn_buf += self.spawn_delay
        else:
            self.spawn_buf -= 1

    def on_touch_down(self, touch):
        if touch.grab_current is self:
            print "yeaaaa"
        if ('pos' in touch.profile) or ('pos3d' in touch.profile):
            print "yeaaaa"

        print touch
        self.make_bubble(touch)
        self.spawn_buf = self.spawn_delay

    def on_touch_up(self, touch):
        pass

    def make_bubble(self, touch):
        # initial settings for:
        #graphics
        p = touch.pos
        r = self.gain_to_radius()
        #r = randint(self.MIN_SIZE,self.MAX_SIZE)
        #c = (random(), random(), random())
        d = self.duration
        t = self.timbre_to_segments()
        bubble = Bubble(p,r,d,t)
        self.objects.add(bubble)
        #audio
        p = self.pos_to_pitch(touch.pos[1])
        #p = 69+np.ceil(10*random()-5)
        g = self.gain
        d = bubble.get_duration()
        h = self.timbre
        self.mixer.add(NoteGenerator(p, g, d, h))

    def pos_to_pitch(self, pos_y):
        if self.arpeggio == 'major':
            arpeggios = self.arpeggios
            l = 5
        elif self.arpeggio == 'minor':
            arpeggios = self.arpeggios_m
            l = 5
        elif self.arpeggio == 'augment':
            arpeggios = self.arpeggios_a
            l = 5

        n = round(self.remap(pos_y, -50.0, Window.height+50, l/2, len(arpeggios)-(l/2)-1))
        n = int(n)
        pitches = arpeggios[n-(l/2):n+(l/2)+1]
        assert(len(pitches) == l)
        return choice(pitches)

    def remap(self, x , in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def gain_to_radius(self):
        M = self.MIN_SIZE/2 + self.MAX_SIZE/2 #median desired radius
        G = 0.1 #starting gain value
        Gi = self.gain_multi #gain multiplicative increment value
        a = (self.MAX_SIZE - M)/(G*(Gi**5 - 1)) #solving set of eqns
        b = M - G*a #solving set of eqns
        return self.gain*a + b

    def timbre_to_segments(self):
        timbre = lookup(self.timbre, ('sine','square','saw','tri'), (40,4,6,3))
        return timbre

    def on_update(self):
        self.objects.on_update()
        self.audio.on_update()

        self.info.text = str(Window.mouse_pos)
        self.info.text += '\nfps:   %d' % kivyClock.get_fps()
        self.info.text += '\nobjects:   %d' % len(self.objects.objects)
        self.info.text += '\ngens:   %d' % self.mixer.get_num_generators()
        self.info.text += '\nduration [1,2,3,4,5]:   %.2f' % self.duration
        self.info.text += '\ngain [a,s]:   %.4f' % self.gain
        self.info.text += '\nmax_size [g,h]:   %.2f' % self.MAX_SIZE
        self.info.text += '\nshape [z,x,c,v]:   '
        self.info.text += self.timbre
        self.info.text += '\ndelay [left,right]:   %.2f' % self.spawn_delay
        self.info.text += '\nquality [q,w,e]:   '
        self.info.text += self.arpeggio

    def on_key_down(self, keycode, modifiers):
        print 'keydown', keycode, modifiers

        dur = lookup(keycode[1], ('1','2','3','4','5'), (0.25,0.5,1.0,2.0,4.0))
        if dur:
            self.duration = dur

        gain = lookup(keycode[1], ('s','a'), (self.gain_multi, 1/self.gain_multi))
        if gain:
            self.gain *= gain

        size = lookup(keycode[1], ('h','g'), (1.5, 1/1.5))
        if size:
            self.MAX_SIZE *= size

        timbre = lookup(keycode[1], ('z','x','c','v'), ('sine','square','saw','tri'))
        if timbre:
            self.timbre = timbre

        arpeggio = lookup(keycode[1], ('q','w','e'), ('major','minor','augment'))
        if arpeggio:
            self.arpeggio = arpeggio

        delay = lookup(keycode[1], ('left','right'), (0.5,2.0))
        if delay:
            self.spawn_delay *= delay


    def on_key_up(self, keycode):
        print 'keyup', keycode


class Bubble(InstructionGroup):
    def __init__(self, pos, r, duration, timbre):
        super(Bubble, self).__init__()

        center_x = Window.width/2
        center_y = Window.height/2

        self.endtime = duration

        self.radius_anim = KFAnim((0, r), (.1, 2*r), (self.endtime, 0))
        self.pos_anim    = KFAnim((0, pos[0], pos[1]), (self.endtime, center_x, center_y))

        color = [pos[0]/Window.width, 1,1]
        self.color = Color(hsv=(color[0],color[1],color[2]))
        self.add(self.color)

        self.circle = CEllipse(cpos = pos, size = (2*r, 2*r), segments = timbre)
        self.add(self.circle)

        self.time = 0
        self.on_update(0)

    def on_update(self, dt):
        # animate radius
        rad = self.radius_anim.eval(self.time)
        self.circle.csize = (2*rad, 2*rad)

        # animate position
        pos = self.pos_anim.eval(self.time)
        self.circle.cpos = pos

        # advance time
        self.time += dt
        # continue flag
        return self.radius_anim.is_active(self.time)

    def get_duration(self):
        return self.endtime

run(MainWidget)
