import random

'''
Class handling logic for storing and retrieving musical notes
and MIDI pitches
'''
class MusicHelper(object):

    wholeStep = 12

    # TODO: mechanism for supporting other keys; enharmonic notes
    noteToMidi = {'c': 60, 'd': 62, 'e': 64, 'f': 65, 'g': 67, 'a': 69, 'b': 71}

    majorChordToNotes = {"I": "ceg", "ii": "dfa", "iii": "egb", "IV": "fac", "V": "gbe", "VI": "ace", "vii": "bdf"}

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
            third += MusicHelper.wholeStep
        if fifth < root:
            fifth += MusicHelper.wholeStep

        return [root, third, fifth]

    '''
    Return a string of notes for a chord, where one note is not
    part of the actual chord. Returns the proper and dissonant chords,
    eachh as a list of the notes in the chord in order, and the
    index of the wrong note.
    '''
    @staticmethod
    def get_dissonant_chord(key, chord):
        # TODO: distinguish between major and minor keys
        properChord = list(MusicHelper.majorChordToNotes[chord])
        dissonantChord = list(properChord)

        pickedNote = random.choice(properChord)

        wrongNote = None
        while True:
            wrongNote = random.choice(MusicHelper.noteToMidi.keys())
            if wrongNote not in properChord:
                break

        noteIndex = properChord.index(pickedNote)
        dissonantChord[noteIndex] = wrongNote

        return properChord, dissonantChord, noteIndex

