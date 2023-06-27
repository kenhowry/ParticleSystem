"""
Particle System
This program simulates complicated phenomena with moving parts using Classes & Inheritance.

File Name: howry_particle_system.py
Author: Ken Howry
Date: 10.3.23
Course: COMP 1352
Assignment: Project VII
Collaborators: COMP 1352 Instructors
Internet Source: N/A
"""
#imports
import dudraw
import math
import random
from dudraw import Color #a Color object that models an RGB color

#this class was provided by the instructor
#stores the x and y position
class Vector:
    def __init__(self, some_x=0, some_y=0):
        self.x = some_x
        self.y = some_y

    def limit(self, l):
        if(self.length() >= l):
            self.resize(l)

    def resize(self, l):
        length = math.sqrt(self.x ** 2 + self.y**2)
        self.x *= (l/length)
        self.y *= (l/length)

    def __add__(self, other_vector)->None:
        return Vector(self.x+other_vector.x, self.y + other_vector.y)

    def __sub__(self, other_vector)->None:
        return Vector(self.x-other_vector.x, self.y - other_vector.y)

    def __isub__(self, other_vector)->None:
        self.x -= other_vector.x
        self.y -= other_vector.y
        return self

    def __iadd__(self, other_vector):
        self.x += other_vector.x
        self.y += other_vector.y
        return self

    def divide(self, s):
        self.x /= s
        self.y /= s

    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    def angle_in_radians(self):
        return math.tan((self.y/self.x))

#this class was provided by the instructor
#class Time: tick() - time the animation loop; time() - get current time
class Time:
    frame = 0

    def tick():
        Time.frame += 1
    
    def time():
        return Time.frame

#Particle class - parent class
class Particle(): 
    def __init__(self, x_pos, y_pos, x_vel, y_vel, size, lifetime):
        """
        Description of Function: Intializing instance variables

        Parameters: 
        pos: Vector; stores the position of the particle
        vel: Vector; stores the velocity of the particle
        size: float; stores the size of the particle
        color: Color; stores the color set to random by constructor
        lifetime: int; lifetime of the particle

        Return: None
        """
        self.pos = Vector(x_pos, y_pos)
        self.vel = Vector(x_vel, y_vel)
        self.size = size
        self.lifetime = lifetime + Time.time()
        self.color = Color(random.randint(0,255), random.randint(0,255), random.randint(0,255))
                           
    def has_expired(self):
        """
        Description of Function: returns True if the particle has expired (lifetime exceeded)

        Parameters: N/A

        Return: bool
        """
        return Time.time() > self.lifetime

    def move(self):
        """
        Description of Function: adds the velocity vector to position vector if the shape has not expired

        Parameters: N/A

        Return: None
        """
        self.lifetime -= 1
        if self.has_expired() == False:
            self.pos += self.vel
        
#SparkParticle class - Particle Child Class
class SparkParticle(Particle):
    def __init__(self, x_pos, y_pos, x_vel, y_vel, size, lifetime):
        """
        Description of Function: inherits the parameters of the parent; sets the color to a new shade

        Parameters: N/A

        Return: None
        """
        Particle.__init__(self, x_pos, y_pos, x_vel, y_vel, size, lifetime)
        self.color = dudraw.Color(191, 128, 255)

    def draw(self):
        """
        Description of Function: draws a line in direction of velocity with sparkle color

        Parameters: N/A

        Return: None
        """
        dudraw.set_pen_color(self.color)
        dudraw.line(self.pos.x, self.pos.y, self.pos.x + self.vel.x, self.pos.y + self.vel.y) 

#FireParticle class - Particle Child Class
class FireParticle(Particle):
    def __init__(self, x_pos, y_pos, x_vel, y_vel, size, lifetime):
        """
        Description of Function: inherits the parameters of the parent; set color to yellow

        Parameters: N/A

        Return: None
        """
        Particle.__init__(self, x_pos, y_pos, x_vel, y_vel, size, lifetime)
        self.green = 255

    def draw(self):
        """
        Description of Function: change color toward red decrease green value and draw as a circle

        Parameters: N/A

        Return: None
        """
        if self.green >= 5:
            self.green -= 5
        dudraw.set_pen_color_rgb(255, self.green, 0)
        dudraw.filled_circle(self.pos.x, self.pos.y, self.size) # guessing on drawing a fire with .x or .y at the end 
    
    def move(self):
        """
        Description of Function: moves like parent and decreases size

        Parameters: N/A

        Return: None
        """
        Particle.move(self)
        self.size -= .0002

#AcceleratingParticle class - Particle Child Class
class AcceleratingParticle(Particle):
    def __init__(self, x_pos, y_pos, x_vel, y_vel, x_acc, y_acc, size, lifetime):
        """
        Description of Function: inherits the parameters of the parent; adds the acceleration variable

        Parameters: 
        acc: Vector; Vector store acceleration of the particle

        Return: None
        """
        Particle.__init__(self, x_pos, y_pos, x_vel, y_vel, size, lifetime)
        self.acc = Vector(x_acc, y_acc)

    def move(self):
        """
        Description of Function: same as parent and adds the acceleration vector to the velocity vector

        Parameters: N/A

        Return: None
        """
        Particle.move(self)
        self.vel += self.acc

#FireworkParticle class - AcceleratingParticle Child Class
class FireworkParticle(AcceleratingParticle):
    def __init__(self, x_pos, y_pos, x_vel, y_vel, x_acc, y_acc, size, lifetime):
        """
        Description of Function: inherits the parameters of the parent

        Parameters: N/A

        Return: None
        """
        AcceleratingParticle.__init__(self, x_pos, y_pos, x_vel, y_vel, x_acc, y_acc, size, lifetime)

    def draw(self):
        """
        Description of Function: draw a square with the color

        Parameters: N/A

        Return: None
        """
        dudraw.set_pen_color(self.color)
        dudraw.filled_square(self.pos.x, self.pos.y, self.size)

#MarbleParticle class - AcceleratingParticle Child Class
class MarbleParticle(AcceleratingParticle):
    def __init__(self, x_pos, y_pos, x_vel, y_vel, x_acc, y_acc, size, lifetime):
        """
        Description of Function: inherits the parameters of the parent

        Parameters: N/A

        Return: None
        """
        AcceleratingParticle.__init__(self, x_pos, y_pos, x_vel, y_vel, x_acc, y_acc, size, lifetime)

    def draw(self):
        """
        Description of Function: draw a circle with marble color

        Parameters: N/A

        Return: None
        """
        dudraw.set_pen_color(self.color)
        dudraw.filled_circle(self.pos.x, self.pos.y, self.size) 

#ParticleContainer class - parent class
class ParticleContainer():
    def __init__(self, x_pos:float, y_pos:float):
        """
        Description of Function: instance variables

        Parameters: 
        pos: Vector; Vector store the position of the particle
        particle: list; a list to store particles

        Return: None
        """
        self.pos = Vector(x_pos, y_pos)
        #creates empty particle list
        self.particle = []

    def animate(self):
        """
        Description of Function: go through the list of particle and draw() and move() them; also removes all expired particles

        Parameters: N/A

        Return: None
        """
        for i in range(len(self.particle)-1, -1, -1):
            self.particle[i].move()
            self.particle[i].draw()
            #removes expired particles
            if self.particle[i].has_expired():
                self.particle.pop(i)
            
#Emitter class - ParticleContainer Child Class
class Emitter(ParticleContainer):
    def __init__(self, x_pos, y_pos, fire_rate):
        """
        Description of Function: inherits parameters of parent; adds fire_rate variable

        Parameters: 
        fire_rate: int; number of particles added to list each frame

        Return: None
        """
        ParticleContainer.__init__(self, x_pos, y_pos)
        self.fire_rate = fire_rate
            
#Firework class - ParticleContainer Child Class
class Firework(ParticleContainer):
    def __init__(self, x_pos, y_pos):
        """
        Description of Function: inherits parameters of parent; appends 500 FireworkParticles

        Parameters: N/A

        Return: None
        """
        ParticleContainer.__init__(self, x_pos, y_pos)

        #appending FireworkParticles
        for i in range(500):
            self.particle.append(FireworkParticle(self.pos.x, self.pos.y, 0.01*random.randint(-4, 4), 0.01*random.randint(-4, 4), 0, 0.001*random.randint(-12, -8), 0.004, 50))
            
#Marbles class - ParticleContainer Child Class
class Marbles(ParticleContainer):
    def __init__(self, x_pos, y_pos):
        """
        Description of Function: inherits parameters of parent; appends 10 MarbleParticles

        Parameters: N/A

        Return: None
        """
        ParticleContainer.__init__(self, x_pos, y_pos)

        #appending MarbleParticles
        for i in range(10):
            self.particle.append(MarbleParticle(0.01*random.randint(5, 95), 0.01*random.randint(5, 95), 0.01*random.randint(-4, 4), 0.01*random.randint(-4, 4), 0, 0.001*random.randrange(-2, -1), 0.05, 500))

    def animate(self):
        """
        Description of Function: animates like parent; marbles stay within the boundary of the screen

        Parameters: N/A

        Return: None
        """
        ParticleContainer.animate(self)
        for part in self.particle[::-1]:
            if part.pos.x > 1 - part.size and part.vel.x > 0 or part.pos.x < 0+part.size and part.vel.x < 0:
                part.vel.x =-part.vel.x
            if part.pos.y > 1 - part.size and part.vel.y >0 or part.pos.y < 0+part.size and part.vel.y <0:
                part.vel.y =-part.vel.y
    
#Fire class - Emitter Child Class
class Fire(Emitter):
    def animate(self):
        """
        Description of Function: animates like parent; adds "fire_rate" new FireParticles

        Parameters: N/A

        Return: None
        """
        Emitter.animate(self)

        #appending "fire_rate" FireParticle particles
        for i in range(self.fire_rate):
            self.particle.append(FireParticle(self.pos.x, self.pos.y, 0.001*random.randint(-2, 2), 0.001*random.randint(2, 5), 0.01*random.randint(1, 3), 50))

#Sparkler class - Emitter Child Class
class Sparkler(Emitter):
    def animate(self):
        """
        Description of Function: animates like parent; adds "fire_rate" new SparkParticle particles

        Parameters: N/A

        Return: None
        """
        Emitter.animate(self)

        #drawing a line for the sparkler
        dudraw.set_pen_color(dudraw.WHITE)
        dudraw.line(self.pos.x, self.pos.y, self.pos.x, self.pos.y - .3)

        #appending "fire_rate" SparkParticle particles
        for i in range(self.fire_rate):
            self.particle.append(SparkParticle(self.pos.x, self.pos.y, 0.01*random.randint(-7, 7), 0.01*random.randint(-7, 7), 0.04, 5))

#main code block

#empty list
containers = []

#setting key variable
key = " "

#appending Particles
containers.append(Fire(0.75, 0.25, 30))
containers.append(Sparkler(.25,.75, 30))

#while loop
while True:
    Time.tick()
    dudraw.clear(dudraw.BLACK)

    #animating
    for container in containers:
        container.animate()

    #has_next_key_typed() and appending Fireworks
    if dudraw.has_next_key_typed():
        key = dudraw.next_key_typed()
        if key == "f":
            containers.append(Firework(dudraw.mouse_x(),dudraw.mouse_y()))
    
    #mouse_clicked() and appending Marbles
    if dudraw.mouse_clicked():
        containers.append(Marbles(dudraw.mouse_x(),dudraw.mouse_y()))
    
    #show
    dudraw.show(50)