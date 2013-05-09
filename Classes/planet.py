import pygame, sys, math
from calc_gravity import Calc_gravity

# Generic image loading function. Useful to have around
def load_image(name):
	image = pygame.image.load(name).convert_alpha()
	return(image)

	
# Holds the information for small, orbiting planetary bodies
# Variable  | description
#------------------------------------------------------------
# Mass      | Holds the mass of the orbiting body
# Parent    | The body that this body orbits around
# Semimajor | The semimajor axis of the body. The body will start orbiting
#			| on the right hand side of its parent at this distance (in px)
# Velocity  | Initial velocity (in px/s)
# Colour	| Colour of the planet. Used to choose which image file to load

class Planet(pygame.sprite.Sprite):
	def __init__(self, mass, parent, semimajor, velocity, colour):
		pygame.sprite.Sprite.__init__(self)  
		# Assign variables to class
		self.parent = parent
		self.mass = mass
		self.apparent_mass = mass
		self.semimajor = semimajor
		self.sphere_of_influence = mass * 2
		# Starting location relative to its parent
		self.location = [semimajor, 0]
		# Location of the body relative to (0,0) on the screen
		self.display_location = [self.location[0] + self.parent.display_location[0], self.location[1] + self.parent.display_location[1]]
		self.velocity = [0, velocity]
		# Placeholder variables for min/max distance info
		
		# Imports and resizes image
		planet_type = ["Blue", "Green", "Pink", "Red"]
		self.image = load_image('Images/planet' + planet_type[colour] + '.png')
		self.image = pygame.transform.scale(self.image, (self.mass, self.mass))
		self.rect = self.image.get_rect()
		self.rect.center = self.display_location
		
		
	# Code for updating the location of the body	
	def update(self):
		# Calculates the force applied by the parent
		force = Calc_gravity(self, self.location[0], 0, self.location[1], 0, self.mass, self.parent.mass)
		
		# Modifies the velocity of the body
		self.velocity[0] -= force[0] / (self.mass)
		self.velocity[1] += force[1] / (self.mass)
		
		# And from that, the location
		self.location[0] += self.velocity[0]
		self.location[1] -= self.velocity[1]
		
		# Updates the display location, aka the location relative to (0,0)
		self.display_location = [self.location[0] + self.parent.display_location[0] + (self.parent.apparent_mass / 2), self.location[1] + self.parent.display_location[1] + (self.parent.apparent_mass / 2)]
		self.rect.center = self.display_location
