from pyplasm import *


"""Resize if a function that has the task to adjust the given dimensions of the door/window in
order to fit the dimensions of the box passed as parameter.
@Param:
x : list of distances of a x points calculated from the previous one 
y : list of distances of a y points calculated from the previous one
occurences: matrix of bools that indicates the nature of the cells (wooden, glass)
dx: dimension of the box on the x axis
dz: dimension of the box on the z axis"""
def resize(x,y,occurences,dx,dz):
	sumY = sum(y)
	sumX = sum(x)
	emptyCells = 0
	for j in range(len(y)):
		for i in range(len(x)):
			if occurences[j][i] == False:
				emptyCells += 1
	diffX = (dx-sumX)/emptyCells
	diffY = (dz-sumY)/emptyCells

	for j in range(len(y)):
		for i in range(len(x)):
			if occurences[j][i] == False:
				x[i]+=diffX
				y[j]+= diffY
				

"""Function that creates a door of the given dimensions.
This function calls another function door (curried one) that creates the door according to the dimensions of a box
passed as parameters. The door function calls the resize metod. 
@Param:
x : list of distances of a x points calculated from the previous one 
y : list of distances of a y points calculated from the previous one
occurences: matrix of bools that indicates the nature of the cells (wooden, glass)
dx: dimension of the box on the x axis
dz: dimension of the box on the z axis"""
def ggpl_doors(x,y,occurences):
	def doors(dx,dy,dz):
		s=STRUCT([CUBOID([0,0,0])])
		resize(x,y,occurences,dx,dz)
		for i in range(len(x)):
			#counter for translation
			sumX=sum(x[:i])
			for j in range(len(y)):
				sumY=sum(y[:j])
				if occurences[j][i]==True:
					cube = CUBOID([x[i],y[j],dy])
					cube = TEXTURE(["Texture/wooden_texture.jpg"])(cube) 
					s=STRUCT([s,T([1,2])([sumX,sumY])(cube)])
				else:
					cube = CUBOID([x[i],y[j],dy])
					cube = TEXTURE(["Texture/glass_texture_2.jpg"])(cube) 
					s=STRUCT([s,T([1,2])([sumX,sumY])(cube)])

		s = R([2,3])(PI/2)(s)
		s = T(2)(dy)(s)
		lockBase = CUBOID([.01,0.1,0.5])
		lockCylinder = CYLINDER([0.02,0.1])(30)
		lockCylinder = R([1,3])(PI/2)(lockCylinder)
		lockOrizzontalCylinder =CYLINDER([0.02,0.2])(30)
		lockOrizzontalCylinder = R([2,3])(PI/2)(lockOrizzontalCylinder)
		lockOrizzontalCylinderReverse = R([2,3])(-PI)(lockOrizzontalCylinder) 
		lock = STRUCT([lockBase,T([2,3])([0.05,0.3]),lockCylinder])
		lock = STRUCT([lock,T([1,2,3])([-0.1,0.065,0.3]),lockOrizzontalCylinder])
		lock = TEXTURE(["Texture/gold_texture.jpg"])(lock)
		lock = R([1,2])(-PI/2)(lock)
		door = STRUCT([s,SKEL_1(CUBOID([dx,dy,dz]))])
		door = STRUCT([door,T([1,2,3])([dx-0.15,dy+0.01,dz/2.5]),lock])
		lockReverse = STRUCT([lockBase,T([2,3])([0.05,0.3]),lockCylinder]) 
		lockReverse = STRUCT([lockReverse,T([1,2,3])([-0.1,0.065,0.3]),lockOrizzontalCylinderReverse])
		lockReverse = TEXTURE(["Texture/gold_texture.jpg"])(lockReverse)
		lockReverse = R([1,2])(-PI/2)(lockReverse)
		lockReverse = R([1,2])(PI)(lockReverse)
		door = STRUCT([door,T([1,2,3])([dx-0.015,-0.01,dz/2.5]),lockReverse])
		return door
        			
	return doors

"""Function that creates a window by calling a curried function.
This function has the task to create the window and to resize it in order to fill a bo of given 
dimensions.
@Param : The same of the door function"""
def ggpl_windows(x,y,occurences):
	def windows(dx,dy,dz):
		s=STRUCT([CUBOID([0,0,0])])
		resize(x,y,occurences,dx,dz)
		for i in range(len(x)):
			#counter for translation
			sumX=sum(x[:i])
			for j in range(len(y)):
				sumY=sum(y[:j])
				if occurences[j][i]==True:
					cube=CUBOID([x[i],y[j],dy])
					cube = TEXTURE(["Texture/white_wood_texture.jpg"])(cube) 
					s=STRUCT([s,T([1,2])([sumX,sumY])(cube)])
				else:
					cube = CUBOID([x[i],y[j],dy])
					cube = TEXTURE(["Texture/glass_texture.jpg"])(cube) 
					s=STRUCT([s,T([1,2])([sumX,sumY])(cube)])
		window = R([2,3])(PI/2)(s)
		window = T(2)(dy)(window)

		return window
	return windows		
	
if __name__=='__main__':
	#Window1
	XWindow = [.1,.2,.1,.5,.1,.2,.1]
	YWindow = [.1,.6,.1]
	occurencesWindow = [[True]*7,[True,False,True,False,True,False,True],[True]*7]
	#Door1		  		
	XDoor = [.2,.4,.1,.4,.2]
	YDoor = [.3,.6,.1,.6,.1,.6,.1,.6,.3]
	occurencesDoor = [[True]*5, [True,False,True,False,True], [True]*5, [True,False,True,False,True], 
	[True]*5, [True,False,True,False,True], [True]*5, [True,False,True,False,True], [True]*5]
	#Door2
	"""
	XDoor = [.2,.2,.3,.2,.2]
	YDoor = [.4,.4,.4,.4,.4,.4,.4]
	occurencesDoor = [[True]*5,[True,False,False,True,True],[True]*5,
	[True,True,False,False,True],[True]*5,[True,False,False,True,True],[True]*5]
	"""
	#window = ggpl_windows(XWindow,YWindow,occurencesWindow)(3,0.05,2)
	VIEW(ggpl_windows(XWindow,YWindow,occurencesWindow)(3,0.05,2))
	VIEW(ggpl_doors(XDoor,YDoor,occurencesDoor)(1.5,0.1,3))