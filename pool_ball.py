
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
        self.max_x = (7.7/2) - self.radius
        self.min_x = -7.7/2 + self.radius

        self.max_z = 3.7/2 - self.radius
        self.min_z = -3.7/2 + self.radius


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
            self.position_x += (self.direction.dx * self.power)
            self.position_z += (self.direction.dz * self.power)
            self.power *= .963
            if self.power < .005:
                self.power = 0
            if self.position_x >= self.max_x and self.direction.dx > 0:
                self.direction.dx *= -1
            if self.position_x <= self.min_x and self.direction.dx < 0:
                self.direction.dx *= -1
            if self.position_z >= self.max_z and self.direction.dz > 0:
                self.direction.dz *= -1
            if self.position_z <= self.min_z and self.direction.dz < 0:
                self.direction.dz *= -1

    @staticmethod
    def draw_dash(cue_ball, angle, dashNum):
        dashX = cue_ball.position_x + ((.48) * dashNum) * math.cos(math.radians(angle))
        dashZ = cue_ball.position_z + ((-.48) * dashNum) * math.sin(math.radians(angle))
        space = .4  # aprox 4.8 in
        glPushMatrix()

        # Go to the center of the ball
        if dashNum == 1:
            glTranslate(cue_ball.position_x, .075, cue_ball.position_z)
            glRotate(angle, 0, 1, 0)
        else:
            glTranslate(space, 0, 0)
        
        
        
        Materials.set_material(GL_FRONT, Materials.BALL_RESIN)
        BasicShapes.draw_rectangle(.08, 0.125, 0.04) # line is 1.5 in wide, 0.5 in tall
        if dashNum == 10:
            print(cue_ball.position_x + ((.48) * dashNum) * math.cos(math.radians(angle)))
        if (dashX < 4.6 and  dashX > -4 and dashZ < 2 and dashZ > -2):
            PoolBall.draw_dash(cue_ball,angle, dashNum + 1)
        glPopMatrix()