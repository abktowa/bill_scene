import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import math
from utils import Point
from camera import Camera

# Window settings
window_dimensions = (1200, 800)
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FPS = 60

# Room dimensions
ROOM_WIDTH = 10.0
ROOM_HEIGHT = 4.0
ROOM_DEPTH = 10.0

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
        glEnable(GL_COLOR_MATERIAL)
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

    def create_checkerboard_texture(self):
        # Professor Duncan told in the project that we need a checkerboard pattern for the floor so for that
        # First, we ask OpenGL to give us a new texture(Think of it like wallpaper or gift wrapping paper that you apply to an object.) ID (like getting a new blank canvas)
        texture = glGenTextures(1)
        # Tell OpenGL we want to work on this texture (like picking up our canvas to draw on it)
        glBindTexture(GL_TEXTURE_2D, texture)
        
        size = 64
        checker_size = 8
        # Each checker square will be 8x8 pixels
        # This list will hold all our colors (we'll fill it with numbers for black and white)
        data = []
        # This list will hold all our colors (we'll fill it with numbers for black and white)
        # The Logic:
    # 1. We have a big 64x64 pixel image
    # 2. We want to make checker squares that are 8x8 pixels each
    # 3. So our image will have 8 checker squares across and 8 down (64 ÷ 8 = 8)
    # 4. When the texture repeats 4 times on the floor, we'll see 32x32 checker squares!
    
# Loop through each pixel in our 64x64 image
        for i in range(size): # 0-63 rows iterate
            for j in range(size):  #0-63 columns
            # i // checker_size -> Divides row number by 8, dropping the remainder
            # j // checker_size -> Divides column number by 8, dropping the remainder
            # When we add these and check if the sum is odd or even,
            # we get alternating squares!
            
            # Example:
            # For pixel (0,0):  0//8 + 0//8 = 0 + 0 = 0 (even = white)
            # For pixel (0,8):  0//8 + 8//8 = 0 + 1 = 1 (odd = black)
            # For pixel (8,0):  8//8 + 0//8 = 1 + 0 = 1 (odd = black)
            # For pixel (8,8):  8//8 + 8//8 = 1 + 1 = 2 (even = white)
                if ((i // checker_size) + (j // checker_size)) % 2:
                     # If the sum is odd, make this pixel black
                    data.extend([0, 0, 0])  # Black square
                else:
                    # If the sum is even, make this pixel white
                    data.extend([255, 255, 255])  # White square
         # Convert our list of numbers to bytes (the format OpenGL expects)            
        data = bytes(data)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, size, size, 0, GL_RGB, GL_UNSIGNED_BYTE, data)
        # Tell OpenGL how to handle the texture when it's stretched or shrunk
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        return texture

    def create_wall_texture(self):
        """Create a simple solid color texture for walls"""
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        
        size = 64
        # Light gray color for walls
        color = [192, 192, 192]  # Light gray
        data = []
        
        # Fill the entire texture with the same color
        for i in range(size * size):
            data.extend(color)
                    
        data = bytes(data)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, size, size, 0, GL_RGB, GL_UNSIGNED_BYTE, data)
        
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        return texture

    def create_ceiling_texture(self):
        """Create a simple solid color texture for ceiling"""
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        
        size = 64
        # Dark gray color for ceiling
        color = [64, 64, 64]  # Dark gray
        data = []
        
        # Fill the entire texture with the same color
        for i in range(size * size):
            data.extend(color)
                    
        data = bytes(data)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, size, size, 0, GL_RGB, GL_UNSIGNED_BYTE, data)
        
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        return texture

    def create_textures(self):
        """Create all textures"""
        self.textures = {
            'floor': self.create_checkerboard_texture(),
            'wall': self.create_wall_texture(),
            'ceiling': self.create_ceiling_texture()
        }

    def draw_room(self):
        """Draw the room with textured walls, floor, and ceiling"""
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

    def toggle_light(self, index):
        """Toggle specific light based on index"""
        light_names = ['main', 'spotlight', 'desk', 'red', 'green', 'blue']
        if index < len(light_names):
            self.lights[light_names[index]] = not self.lights[light_names[index]]

    def display(self):
        """Main display function"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        self.camera.setProjection()
        self.camera.placeCamera()
        
        self.setup_lights()
        self.draw_room()
        
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