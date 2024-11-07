"""
This class contains the functions that draw the components in our scene
with functions such as draw_pool_table(), draw_dice(), etc.
"""

from OpenGL.GLU import *
from OpenGL.GL import *
from basic_shapes import *


class Components:
	
    #==============================
    # Table components
    #==============================

    def draw_intricate_leg():
        glPushMatrix() # save current matrix
    
        # Draw main part of leg
        BasicShapes.draw_rectangle(0.125,0.125,2.5)
        
        # Draw the designs (pryramids and a sphere)
        BasicShapes.draw_pyramid(0.5,0.5)
        
        glTranslatef(0,1,0) # Move up from the ground
        glRotated(180,1,0,0) # rotate
        BasicShapes.draw_pyramid(0.5,0.5)
        glRotated(-180,1,0,0) # rotate back
        BasicShapes.draw_pyramid(0.5,0.5)

        glTranslatef(0,0.5,0) # Move up more
        BasicShapes.draw_sphere(0.25)

        glTranslatef(0,1,0) # Move up more
        glRotated(180,1,0,0) # rotate
        BasicShapes.draw_pyramid(0.5,0.5)


        glPopMatrix()
