"""
Light Class for Managing OpenGL Lights

This class encapsulates OpenGL light properties and behaviors, 
allowing for the creation, configuration, and management of 
light objects in the project. 
"""

from OpenGL.GL import *
from OpenGL.GLU import *

class Light:
    def __init__(self, light_num, position, diffuse, specular, attenuation=None, spot_direction=None, spot_cutoff=None, spot_exponent=None):
        self.light_num = light_num
        self.position = position
        self.diffuse = diffuse
        self.specular = specular
        self.attenuation = attenuation or {"constant": 1.0, "linear": 0.01, "quadratic": 0.001}
        self.spot_direction = spot_direction
        self.spot_cutoff = spot_cutoff
        self.spot_exponent = spot_exponent

    def enable(self):
        """Enable and configure the light."""
        glEnable(self.light_num)
        glLightfv(self.light_num, GL_POSITION, self.position)
        glLightfv(self.light_num, GL_DIFFUSE, self.diffuse)
        glLightfv(self.light_num, GL_SPECULAR, self.specular)

        # Apply distance attenuation if provided
        glLightf(self.light_num, GL_CONSTANT_ATTENUATION, self.attenuation["constant"])
        glLightf(self.light_num, GL_LINEAR_ATTENUATION, self.attenuation["linear"])
        glLightf(self.light_num, GL_QUADRATIC_ATTENUATION, self.attenuation["quadratic"])

        # Apply spotlight settings if applicable
        if self.spot_direction:
            glLightfv(self.light_num, GL_SPOT_DIRECTION, self.spot_direction)
        if self.spot_cutoff:
            glLightf(self.light_num, GL_SPOT_CUTOFF, self.spot_cutoff)
        if self.spot_exponent:
            glLightf(self.light_num, GL_SPOT_EXPONENT, self.spot_exponent)

    def disable(self):
        """Disable the light."""
        glDisable(self.light_num)
