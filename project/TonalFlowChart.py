from MusicHelper import *
import random 

'''
Representation of a tonal chord
'''
class Chord:
    # Accepted chord types for init method
    majorChord = "major"
    minorChord = "minor"
    diminishedChord = "diminished"
    dissonantChord = "dissonantBruh"

    majorIntervals = (4, 7)
    minorIntervals = (3, 7)
    diminishedIntervals = (3, 6)

    scaleDegreeIntervals = (2, 4)

    # Number of semitones above root for third and fifth of the chord, respectively
    chordIntervalSize = {majorChord: majorIntervals, minorChord: minorIntervals, diminishedChord: diminishedIntervals}

    majorKeyRomanNumerals = {1: "I", 2: "ii", 3: "iii", 4: "IV", 5: "V", 6: "vi", 7: "vii*"}

    def __init__(self, key):
        self.key = key
        self.pitches = []

        pitchesInKey = sorted([x + key.get_pitch() for x in MusicHelper.scaleDegreeTonicDistance.values()])
        size = len(pitchesInKey)

        pitch = random.choice(pitchesInKey)

        idx = pitchesInKey.index(pitch)
        
        aboveNotes = [ pitchesInKey[(x % size)] for x in xrange(idx+1, idx +4) ]
        abovePitch = random.choice(aboveNotes)
        aboveIndex = aboveNotes.index(abovePitch)
        if abovePitch < pitch:
            abovePitch += MusicHelper.octave
        
        while True:
            belowNotes = [ pitchesInKey[(x % size)] for x in xrange(idx-1, idx-4, -1)]
            belowNotes.pop(aboveIndex)
            belowPitch = random.choice(belowNotes)

            if belowPitch >= pitch:
                belowPitch -= MusicHelper.octave
            
            self.pitches = [belowPitch, pitch, abovePitch]
            if Chord.is_valid_chord(self.key, self.pitches):
                continue

            if (abovePitch - pitch) != (pitch - belowPitch):
                break

        self.chord_type = Chord.get_chord_type(self.key, self.pitches)


    def get_chord_intervals(self):
        return Chord.chordIntervalSize[self.chord_type]

    @staticmethod
    def is_valid_chord(key, pitches):
        chord_type, root = Chord.get_chord_type(key, pitches)
        if chord_type == Chord.dissonantChord:
            return False

        return True

        # dist = root - key.get_pitch()
        # if dist in MusicHelper.tonicDistanceScaleDegreeMap:
        #     scaleDeg = MusicHelper.tonicDistanceScaleDegreeMap[dist]
        #     return True
        # else:
        #     return False

    @staticmethod
    def get_roman_numeral(key, pitch):
        scaleDeg = MusicHelper.get_scale_degree(key)
        return Chord.majorKeyRomanNumerals[key]


    @staticmethod
    def get_chord_type(key, pitches):

        chordType = Chord.dissonantChord
        root = None
        size = len(pitches)

        numDegrees = 7

        scaleDeg = sorted([MusicHelper.get_scale_degree(key, x % 12) for x in pitches])

        for i in xrange(size):
            firstDeg = scaleDeg[i]
            a = scaleDeg[(i + 1) % size]
            b = scaleDeg[(i + 2) % size]

            if a < firstDeg:
                a += numDegrees
            if b < firstDeg:
                b += numDegrees

            thirdDeg = None
            fifthDeg = None
            if a < b:
                thirdDeg = a
                fifthDeg = b
            else:
                thirdDeg = b
                fifthDeg = a

            intervals = (thirdDeg - firstDeg, fifthDeg - firstDeg)

            if intervals == Chord.scaleDegreeIntervals:
                chordType = Chord.majorChord # Incorrect, but not used if not dissonant
                root = firstDeg
                break

        return chordType, root

# '''
# Encapsulates the logic of to determine valid chord
# progressions in tonal music.
# '''
class TonalFlowChart:
    MAJOR = "major_chord_tfc"
    MINOR = "minor_chord_tfc"

    SCALE_DEG_ONE = 1

    '''
    Note: since the one chord can go to anything, this is left out of the mappings.
    We explicitly check for this case in the functions of the class.
    '''
    nextChordMapMajor = {2: (5, 7),\
                         3: (6, 7),\
                         4: (1, 2, 5),\
                         5: (1, 7, 6),\
                         6: (4, 2),\
                         7: (1)}

    # nextChordMapMinor = {Chords.MAJOR_SEVEN: (Chords.MAJOR_THREE),\
    #                      Chords.MAJOR_THREE: (Chords.MAJOR_SIX, Chords.MINOR_FOUR),\
    #                      Chords.MAJOR_SIX: (Chords.MINOR_FOUR, Chords.DIMINISHED_TWO),\
    #                      Chords.MINOR_FOUR: (Chords.MINOR_ONE, Chords.DIMINISHED_TWO, Chords.MAJOR_FIVE),\
    #                      Chords.DIMINISHED_TWO: (Chords.MAJOR_FIVE, Chords.DIMINISHED_SEVEN),\
    #                      Chords.MAJOR_FIVE: (Chords.DIMINISHED_SEVEN, Chords.MAJOR_SIX, Chords.MINOR_ONE),\
    #                      Chords.DIMINISHED_SEVEN: (Chords.MINOR_ONE)}

    def __init__(self, chart_type = MAJOR):
        self.chart_type = chart_type

        if (chart_type == TonalFlowChart.MAJOR):
            self.chartMap = TonalFlowChart.nextChordMapMajor
        else:
            self.chartMap = TonalFlowChart.nextChordMapMinor

    def is_valid_progression(self, scale_degree):
        return chord == TonalFlowChart.SCALE_DEG_ONE  or scale_degree in self.chartMap[chord]

    def get_next_chords(self, scale_degree):
        chordIsOne = chord == TonalFlowChart.SCALE_DEG_ONE
        
        if chordIsOne and self.chart_type == TonalFlowChart.MAJOR:
            return xrange(2, 8)
        else:
            return self.chartMap[chord]

    # TODO: expand for mode mixture; check parallel chartMap