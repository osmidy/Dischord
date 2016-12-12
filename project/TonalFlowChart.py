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
    minorIntervals = (3, 4)
    diminishedIntervals = (3, 3)

    # Number of semitones above root for third and fifth of the chord, respectively
    chordIntervalSize = {majorChord: majorIntervals, minorChord: minorIntervals, diminishedChord: diminishedIntervals}

    majorKeyRomanNumerals = {1: "I", 2: "ii", 3: "iii", 4: "IV", 5: "V", 6: "vi", 7: "vii*"}

    def __init__(self, key):
        self.key = key
        
        # Generate chord
        tonicDist = random.choice(MusicHelper.scaleDegreeTonicDistance.values())
        pitch = key.get_pitch() + tonicDist

        abovePitch = pitch + random.choice(MusicHelper.scaleDegreeTonicDistance.values())
        belowPitch = pitch - random.choice(MusicHelper.scaleDegreeTonicDistance.values())

        # Ensure we can actually resolve with one shot - avoid two major seconds or perfect fourths both above and below pitch
        aboveDiff = abovePitch - pitch
        belowDiff = pitch - belowPitch
        while (aboveDiff == 2 and belowDiff == 2) or (aboveDiff == 5 and belowDiff == 5):
            abovePitch = pitch + random.choice(MusicHelper.scaleDegreeTonicDistance.values())
            belowPitch = pitch - random.choice(MusicHelper.scaleDegreeTonicDistance.values())

            aboveDiff = abovePitch - pitch
            belowDiff = pitch - belowPitch

        self.pitches = [pitch, abovePitch, belowPitch]

        self.chord_type = Chord.get_chord_type(self.pitches)


    def get_chord_intervals(self):
        return Chord.chordIntervalSize[self.chord_type]

    @staticmethod
    def is_valid_chord(key, pitches):
        chord_type, root = Chord.get_chord_type(pitches)
        if chord_type == Chord.dissonantChord:
            return False

        dist = root - key
        if dist in MusicHelper.tonicDistanceScaleDegreeMap:
            scaleDeg = MusicHelper.tonicDistanceScaleDegreeMap[dist]
            return True

    @staticmethod
    def get_roman_numeral(key, pitch):
        scaleDeg = MusicHelper.get_scale_degree(key)
        return Chord.majorKeyRomanNumerals[key]


    @staticmethod
    def get_chord_type(pitches):

        chordType = Chord.dissonantChord
        root = None

        for pitch in pitches:
            root = pitch

            copy = list(pitches)
            copy.remove(pitch)
            third, fifth = copy

            if third <= pitch:
                third += MusicHelper.octave
            if fifth <= pitch:
                fifth += MusicHelper.octave

            intervals = (third - pitch, fifth - pitch)

            if (intervals == Chord.majorIntervals):
                chord = Chord.majorChord
                root = pitch
            elif (intervals == Chord.minorIntervals):
                chord = Chord.minorChord
                root = pitch
            elif (intervals == Chord.diminishedIntervals):
                chord = Chord.diminishedChord
                root = pitch

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