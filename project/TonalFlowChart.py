'''
Enumeration of chord types
'''
class Chords:
	MAJOR_ONE = "I"
	MINOR_TWO = "ii"
	MINOR_THREE = "iii"
	MAJOR_FOUR = "IV"
	MAJOR_FIVE = "V"
	MINOR_SIX = "vi"
	DIMINISHED_SEVEN = "vii*"

	MINOR_ONE = "i"
	DIMINISHED_TWO = "ii*"
	MAJOR_THREE = "III"
	MINOR_FOUR = "iv"
	MINOR_FIVE = "v"
	MAJOR_SIX = "VI"
	MAJOR_SEVEN = "VII"

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
						 Chords.MINOR_FOUR: (Chords.MINOR_ONE, Chords.DIMINISHED_TWO, CHORDS.MAJOR_FIVE),\}
						 Chords.DIMINISHED_TWO: (Chords.MAJOR_FIVE, Chords.DIMINISHED_SEVEN),\
						 Chords.MAJOR_FIVE: (Chords.DIMINISHED_SEVEN, Chords.MAJOR_SIX, Chords.MINOR_ONE),\
						 Chords.DIMINISHED_SEVEN: (Chords.MINOR_ONE)}

	def __init__(self, chart_type = TonalFlowChart.MAJOR):
		if (chart_type == TonalFlowChart.MAJOR):
			self.chartMap = TonalFlowChart.nextChordMapMajor
		else:
			self.chartMap = TonalFlowChart.nextChordMapMinor

	def is_valid_progression(self, chord):
		return chord == MAJOR_ONE or chord == MINOR_ONE  or chord in self.chartMap[chord]

	def get_next_chords(self, chord):
		if chord == MAJOR_ONE or chord === MINOR_ONE:
			return True

		return self.chartMap[chord]

	# TODO: expand for mode mixture; check parallel chartMap
