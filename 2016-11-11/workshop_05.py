from pyplasm import *
"""function that creates a blackboard"""
def create_blackboard(dx,dy,dz):
	blackboard = COLOR(BLACK)(CUBOID([0.05,2,1]))
	skel = OFFSET([.02,.02,.02])(SKEL_1(blackboard))
	skel = COLOR(Color4f([205/255.0,170/255.0,125/255.0,1]))(skel)
	blackboard = STRUCT([skel,blackboard])
	blackboard = T([2,3])([dy/3,dz/3])(blackboard)
	return blackboard
"""function that creates a bookshelf"""
def create_bookshelf(dx,dy,dz):
	panel = CUBOID([0.1,0.5,1])
	panels = STRUCT([panel,T(1)(1),panel])
	basement = CUBOID([2,0.5,0.1])
	bookshelf = STRUCT([panel,basement])
	bookshelf = STRUCT([bookshelf,T(1)(2),panel])
	upperPanel = CUBOID([2.1,0.5,0.1])
	bookshelf = STRUCT([bookshelf,T(3)(1),upperPanel])
	bookshelf = STRUCT([bookshelf,T(3)(0.5),basement])
	bookshelf = T(1)(dx/3)(bookshelf)
	bookshelf = COLOR(Color4f([205/255.0,170/255.0,125/255.0,1]))(bookshelf)
	return bookshelf

"""function that creates a teaching desk"""
def create_teaching_desk(dx,dy,dz):
	leg = CYLINDER([0.05,0.5])(30)
	leg = T([1,2])([0.05,0.05])(leg)
	leg = COLOR(Color4f([205/255.0,170/255.0,125/255.0,1]))(leg)
	legs = STRUCT([leg,T(2)(1.25),leg])
	legs = STRUCT([legs,T(1)(0.7),legs])
	deskPlane = CUBOID([0.8,1.35,0.1])
	deskPlane = COLOR(RED)(deskPlane)
	teachingDesk = STRUCT([legs,T(3)(0.5),deskPlane])
	coveringFront=CUBOID([0.01,1.3,0.4])
	coveringFront= COLOR(RED)(coveringFront) 
	teachingDesk=STRUCT([teachingDesk,T([1,3])([0.8,0.05]),coveringFront])
	coverLateral=CUBOID([0.75,0.01,0.4])
	coverLateral = COLOR(YELLOW)(coverLateral)
	teachingDesk=STRUCT([teachingDesk,T([2,3])([1.3,0.05]),coverLateral])
	teachingDesk=STRUCT([teachingDesk,T(3)(0.1),coverLateral])
	teachingChair = create_chair()
	teachingChair = R([1,2])(PI)(teachingChair)
	teachingChair = T(2)(0.8)(teachingChair)
	teachingChair = S([1,2,3])([1.2,1.2,1.2])(teachingChair)
	teachingDesk = STRUCT([teachingDesk,teachingChair])
	teachingDesk = T([1,2])([0.5,dy/3])(teachingDesk)
	return teachingDesk

"""function that creates a chair"""
def create_chair():
	chairLeg = CUBOID([0.05,0.05,0.3])
	chairSit = CUBOID([0.3,0.3,0.05])
	backLeg = CUBOID([0.04,0.04,0.2])
	backLeg= STRUCT([backLeg,T(2)(0.26),backLeg])
	backLeg = COLOR(GRAY)(backLeg) 
	chairSit = COLOR(YELLOW)(chairSit)
	chairLegs = STRUCT([chairLeg,T(2)(0.25),chairLeg])
	chairBack = CUBOID([0.04,0.3,0.1])
	chairBack = COLOR(YELLOW)(chairBack)
	chairBack = STRUCT([backLeg,T(3)(0.2),chairBack])
	chairLegs = STRUCT([chairLegs,T(1)(0.25),chairLegs])
	chairLegs = COLOR(GRAY)(chairLegs)
	chair = STRUCT([chairLegs,T(3)(0.3),chairSit])
	chair =STRUCT([chair,T([1,3])([0.26,0.35]),chairBack])
	return chair

"""function that creates a chair"""
def create_desks(dx,dy,dz):
	teachingDeskDimension = 0.8
	bookshelfDimension = 0.5
	deskLeg = CUBOID([0.05,0.05,0.5])
	desk = CUBOID([0.4,0.6,0.05])
	desk = COLOR(RED)(desk)	
	deskLegs = STRUCT([deskLeg,T(1)(0.35),deskLeg])
	deskLegs = STRUCT([deskLegs,T(2)(0.55),deskLegs])
	deskLegs = COLOR(Color4f([205/255.0,170/255.0,125/255.0,1]))(deskLegs)
	desk = STRUCT([deskLegs,T(3)(0.5),desk])
	box = SKEL_1(CUBOID([dx,dy,dz]))
	chair = create_chair()
	chairAndDesk = STRUCT([desk,T([1,2])([0.2,0.2]),chair])
	if dx/4> teachingDeskDimension*2:
		if dy/8>bookshelfDimension:
			chairAndDesk = T([1,2])([dx/4.0,dy/8.0])(chairAndDesk)
		else:
			chairAndDesk = T([1,2])([dx/4.0,bookshelfDimension*1.5])(chairAndDesk)
	else:
		if dy/8>bookshelfDimension: 
			chairAndDesk = T([1,2])([teachingDeskDimension*2,dy/8.0])(chairAndDesk)
		else:
			chairAndDesk = T([1,2])([teachingDeskDimension*2,bookshelfDimension*2])(chairAndDesk)
	i =0.8
	desks = chairAndDesk
	emptySpaceX = dx-dx/4.0
	emptySpaceY = dy-dy/4.0
	while i< emptySpaceX:
		j= i
		if j+0.8 <emptySpaceX:
			desks = STRUCT([desks,T(1)(i),chairAndDesk])
		i += 0.8

	i=1.2
	finalDesks=desks
	while i< emptySpaceY:
		j=i
		if j+1.2 <=emptySpaceY:
			finalDesks = STRUCT([finalDesks,T(2)(i),desks])
		i += 1.2 
		
	result = STRUCT([box,finalDesks])
	return result
	

"""calls the other functions and creates a classroom
   @Param dx,dy,dz dimensions of the room in meters"""
def ggpl_school_furniture(dx,dy,dz):
	box = SKEL_1(CUBOID([dx,dy,dz]))
	desks = create_desks(dx,dy,dz)
	blackboard = create_blackboard(dx,dy,dz)
	result = STRUCT([desks,blackboard])
	result = STRUCT([result,box])
	teachingDesk= create_teaching_desk(dx,dy,dz)
	result = STRUCT([result,teachingDesk])
	bookshelf = create_bookshelf(dx,dy,dz)
	result = STRUCT([result,bookshelf])
	VIEW(result)
	return result

#classroom 1 8,8,3
#classroom 2 5,5,3
#classroom 3 10,10,3
if __name__=="__main__":
	ggpl_school_furniture(8.0,8.0,3.0)