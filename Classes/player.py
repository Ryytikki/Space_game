import pygame, sys, math
from pygame.locals import *
from calc_gravity import Calc_gravity
from vector_Class import Vector_distance

# Generic image loading function. Useful to have around
def load_image(name):
	image = pygame.image.load(name).convert_alpha()
	return(image)

class Player(pygame.sprite.Sprite):
	def __init__(self, start_location, start_velocity, mass, parent):
		pygame.sprite.Sprite.__init__(self)
		self.velocity = start_velocity
		self.mass = mass
		self.parent = parent
		self.location = start_location
		self.fuel = mass - 1
		self.display_location = [start_location[0] + self.parent.display_location[0] + (self.parent.apparent_mass / 2), start_location[1] + self.parent.display_location[1] + (self.parent.apparent_mass / 2)]
		self.x_direction = 0
		self.y_direction = 0
		
		self.image = load_image("Images/player.png")
		self.image = pygame.transform.scale(self.image, (self.mass * 5, self.mass * 5))
		
	def update(self, stars, bodies):
		location = [0,0]
		# Keyboard controls
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.event.post(pygame.event.Event(QUIT))
			if event.type == MOUSEBUTTONUP:
				# Gets the mouse location relative to the player
				pos = pygame.mouse.get_pos()
				location[0] = pos[0] - self.display_location[0]
				location[1] = pos[1] - self.display_location[1]
				
				# Fuel control and velocity change
				if self.fuel > 0:
					angle = math.atan2(location[1], location[0])
					
					print(angle * 180 / 3.1415)
					self.velocity[1] -= math.sin(angle)
					self.velocity[0] += math.cos(angle)
					#self.mass -= 1
					#self.fuel -= 1
					# fire_bullet(angle + 1.57, self.display_location)
				
					
		# Calculates the force applied by the parent and other nearby planets
		force = [0,0]
		result = [0,0]
		# Star controls
		for star in stars:
			# If within SoI, make gravity work and shit yo
			if Vector_distance(self.display_location, star.display_location) < star.sphere_of_influence:
				self.parent = star
				self.location = [self.display_location[0] - self.parent.display_location[0], self.display_location[1] - self.parent.display_location[1]]
		
		# Planet controls
		for planet in bodies:
			# Same SoI check
			if Vector_distance(self.display_location, planet.display_location) < planet.sphere_of_influence:
				result = Calc_gravity(self, self.display_location[0], planet.display_location[0], self.display_location[1], planet.display_location[1], self.mass, planet.mass)
				force = [force[0] + result[0], force[1] + result[1]]
		
		result = Calc_gravity(self, self.location[0], 0, self.location[1], 0, self.mass, self.parent.mass)
		force = [force[0] + result[0], force[1] + result[1]]

		# Modifies the velocity of the body
		self.velocity[0] -= force[0] / (self.mass)
		self.velocity[1] += force[1] / (self.mass)
		
		# And from that, the location
		self.location[0] += self.velocity[0]
		self.location[1] -= self.velocity[1]
		
			# Updates the display location, aka the location relative to (0,0)
		self.display_location = [self.location[0] + self.parent.display_location[0] + (self.parent.apparent_mass / 2), self.location[1] + self.parent.display_location[1] + (self.parent.apparent_mass / 2)]
		
		if self.display_location[0] < 0 or self.display_location[0] > 1024 or self.display_location[1] < 0 or self.display_location[1] > 768:
			self.display_location = [100 + self.parent.display_location[0] + (self.parent.apparent_mass / 2), 100 + self.parent.display_location[1] + (self.parent.apparent_mass / 2)]
			self.location = [100, 100]
