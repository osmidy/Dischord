from LeapHand import *

'''
Representation of a crosshair used by the player to aim at targets.
Backed by a LeapHand.
'''
class Crosshair(LeapHand):
    def __init__(self):
        super(Crosshair, self).__init__()

        self.crosshairHeight = .3 * Window.height

        self.pos = (300, self.crosshairHeight)

        self.halfLineLength = 25

        self.color = Color(1, 0, 0)
        self.add(self.color)
        
        self.verticalLine = Line()
        self.horizonatlLine = Line()
        self.set_lines()

        self.add(self.verticalLine)
        self.add(self.horizonatlLine)

    def set_pos(self, pos):
        super(Crosshair, self).set_pos(pos)
        self.set_lines()

    def get_pos(self):
        return self.pos

    def set_lines(self):
        # We only allow horizontal movement of the crosshair,
        # so vertical position of crosshair is fixed
        x = self.pos[0]
        self.verticalLine.points = [x, self.crosshairHeight - self.halfLineLength, x, self.crosshairHeight + self.halfLineLength]
        self.horizonatlLine.points = [x - self.halfLineLength, self.crosshairHeight, x + self.halfLineLength, self.crosshairHeight]