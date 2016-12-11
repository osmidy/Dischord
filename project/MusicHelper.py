import random
from TonalFlowChart import *

'''
Represenation of musical notes/midi pitches
'''
class Note:
    def __init__(self, note_name, midi_pitch):
        self.note_name = note_name
        self.midi_pitch = midi_pitch

    def get_pitch(self):
        return self.midi_pitch

    def get_name(self):
        return self.note_name

'''
Enumeration of note types
'''
class Notes:
    C = Note("C", 60)
    B_SHARP = Note("B#", 60)
    
    C_SHARP = Note("C#", 61)
    D_FLAT = Note("Db", 61)
    
    D = Note("D", 62)

    D_SHARP = Note("D#", 63)
    E_FLAT = Note("Eb", 63)

    E = Note("E", 64)
    F_FLAT = Note("Fb", 64)

    F = Note("F", 65)
    E_SHARP = Note("E#", 65)

    F_SHARP = Note("F#", 66)
    G_FLAT = Note("Gb", 66)

    G = Note("G",  67)

    G_SHARP = Note("G#", 68)
    A_FLAT = Note("Ab", 68)

    A = Note("A", 69)

    A_SHARP = Note("A#", 70)
    B_FLAT = Note("Bb", 70)

    B = Note("B", 71)
    C_FLAT = Note("Cb", 71)

'''
Class handling logic for storing and retrieving musical notes
and MIDI pitches
'''
class MusicHelper(object):

    octave = 12

    # TODO: mechanism for supporting other keys; enharmonic notes
    noteToMidi = {'c': 60, 'd': 62, 'e': 64, 'f': 65, 'g': 67, 'a': 69, 'b': 71}

    # Given a certain chord type, the number of semitones its root is above the tonic
    tonicSemitoneDistance = {Chords.MAJOR_ONE: 0,\
                                Chords.MINOR_TWO: 2,\
                                Chords.MINOR_THREE: 4,\
                                Chords.MAJOR_FOUR: 5,\
                                Chords.MAJOR_FIVE: 7,\
                                Chords.MINOR_SIX: 9,\
                                Chords.DIMINISHED_SEVEN: 11,\

                                Chords.MINOR_ONE: 0,\
                                Chords.DIMINISHED_TWO: 2,\
                                Chords.MAJOR_THREE: 3,\
                                Chords.MINOR_FOUR : 5,\
                                Chords.MINOR_FIVE: 7,\
                                Chords.MAJOR_SIX : 8,\
                                Chords.MAJOR_SEVEN: 10}

    '''
    Builds the specified midi chord in the given key. Returns a list of the 
    three (or more) pitches
    '''
    @staticmethod
    def get_proper_chord(key, chord):
        pitch = key.get_pitch()

        rootDiff = MusicHelper.tonicSemitoneDistance[chord]
        root = pitch + rootDiff

        thirdDiff, fifthDiff = chord.get_chord_intervals()
        third = pitch + thirdDiff
        fifth = pitch + fifthDiff

        return [root, third, fifth]


    '''
    Returns a dissonant form of the given proper chord as a list of notes in the chord,
    and the index of the wrong note.
    '''
    @staticmethod
    def get_dissonant_chord(properChord):
        replacedNote = random.choice(properChord)

        wrongNote = None        
        choiceRange = xrange(replacedNote - 4, replacedNote + 4)
        
        while True:
            wrongNote = random.choice(choiceRange)
            if wrongNote not in properChord:
                break

        dissonantChord = list(properChord)
        noteIndex = properChord.index(replacedNote)
        dissonantChord[noteIndex] = wrongNote

        return dissonantChord, noteIndex
