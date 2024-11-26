
from materials import *
from textures import *
from basic_shapes import *
from utils import Vector

class PoolBall:

    def __init__(self, has_texture, texture_name, is_cue):
        
        self.radius = 0.186 # Standard radius (in feet) for a pool ball

        self.position_x = 0
        self.position_z = 0

        self.rotation_x = 0
        self.rotation_z = 0

        self.power = 0

        point = Point(0,0,0)
        self.direction = Vector(point,point) 

        # Confine the ball to our table (Our table is 7.7 units long, 3.7 units wide, and centered at the origin)
        self.max_x = 7.7/2
        self.min_x = -7.7/2

        self.max_z = 3.7/2
        self.min_z = -3.7/2


        self.has_texture = has_texture
    
        if has_texture:
            self.texture = texture_name

        if is_cue or has_texture:
            self.material = Materials.BALL_RESIN
        else:
           self.material = Materials.SILVER


    def set_config(self, position_x, position_z, rotation_x, rotation_z):
        
        self.position_x = position_x
        self.position_z = position_z

        self.rotation_x = rotation_x
        self.rotation_z = rotation_z


    def draw(self):

        # Set the materials/texture

        Materials.set_material(GL_FRONT, self.material)
        if self.has_texture:
            Textures.set_texture(self.texture)

        BasicShapes.draw_animated_sphere(self.radius, self.position_x, self.position_z, self.rotation_x, self.rotation_z)

        if self.power != 0:
            i = 1 + 2

    @staticmethod
    def draw_dash(cue_ball, angle, dashNum):
        dashX = cue_ball.position_x + ((.48) * dashNum) * math.cos(math.radians(angle))
        dashZ = cue_ball.position_z + ((.48) * dashNum) * math.sin(math.radians(angle))
        glPushMatrix()

        # Go to the center of the ball
        if dashNum == 1:
            glTranslate(cue_ball.position_x, .075, cue_ball.position_z)
            glRotate(angle, 0, 1, 0)
        else:
            glTranslate(.4, 0, 0)
        
        

        # move to the edge of the ball
        # glTranslate(cue_ball.radius * 2, 0, 0) 
        
        # Line is confined to the table space of 7.7 * 3.7
        
        # Draw the dashed line
        space = 1.2  # aprox 2 in
        # glTranslate(space, 0, 0)
        # Rotate the aim
        
        BasicShapes.draw_white_rectangle(.08, 0.125, 0.04) # line is 1.5 in wide, 0.5 in tall
        if dashNum == 10:
            print(cue_ball.position_x + ((.48) * dashNum) * math.cos(math.radians(angle)))
        if (dashX < 4.6 and  dashX > -4 and dashZ < 2 and dashZ > -2):
            PoolBall.draw_dash(cue_ball,angle, dashNum + 1)
        glPopMatrix()