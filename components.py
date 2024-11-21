"""
This class contains the functions that draw the components in our scene
with functions such as draw_pool_table(), draw_dice(), etc.
"""

from OpenGL.GLU import *
from OpenGL.GL import *
from basic_shapes import *
from components import *
from materials import *
from textures import *
from initialize_textures import *


class Components:
	
    InitializeTextures.init()  # Ensure textures are loaded

    
    #==============================
    # Table functions
    #==============================


    def draw_elegant_table(length, width, texture=None):
        glPushMatrix() 

        if texture:  # Apply the texture if provided
            Textures.set_texture(texture)

        glTranslatef(0, 2.5, 0)  # Move up from the ground
        BasicShapes.draw_rectangle(length, width, 0.5)  # Draw surface
        glTranslatef(0, -2.5, 0)  # Move back down

        percent_length = length * 0.75
        percent_width = width * 0.75

        glTranslatef(percent_length / 2, 0, percent_width / 2)
        Components.draw_elegant_table_leg(texture)  # Pass the texture to the legs
        glTranslatef(-percent_length, 0, 0)
        Components.draw_elegant_table_leg(texture)
        glTranslatef(0, 0, -percent_width)
        Components.draw_elegant_table_leg(texture)
        glTranslatef(percent_length, 0, 0)
        Components.draw_elegant_table_leg(texture)
        glPopMatrix()


    def draw_elegant_table_leg(texture=None):
        glPushMatrix()  # Save current matrix
        
        if texture:  # Apply the texture if provided
            Textures.set_texture(texture)

        # Draw main part of leg
        BasicShapes.draw_rectangle(0.125, 0.125, 2.5)
        
        # Draw the designs (pyramids and a sphere)
        BasicShapes.draw_pyramid(0.5, 0.5)

        glTranslatef(0, 1, 0)  # Move up from the ground
        glRotated(180, 1, 0, 0)  # Rotate
        BasicShapes.draw_pyramid(0.5, 0.5)
        glRotated(-180, 1, 0, 0)  # Rotate back
        BasicShapes.draw_pyramid(0.5, 0.5)

        glTranslatef(0, 0.5, 0)  # Move up more
        if texture:  # Apply texture for the sphere
            Textures.set_texture(texture)
        BasicShapes.draw_sphere(0.25)

        glTranslatef(0, 1, 0)  # Move up more
        glRotated(180, 1, 0, 0)  # Rotate
        BasicShapes.draw_pyramid(0.5, 0.5)

        glPopMatrix()


    #==============================
    # Lamp functions
    #==============================

    def draw_lamp_shade(height):
        BasicShapes.draw_adjustable_cylinder(height, height/2, height) # bottom_radius, top_radius, height

    def draw_lamp_base():
        """Draws the lamp base with two stacked spheres."""
        glPushMatrix()
        
        # Bottom sphere (larger)
        BasicShapes.draw_sphere(radius=2.0)  # Radius of the larger sphere

        # Top sphere (smaller, stacked above)
        glTranslatef(0, 3, 0)  # Move up by the radius of the bottom sphere + some offset
        BasicShapes.draw_sphere(radius=1.5)  # Radius of the smaller sphere

        glPopMatrix()

    def draw_lamp():
        """Draws the complete lamp (base + shade)."""
        glPushMatrix()

        # Draw the base (two spheres)
        Materials.set_material(GL_FRONT_AND_BACK, Materials.GOLD)
        Components.draw_lamp_base()

        # Draw the lamp shade
        glTranslatef(0, 6, 0)  # Move above the smaller sphere (base height + offset for stacking)
        Components.draw_lamp_shade(height=3.0)  # Adjust height as needed
        Materials.set_material(GL_FRONT_AND_BACK, Materials.LIGHTBULB)
        Components.draw_light_bulb()

        glPopMatrix()

    def setup_lightbulb_lighting():
            """Sets up a light source at the position of the lightbulb."""
            # Define light properties
            light_position = [0.0, 1.5, 0.0, 1.0]  # Relative to the lamp
            diffuse_color = [2.0, 2.0, 1.8, 1.0]   # Intense warm white light (double the normal intensity)
            ambient_color = [0.5, 0.5, 0.4, 1.0]   # Soft ambient glow
            specular_color = [1.5, 1.5, 1.5, 1.0]  # Strong highlights for reflective surfaces


            # Configure the light source
            glEnable(GL_LIGHT3)  # Enable light for the bulb
            glLightfv(GL_LIGHT3, GL_POSITION, light_position)
            glLightfv(GL_LIGHT3, GL_DIFFUSE, diffuse_color)
            glLightfv(GL_LIGHT3, GL_AMBIENT, ambient_color)
            glLightfv(GL_LIGHT3, GL_SPECULAR, specular_color)


    def draw_light_bulb():
        """Draws a small light bulb inside the lamp shade."""
        glPushMatrix()
        glTranslatef(0, 1.5, 0)  # Position inside the lamp shade
          # Set up light source at the bulb
        Components.setup_lightbulb_lighting()
        BasicShapes.draw_sphere(radius=0.5)  # Small sphere for the bulb
        glPopMatrix()


    def draw_table_with_lamp(table_length, table_width):
        """Draws a table with a lamp placed on top, scaling the lamp down."""
        glPushMatrix()

        # Draw the table
        Materials.set_material(GL_FRONT_AND_BACK, Materials.REDDISH_WOOD)
        # Textures.set_texture(InitializeTextures.wood_two)
        Components.draw_elegant_table(table_length, table_width, InitializeTextures.wood_two_name)

        # Position and scale the lamp
        glPushMatrix()
        glTranslatef(0, 3, 0)  # Move the lamp up to the surface of the table
        glScalef(0.3, 0.3, 0.3)  # Scale the lamp down (adjust the factors as needed)
        Components.draw_lamp()  # Draw the lamp
        glPopMatrix()

        glPopMatrix()

    def help_message():
        print("Hi! The controls are as follows:\nPress \"W\" to move forward\nPress \"S\" to move backward")
        print("Press \"A\" to move to the left\nPress \"D\" to move to the right")
        print("Press the Up Arrow key to look up\nPress the Down Arrow key to look down\nPress the Left Arrow key to look left")
        print("Press the Right Arrow key to look right\nPress \"TBD\" to reset to starting position\nPress \"TBD\" to reset camera")
        print("Press 0 to turn the main light on/off\nPress 1 to turn the spotlight on/off\nPress 2 to turn the desk light on/off")
        print("Press 3 to turn the red light on/off\nPress 4 to turn the green light on/off\nPress 5 to turn the blue light on/off")

    #==============================
    # Cue Sticks
    #==============================

    def draw_cue_stick():
        BasicShapes.draw_adjustable_cylinder(0.0984, 0.0426, 4.57) # bottom_radius, top_radius, height

    #==============================
    # Ball functions
    #==============================

    def draw_1ball():
        glPushMatrix()
        BasicShapes.draw_sphere(0.186)
        glPopMatrix()

    def draw_rotated_1ball(rotate_x, rotate_y, rotate_z):
        glPushMatrix()
        BasicShapes.draw_rotated_sphere(0.186, rotate_x, rotate_y, rotate_z)
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

    def draw_die(): 
        glPushMatrix()
        glTranslatef(1, 0, 0)
        BasicShapes.draw_cube(0.10, 0.10, 0.10)
        glPopMatrix()

    """ def draw_dice():
        glPushMatrix()
        glTranslatef(1, 0, 0)
        BasicShapes.draw_cube(0.10, 0.10, 0.10)
        glTranslatef(0.13, 0, 0)
        glPopMatrix() """
    
       
    #==============================
    # Pool table functions
    #==============================

    # Draws the pool table with the billiard balls on it
    def draw_pool_table_with_abans_children():
        glPushMatrix()
        
        Components.draw_pool_table()

        glTranslatef(0, 3.08, 0)  # Move up from the ground

        # Draw the balls
        Materials.set_material(GL_FRONT, Materials.SILVER) # Set the material
        glTranslatef(-1.2, 0, 1.2)
        Components.draw_1ball()
        glTranslatef(1.6, 0, -1.1)
        Components.draw_1ball()
        glTranslatef(1.3, 0, -1.5)
        Components.draw_1ball()
        glTranslatef(-1.9, 0, 0.8)
        Components.draw_1ball()

        # Draw the Q balls
        Materials.set_material(GL_FRONT, Materials.BALL_RESIN) # Set the material
        glTranslatef(-2.2, 0, 0.2)
        Components.draw_1ball()

        # Draw the 8 ball
        Textures.set_texture(InitializeTextures.eight_ball_texture_name) # Set the texture
        glTranslatef(4, 0, 0)
        Components.draw_rotated_1ball(100,0,0)

        glPopMatrix()



    # Draws a pool table that is 8 units long, 4 units wide, and 3.08 units tall (aprox. 3 ft 1 in)
    def draw_pool_table():
        glPushMatrix()
        
        length=8 
        width=4

        # Draw the main table
        Components.draw_elegant_table(length, width, InitializeTextures.wood_one_name)
        
        Textures.set_texture(InitializeTextures.wood_one_name) # Set the texture
        glTranslatef(0, 1.5, 0)  # Move up from the ground
        BasicShapes.draw_rectangle(7.7,3.7,1) # Draw the trim

        glTranslatef(0, 1.5, 0)  # Move up more
        Materials.set_material(GL_FRONT, Materials.GREEN_FELT) # Set the material
        BasicShapes.draw_rectangle(7.7,3.7,0.08) # Draw the felt


        # Draw the bumper
        Materials.set_material(GL_FRONT, Materials.RUBBER_BUMPER) # Set the material

        glPushMatrix()
        glTranslatef(-7.7/2, 0, 0)  # Move to the side
        BasicShapes.draw_rectangle(0.3, 4, 0.2)
        glTranslatef(7.7, 0, 0)  # Move to the other side
        BasicShapes.draw_rectangle(0.3, 4, 0.2)
        glPopMatrix()
        glTranslatef(0, 0, (3.7/2))  # Move back
        BasicShapes.draw_rectangle(8, 0.3, 0.2)
        glTranslatef(0, 0, - (3.7))  # Move forward
        BasicShapes.draw_rectangle(8, 0.3, 0.2)


        glPopMatrix()