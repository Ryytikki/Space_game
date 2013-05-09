import pygame, sys, math
from pygame.locals import *
from Classes.planet import Planet
from Classes.player import Player

# Generic image loading function. Useful to have around
def load_image(name):
	image = pygame.image.load(name).convert_alpha()
	return(image)

class Star(pygame.sprite.Sprite):
	def __init__(self, mass, location):
		pygame.sprite.Sprite.__init__(self)  
		self.mass = mass
		self.sphere_of_influence = mass * 2
		self.apparent_mass = 0
		self.display_location = location
		self.image = load_image('Images/star1.png')
		self.image = pygame.transform.scale(self.image, (self.mass, self.mass))
		self.rect = self.image.get_rect()
		self.rect.center = self.display_location
		self.frame_ID = 0
		
	def update(self):
		self.image = load_image('Images/star' + str(self.frame_ID / 15) + '.png')
		self.frame_ID += 1
		if self.frame_ID >= 30:
			self.frame_ID = 0


def main():
	# Initiate pygame
	pygame.init()
	# Prep the fps timer
	fpsclock = pygame.time.Clock()
	
	# Define the main surfaces and set the caption
	window_surface = pygame.display.set_mode((1024,768))
	trace_surface = pygame.Surface((1024, 768))
	pygame.display.set_caption("Space Simulator")
	
	# Define colours that will be used
	black_colour = pygame.Color(0,0,0)
	yellow_colour = pygame.Color(255, 255, 0)
	green_colour = pygame.Color(0, 255, 0)
	red_colour = pygame.Color(255, 0, 0)
	
	# Define fonts to be used
	text_font = pygame.font.SysFont("monospace", 12)
	
	# Planetary bodies currently being tested
	bodies = pygame.sprite.Group()
	stars = pygame.sprite.Group()
	
	sun = Star(100, [550, 484])
	urf = Planet(20, sun, 200.0, 1,1)
	munjd = Planet(3, urf, 22.0, 2.0, 2)
	plr = Player([100, 100], [1,1], 5, sun)
	
	stars.add((sun))
	bodies.add((urf, munjd))
	
	
	while True:
		# Reset the main surface and overlay the trace surface
		window_surface.fill(black_colour)
		window_surface.blit(trace_surface, (0,0))
		
		# Draw stars
		for star in stars:
		#	pygame.draw.circle(window_surface, yellow_colour, star.display_location, star.sphere_of_influence)
			window_surface.blit(star.image, (star.rect))
		stars.update()

		
		# Draw planets
		for planet in bodies:
			#pygame.draw.circle(window_surface, green_colour, [int(planet.display_location[0]), int(planet.display_location[1])], planet.sphere_of_influence)
			window_surface.blit(planet.image, (planet.rect))
		bodies.update()
		
		# Draw player	
		window_surface.blit(plr.image, (plr.display_location))
		plr.update(stars, bodies)
		
		# Draw text
		text_surface = text_font.render("Fuel: " + str(plr.fuel), False, yellow_colour)
		window_surface.blit(text_surface, (0, 0))
		
		# Event handling code
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.event.post(pygame.event.Event(QUIT))
		
		# Update planetary bodies
		
		
		# Update the screen
		pygame.display.update()
		
		# Keep the fps at a fixed amount
		fpsclock.tick(30)
	
if __name__ == '__main__':
	main()