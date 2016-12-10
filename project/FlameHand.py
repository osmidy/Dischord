from LeapHand import *
from common.kivyparticle import ParticleSystem

'''
Representation of a flame used by the player to attack enemies
Backed by a LeapHand.
'''
class FlameHand(LeapHand):
    def __init__(self):
        super(FlameHand, self).__init__()

        # Particle is added to the main widget in Game at runtime
        self.flameParticle = ParticleSystem("../particle/flame.pex")
        self.flameParticle.emitter_x = self.pos[0]
        self.flameParticle.emitter_y = self.pos[1]

        self.flameParticle.start()

    def set_pos(self, pos):
        super(FlameHand, self).set_pos(pos)
        self.flameParticle.emitter_x = self.pos[0]
        self.flameParticle.emitter_y = self.pos[1]

    def set_brightness(self, val):
        pass