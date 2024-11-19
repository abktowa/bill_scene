"""
This class contains the functions for drawing basic shapes, 
They can be used to construct the complex components in out scene.


Here are some some example calls to functions in this class:

BasicShapes.draw_sphere(1) # (radius)
BasicShapes.draw_rectangle(3,3,3) # (length, width, height)
BasicShapes.draw_pyramid(3,3) # (base, height)
BasicShapes.draw_prism(8,1,2) # (sides, height, side_length)
BasicShapes.draw_cone(1,3) # (radius, height)
BasicShapes.draw_cylinder(1,3) # (radius, height)
"""

from OpenGL.GLU import *
from OpenGL.GL import *
from utils import *
import math


class BasicShapes:

    def draw_sphere(radius):
        quad = gluNewQuadric()  # Create a new quadric for the sphere
        
        glPushMatrix()  # Save the current matrix
        glTranslatef(0.0, radius, 0.0)  # Translate to place sphere on the y = 0 plane
        
        # Draw the sphere with specified radius, smooth appearance with 32 slices and stacks
        gluSphere(quad, radius, 32, 32)
        
        glPopMatrix()  # Restore the previous matrix state
        gluDeleteQuadric(quad)  # Clean up the quadric object


    # Draws a rectangle, with the following three paramates:
    # length is the distance in the x direction, width is in the z direction, and height is in the y direction
    def draw_rectangle(length, width, height):
        glPushMatrix()

        # Calculate half length and width sizes (for centering the pyramid on the x and z axes)
        half_length = length/2
        half_width = width/2

        # Define vertices for a rectangle
        vertices = [
            [-half_length, 0, -half_width],       # Vertex 0
            [half_length, 0, -half_width],        # Vertex 1
            [half_length, height, -half_width],   # Vertex 2
            [-half_length, height, -half_width],  # Vertex 3
            [-half_length, 0, half_width],        # Vertex 4
            [half_length, 0, half_width],         # Vertex 5
            [half_length, height, half_width],    # Vertex 6
            [-half_length, height, half_width]    # Vertex 7
        ]

        # Defines the rectangle faces created by the given vertices
        # For example the first face is the bottom, created with vertices 0,1,2 and 3 above
        faces = [
            (0, 3, 2, 1), # Face 1 (bottom) #
            (3, 7, 6, 2), # Face 2 (back) #
            (7, 4, 5, 6), # Face 3 (top) #
            (0, 1, 5, 4), # Face 4 (front) #
            (0, 4, 7, 3), # Face 5 (left) 
            (1, 2, 6, 5)  # Face 6 (right)
        ]
        
        # Draw the cube
        glBegin(GL_QUADS)
        for face in faces:
            for vertex in face:
                glVertex3fv(vertices[vertex])
        glEnd()

        glPopMatrix()

        """
        Visual repersentation with vertexes labled:

          7 ──────── 6
          /|        /|
         / |       / |
        4 ──────── 5 |
        |  |      |  |
        |  |      |  |
        |  3 ─────── 2
        | /       | /
        |/        |/
       0 ──────── 1

        """

    # Function to draw a dice

    def draw_cube(length, width, height):
        glPushMatrix()

        # Calculate half length and width sizes (for centering the pyramid on the x and z axes)
        half_length = length/2
        half_width = width/2

        # Define vertices for a rectangle
        vertices = [
            [-half_length, 0, -half_width],       # Vertex 0
            [half_length, 0, -half_width],        # Vertex 1
            [half_length, height, -half_width],   # Vertex 2
            [-half_length, height, -half_width],  # Vertex 3
            [-half_length, 0, half_width],        # Vertex 4
            [half_length, 0, half_width],         # Vertex 5
            [half_length, height, half_width],    # Vertex 6
            [-half_length, height, half_width]    # Vertex 7
        ]

        # Defines the rectangle faces created by the given vertices
        # For example the first face is the bottom, created with vertices 0,1,2 and 3 above
        faces = [
            (0, 3, 2, 1), # Face 1 (bottom) #
            (3, 7, 6, 2), # Face 2 (back) #
            (7, 4, 5, 6), # Face 3 (top) #
            (0, 1, 5, 4), # Face 4 (front) #
            (0, 4, 7, 3), # Face 5 (left) 
            (1, 2, 6, 5)  # Face 6 (right)
        ]
        
        # Draw the cube
        glBegin(GL_QUADS)
        for face in faces:
            for vertex in face:
                glVertex3fv(vertices[vertex])
        glEnd()

        glPopMatrix()
        
    # Function to generate a standard pyramid
    def draw_pyramid(base_size, height):
        BasicShapes.draw_rectangular_pyramid(base_size, base_size, height)


    # Function to generate a pyramid with a rectangular base
    def draw_rectangular_pyramid(base_width, base_length, height):
        glPushMatrix()
        # Calculate half base size (for centering the pyramid on the x and z axes)
        half_width = base_width / 2.0
        half_length = base_length / 2.0

        # Define the vertices for the pyramid
        vertices = [
            # Base vertices (rectangle base)
            [-half_width, 0.0, -half_length],  # 0
            [ half_width, 0.0, -half_length],  # 1
            [ half_width, 0.0,  half_length],  # 2
            [-half_width, 0.0,  half_length],  # 3

            # Apex of the pyramid
            [0.0, height, 0.0]  # 4 (Apex)
        ]
        
        # Define the indices for the triangles (4 sides + base)
        indices = [
            # Sides (4 triangles)
            [0, 4, 1],  # Triangle 1
            [1, 4, 2],  # Triangle 2
            [2, 4, 3],  # Triangle 3
            [3, 4, 0],  # Triangle 4

            # Base (1 square, 2 triangles)
            [0, 1, 2],  # Triangle 5
            [0, 2, 3]   # Triangle 6
        ]

        # Begin drawing triangles
        glBegin(GL_TRIANGLES)
        for face in indices:
            for vertex in face:
                glVertex3fv(vertices[vertex])
        glEnd()

        glPopMatrix()

        """
        Visual repersentation with vertexes labled:

               4
              /|\
             / | \
            /  |  \
           /   |   \ 
          /    |    \
        3 _____|______ 2
         \     |       \ 
          \    |        \
           \   |         \
            \  |          \
               0 __________ 1 
                           
        """

    def draw_cone(base_radius, height, slices=32, stacks=1):
        glPushMatrix()
        glRotatef(270, 1.0, 0.0, 0.0)  # Rotate the cone to be vertical along the Y-axis
        quadric = gluNewQuadric()
        gluCylinder(quadric, base_radius, 0.0, height, slices, stacks)  # Create the cone
        gluDeleteQuadric(quadric)
        glPopMatrix()

    def draw_cylinder(radius, height, slices=32, stacks=1):
        glPushMatrix()
        glRotatef(270, 1.0, 0.0, 0.0)  # Rotate the cylinder to be vertical along the Y-axis
        quadric = gluNewQuadric()
        gluCylinder(quadric, radius, radius, height, slices, stacks)  # Create the cylinder
        gluDeleteQuadric(quadric)
        glPopMatrix()

    def draw_adjustable_cylinder(bottom_radius, top_radius, height, slices=32, stacks=1):
        glPushMatrix()
        glRotatef(270, 1.0, 0.0, 0.0)  # Rotate the cylinder to be vertical along the Y-axis
        quadric = gluNewQuadric()
        gluCylinder(quadric, bottom_radius, top_radius, height, slices, stacks)  # Create the cylinder
        gluDeleteQuadric(quadric)
        glPopMatrix()

    #=======================================
    # Prism functions
    #=======================================

    def draw_prism(sides, height, side_length):
        glPushMatrix()

        glTranslatef(0.0, height / 2, 0.0)  # Center the prism so it rests on the ground at y=0

        # Generate the vertices and faces based on the number of sides, height, and side length
        vertices = BasicShapes.generate_prism_vertices(sides, height, side_length)
        lat_faces = BasicShapes.generate_prism_lateral_faces(sides)
        bases = BasicShapes.generate_prism_bases(sides)

        # Draw the lateral faces
        glBegin(GL_QUADS)
        for face in lat_faces:
            for vertex in face:
                glVertex3fv(vertices[vertex])
        glEnd()

        # Draw the bases
        for base in bases:
            glBegin(GL_POLYGON)
            for vertex in base:
                glVertex3fv(vertices[vertex])
            glEnd()


        glPopMatrix()



    # Function to generate the vertices of a regular polygonal prism
    def generate_prism_vertices(sides, thickness, side_length):
        vertices = []
        angle_step = 2 * math.pi / sides

        # Generate vertices for the bottom base
        for i in range(sides):
            angle = i * angle_step
            x = math.cos(angle) * side_length
            z = math.sin(angle) * side_length
            vertices.append([x, -thickness / 2, z])  # Bottom base vertices

        # Generate vertices for the top base (shifted vertically by thickness)
        for i in range(sides):
            angle = i * angle_step
            x = math.cos(angle) * side_length
            z = math.sin(angle) * side_length
            vertices.append([x, thickness / 2, z])  # Top base vertices

        return vertices

    # Function to generate the faces of the prism
    def generate_prism_lateral_faces(sides):
        faces = []

        # Generate the faces for the sides of the prism (connecting corresponding vertices of top and bottom base)
        for i in range(sides):
            next_i = (i + 1) % sides
            # Ensure faces are ordered correctly for right-hand rule (counter-clockwise winding)
            faces.append([i, i + sides, next_i + sides, next_i])  # Side faces

        return faces
    
    def generate_prism_bases(sides):
        bases = []

        # Generate the faces for the bottom and top bases
        bottom_face = [i for i in range(sides)]
        top_face = [i + sides for i in range(sides)]

        bases.append(bottom_face)  # Bottom face (counter-clockwise winding)
        bases.append(top_face[::-1])  # Top face (clockwise winding)

        return bases

        
    #=======================================
    # Coordinate frame (To help with creating models)
    #=======================================

    # Draws a nice coordinate frame (using rays with tick marks)
    def draw_coordinate_frame():
        origin = Point(0, 0)
        xPoint = Point(10, 0)
        yPoint = Point(0, 10)
        BasicShapes.draw_ray(origin, xPoint, 10)
        BasicShapes.draw_ray(origin, yPoint, 10)


    # Draw a Ray from start to end with the proper number of tick marks
    def draw_ray(start, end, ticks=0):
        # First draw the line segment itself
        glBegin(GL_LINES)
        glVertex2f(start.x, start.y)
        glVertex2f(end.x, end.y)
        glEnd()
        
        # Now draw the triangular arrow at the end
        r = start.lerp(end, 0.9)  # 90% of way from start to end
        n = BasicShapes.Vector2D(start, end)
        nperp = n.perp()
        r1 = r.lerpV(nperp, 0.02)
        r2 = r.lerpV(nperp, -0.02)
        glBegin(GL_TRIANGLES)
        glVertex2f(end.x, end.y)
        glVertex2f(r1.x, r1.y)
        glVertex2f(r2.x, r2.y)
        glEnd()
        
        if ticks > 0:
            # Draw tick marks
            step = 1.0/ticks
            glBegin(GL_LINES)
            for t in range(ticks):
                r = start.lerp(end, t*step)  # Could speed up - but necessary?
                r1 = r.lerpV(nperp, 0.02)
                r2 = r.lerpV(nperp, -0.02)
                glVertex2f(r1.x, r1.y)
                glVertex2f(r2.x, r2.y)
            glEnd()


    class Vector2D:
        """A simple 2D Vector Class"""
        def __init__(self, p=None, q=None):
            """A constructor for Vector class between two Points p and q"""
            if q is None:
                if p is None:
                    self.dx = 0; self.dy = 0   # No direction at all
                else:
                    self.dx = p.x; self.dy = p.y  # Origin to p
            else:
                self.dx = q.x - p.x; self.dy = q.y - p.y

        def __str__(self):
            """Basic string representation of this point"""
            return "<%s,%s>"%(self.dx,self.dy)

        def perp(self):
            """Returns a vector perpendicular to this vector (CCW)"""
            answer = Vector()
            answer.dx = -self.dy
            answer.dy = self.dx
            return answer
