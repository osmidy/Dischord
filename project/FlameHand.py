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

        # taken from ../particle/flame.pex -> start_color
        self.color = (1, .85, .85)
        self.alpha = .4

        self.is_armed = False
        self.selectedButton = None

    def arm_weapon(self, btn):
        self.selectedButton = btn
        self.color = btn.rgb
        self.update_color()
        self.is_armed = True

    def unarm_weapon(self, btn):
        self.is_armed = False
        self.selectedButton = None
        self.color = (1, 1, 1) # White
        self.update_color()

    def set_button(self, btn):
        self.selectedButton = btn

    def get_button(self):
        return self.selectedButton

    def set_brightness(self):
        val = self.hand.palm_normal.y + 1.0
        self.alpha = .4 + val/2.0

    def brigten_flame(self):
        self.alpha = 1.0

    def dim_flame(self):
        self.alpha = 0.4

    def update_color(self):
        prop = list(self.color + tuple(self.alpha))
        self.flameParticle.start_color = ListProperty(prop)
        self.flameParticle.end_color = ListProperty(prop)

    def set_pos(self, pos):
        super(FlameHand, self).set_pos(pos)
        self.flameParticle.emitter_x = self.pos[0]
        self.flameParticle.emitter_y = self.pos[1]
        