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

    def __init__(self, key):
        self.key = key
        
        # Generate chord
        pitch = key.get_pitch() + random.choice(MusicHelper.scaleDegTonicDistance.values())

        diffRange = xrange(2, 4)

        abovePitch = pitch + random.choice(diffRange)
        belowPitch = pitch - random.choice(diffRange)

        self.pitches = [pitch, abovePitch, belowPitch]

        self.chord_type = Chord.get_chord_type(self.pitches)


    def get_chord_intervals(self):
        return Chord.chordIntervalSize[self.chord_type]

    def get_chord_name(self):
        return self.chord_name

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
# class TonalFlowChart:
#     MAJOR = "major_chord_tfc"
#     MINOR = "minor_chord_tfc"

#     '''
#     Note: since the one chord can go to anything, this is left out of the mappings.
#     We explicitly check for this case in the functions of the class.
#     '''
#     nextChordMapMajor = {Chords.MINOR_TWO: (Chords.MAJOR_FIVE, Chords.DIMINISHED_SEVEN),\
#                          Chords.MINOR_THREE: (Chords.MINOR_SIX, Chords.MAJOR_FOUR),\
#                          Chords.MAJOR_FOUR: (Chords.MAJOR_ONE, Chords.MINOR_TWO, Chords.MAJOR_FIVE),\
#                          Chords.MAJOR_FIVE: (Chords.MAJOR_ONE, Chords.DIMINISHED_SEVEN, Chords.MINOR_SIX),\
#                          Chords.MINOR_SIX: (Chords.MAJOR_FOUR, Chords.MINOR_TWO),\
#                          Chords.DIMINISHED_SEVEN: (Chords.MAJOR_ONE)}

#     nextChordMapMinor = {Chords.MAJOR_SEVEN: (Chords.MAJOR_THREE),\
#                          Chords.MAJOR_THREE: (Chords.MAJOR_SIX, Chords.MINOR_FOUR),\
#                          Chords.MAJOR_SIX: (Chords.MINOR_FOUR, Chords.DIMINISHED_TWO),\
#                          Chords.MINOR_FOUR: (Chords.MINOR_ONE, Chords.DIMINISHED_TWO, Chords.MAJOR_FIVE),\
#                          Chords.DIMINISHED_TWO: (Chords.MAJOR_FIVE, Chords.DIMINISHED_SEVEN),\
#                          Chords.MAJOR_FIVE: (Chords.DIMINISHED_SEVEN, Chords.MAJOR_SIX, Chords.MINOR_ONE),\
#                          Chords.DIMINISHED_SEVEN: (Chords.MINOR_ONE)}

#     def __init__(self, chart_type = MAJOR):
#         self.chart_type = chart_type

#         if (chart_type == TonalFlowChart.MAJOR):
#             self.chartMap = TonalFlowChart.nextChordMapMajor
#         else:
#             self.chartMap = TonalFlowChart.nextChordMapMinor

#     def is_valid_progression(self, chord):
#         return chord == MAJOR_ONE or chord == MINOR_ONE  or chord in self.chartMap[chord]

#     def get_next_chords(self, chord):
#         chordIsOne = chord == Chords.MAJOR_ONE or chord == Chords.MINOR_ONE
        
#         if chordIsOne and self.chart_type == TonalFlowChart.MAJOR:
#             return [Chords.MINOR_TWO, Chords.MINOR_THREE, Chords.MAJOR_FOUR, Chords.MAJOR_FIVE, Chords.MINOR_SIX, Chords.DIMINISHED_SEVEN]
#         elif chordIsOne:
#             return [Chords.DIMINISHED_TWO, Chords.MAJOR_THREE, Chords.MINOR_FOUR, Chords.MINOR_FIVE, Chords.MAJOR_SIX, Chords.MAJOR_SEVEN]
#         else:
#             return self.chartMap[chord]

    # TODO: expand for mode mixture; check parallel chartMap