from OpenGL.GLU import *
from OpenGL.GL import *

class Materials:
	
	# Material class with properties for ambient, diffuse, specular, and shininess
	class Material:
		def __init__(self, ambient, diffuse, specular, shininess):
			self.ambient = ambient
			self.diffuse = diffuse
			self.specular = specular
			self.shininess = shininess
	
	# A list of materials

	# To add a new material, use the following format:
	# MaterialName = Material(
	#     [ambient_red, ambient_green, ambient_blue, ambient_alpha],  
	#     [diffuse_red, diffuse_green, diffuse_blue, diffuse_alpha],  
	#     [specular_red, specular_green, specular_blue, specular_alpha], 
	#     shininess_value  
	# )
	# You can look up material properties online.

	# Pool Table Materials
	Wood = Material([0.3, 0.2, 0.1, 1.0], [0.6, 0.4, 0.2, 1.0], [0.4, 0.4, 0.3, 1.0], 25.0)
	GreenFelt = Material([0.1, 0.2, 0.1, 1.0], [0.3, 0.6, 0.3, 1.0], [0.4, 0.4, 0.4, 1.0], 10.0)
	BallPlastic = Material([0.8, 0.8, 0.8, 1.0], [1.0, 1.0, 1.0, 1.0], [0.2, 0.2, 0.2, 1.0], 10.0)
	BallResin = Material([0.9, 0.9, 0.9, 1.0], [1.0, 1.0, 1.0, 1.0], [0.6, 0.6, 0.6, 1.0], 30.0)
	RubberBumper = Material([0.05, 0.05, 0.05, 1.0], [0.2, 0.2, 0.2, 1.0], [0.1, 0.1, 0.1, 1.0], 5.0)

	# Common Materials
	Brass = Material([0.329412, 0.223529, 0.027451, 1.0], [0.780392, 0.568627, 0.113725, 1.0], [0.992157, 0.941176, 0.807843, 1.0], 27.8974)
	Bronze = Material([0.2125, 0.1275, 0.054, 1.0], [0.714, 0.4284, 0.18144, 1.0], [0.393548, 0.271906, 0.166721, 1.0], 25.6)
	Chrome = Material([0.25, 0.25, 0.25, 1.0], [0.4, 0.4, 0.4, 1.0], [0.774597, 0.774597, 0.774597, 1.0], 76.8)
	Copper = Material([0.19125, 0.0735, 0.0225, 1.0], [0.256777, 0.137622, 0.086014, 1.0], [0.256777, 0.137622, 0.086014, 1.0], 128.0)
	Emerald = Material([0.0215, 0.1745, 0.0215, 0.55], [0.07568, 0.61424, 0.07568, 0.55], [0.633, 0.727811, 0.633, 0.55], 76.8)
	Gold = Material([0.24725, 0.1995, 0.0745, 1.0], [0.75164, 0.60648, 0.22648, 1.0], [0.628281, 0.555802, 0.366065, 1.0], 51.2)
	Jade = Material([0.135, 0.2225, 0.1575, 0.95], [0.54, 0.89, 0.63, 0.95], [0.316228, 0.316228, 0.316228, 0.95], 12.8)
	Obsidian = Material([0.05375, 0.05, 0.06625, 1.0], [0.18275, 0.17, 0.22525, 1.0], [0.332741, 0.328634, 0.346435, 1.0], 38.4)
	Pewter = Material([0.10588, 0.058824, 0.113725, 1.0],[0.427451, 0.470588, 0.541176, 1.0],[0.3333, 0.3333, 0.521569, 1.0],9.84615)	
	Plastic = Material([0.0, 0.0, 0.0, 1.0], [0.55, 0.55, 0.55, 1.0], [0.7, 0.7, 0.7, 1.0], 32.0)
	Rubber = Material([0.02, 0.02, 0.02, 1.0], [0.01, 0.01, 0.01, 1.0], [0.4, 0.4, 0.4, 1.0], 10.0)
	Silver = Material([0.19225, 0.19225, 0.19225, 1.0], [0.50754, 0.50754, 0.50754, 1.0], [0.508273, 0.508273, 0.508273, 1.0], 51.2)
	Turquoise = Material([0.1, 0.18725, 0.1745, 0.8], [0.396, 0.74151, 0.69102, 0.8], [0.297254, 0.30829, 0.306678, 0.8], 12.8)

		
	@staticmethod
	def set_material(face, material):
		"""
		Sets material properties for a specified face of a polygon.

		Parameters:
		face -- Specifies the polygon face, options are:
		  - GL_FRONT: Apply material to the front-facing side of polygons.
		  - GL_BACK: Apply material to the back-facing side of polygons.
		  - GL_FRONT_AND_BACK: Apply material to both front and back sides.
		material -- Material instance, such as Materials.Copper or Materials.Pewter.
		"""

		glMaterialfv(face, GL_AMBIENT, material.ambient)
		glMaterialfv(face, GL_DIFFUSE, material.diffuse)
		glMaterialfv(face, GL_SPECULAR, material.specular)
		glMaterialf(face, GL_SHININESS, material.shininess)

