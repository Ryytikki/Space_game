import math
from vector_Class import *
# Modified version of G taking into account the game's unit system
GRAV_CONST = 3

def Calc_gravity(object, x1, x2, y1, y2, mass, parent_mass):
	
	# Two unit vectors containing the locations of the two bodies
	r1 = Vector(x1, y1)
	r2 = Vector(x2, y2)
	# Unit vector, used to control the direction of the force
	unit_vector = Vector()
	# Calculates the length between the vectors
	dif_r = Vector_distance(r1,r2)

	# Calculates the respective unit vector
	unit_vector = r1.__sub__(r2) / dif_r
	
	# if statement here to stop 1/0 errors
	if dif_r > 10:
		# Calculate the gravitational force
		force = GRAV_CONST * (mass * parent_mass) / ((dif_r ** 2))
	else:
		force = 0
	
	# Converts the force into the unit vector
	force_vector = unit_vector.__mul__(force)
	
	# Have to modify the x axis thanks to the annoying as hell unit system of programming languages
	if abs(x1 - x2) < 0:
		force_array = [force_vector.__getitem__(0) * -1, force_vector.__getitem__(1)]
	else:
		force_array = [force_vector.__getitem__(0) , force_vector.__getitem__(1)]

	return(force_array)