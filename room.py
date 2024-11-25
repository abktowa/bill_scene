import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import math
from utils import Point
from camera import Camera
from textures import *
from materials import *
from components import *
from collision import Collision
from light import *

# Window settings
window_dimensions = (1200, 800)
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FPS = 60

# Room dimensions
ROOM_WIDTH = 20.0
ROOM_HEIGHT = 15.0
ROOM_DEPTH = 20.0

# Camera settings
CAM_ANGLE = 60.0
CAM_NEAR = 0.01
CAM_FAR = 1000.0
INITIAL_EYE = Point(0, 5.67, 8)
INITIAL_LOOK_ANGLE = 0

# List for collision boxes
collisionList = []

class Room:

    # pool shooting variables
    in_shooting_mode = False
    shooting_angle = 0

    # Animation frames
    global_frame = 0 # Used to keep track of time
    dice_frame = 0
    initial_dice_frame = 0
    hanging_light_frame = 0
    initial_hanging_light_frame = 0

    # Animation booleans
    animate_dice = False
    animate_hanging_light = False

    # other animation variables
    swing_factor = 0

    # Picture boolean
    show_picture = False


    def __init__(self):
        pygame.init()
        pygame.display.set_mode(window_dimensions, pygame.DOUBLEBUF | pygame.OPENGL)
        self.clock = pygame.time.Clock()
        
        self.camera = Camera(CAM_ANGLE, window_dimensions[0]/window_dimensions[1], CAM_NEAR, CAM_FAR, 
                           INITIAL_EYE, INITIAL_LOOK_ANGLE)
        
        self.init_gl()
        self.create_textures()
        
        # Light states
        self.light_states = {
            'red': False,
            'green': False,
            'blue': False,
            'spotlight': False,
            'lamp': False,
            'flashlight': False
        }
        
        self.running = True

    def should_we_show_picture(self):
        # Iterate through the light states
        for light_name, this_light_is_on in self.light_states.items(): 
            # Ignore the flashlight and check other lights
            if light_name != 'flashlight' and this_light_is_on:
                return False  # If any non-flashlight light is on, don't show the picture
        
        # If no non-flashlight lights are on, show the picture
        return True

    def init_gl(self):
        """Initialize OpenGL settings"""
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_NORMALIZE)
        glEnable(GL_TEXTURE_2D)
        
        # Set up basic lighting
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHT1)
        glEnable(GL_LIGHT2)
        glEnable(GL_LIGHT3) # Red and intially disabled
        glEnable(GL_LIGHT4) # Green and intially disabled
        glEnable(GL_LIGHT5) # Blue and intially disabled
        
        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
        glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glMaterialf(GL_FRONT, GL_SHININESS, 100.0)
        

    def handle_input(self):
        """Handle keyboard and mouse input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r: # Reset Camera to starting point
                    self.camera.eye.x = 0
                    self.camera.eye.y = 5.67
                    self.camera.eye.z = 8
                    # Reset collision point to match the camera's position
                    self.camera.collisionPoint.x = self.camera.eye.x
                    self.camera.collisionPoint.y = self.camera.eye.y
                    self.camera.collisionPoint.z = self.camera.eye.z
                elif event.key == pygame.K_t:  # Reset Vertical Camera position
                    self.camera.heightAngle = INITIAL_LOOK_ANGLE

                elif event.key in [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]:
                    light_index = event.key - pygame.K_0
                    self.toggle_light(light_index)
                elif event.key == pygame.K_h: # Prints to console help message
                    Components.help_message()

        keys = pygame.key.get_pressed()
        moveBack = False
        if keys[pygame.K_w]:
            self.camera.slideCollision(0,0,-0.1)
            for i in range(len(collisionList)):
                if collisionList[i].pointInside(self.camera.collisionPoint):
                    moveBack = True
            if self.camera.collisionPoint.x < .2 -ROOM_WIDTH/2 or self.camera.collisionPoint.x > -.2 + ROOM_WIDTH/2 or self.camera.collisionPoint.z < .2 -ROOM_DEPTH/2 or self.camera.collisionPoint.z > -.2 + ROOM_DEPTH/2:
                moveBack = True
            
            if moveBack == True:
                self.camera.slideCollision(0,0,.1)
            else:
                self.camera.slide(0, 0, -0.1)

        if keys[pygame.K_s]:
            self.camera.slideCollision(0,0,0.1)
            for i in range(len(collisionList)):
                if collisionList[i].pointInside(self.camera.collisionPoint):
                    moveBack = True
            if self.camera.collisionPoint.x < .2 -ROOM_WIDTH/2 or self.camera.collisionPoint.x > -.2 + ROOM_WIDTH/2 or self.camera.collisionPoint.z < .2 -ROOM_DEPTH/2 or self.camera.collisionPoint.z > -.2 + ROOM_DEPTH/2:
                moveBack = True

            if moveBack == True:
                self.camera.slideCollision(0,0,-.1)
            else:
                self.camera.slide(0, 0, 0.1)
        if keys[pygame.K_a]:
            self.camera.slideCollision(-.1,0,0)
            for i in range(len(collisionList)):
                if collisionList[i].pointInside(self.camera.collisionPoint):
                    moveBack = True
            if self.camera.collisionPoint.x < .2 -ROOM_WIDTH/2 or self.camera.collisionPoint.x > -.2 + ROOM_WIDTH/2 or self.camera.collisionPoint.z < .2 -ROOM_DEPTH/2 or self.camera.collisionPoint.z > -.2 + ROOM_DEPTH/2:
                moveBack = True
            if moveBack == True:
                self.camera.slideCollision(.1,0,0)
            else:
                self.camera.slide(-.1, 0, 0)
        if keys[pygame.K_d]:
            
            self.camera.slideCollision(.1,0,0)
            for i in range(len(collisionList)):
                if collisionList[i].pointInside(self.camera.collisionPoint):
                    moveBack = True
            if self.camera.collisionPoint.x < .2 -ROOM_WIDTH/2 or self.camera.collisionPoint.x > -.2 + ROOM_WIDTH/2 or self.camera.collisionPoint.z < .2 -ROOM_DEPTH/2 or self.camera.collisionPoint.z > -.2 + ROOM_DEPTH/2:
                moveBack = True

            if moveBack == True:
                self.camera.slideCollision(-.1,0,0)
            else:
                self.camera.slide(.1, 0, 0)
        if keys[pygame.K_LEFT]:
            self.camera.turn(1)
        if keys[pygame.K_RIGHT]:
            self.camera.turn(-1) 
        if keys[pygame.K_DOWN]:
            self.camera.rise(-1)
        if keys[pygame.K_UP]:
            self.camera.rise(1) 
        
        if keys[pygame.K_x]:
            Room.initial_dice_frame =  Room.global_frame
            Room.animate_dice = True
        if keys[pygame.K_c]:
            Room.animate_hanging_light = not Room.animate_hanging_light

    def animate(self):

        Room.global_frame += 1

        if Room.animate_dice:
            Room.dice_frame += 1
            if Room.global_frame - Room.initial_dice_frame > 200:
                Room.animate_dice = False
        
        if Room.animate_hanging_light:
            Room.swing_factor = 8
            Room.hanging_light_frame += 1
        else:
            if 0 < Room.swing_factor:
                Room.hanging_light_frame += 1
                Room.swing_factor -= 0.03
            else:
                Room.hanging_light_frame = 0
                    
                
        
           


    def setup_lights(self):

        if self.light_states['red']:
            red = Light(GL_LIGHT0, [-6, ROOM_HEIGHT - 1.0, -5, 1], ambient=[0.0, 0.0, 0.0, 0.2], 
                        diffuse=[1.0, 0.0, 0.0, 1.0], specular=[1.0, 0.0, 0.0, 1.0])
            red.place_light()
        else:
            glDisable(GL_LIGHT0)
        
        if self.light_states['green']:
            green = Light(GL_LIGHT1, [0, ROOM_HEIGHT - 1.0, -5, 1], ambient=[0.0, 0.0, 0.0, 0.2], 
                        diffuse=[0.0, 1.0, 0.0, 1.0], specular=[0.0, 1.0, 0.0, 1.0])
            green.place_light()
        else:
            glDisable(GL_LIGHT1)

        if self.light_states['blue']: # Working when 0 is on
            blue = Light(GL_LIGHT2, [6, ROOM_HEIGHT - 1.0, -5, 1], ambient=[0.0, 0.0, 0.0, 0.2], 
                        diffuse=[0.0, 0.0, 1.0, 1.0], specular=[0.0, 0.0, 1.0, 1.0])
            blue.place_light()
        else:
            glDisable(GL_LIGHT2)

        if self.light_states['spotlight']:
            spotlight = Light(GL_LIGHT3, [0, ROOM_HEIGHT - 0.1, 0, 1], ambient=[0.5, 0.5, 0.5, 0.7], 
                        diffuse=[1.0, 1.0, 1.0, 1.0], specular=[1.0, 1.0, 1.0, 1.0])
            spotlight.place_light()
        else:
            glDisable(GL_LIGHT3)

        if self.light_states['lamp']:
            lamp = Light(GL_LIGHT4, [0, ROOM_HEIGHT - 0.1, 0, 1], ambient=[0.5, 0.5, 0.5, 0.7], 
                        diffuse=[1.0, 1.0, 1.0, 1.0], specular=[1.0, 1.0, 1.0, 1.0])
            lamp.place_light()
        else:
            glDisable(GL_LIGHT4)

        if self.light_states['flashlight']: # Working with 0 pressed
            flashlight = Light(GL_LIGHT5, [0, ROOM_HEIGHT - 0.1, 0, 1], ambient=[0.5, 0.5, 0.5, 0.7], 
                        diffuse=[1.0, 1.0, 1.0, 1.0], specular=[1.0, 1.0, 1.0, 1.0])
            flashlight.place_light()
        else:
            glDisable(GL_LIGHT5) 


    def toggle_light(self, index):
        """Toggle specific light based on index"""
        light_names = ['red', 'green', 'blue', 'spotlight', 'lamp', 'flashlight']
        if index < len(light_names):
            self.light_states[light_names[index]] = not self.light_states[light_names[index]]

    def create_textures(self):
        """Create all textures"""
        self.textures = {
            'floor': Textures.create_checkerboard_texture(),
            'wall': Textures.create_wall_texture(),
            'ceiling': Textures.create_ceiling_texture()
        }


    def draw_room(self):
        """Draw the room with textured walls, floor, and ceiling"""
        
        # Set the material to be combined with the textures
        Materials.set_material(GL_FRONT, Materials.BALL_RESIN)
        
        # Floor with checkerboard texture
        Textures.set_texture(self.textures['floor'])

        glBegin(GL_QUADS)
        glNormal3f(0, 1, 0)
        glTexCoord2f(0, 0); glVertex3f(-ROOM_WIDTH/2, 0, -ROOM_DEPTH/2)
        glTexCoord2f(0, 4); glVertex3f(-ROOM_WIDTH/2, 0, ROOM_DEPTH/2)
        glTexCoord2f(4, 4); glVertex3f(ROOM_WIDTH/2, 0, ROOM_DEPTH/2)
        glTexCoord2f(4, 0); glVertex3f(ROOM_WIDTH/2, 0, -ROOM_DEPTH/2)
        glEnd()


        # Walls
        Textures.set_texture(InitializeTextures.wall_name)
        
        # Back wall
        glPushMatrix()
        glTranslate(0,0,ROOM_DEPTH/2 + 0.5) # Move back
        glRotate(270,0,1,0)
        glRotate(180,1,0,0)
        glTranslate(0,-ROOM_HEIGHT,0)
        BasicShapes.draw_rectangle(1, ROOM_DEPTH, ROOM_HEIGHT)
        glPopMatrix()

        # Front wall
        glPushMatrix()
        glTranslate(0,0,-(ROOM_DEPTH/2 + 0.5)) # Move forward
        glRotate(90,0,1,0)
        glRotate(180,1,0,0)
        glTranslate(0,-ROOM_HEIGHT,0)
        BasicShapes.draw_rectangle(1, ROOM_DEPTH, ROOM_HEIGHT)
        glPopMatrix()

        # Left wall
        glPushMatrix()
        glTranslate(-(ROOM_WIDTH/2 + 0.5),0,0) # Move left
        glRotate(180,0,0,1)
        glTranslate(0,-ROOM_HEIGHT,0)
        BasicShapes.draw_rectangle(1, ROOM_DEPTH, ROOM_HEIGHT)
        glPopMatrix()


        # Right wall
        glPushMatrix()
        glTranslate(ROOM_WIDTH/2 + 0.5,0,0) # Move right
        glRotate(180,0,1,0)
        glRotate(180,0,0,1)
        glTranslate(0,-ROOM_HEIGHT,0)
        BasicShapes.draw_rectangle(1, ROOM_DEPTH, ROOM_HEIGHT)
        glPopMatrix()

        # Ceiling
        glPushMatrix()
        glTranslate(0, ROOM_HEIGHT, 0) # Move right
        BasicShapes.draw_rectangle(ROOM_WIDTH, ROOM_DEPTH, 1)
        glPopMatrix()

    def draw_components(self):
        
        Components.draw_animated_pool_table_scene(Room.in_shooting_mode, Room.shooting_angle)
        collisionList.append(Collision(8,4,0,0)) #Create collision box for pool table

        # Place the corner table in the bottom-left corner
        glPushMatrix()  # Save current transformation matrix
        glTranslatef(-ROOM_WIDTH/2 + 1.3, 0, -ROOM_DEPTH/2 + 1.3)  # Move to corner
        Components.draw_table_with_lamp(2, 2, Room.dice_frame)  # Draw table
        collisionList.append(Collision(2,2,-ROOM_WIDTH/2 +1.3,-ROOM_DEPTH/2 + 1.3)) #Create collision box for table
        glPopMatrix()  # Restore previous transformation matrix

        glPushMatrix()  # Save current transformation matrix
        glTranslatef(0, ROOM_HEIGHT - 0.4, 0)  # Move to Center
        Components.draw_red_ball()
        glPopMatrix()  # Restore previous transformation matrix

        glPushMatrix()  # Save current transformation matrix
        glTranslatef(0 , ROOM_HEIGHT - 6, 0)  # Move to ceiling
        hanging_light_equation = Room.swing_factor * math.sin(0.03 * Room.hanging_light_frame)
        Components.draw_animated_hanging_spotlight(hanging_light_equation)
        glPopMatrix()  # Restore previous transformation matrix

        if self.show_picture:
            # Add a frame to the back wall
            glPushMatrix()
            glTranslatef(0, ROOM_HEIGHT / 2, -ROOM_DEPTH / 2 + 0.25)  # Center frame on the back wall and move aout a little
            glRotatef(90, 0, 0, -1)  # Rotate 90 degrees clockwise around the Z-axis
            Components.draw_framed_picture(3, 1.2, 3)  # Frame size: 3x3   
            glPopMatrix()



    def display(self):
        """Main display function"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        

        self.camera.setProjection()
        self.camera.placeCamera()
        
        self.setup_lights()
        self.show_picture = self.should_we_show_picture()
        self.draw_room()

        self.animate()
        self.draw_components()
        
        pygame.display.flip()


    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_input()
            self.display()
            self.clock.tick(FPS)


def main():
    room = Room()
    room.run()
    pygame.quit()


if __name__ == "__main__":
    main()