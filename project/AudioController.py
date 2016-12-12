import sys
sys.path.append('..')
from common.core import *
from common.audio import *
from common.clock import *
from common.synth import *
from common.metro import *
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


class NoteSequencer(object):
    def __init__(self, sched, synth, channel, patch):
        super(NoteSequencer, self).__init__()

        # output parameters
        self.sched = sched
        self.synth = synth
        self.channel = channel
        self.patch = patch

        # note sequencer parameters:
        self.note_grid = kTicksPerQuarter / 4
        self.note_len_ratio = 0.90
        self.notes = []

        # run-time variables
        self.cur_idx = 0
        self.idx_inc = 1
        self.on_cmd = None
        self.off_cmd = None
        self.playing = False
        self.looping = False

    def set_notes(self, notes, loop):
        self.notes = notes
        self.looping = loop

    def get_channel(self):
        return self.channel

    def set_note_len_ratio(self, nlr):
        self.note_len_ratio = nlr

    def start(self):
        if not self.playing:
            self.cur_idx = 0
            self.playing = True

            self.synth.program(self.channel, self.patch[0], self.patch[1])
            now = self.sched.get_tick()
            next_tick = now - (now % kTicksPerQuarter/16) + kTicksPerQuarter/16
            self.on_cmd  = self.sched.post_at_tick(next_tick, self._noteon, None)

    def stop(self):
        if self.playing:
            self.cur_idx = 0
            self.playing = False

            self.sched.remove(self.on_cmd)
            self.sched.remove(self.off_cmd)
            if self.off_cmd:
                self.off_cmd.execute()

            # reset these so we don't have a reference to old commands.
            self.on_cmd = None
            self.off_cmd = None

    # find the pitch we should play based on the notes, the current note index
    def _get_next_note(self):
        note = self.notes[self.cur_idx]

        notes_len = len(self.notes)

        # advance index
        self.cur_idx += self.idx_inc

        if not self.looping:
            if self.cur_idx >= notes_len:
                self.stop()
                return (None,None)

        # keep in bounds if looping
        self.cur_idx = self.cur_idx % notes_len

        return note

    def _noteon(self, tick, ignore):
        (duration, pitches) = self._get_next_note()

        if duration:
            # play note on:
            velocity = 100
            for pitch in pitches:
                self.synth.noteon(self.channel, pitch, velocity)

            # post the note-off at the appropriate tick:
            off_tick = tick + duration * self.note_len_ratio
            for pitch in pitches:
                self.off_cmd = self.sched.post_at_tick(off_tick, self._noteoff, pitch)

            # post next note. quantize tick to line up with grid of current note length
            tick -= tick % self.note_grid
            next_tick = tick + duration
            self.on_cmd  = self.sched.post_at_tick(next_tick, self._noteon, None)

    def _noteoff(self, tick, pitch):
        self.synth.noteoff(self.channel, pitch)


class AudioController(object):
    def __init__(self):
        super(AudioController, self).__init__()
        self.audio = Audio(2)
        self.mixer = Mixer()
        self.audio.set_generator(self.mixer)

        song_path = "../data/Fuyu_no_Nazo_Tochi.wav"


        # Wav file for background music
        self.bg_track1 = WaveGenerator(WaveFile(song_path), True)
        self.mixer.add(self.bg_track1)

        # Scheduler (generator) for sequencing/arpeggiating
        self.tempo_map  = SimpleTempoMap(200)
        self.sched = AudioScheduler(self.tempo_map)
        self.mixer.add(self.sched)
        self.synth = Synth('../data/FluidR3_GM.sf2')
        self.sched.set_generator(self.synth)

        self.occupied_channels = []
        self.sequencers = []

    def add_enemy_sound(self, pitches):
        next_open_channel = 0
        while next_open_channel in self.occupied_channels:
            next_open_channel += 1
        print next_open_channel

        seq = NoteSequencer(self.sched, self.synth, channel = next_open_channel, patch = (0, 35))
        self.sequencers.append(seq)
        self.occupied_channels.append(next_open_channel)
        rhythm = ( (240*2,pitches), (480*2,[0]), (240*2,pitches), (240*2*4,[0]) )
        seq.set_notes(rhythm, True)
        seq.start()

        return seq

    def remove_enemy_sound(self, seq):
        if seq in self.sequencers:
            self.sequencers.remove(seq)
            seq.stop()
        if seq.get_channel() in self.occupied_channels:
            self.occupied_channels.remove(seq.get_channel())
        del seq

    # start / stop the song
    def toggle(self):
        for g in self.mixer.generators:
            g.play_toggle()

    # mute / unmute the solo track
    def set_mute(self, mute):
        pass

    # play a sound-fx (miss sound)
    def play_sfx(self, pitch):
        # play midi pitch
        self.mixer.add(NoteGenerator(pitch, 0.2, 0.2, harmonics = ((1., 1/2., 1/3., 1/4., 1/5., 1/6., 1/7., 1/8., 1/9.))))

    # needed to update audio
    def on_update(self):
        self.audio.on_update()


