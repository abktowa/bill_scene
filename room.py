import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import math
from utils import Point
from camera import Camera
from textures import *
from materials import *
from components import *

# Window settings
window_dimensions = (1200, 800)
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FPS = 60

# Room dimensions
ROOM_WIDTH = 15.0
ROOM_HEIGHT = 8.0
ROOM_DEPTH = 15.0

# Camera settings
CAM_ANGLE = 60.0
CAM_NEAR = 0.01
CAM_FAR = 1000.0
INITIAL_EYE = Point(0, 2, 8)
INITIAL_LOOK_ANGLE = 0

class Room:

    def __init__(self):
        pygame.init()
        pygame.display.set_mode(window_dimensions, pygame.DOUBLEBUF | pygame.OPENGL)
        self.clock = pygame.time.Clock()
        
        self.camera = Camera(CAM_ANGLE, window_dimensions[0]/window_dimensions[1], CAM_NEAR, CAM_FAR, 
                           INITIAL_EYE, INITIAL_LOOK_ANGLE)
        
        self.init_gl()
        self.create_textures()
        
        # Light states
        self.lights = {
            'main': True,
            'spotlight': True,
            'desk': True,
            'red': True,
            'green': True,
            'blue': True
        }
        
        self.running = True


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
                elif event.key == pygame.K_h:  # Home position
                    self.camera.eye = INITIAL_EYE
                    self.camera.lookAngle = INITIAL_LOOK_ANGLE
                elif event.key in [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]:
                    light_index = event.key - pygame.K_0
                    self.toggle_light(light_index)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.camera.slide(0, 0, -0.1)
        if keys[pygame.K_s]:
            self.camera.slide(0, 0, 0.1)
        if keys[pygame.K_a]:
            self.camera.turn(1)
        if keys[pygame.K_d]:
            self.camera.turn(-1)   


    def setup_lights(self):
        """Setup all lights in the scene"""
        # Main ceiling light
        if self.lights['main']:
            glEnable(GL_LIGHT0)
            glLightfv(GL_LIGHT0, GL_POSITION, [0, ROOM_HEIGHT-0.1, 0, 1])
            glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
            glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        else:
            glDisable(GL_LIGHT0)

        # Spotlight over pool table
        if self.lights['spotlight']:
            glEnable(GL_LIGHT1)
            glLightfv(GL_LIGHT1, GL_POSITION, [0, ROOM_HEIGHT-0.5, 0, 1])
            glLightfv(GL_LIGHT1, GL_SPOT_DIRECTION, [0, -1, 0])
            glLightf(GL_LIGHT1, GL_SPOT_CUTOFF, 30.0)
            glLightf(GL_LIGHT1, GL_SPOT_EXPONENT, 2.0)
            glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.5, 0.5, 0.2, 1.0])
        else:
            glDisable(GL_LIGHT1)


    def toggle_light(self, index):
        """Toggle specific light based on index"""
        light_names = ['main', 'spotlight', 'desk', 'red', 'green', 'blue']
        if index < len(light_names):
            self.lights[light_names[index]] = not self.lights[light_names[index]]


    def create_textures(self):
        """Create all textures"""
        self.textures = {
            'floor': Textures.create_checkerboard_texture(),
            'wall': Textures.create_wall_texture(),
            'ceiling': Textures.create_ceiling_texture()
        }


    def draw_room(self):
        """Draw the room with textured walls, floor, and ceiling"""
        glEnable(GL_TEXTURE_2D)  # Enable texture
        glEnable(GL_COLOR_MATERIAL) # Allows glColor* to set material colors

        # Floor with checkerboard texture
        glBindTexture(GL_TEXTURE_2D, self.textures['floor'])
        glBegin(GL_QUADS)
        glNormal3f(0, 1, 0)
        glTexCoord2f(0, 0); glVertex3f(-ROOM_WIDTH/2, 0, -ROOM_DEPTH/2)
        glTexCoord2f(0, 4); glVertex3f(-ROOM_WIDTH/2, 0, ROOM_DEPTH/2)
        glTexCoord2f(4, 4); glVertex3f(ROOM_WIDTH/2, 0, ROOM_DEPTH/2)
        glTexCoord2f(4, 0); glVertex3f(ROOM_WIDTH/2, 0, -ROOM_DEPTH/2)
        glEnd()

        # Walls
        glBindTexture(GL_TEXTURE_2D, self.textures['wall'])
        
        # Back wall
        glBegin(GL_QUADS)
        glNormal3f(0, 0, 1)
        glTexCoord2f(0, 0); glVertex3f(-ROOM_WIDTH/2, 0, -ROOM_DEPTH/2)
        glTexCoord2f(2, 0); glVertex3f(ROOM_WIDTH/2, 0, -ROOM_DEPTH/2)
        glTexCoord2f(2, 1); glVertex3f(ROOM_WIDTH/2, ROOM_HEIGHT, -ROOM_DEPTH/2)
        glTexCoord2f(0, 1); glVertex3f(-ROOM_WIDTH/2, ROOM_HEIGHT, -ROOM_DEPTH/2)
        glEnd()

        # Front wall
        glBegin(GL_QUADS)
        glNormal3f(0, 0, -1)
        glTexCoord2f(0, 0); glVertex3f(-ROOM_WIDTH/2, 0, ROOM_DEPTH/2)
        glTexCoord2f(2, 0); glVertex3f(ROOM_WIDTH/2, 0, ROOM_DEPTH/2)
        glTexCoord2f(2, 1); glVertex3f(ROOM_WIDTH/2, ROOM_HEIGHT, ROOM_DEPTH/2)
        glTexCoord2f(0, 1); glVertex3f(-ROOM_WIDTH/2, ROOM_HEIGHT, ROOM_DEPTH/2)
        glEnd()

        # Left wall
        glBegin(GL_QUADS)
        glNormal3f(1, 0, 0)
        glTexCoord2f(0, 0); glVertex3f(-ROOM_WIDTH/2, 0, -ROOM_DEPTH/2)
        glTexCoord2f(2, 0); glVertex3f(-ROOM_WIDTH/2, 0, ROOM_DEPTH/2)
        glTexCoord2f(2, 1); glVertex3f(-ROOM_WIDTH/2, ROOM_HEIGHT, ROOM_DEPTH/2)
        glTexCoord2f(0, 1); glVertex3f(-ROOM_WIDTH/2, ROOM_HEIGHT, -ROOM_DEPTH/2)
        glEnd()

        # Right wall
        glBegin(GL_QUADS)
        glNormal3f(-1, 0, 0)
        glTexCoord2f(0, 0); glVertex3f(ROOM_WIDTH/2, 0, -ROOM_DEPTH/2)
        glTexCoord2f(2, 0); glVertex3f(ROOM_WIDTH/2, 0, ROOM_DEPTH/2)
        glTexCoord2f(2, 1); glVertex3f(ROOM_WIDTH/2, ROOM_HEIGHT, ROOM_DEPTH/2)
        glTexCoord2f(0, 1); glVertex3f(ROOM_WIDTH/2, ROOM_HEIGHT, -ROOM_DEPTH/2)
        glEnd()

        # Ceiling
        glBindTexture(GL_TEXTURE_2D, self.textures['ceiling'])
        glBegin(GL_QUADS)
        glNormal3f(0, -1, 0)
        glTexCoord2f(0, 0); glVertex3f(-ROOM_WIDTH/2, ROOM_HEIGHT, -ROOM_DEPTH/2)
        glTexCoord2f(2, 0); glVertex3f(ROOM_WIDTH/2, ROOM_HEIGHT, -ROOM_DEPTH/2)
        glTexCoord2f(2, 2); glVertex3f(ROOM_WIDTH/2, ROOM_HEIGHT, ROOM_DEPTH/2)
        glTexCoord2f(0, 2); glVertex3f(-ROOM_WIDTH/2, ROOM_HEIGHT, ROOM_DEPTH/2)
        glEnd()

        glDisable(GL_COLOR_MATERIAL) # Disable glColor* from setting material colors to allow custom materials
        glDisable(GL_TEXTURE_2D)  # Disable texture


    def draw_components(self):
        
        Materials.set_material(GL_FRONT, Materials.WOOD)
        Components.draw_elegant_table(5, 3)

         # Place the corner table in the bottom-left corner
        glPushMatrix()  # Save current transformation matrix
        glTranslatef(-ROOM_WIDTH/2 + 2.5, 0, -ROOM_DEPTH/2 + 1.5)  # Move to corner
        Components.draw_table_with_lamp(2, 2)  # Draw table
        glPopMatrix()  # Restore previous transformation matrix


    def display(self):
        """Main display function"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        self.camera.setProjection()
        self.camera.placeCamera()
        
        self.setup_lights()
        self.draw_room()
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