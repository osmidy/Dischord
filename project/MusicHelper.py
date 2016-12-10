import random
from TonalFlowChart import *

'''
Represenation of musical notes/midi pitches
'''
class Note:
    C = 60
    B_SHARP = 60
    
    C_SHARP = 61
    D_FLAT = 61
    
    D = 62

    D_SHARP = 63
    D_FLAT = 63

    E = 64
    F_FLAT = 65

    F = 65
    E_SHARP = 65

    G = 67

    G_SHARP = 68
    A_FLAT = 68

    A = 69

    A_SHARP = 70
    B_FLAT = 70

    B = 71

'''
Class handling logic for storing and retrieving musical notes
and MIDI pitches
'''
class MusicHelper(object):

    octave = 12

    # TODO: mechanism for supporting other keys; enharmonic notes
    noteToMidi = {'c': 60, 'd': 62, 'e': 64, 'f': 65, 'g': 67, 'a': 69, 'b': 71}

    # Number of semitones above the tonic the root of a given chord is
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

    majorChordToNotes = {"I": "ceg", "ii": "dfa", "iii": "egb", "IV": "fac", "V": "gbd", "VI": "ace", "vii": "bdf"}

    # TODO: better chord resolution
    '''
    Builds a chord with the specified notes (dissonant or not)
    TODO: support inversions of chords and seven chords
    '''
    @staticmethod
    def build_midi_chord(notes):

        def get_midi_pitch(note):
            lowerCase = str.lower(note)
            return MusicHelper.noteToMidi[lowerCase]


        # TODO: only root chords supported for now
        root = get_midi_pitch(notes[0])
        third = get_midi_pitch(notes[1])
        fifth = get_midi_pitch(notes[2])

        if third < root:
            third += MusicHelper.octave
        if fifth < root:
            fifth += MusicHelper.octave

        return [root, third, fifth]

    '''
    Return a string of notes for a chord, where one note is not
    part of the actual chord. Returns the dissonant and proper chords,
    eachh as a list of the notes in the chord in order, and the
    index of the wrong note.
    '''
    @staticmethod
    def get_dissonant_chord(key, chord):
        # TODO: distinguish between major and minor keys
        properChord = list(MusicHelper.majorChordToNotes[chord])
        dissonantChord = list(properChord)

        pickedNote = random.choice(properChord)

        # wrongNote = None
        # while True:
        #     wrongNote = random.choice(MusicHelper.noteToMidi.keys())
        #     if wrongNote not in properChord:
        #         break

        # noteIndex = properChord.index(pickedNote)
        # dissonantChord[noteIndex] = wrongNote

        dissonantChord = ['g', 'c', 'd']
        noteIndex = 1

        return dissonantChord, properChord, noteIndex

