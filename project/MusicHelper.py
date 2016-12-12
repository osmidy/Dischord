import random

'''
Class handling logic for storing and retrieving musical notes
and MIDI pitches
'''
class MusicHelper(object):

    octave = 12

    scaleDegTonicDistance = {1: 0,\
                                2: 2,\
                                3: 4,\
                                4: 5,\
                                5: 7,\
                                6: 9,\
                                7: 11}

    tonicDistanceScaleDegreeMap = {0: 1,\
                                        2: 2,\
                                        4: 3,\
                                        5: 4,\
                                        7: 5,\
                                        9: 6,\
                                        11: 7}

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
    Get harmonically correct form of the Note for pitch in the given key
    '''
    @staticmethod
    def pitch_to_note(pitch, key):
        pitchToNoteSharp = {0: Notes.B_SHARP, 3: Notes.D_SHARP, 5: Notes.E_SHARP, 6: Notes.F_SHARP, 8: Notes.G_SHARP, 10: Notes.A_SHARP}
        pitchToNoteNatural = {0: Notes.C, 2: Notes.D, 4: Notes.E, 5: Notes.F, 7: Notes.G, 9: Notes.A, 11: Notes.B}
        pitchToNoteFlat = {1: Notes.D_FLAT, 3: Notes.E_FLAT, 4: Notes.F_FLAT, 6: Notes.G_FLAT, 8: Notes.A_FLAT, 10: Notes.B_FLAT, 11: Notes.C_FLAT}

        # See if key is sharp or flat
        isSharp = False
        if "#" in key.get_name():
            isSharp = True

        basePitch = pitch % 12
        if isSharp and basePitch in pitchToNoteSharp:
            return pitchToNoteSharp[basePitch]
        elif basePitch in pitchToNoteFlat:
            return pitchToNoteFlat[basePitch]
        else:
            return pitchToNoteNatural