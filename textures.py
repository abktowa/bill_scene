"""
This class containes the textures for our projects

"""

from OpenGL.GL import *
from OpenGL.GLU import *

class Textures:
        
        def create_checkerboard_texture():
            # Professor Duncan told in the project that we need a checkerboard pattern for the floor so for that
            # First, we ask OpenGL to give us a new texture (Think of it like wallpaper or gift wrapping paper that you apply to an object.) ID (like getting a new blank canvas)
            texture = glGenTextures(1)
            # Tell OpenGL we want to work on this texture (like picking up our canvas to draw on it)
            glBindTexture(GL_TEXTURE_2D, texture)
            
            size = 64
            checker_size = 8
            # Each checker square will be 8x8 pixels
            # This list will hold all our colors (we'll fill it with numbers for black and white)
            data = []
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

        def create_wall_texture():
            """Create a simple solid color texture for walls"""
            texture = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture)
            
            size = 64
            # Light gray color for walls
            gray_level = 192
            color = [gray_level, gray_level, gray_level]  # Light gray
            data = []
            
            # Fill the entire texture with the same color
            for i in range(size * size):
                data.extend(color)
                        
            data = bytes(data)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, size, size, 0, GL_RGB, GL_UNSIGNED_BYTE, data)
            
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            return texture

        def create_ceiling_texture():
            """Create a simple solid color texture for ceiling"""
            texture = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture)
            
            size = 64
            # Dark gray color for ceiling
            gray_level = 84
            color = [gray_level, gray_level, gray_level]  # Dark gray
            data = []
            
            # Fill the entire texture with the same color
            for i in range(size * size):
                data.extend(color)
                        
            data = bytes(data)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, size, size, 0, GL_RGB, GL_UNSIGNED_BYTE, data)
            
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            return texture