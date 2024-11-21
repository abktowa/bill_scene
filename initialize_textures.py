"""""
Unlike the other preview program, this one has textures set up and features a strong backlight

This program can be used to preview an element
It has basic lighting, navigation, and aniamtion set up


Navigation: The 'W' and 'S' keys zoom in and out. The 'D' and 'A' keys rotate side to side. 
The 'I' and 'K' keys rotate up and down. The arrow keys move up or down and side to side.
"""""

import sys
import math
import pygame
from OpenGL.GLU import *
from OpenGL.GL import *
from camera import *
from utils import *
from basic_shapes import *
from components import *
from materials import *
from textures import *
from initialize_textures import *
from sub_scenes import *

class InitializeTextures:

    # These parameters describe window properties
    window_dimensions = (1200, 800)
    win_name = b'Keep the ball rolling!'

    # These parameters define simple animation properties
    FPS = 60.0
    toggle = GL_TRUE            # Used to toggle a feature on/off
    animate = False
    rotation_angle = 0
    angle_step = -0.5
    flash_light_angle = 0.0     # Degree of rotation (about y-axis) of flashlight

    # Texture data
    wood_two_file = "textures/wood2.jpeg"
    wood_one_file = "textures/wood1.jpeg"
    eight_ball_file = "textures/eight_ball.jpeg"
    eight_ball_texture = None
    wood_one_texture = None
    checkerboard_texture_name = None
    wood_two_texture = None

    # Navigation variables
    turn_degree_x = 0
    turn_degree_y = 0
    view_x = 0
    view_y = 0
    view_z = 0

    # These parameters define the camera's initial parameters
    CAM_ANGLE = 60.0
    CAM_NEAR = 0.01
    CAM_FAR = 1000.0
    INITIAL_EYE = Point(0, 3, 15)
    INITIAL_LOOK_ANGLE = 0
    camera = Camera(CAM_ANGLE, window_dimensions[0]/window_dimensions[1], CAM_NEAR, CAM_FAR, INITIAL_EYE, INITIAL_LOOK_ANGLE)

    def main():
        InitializeTextures.init()

        # Enters the main loop.   
        # Displays the window and starts listening for events.
        InitializeTextures.main_loop()
        return

    def init():
        """Perform basic OpenGL initialization."""
        global concrete_texture_name, boomer_texture_name, running, clock, ball, can

        # pygame setup
        pygame.init()
        screen = pygame.display.set_mode(InitializeTextures.window_dimensions, pygame.DOUBLEBUF|pygame.OPENGL)
        clock = pygame.time.Clock()
        pygame.key.set_repeat(300, 50)  # Key repeat rate
        running = True

        # Set up depth-test
        glEnable(GL_DEPTH_TEST)   # For z-buffering!

        # Create or load the textures
        InitializeTextures.texture_array = glGenTextures(3)  # Texture names for all three textures to create
        InitializeTextures.eight_ball_texture = InitializeTextures.texture_array[0]
        InitializeTextures.wood_one_texture = InitializeTextures.texture_array[1]
        InitializeTextures.wood_two_texture = InitializeTextures.texture_array[2]
        InitializeTextures.load_texture(InitializeTextures.eight_ball_texture, InitializeTextures.eight_ball_file, (0,0,512,512))
        InitializeTextures.load_texture(InitializeTextures.wood_one_texture, InitializeTextures.wood_one_file, (0,0,512,512))
        InitializeTextures.load_texture(InitializeTextures.wood_two_texture, InitializeTextures.wood_two_file, (0,0,512,512))

    def main_loop():
        global running, clock, animate
        while running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    InitializeTextures.keyboard(event)

            if InitializeTextures.animate:
                # Advance the scene one frame
                InitializeTextures.advance()

            # (Re)draw the scene (should only do this when necessary!)
            InitializeTextures.display()

            # Flipping causes the current image to be seen. (Double-Buffering)
            pygame.display.flip()

            clock.tick(InitializeTextures.FPS)  # delays to keep it at FPS frame rate

    def advance():
        global rotation_angle
        InitializeTextures.rotation_angle += InitializeTextures.angle_step
        if InitializeTextures.rotation_angle >= 360:
            InitializeTextures.rotation_angle -= 360   # So doesn't get too large
        elif InitializeTextures.rotation_angle < 0:
            InitializeTextures.rotation_angle += 360    

    def display():
        """Display the current scene."""
        # Set the viewport to the full screen.
        win_width = InitializeTextures.window_dimensions[0]
        win_height = InitializeTextures.window_dimensions[1]
        glViewport(0, 0, win_width, win_height)

        InitializeTextures.camera.setProjection()
        InitializeTextures.adjust_navigation_position()
        # Clear the Screen.
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glFlush()
        
        # Use the smooth (Gouraud) shading model
        glShadeModel(GL_SMOOTH)

        # Draw and show the "Scene".
        InitializeTextures.draw_scene()
        glFlush()


    # Function used to handle any key events
    # event: The keyboard event that happened
    def keyboard(event):
        global is_red, running, animate, turn_degree_x, turn_degree_y, view_x, view_y, view_z
        key = event.key # "ASCII" value of the key pressed
        if key == 27:  # ASCII code 27 = ESC-key
            running = False
        elif key == ord(' '):
            InitializeTextures.animate = not InitializeTextures.animate
        elif key == pygame.K_LEFT:
            # Move left
            InitializeTextures.view_x += 1
        elif key == pygame.K_RIGHT:
            # Move right
            InitializeTextures.view_x -= 1
        elif key == pygame.K_UP:
            # Go up
            InitializeTextures.view_y -= 1
        elif key == pygame.K_DOWN:
            # Go down
            InitializeTextures.view_y += 1            
        elif key == ord('w'):
            # Zoom in
            InitializeTextures.view_z += 1
        elif key == ord('s'):
            # Zoom out
            InitializeTextures.view_z -= 1
        elif key == ord('a'):
            # tilt left
            InitializeTextures.turn_degree_x +=1
        elif key == ord('d'):
            # tilt right
            InitializeTextures.turn_degree_x -= 1
        elif key == ord('i'):
            # Tilt forward
            InitializeTextures.turn_degree_y += 1
        elif key == ord('k'):
            # Tilt backward
            InitializeTextures.turn_degree_y -= 1

        # Adjust the navigation bsed on the keyboard input
    def adjust_navigation_position():
        moveSpeed = 0.2
        glTranslatef(InitializeTextures.view_x*moveSpeed,InitializeTextures.view_y*moveSpeed,InitializeTextures.view_z*moveSpeed)

    def adjust_navigation_tilt():
        tiltSpeed = 1
        glRotated(InitializeTextures.turn_degree_x*tiltSpeed,0,1,0)
        glRotated(InitializeTextures.turn_degree_y*tiltSpeed,1,0,0)

    def draw_scene():
        """Draws a simple scene with a few shapes."""
        # Place the camera
        glEnable(GL_LIGHTING)
        glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)

        InitializeTextures.camera.placeCamera()

        InitializeTextures.place_backlight(GL_LIGHT0)
        glColor3f(0.5, 0.5, 0.5)

        InitializeTextures.adjust_navigation_tilt()

        # Draw a textured sphere
        glRotated(InitializeTextures.rotation_angle, 0, 1, 0)   # Spin around y-axis
        glPushMatrix()
        glRotate(-90,1,0,0)
        Materials.set_material(GL_FRONT, Materials.GOLD)
        BasicShapes.draw_sphere(2)
        glPopMatrix()

        Textures.set_texture(InitializeTextures.wood_two_texture)
        glPushMatrix()
        glTranslated(3, 0, 0)
        glTranslate(0,-1.5,0)
        glRotate(270,1,0,0)
        BasicShapes.draw_cylinder(1,3)
        glPopMatrix()



    def place_backlight(light_num):
        """ This creates a (spotlight) flashlight near the viewer/camera"""
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        light_position = [ 0.2, -0.5, 0.0, 1.0 ]
        rad = math.radians(InitializeTextures.flash_light_angle)
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
        #glLightf(light_num, GL_SPOT_CUTOFF, 15.0)
        glLightf(light_num, GL_SPOT_EXPONENT, 0.0)

        # Distance attenuation
        glLightf(light_num, GL_CONSTANT_ATTENUATION, 1.0)
        glLightf(light_num, GL_LINEAR_ATTENUATION, 0.10)
        glLightf(light_num, GL_QUADRATIC_ATTENUATION, 0.00)
        glEnable(light_num)
        glPopMatrix()

    def place_flashlight(light_num):
        """ This creates a (spotlight) flashlight near the viewer/camera"""
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        light_position = [ 0.2, -0.5, 0.0, 1.0 ]
        rad = math.radians(InitializeTextures.flash_light_angle)
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


    def load_texture(texture_name, file_name, crop_dimensions=None):
        # Load the image. Crop if requested (should be a 4-tuple: e.g. (0,0,128,128)
        im = Image.open(file_name)
        print("Image dimensions: {0}".format(im.size))  # If you want to see the image's original dimensions
        if crop_dimensions != None:
            # We are asked to crop the texture
            im = im.crop(crop_dimensions)

        dimX = im.size[0]
        dimY = im.size[1]
        texture = im.tobytes("raw")   # The cropped texture
        glBindTexture(GL_TEXTURE_2D, texture_name)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, dimX, dimY, 0, GL_RGB,
                    GL_UNSIGNED_BYTE, texture)

    def set_white(face):
        """Set the material properties of the given face to bright white.

        Keyword arguments:
        face -- which face (GL_FRONT, GL_BACK, or GL_FRONT_AND_BACK)
        """
        ambient = [ 1, 1, 1, 1.0 ]
        diffuse = [ 1, 1, 1, 1.0 ]
        specular = [ 1, 1, 1, 1.0 ]
        shininess = 1
        glMaterialfv(face, GL_AMBIENT, ambient);
        glMaterialfv(face, GL_DIFFUSE, diffuse);
        glMaterialfv(face, GL_SPECULAR, specular);
        glMaterialf(face, GL_SHININESS, shininess);

    if __name__ == '__main__': main()
