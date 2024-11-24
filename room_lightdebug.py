import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import math
from utils import Point
from camera import Camera
from textures import *
from materials import *
from components import *
from initialize_textures import *
from light import Light

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

class Room:
    def __init__(self):
        pygame.init()
        pygame.display.set_mode(window_dimensions, pygame.DOUBLEBUF | pygame.OPENGL)
        self.clock = pygame.time.Clock()
        
        self.camera = Camera(CAM_ANGLE, window_dimensions[0]/window_dimensions[1], CAM_NEAR, CAM_FAR, 
                           INITIAL_EYE, INITIAL_LOOK_ANGLE)
        
        self.init_gl()
        self.create_textures()
        
        # MANAGE LIGHT STATE
        self.lights = {
            'main': Light(GL_LIGHT0, [0, ROOM_HEIGHT - 0.1, 0, 1], ambient=[0.5, 0.5, 0.5, 0.7], 
                        diffuse=[1.0, 1.0, 1.0, 1.0], specular=[1.0, 1.0, 1.0, 1.0]),
            # 'spotlight': Light(GL_LIGHT1, [0, ROOM_HEIGHT - 0.5, 0, 1], ambient=[0.0, 0.0, 0.0, 1.0],
                         # diffuse=[0.5, 0.5, 0.2, 1.0], specular=[1.0, 1.0, 1.0, 1.0]),
            'red': Light(GL_LIGHT2, [-6, ROOM_HEIGHT - 1.0, -5, 1], ambient=[0.0, 0.0, 0.0, 0.2], 
                        diffuse=[1.0, 0.0, 0.0, 1.0], specular=[1.0, 0.0, 0.0, 1.0]),
            'green': Light(GL_LIGHT3, [0, ROOM_HEIGHT - 1.0, -5, 1], ambient=[0.0, 0.0, 0.0, 0.2], 
                        diffuse=[0.0, 1.0, 0.0, 1.0], specular=[0.0, 1.0, 0.0, 1.0]),
            'blue': Light(GL_LIGHT4, [6, ROOM_HEIGHT - 1.0, -5, 1], ambient=[0.0, 0.0, 0.0, 0.2], 
                        diffuse=[0.0, 0.0, 1.0, 1.0], specular=[0.0, 0.0, 1.0, 1.0])
            # ADD MORE LIGHTS HERE
        }
        
        self.running = True


    def init_gl(self):
        """Initialize OpenGL settings"""
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_NORMALIZE)
        glEnable(GL_TEXTURE_2D)

        # Lighting model (global ambient light)
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
        
        # Set material properties for the whole scene to ensure it reflects light appropriately
        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.5, 0.5, 0.5, 1.0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
        glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glMaterialf(GL_FRONT, GL_SHININESS, 50.0)

        # Enable the main lights
        # glEnable(GL_LIGHT0)
        # glEnable(GL_LIGHT1)


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

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.camera.slide(0, 0, -0.1)
        if keys[pygame.K_s]:
            self.camera.slide(0, 0, 0.1)
        if keys[pygame.K_a]:
            self.camera.slide(-0.1, 0, 0)
        if keys[pygame.K_d]:
            self.camera.slide(0.1, 0, 0)
        if keys[pygame.K_LEFT]:
            self.camera.turn(1)
        if keys[pygame.K_RIGHT]:
            self.camera.turn(-1)
        if keys[pygame.K_DOWN]:
            self.camera.rise(-1)
        if keys[pygame.K_UP]:
            self.camera.rise(1)
        if keys[pygame.K_1]:
            self.toggle_light(0)
        if keys[pygame.K_2]:
            self.toggle_light(1)
        if keys[pygame.K_3]:
            self.toggle_light(2)
        if keys[pygame.K_9]:
            self.toggle_light(3)


    def setup_lights(self):
        """Setup all lights in the scene"""
        Light.place_flashlight(GL_LIGHT5)
        main_light = self.lights['main']
        for light_name, light in self.lights.items():
            if light.is_enabled:
                # Place the light
                light.place_light()
            
            # Set light attenuation to ensure it illuminates fully without fall-off
            if light_name == 'main':
                glLightf(light.light_id, GL_CONSTANT_ATTENUATION, 1.0)
                glLightf(light.light_id, GL_LINEAR_ATTENUATION, 0.0)
                glLightf(light.light_id, GL_QUADRATIC_ATTENUATION, 0.0)
            else:
                glDisable(light.light_id)

    def toggle_light(self, index):
        """Toggle specific light based on index"""
        light_names = list(self.lights.keys())
        if index < len(light_names):
            light = self.lights[light_names[index]]
            if light.is_enabled:
                light.turn_off()
            else:
                light.turn_on()

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
        """Draw additional components like pool table and lamps"""
        Components.draw_animated_pool_table_scene(True, 0)

        # Place the corner table in the bottom-left corner
        glPushMatrix()
        glTranslatef(-ROOM_WIDTH / 2 + 1.3, 0, -ROOM_DEPTH / 2 + 1.3)  # Move to corner
        Components.draw_table_with_lamp(2, 2, 0)  # Draw table with lamp
        glPopMatrix()


    def display(self):
        """Main display function"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.camera.setProjection()
        self.camera.placeCamera()

        self.setup_lights()
        self.draw_room()
        self.draw_components()

        for light_name, light in self.lights.items():
            if light_name != 'main':
                light.draw_light_indicator()

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