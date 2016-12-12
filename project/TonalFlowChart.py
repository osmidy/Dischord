'''
Representation of a tonal chord
'''
class Chord:
    # Accepted chord types for init method
    majorChord = "major"
    minorChord = "minor"
    diminishedChord = "diminished"

    # Number of semitones above root for third and fifth of the chord, respectively
    chordIntervalSize = {majorChord: (4, 7), minorChord: (3, 4), diminishedChord: (3, 6)}

    def __init__(self, chord_name, chord_type):
        self.chord_name = chord_name
        self.chord_type = chord_type

    def get_chord_intervals(self):
        return Chord.chordIntervalSize[self.chord_type]

    def get_chord_name(self):
        return self.chord_name

    def get_chord_type(self):
        return self.chord_type
'''
Enumeration of chord types
'''
class Chords:
    MAJOR_ONE = Chord("I", Chord.majorChord)
    MINOR_TWO = Chord("ii", Chord.minorChord)
    MINOR_THREE = Chord("iii", Chord.minorChord)
    MAJOR_FOUR = Chord("IV", Chord.majorChord)
    MAJOR_FIVE = Chord("V", Chord.majorChord)
    MINOR_SIX = Chord("vi", Chord.minorChord)
    DIMINISHED_SEVEN = Chord("vii*", Chord.diminishedChord)

    MINOR_ONE = Chord("i", Chord.minorChord)
    DIMINISHED_TWO = Chord("ii*", Chord.diminishedChord)
    MAJOR_THREE = Chord("III", Chord.majorChord)
    MINOR_FOUR = Chord("iv", Chord.minorChord)
    MINOR_FIVE = Chord("v", Chord.minorChord)
    MAJOR_SIX = Chord("VI", Chord.majorChord)
    MAJOR_SEVEN = Chord("VII", Chord.majorChord)

'''
Encapsulates the logic of to determine valid chord
progressions in tonal music.
'''
class TonalFlowChart:
    MAJOR = "major_chord_tfc"
    MINOR = "minor_chord_tfc"

    '''
    Note: since the one chord can go to anything, this is left out of the mappings.
    We explicitly check for this case in the functions of the class.
    '''
    nextChordMapMajor = {Chords.MINOR_TWO: (Chords.MAJOR_FIVE, Chords.DIMINISHED_SEVEN),\
                         Chords.MINOR_THREE: (Chords.MINOR_SIX, Chords.MAJOR_FOUR),\
                         Chords.MAJOR_FOUR: (Chords.MAJOR_ONE, Chords.MINOR_TWO, Chords.MAJOR_FIVE),\
                         Chords.MAJOR_FIVE: (Chords.MAJOR_ONE, Chords.DIMINISHED_SEVEN, Chords.MINOR_SIX),\
                         Chords.MINOR_SIX: (Chords.MAJOR_FOUR, Chords.MINOR_TWO),\
                         Chords.DIMINISHED_SEVEN: (Chords.MAJOR_ONE)}

    nextChordMapMinor = {Chords.MAJOR_SEVEN: (Chords.MAJOR_THREE),\
                         Chords.MAJOR_THREE: (Chords.MAJOR_SIX, Chords.MINOR_FOUR),\
                         Chords.MAJOR_SIX: (Chords.MINOR_FOUR, Chords.DIMINISHED_TWO),\
                         Chords.MINOR_FOUR: (Chords.MINOR_ONE, Chords.DIMINISHED_TWO, Chords.MAJOR_FIVE),\
                         Chords.DIMINISHED_TWO: (Chords.MAJOR_FIVE, Chords.DIMINISHED_SEVEN),\
                         Chords.MAJOR_FIVE: (Chords.DIMINISHED_SEVEN, Chords.MAJOR_SIX, Chords.MINOR_ONE),\
                         Chords.DIMINISHED_SEVEN: (Chords.MINOR_ONE)}

    def __init__(self, chart_type = MAJOR):
        self.chart_type = chart_type

        if (chart_type == TonalFlowChart.MAJOR):
            self.chartMap = TonalFlowChart.nextChordMapMajor
        else:
            self.chartMap = TonalFlowChart.nextChordMapMinor

    def is_valid_progression(self, chord):
        return chord == MAJOR_ONE or chord == MINOR_ONE  or chord in self.chartMap[chord]

    def get_next_chords(self, chord):
        chordIsOne = chord == Chords.MAJOR_ONE or chord == Chords.MINOR_ONE
        
        if chordIsOne and self.chart_type == TonalFlowChart.MAJOR:
            return [Chords.MINOR_TWO, Chords.MINOR_THREE, Chords.MAJOR_FOUR, Chords.MAJOR_FIVE, Chords.MINOR_SIX, Chords.DIMINISHED_SEVEN]
        elif chordIsOne:
            return [Chords.DIMINISHED_TWO, Chords.MAJOR_THREE, Chords.MINOR_FOUR, Chords.MINOR_FIVE, Chords.MAJOR_SIX, Chords.MAJOR_SEVEN]
        else:
            return self.chartMap[chord]

    # TODO: expand for mode mixture; check parallel chartMap