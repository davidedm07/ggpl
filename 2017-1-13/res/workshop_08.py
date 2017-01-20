
import csv
from pyplasm import *
from workshop_07 import ggpl_doors
from workshop_07 import ggpl_windows
from workshop_03 import ggpl_stair
from workshop_09 import builder_roof
def ggpl_house_builder():

	XDoor = [.2,.4,.1,.4,.2]
	YDoor = [.3,.6,.1,.6,.1,.6,.1,.6,.3]
	occurencesDoor = [[True]*5, [True,False,True,False,True], [True]*5, [True,False,True,False,True], 
	[True]*5, [True,False,True,False,True], [True]*5, [True,False,True,False,True], [True]*5]

	XWindow = [.1,.2,.1,.5,.1,.2,.1]
	YWindow = [.1,.6,.1]
	occurencesWindow = [[True]*7,[True,False,True,False,True,False,True],[True]*7]
	""" Creation of the external walls of the house"""
	with open("Lines_Files/Modello_1/muri_esterni.lines", "rb") as csvfile:
		csvReader = csv.reader(csvfile,delimiter=",")
		externalWalls_list = []
		for row in csvReader :
			externalWalls_list.append(POLYLINE([[float(row[0]),float(row[1])],[float(row[2]),float(row[3])]]))
	externalWalls = STRUCT(externalWalls_list)
	xScale = 16/SIZE([1])(externalWalls)[0]
	yScale = 16/SIZE([2])(externalWalls)[0]
	externalWalls = S([1,2])([xScale,yScale])(externalWalls)
	pavement = SOLIDIFY (externalWalls)
	externalWalls = OFFSET([.2,.2])(externalWalls)
	externalWalls = PROD([externalWalls,Q(3.5)])
	pavement = TEXTURE("Texture/parquet_texture.jpg")(pavement)
	roof = builder_roof()
	roof = T([1,2])([float(row[0]),float(row[1])])(roof)
	roof = S([1,2])([xScale,yScale])(roof)
	roof = TEXTURE("Texture/roof_texture.png")(roof)

	""" Creation of the internal walls of the house"""
	with open("Lines_Files/Modello_1/muri_interni.lines", "rb") as csvfile:
		csvReader = csv.reader(csvfile,delimiter=",")
		internalWalls_list = []
		for row in csvReader :
			internalWalls_list.append(POLYLINE([[float(row[0]),float(row[1])],[float(row[2]),float(row[3])]]))
	internalWalls = STRUCT(internalWalls_list)
	internalWalls = S([1,2])([xScale,yScale])(internalWalls)
	internalWalls = OFFSET([.2,.2])(internalWalls)
	internalWalls = PROD([internalWalls,Q(3)])
	
	"""Creation of the doors of the house"""
	with open("Lines_Files/Modello_1/porte.lines", "rb") as csvfile:
		csvReader = csv.reader(csvfile,delimiter=",")
		listDoorsHoles = []
		cuboid = []
		initHoles = True
		cont = 0
		xDoors = 0
		yDiff = 0
		listDoorsCreated = []
		for row in csvReader:
			cont += 1
			cuboid.append([float(row[0])*xScale,float(row[1])*yScale])
			if cont <=2:
				if 	round(float(row[0]),1) == round(float(row[2]),1):
					yDiff = abs(float(row[3]) - float(row[1]))
				
				elif round(float(row[1]),1) == round(float(row[3]),1):
					xDiff = abs(float(row[2]) - float(row[0]))

			if cont == 4:
				listDoorsHoles.append(MKPOL([cuboid,[[1,2,3,4]],None]))
				cuboid = []
				door = []
				cont = 0
				if xDiff < yDiff:
					door = ggpl_doors(XDoor,YDoor,occurencesDoor)(yDiff*yScale,.2,3)
					door = T([1,2])([-0.1,0.1])(door)
					door = R([1,2])(-PI/2)(door)
				else:
					door = ggpl_doors(XDoor,YDoor,occurencesDoor)(xDiff*xScale,.2,3)
					door = T([1,2])([0.2,-0.2])(door)
				door = T([1,2])([float(row[0])*xScale,float(row[1])*yScale])(door)
				listDoorsCreated.append(door)
	
	""" Creation of the windows of the house"""	
	with open("Lines_Files/Modello_1/finestre.lines", "rb") as csvfile:
		csvReader = csv.reader(csvfile,delimiter=",")
		listWindowsHoles = []
		listWindowsCreated = []
		cuboid = []
		cont = 0
		for row in csvReader:
			cont += 1
			cuboid.append([float(row[0])*xScale,float(row[1])*yScale])
			if cont <=2:
				if 	round(float(row[0]),1) == round(float(row[2]),1):
					yDiff = abs(float(row[3]) - float(row[1]))
				
				elif round(float(row[1]),1) == round(float(row[3]),1):
					xDiff = abs(float(row[2]) - float(row[0]))
			if cont == 4:
				listWindowsHoles.append(MKPOL([cuboid,[[1,2,3,4]],None]))
				base = MKPOL([cuboid,[[1,2,3,4]],None])
				base = OFFSET([.1,.1])(base)
				base = PROD([base,Q(1.5)])
				cuboid = []
				cont = 0
				if xDiff < yDiff:
					window = ggpl_windows(XWindow,YWindow,occurencesWindow)(yDiff*yScale,0.2,1.5)
					window = R([1,2])(-PI/2)(window)
				else:
					window = ggpl_windows(XWindow,YWindow,occurencesWindow)((xDiff*xScale),.2,1.5)
					window = T(2)(-0.2)(window)
				
				window = T([1,2,3])([float(row[0])*xScale, float(row[1])*yScale,1])(window)
				listWindowsCreated.append(window)

	""" Creation of the external doors of the house"""
	with open("Lines_Files/Modello_1/porte_esterne.lines","rb") as csvfile:
		csvReader = csv.reader(csvfile, delimiter=",")
		listExternalDoorsHoles = []
		cuboid = []
		initHoles = True
		cont = 0
		xDiff = 0
		yDiff = 0
		listExternalDoorsCreated = []
		for row in csvReader:
			cont += 1
			cuboid.append([float(row[0]) * xScale, float(row[1]) * yScale])
			if cont <= 2:
				if round(float(row[0]), 1) == round(float(row[2]), 1):
					yDiff = abs(float(row[3]) - float(row[1]))

				elif round(float(row[1]), 1) == round(float(row[3]), 1):
					xDiff = abs(float(row[2]) - float(row[0]))

			if cont == 4:
				listExternalDoorsHoles.append(MKPOL([cuboid, [[1, 2, 3, 4]], None]))
				cuboid = []
				door = []
				cont = 0
				if xDiff < yDiff:
					door = ggpl_doors(XDoor, YDoor, occurencesDoor)(yDiff * yScale, .2, 2.5)
					door = T([1, 2])([-0.1, 0.1])(door)
					door = R([1, 2])(-PI / 2)(door)
				
				else:
					door = ggpl_doors(XDoor, YDoor, occurencesDoor)(xDiff * xScale, .2, 2.5)
					door = T( 2)( -0.1)(door)

				door = T([1, 2])([float(row[0]) * xScale, float(row[1]) * yScale])(door)
				listExternalDoorsCreated.append(door)
			
		stair = ggpl_stair(8.,6.,3.5)
		stair = R([1,2])(PI)(stair)
		stair = T([1,2])([float(row[0]) * xScale+2.5, float(row[1]) * yScale+6])(stair)
	
	"""Creation of the garden of the house"""		
	with open("Lines_Files/Modello_1/giardino.lines", "rb") as csvfile:
		csvReader = csv.reader(csvfile,delimiter=",")
		gardenBordersList = []
		for row in csvReader :
			gardenBordersList.append(POLYLINE([[float(row[0]),float(row[1])],[float(row[2]),float(row[3])]]))
	gardenBorders = STRUCT(gardenBordersList)
	garden = SOLIDIFY(gardenBorders)
	garden = S([1,2])([xScale*1.5,yScale*1.5])(garden)
	garden = TEXTURE("Texture/grass_texture.jpg")(garden)

	"""assembling all together"""
	doors = STRUCT(listDoorsHoles)
	externalDoorsHoles = STRUCT(listExternalDoorsHoles)
	windows = STRUCT(listWindowsHoles)
	windows = OFFSET([0.05,0.05])(windows)
	windows = PROD([windows,Q(1.5)])
	windows = T(3)(1)(windows)
	doors = OFFSET([.2,.15])(doors)
	doors = PROD([doors,Q(3)])
	externalDoorsHoles = OFFSET([0,.15])(externalDoorsHoles)
	externalDoorsHoles = PROD([externalDoorsHoles,Q(2.5)])
	externalDoorsCreated = STRUCT(listExternalDoorsCreated)	
	doorsCreated = STRUCT(listDoorsCreated)
	windowsCreated = STRUCT(listWindowsCreated)
	externalWalls = DIFFERENCE([externalWalls,windows])
	externalWalls = DIFFERENCE([externalWalls,externalDoorsHoles])
	externalWalls = TEXTURE("Texture/external_walls.jpg")(externalWalls)
	externalWalls = STRUCT([externalWalls,windowsCreated])
	externalWalls = STRUCT([externalWalls, externalDoorsCreated])
	internalWalls = DIFFERENCE([internalWalls,doors])
	internalWalls = TEXTURE("Texture/internal_walls.jpg")(internalWalls)
	internalWalls = STRUCT([internalWalls,doorsCreated])
	walls = STRUCT([internalWalls,externalWalls])
	house = STRUCT([walls,pavement])
	house = STRUCT([house,T(3)(3.5),house])
	house = STRUCT([house,T(3)(7),roof])
	house = STRUCT([house,stair])
	house = STRUCT([house,garden])
	return house
