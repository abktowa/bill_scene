
from materials import *
from utils import Vector

class PoolBall:

    def __init__(self, has_texture, texture_name, is_cue):
        
        self.position_x = 0
        self.position_z = 0

        self.rotation_x = 0
        self.rotation_z = 0

        self.power = 0
        self.direction = Vector(0,0,0)

        if has_texture:
            texture = texture_name

        if is_cue or has_texture:
            material = Materials.BALL_RESIN
        else:
            material = Materials.SILVER


    def set_config(self, position_x, position_z, rotation_x, rotation_z):
        
        self.position_x = position_x
        self.position_z = position_z

        self.rotation_x = rotation_x
        self.rotation_z = rotation_z

    def draw(self):

        if self.power != 0:
            i = 1 + 2