"""
This class contains the functions that draw the components in our scene
with functions such as draw_pool_table(), draw_dice(), etc.
"""

from OpenGL.GLU import *
from OpenGL.GL import *
from basic_shapes import *
from components import *


class Components:
	
    
    #==============================
    # Table functions
    #==============================

    # Draws a 3 unit tall table with a given length and width
    def draw_elegant_table(length, width):
        glPushMatrix() 

        glTranslatef(0,2.5,0) # Move up from the ground
        BasicShapes.draw_rectangle(length,width,0.5) # Draw surface
        glTranslatef(0,-2.5,0) # Move back down

        percent_length = length * 0.75
        percent_width = width * 0.75


        glTranslatef(percent_length/2, 0, percent_width/2)
        Components.draw_elegant_table_leg()
        glTranslatef(-percent_length, 0, 0)
        Components.draw_elegant_table_leg()
        glTranslatef(0, 0, -percent_width)
        Components.draw_elegant_table_leg()
        glTranslatef(percent_length, 0, 0)
        Components.draw_elegant_table_leg()
        glPopMatrix()


    def draw_elegant_table_leg():
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

    #==============================
    # Lamp functions
    #==============================

    def draw_lamp_shade(height):
        BasicShapes.draw_adjustable_cylinder(height, height/2, height) # bottom_radius, top_radius, height





    #==============================
    # Ball functions
    #==============================

    def draw_1ball():
        glPushMatrix()
        BasicShapes.draw_sphere(0.186)
        glPopMatrix()

    def draw_4ball():
        glPushMatrix()
        # Move to the left for the second ball
        glTranslatef(-0.5, 0, 0.5)
        BasicShapes.draw_sphere(0.186)
        
        # Move to the right for the third ball
        glTranslatef(1.0, 0, 0)
        BasicShapes.draw_sphere(0.186)
        
        # Move to the left for the fourth ball
        glTranslatef(-1.0, 0, 0.5)
        BasicShapes.draw_sphere(0.186)
        
        # Move to the right for the fifth ball
        glTranslatef(1.0, 0, 0)
        BasicShapes.draw_sphere(0.186)
        glPopMatrix()

