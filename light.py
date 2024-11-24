"""
This class contains the functions that draw the light in our scene
with functions such as ***(), ***(), etc.
"""

from OpenGL.GLU import *
from OpenGL.GL import *
import math

class Light:
    def __init__(self, light_id, position, ambient=None, diffuse=None, specular=None):
        """ Initialize the light source.
        Parameters:
        light_id -- OpenGL light identifier (e.g., GL_LIGHT0, GL_LIGHT1, etc.)
        position -- Array [x, y, z, w] defining the light position.
        ambient -- Optional ambient light (l of four values), defaults to [0.0, 0.0, 0.0, 1.0].
        diffuse -- Optional diffuse light (l of four values), defaults to [1.0, 1.0, 1.0, 1.0].
        specular -- Optional specular light (l of four values), defaults to [1.0, 1.0, 1.0, 1.0].
        """
        self.light_id = light_id
        self.position = position
        self.ambient = ambient if ambient else [0.0, 0.0, 0.0, 1.0]
        self.diffuse = diffuse if diffuse else [1.0, 1.0, 1.0, 1.0]
        self.specular = specular if specular else [1.0, 1.0, 1.0, 1.0]
        self.is_enabled = False

    def toggle(self):
        """Turn on/off the light."""
        if self.is_enabled:
            self.turn_off()
        else:
            self.turn_on()

    def turn_on(self):
        """Turn on the light."""
        if not self.is_enabled:
            glEnable(self.light_id)
            self.is_enabled = True

    def turn_off(self):
        """Turn off the light."""
        if self.is_enabled:
            glDisable(self.light_id)
            self.is_enabled = False

    def place_light(self):
        """Place and enable the light in the OpenGL environment."""
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glLightfv(self.light_id, GL_POSITION, self.position)
        glLightfv(self.light_id, GL_AMBIENT, self.ambient)
        glLightfv(self.light_id, GL_DIFFUSE, self.diffuse)
        glLightfv(self.light_id, GL_SPECULAR, self.specular)

        glLightf(self.light_id, GL_CONSTANT_ATTENUATION, 1.0)
        glLightf(self.light_id, GL_LINEAR_ATTENUATION, 0.2)
        glLightf(self.light_id, GL_QUADRATIC_ATTENUATION, 0.05)

        if not self.is_enabled:
            glEnable(self.light_id)
            self.is_enabled = True

    def move_light(self, new_position):
        """Move the light to a new position.
        Parameters:
        new_position -- Array [x, y, z, w] defining the new light position.
        """
        self.position = new_position
        self.place_light()  # Update the light position

    def set_ambient(self, ambient):
        """
        Update the ambient light value.

        Parameters:
        ambient -- Array [r, g, b, a] defining the new ambient light.
        """
        self.ambient = ambient
        glLightfv(self.light_id, GL_AMBIENT, self.ambient)

    def set_diffuse(self, diffuse):
        """
        Update the diffuse light value.

        Parameters:
        diffuse -- Array [r, g, b, a] defining the new diffuse light.
        """
        self.diffuse = diffuse
        glLightfv(self.light_id, GL_DIFFUSE, self.diffuse)

    def set_specular(self, specular):
        """
        Update the specular light value.

        Parameters:
        specular -- Array [r, g, b, a] defining the new specular light.
        """
        self.specular = specular
        glLightfv(self.light_id, GL_SPECULAR, self.specular)

    def draw_light_indicator(self):
        """Drawing sphere at the light's position to indicate where the light is placed."""
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2])
        glDisable(GL_LIGHTING)
        glColor3f(self.diffuse[0], self.diffuse[1], self.diffuse[2])
        gluSphere(gluNewQuadric(), 1, 100, 100)
        glEnable(GL_LIGHTING)
        glPopMatrix()

    def place_flashlight(light_num, flash_light_angle=0.0):
        """Creates a (spotlight) flashlight near the viewer/camera"""
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        light_position = [ 0.2, -0.5, 0.0, 1.0 ]
        rad = math.radians(flash_light_angle)
        light_direction = [ math.sin(rad), 0.0, -math.cos(rad), 0.0]
        light_ambient = [ 1.0, 1.0, 1.0, 1.0 ]
        light_diffuse = [ 1.0, 1.0, 1.0, 1.0 ]
        light_specular = [ 1.0, 1.0, 1.0, 1.0 ]

        # For Light 0, set position, ambient, diffuse, and specular values
        glLightfv(light_num, GL_POSITION, light_position)
        glLightfv(light_num, GL_AMBIENT, light_ambient)
        glLightfv(light_num, GL_DIFFUSE, light_diffuse)
        glLightfv(light_num, GL_SPECULAR, light_specular)

        glLightfv(light_num, GL_SPOT_DIRECTION, light_direction)
        glLightf(light_num, GL_SPOT_CUTOFF, 15.0)
        glLightf(light_num, GL_SPOT_EXPONENT, 0.0)

        # Distance attenuation
        glLightf(light_num, GL_CONSTANT_ATTENUATION, 1.0)
        glLightf(light_num, GL_LINEAR_ATTENUATION, 0.10)
        glLightf(light_num, GL_QUADRATIC_ATTENUATION, 0.00)
        glEnable(light_num)
        glPopMatrix()
