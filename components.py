"""
This class contains the functions that draw the components in our scene
with functions such as draw_pool_table(), draw_dice(), etc.
"""

from OpenGL.GLU import *
from OpenGL.GL import *
from basic_shapes import *
from components import *
from textures import *

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

    #==============================
    # Dice functions
    #==============================

    def draw_die(length, width, height, textures): 
        """
        Draw a textured cube.
        
        Parameters:
        length - Length of the cube.
        width - Width of the cube.
        height - Height of the cube.
        textures - A list of 6 texture names, one for each face of the cube.
        """
        glPushMatrix()

        half_length = length / 2.0
        half_width = width / 2.0

        # Define vertices for a rectangular prism (cube)
        vertices = [
            [-half_length, 0, -half_width],        # Vertex 0
            [half_length, 0, -half_width],         # Vertex 1
            [half_length, height, -half_width],    # Vertex 2
            [-half_length, height, -half_width],   # Vertex 3
            [-half_length, 0, half_width],         # Vertex 4
            [half_length, 0, half_width],          # Vertex 5
            [half_length, height, half_width],     # Vertex 6
            [-half_length, height, half_width]     # Vertex 7
        ]

        # Defines the rectangle faces created by the given vertices
        faces = [
            (0, 3, 2, 1),  # Face 1 (bottom)
            (3, 7, 6, 2),  # Face 2 (back)
            (7, 4, 5, 6),  # Face 3 (top)
            (0, 1, 5, 4),  # Face 4 (front)
            (0, 4, 7, 3),  # Face 5 (left)
            (1, 2, 6, 5)   # Face 6 (right)
        ]

        # Texture coordinates for mapping the full texture to a rectangular face
        tex_coords = [
            (0.0, 0.0),  # Bottom left
            (1.0, 0.0),  # Bottom right
            (1.0, 1.0),  # Top right
            (0.0, 1.0)   # Top left
        ]

        # Enable texturing
        glEnable(GL_TEXTURE_2D)

        # Draw each face of the cube with a different texture
        for i, face in enumerate(faces):
            Textures.set_texture(textures[i])  # Set the texture for the current face

            glBegin(GL_QUADS)
            for j, vertex in enumerate(face):
                glTexCoord2f(tex_coords[j][0], tex_coords[j][1])  # Set texture coordinate for each vertex
                glVertex3fv(vertices[vertex])  # Draw the vertex
            glEnd()

        # Disable texturing
        glDisable(GL_TEXTURE_2D)
    
        glPopMatrix()

        """ def draw_dice():
            glPushMatrix()
            glTranslatef(1, 0, 0)
            BasicShapes.draw_cube(0.10, 0.10, 0.10)
            glTranslatef(0.13, 0, 0)
            glPopMatrix() """