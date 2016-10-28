from pyplasm import *
import math
""" function that creates a l shaped stair"""
def ggpl_zstair(dx,dy,dz):
	"""parameters of the single step""" 
	vertex = [[0,0],[0,0.5],[2,0.5],[1,0]]
	cells = [[1,2,3,4]]
	polls = None
	"""creation of the first step"""
	xstep = MKPOL([vertex, cells, 1])
	step = PROD([QUOTE([3]),xstep])
	"""calculation of the height of the ramps"""
	rampeHeight = math.ceil(dz/2)
	"""calculation of the number of the steps according to the dimension of the box"""
	numStep = math.ceil(dx)
	"""creation of the 2 ramps"""
	xRampe= step
	xRampe2= xRampe
	for i in range(int(numStep)-3):
		xRampe = STRUCT([xRampe,T([2,3])([1,0.5]),xRampe])
		xRampe2 = STRUCT([xRampe2,T([2,3])([1,0.5]),xRampe2])
	"""creation of the platform on the last step"""
	finalStep = CUBOID([dx,2,0.5])
	"""concatenation of the ramps with the platform"""
	xRampe = STRUCT([xRampe,T([2,3])([(numStep-2)*1,(numStep-2)*0.5]),finalStep])
	xRampe2 = STRUCT([xRampe2,T([2,3])([(numStep-3)*1,(numStep-3)*0.5]),finalStep])
	"""rotate the second ramp of 180 degrees"""
	xRampe2= R([1,2])(PI)(xRampe2)
	"""create and display the box"""
	box = SKEL_1(CUBOID([dx,dy,dz]))
	result = STRUCT([box,xRampe])
	"""concatenation of the 2 ramps and display of the result"""
	result = STRUCT([result,T([1,2,3])([dx,dy-1,(numStep-2)*0.5]),xRampe2])
	VIEW(result)
	return result
	
   	





if __name__ == '__main__':
	ggpl_zstair(7,7,7)