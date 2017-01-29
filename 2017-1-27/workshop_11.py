import csv
from pyplasm import *
from res import workshop_10 as w10

def ggpl_build_tree():
	h = 20
	leaves = SPHERE(0)([1,1])
	r = 1
	log = CYLINDER([r,h])(20)
	log = TEXTURE("Texture/tree_texture.jpg")(log)
	leaf = SPHERE(h/6)([24,32])
	leaf = TEXTURE("Texture/leaves_texture.jpg")(leaf)	
	leaves = STRUCT([leaves,T(1)(h/6)(leaf)])
	leaves = STRUCT([leaves,T(1)(-h/6)(leaf)])
	leaves2 = R([1,2])(PI/2)(leaves)
	leaves = STRUCT([leaves,leaves2])	
	
	leaves = T(3)(h)(leaves)
	tree = STRUCT([log,leaves,T(3)(h+h/6)(leaf)])
	return tree

def ggpl_suburban_housing_neighbourhood():
	with open("Lines_Files/contorno1.lines","rb") as csvfile:
		csvReader = csv.reader(csvfile)
		points = []
		for row in csvReader:
			points.append([float(row[0]),float(row[1])])

	outline1 = MAP(BEZIERCURVE(points))(INTERVALS(1)(32))
	outline1 = OFFSET([8,8])(outline1)
	outline1 = PROD([outline1,Q(0.5)])
	
	with open("Lines_Files/contorno2.lines","rb") as csvfile:
		csvReader = csv.reader(csvfile)
		points = []
		for row in csvReader:
			points.append([float(row[0]),float(row[1])])

	outline2 = MAP(BEZIERCURVE(points))(INTERVALS(1)(32))
	outline2 = OFFSET([8,8])(outline2)
	outline2 = PROD([outline2,Q(0.5)])
	
	with open("Lines_Files/contorno3.lines","rb") as csvfile:
		csvReader = csv.reader(csvfile)
		points = []
		for row in csvReader:
			points.append([float(row[0]),float(row[1])])
	outline3 = MAP(BEZIERCURVE(points))(INTERVALS(1)(32))
	outline3 = OFFSET([8,8])(outline3)
	outline3 = PROD([outline3,Q(0.5)])
	streets = STRUCT([outline1,outline2,outline3])
	streets = TEXTURE("Texture/road_texture.jpg")(streets)
	#result = MATERIAL([1,0,0,1,  1,1,1,1,  0,0,0,0, 0,0,0,0, 100])(result)0
	
	with open("Lines_Files/fondamenta.lines", "rb") as cvsfile:
		csvReader = csv.reader(cvsfile)
		points = []
		for row in csvReader:
			points.append(POLYLINE([[float(row[0]),float(row[1])],[float(row[2]),float(row[3])]]))

		basement = STRUCT(points)
		basement = SOLIDIFY(basement)
		woodPlatform = basement
		woodPlatform = PROD([woodPlatform,Q(3)])
		woodPlatform =  MATERIAL([.7,0,0,1,  0,0,0,1,  0,0,0,0, 0,0,0,1, 1])(woodPlatform)
		basement = PROD([basement,Q(0.1)])
		basement = MATERIAL([.15,.3,0,1,  0,0,0,1,  0,0,0,0, 0,0,0,1, 1])(basement)
		#basement = TEXTURE("Texture/grass_texture_2.jpg")(basement)
		basementComplete = STRUCT([woodPlatform,T(3)(3),basement])

	""" Building the houses of the neighbourhood"""
	singleHouse = w10.ggpl_multistory_house()
	houseSizeX = SIZE([1])(singleHouse)[0]
	doubleHouses = STRUCT([singleHouse,T(1)(houseSizeX -8),singleHouse])
	threeHouses =  STRUCT([singleHouse,T(1)(houseSizeX-8),singleHouse])
	threeHouses = STRUCT([threeHouses,T(1)(houseSizeX*2-16),singleHouse])
	doubleHousesReverse = R([1,2])(PI)(doubleHouses)
	threeHousesReverse = R([1,2])(-PI)(threeHouses)
	lateralHouses = R([1,2])(-PI/2.5)(doubleHousesReverse)
	houses = T([1,2])([100,115])(lateralHouses)
	houses = STRUCT([houses,T([1,2])([150,10]),doubleHouses])
	houses = STRUCT([houses,T([1,2])([200,10]),threeHouses])
	houses = STRUCT([houses,T([1,2])([230,70]),doubleHousesReverse])
	houses = STRUCT([houses,T([1,2])([295,75]),threeHousesReverse])
	lateralHouses = R([1,2])(-PI/3.5)(doubleHouses)
	houses = STRUCT([houses,T([1,2])([15,135]),lateralHouses])
	houses = STRUCT([houses,T([1,2])([200,200]),threeHousesReverse])
	houses = STRUCT([houses,T([1,2])([100,205]),R([1,2])(PI/7)(threeHousesReverse)])
	houses = STRUCT([houses,T([1,2])([110,140]),threeHouses])
	neighbourhood = STRUCT([streets,houses])
	neighbourhood = T(3)(3.05)(neighbourhood)
	neighbourhood = STRUCT([neighbourhood,basementComplete])
	""" Putting the trees in the neighbourhood"""
	tree = ggpl_build_tree()
	neighbourhood = STRUCT([neighbourhood,T([1,2])([100,100]),tree])
	neighbourhood = STRUCT([neighbourhood,T([1,2])([150,118]),tree])
	neighbourhood = STRUCT([neighbourhood,T([1,2])([170,118]),tree])
	neighbourhood = STRUCT([neighbourhood,T([1,2])([150,130]),tree])
	neighbourhood = STRUCT([neighbourhood,T([1,2])([170,132]),tree])
	neighbourhood = STRUCT([neighbourhood,T([1,2])([180,118]),tree])
	neighbourhood = STRUCT([neighbourhood,T([1,2])([100,120]),tree])
	neighbourhood = STRUCT([neighbourhood,T([1,2])([205,118]),tree])
	neighbourhood = STRUCT([neighbourhood,T([1,2])([205,135]),tree])
	neighbourhood = STRUCT([neighbourhood,T([1,2])([205,100]),tree])
	neighbourhood = STRUCT([neighbourhood,T([1,2])([200,85]),tree])
	neighbourhood = STRUCT([neighbourhood,T([1,2])([200,150]),tree])
	neighbourhood = STRUCT([neighbourhood,T([1,2])([200,160]),tree])
	neighbourhood = STRUCT([neighbourhood,T([1,2])([130,175]),tree])
	neighbourhood = STRUCT([neighbourhood,T([1,2])([120,175]),tree])
	neighbourhood = STRUCT([neighbourhood,T([1,2])([110,175]),tree])
	neighbourhood = STRUCT([neighbourhood,T([1,2])([100,175]),tree])
	"""trees in the left side of the model, inner part of the street"""
	neighbourhood = STRUCT([neighbourhood,T([1,2])([170,50]),tree])
	neighbourhood = STRUCT([neighbourhood,T([1,2])([175,60]),tree])
	neighbourhood = STRUCT([neighbourhood,T([1,2])([175,70]),tree])
	neighbourhood = STRUCT([neighbourhood,T([1,2])([180,80]),tree])
	neighbourhood = STRUCT([neighbourhood,T([1,2])([180,90]),tree])
	neighbourhood = STRUCT([neighbourhood,T([1,2])([185,100]),tree])
	"""trees in the upper side of the model pointing to the center of the model"""
	neighbourhood = STRUCT([neighbourhood,T([1,2])([160,50]),tree])
	neighbourhood = STRUCT([neighbourhood,T([1,2])([149,50]),tree])
	neighbourhood = STRUCT([neighbourhood,T([1,2])([135,50]),tree])
	neighbourhood = STRUCT([neighbourhood,T([1,2])([125,50]),tree])
	neighbourhood = STRUCT([neighbourhood,T([1,2])([115,53]),tree])
	"""trees in the upper side pointing to the x axis"""
	neighbourhood = STRUCT([neighbourhood,T([1,2])([115,38]),tree])
	neighbourhood = STRUCT([neighbourhood,T([1,2])([125,38]),tree])
	neighbourhood = STRUCT([neighbourhood,T([1,2])([135,38]),tree])
	neighbourhood = STRUCT([neighbourhood,T([1,2])([75,70]),tree])
	neighbourhood = STRUCT([neighbourhood,T([1,2])([70,81]),tree])
	"""building a square"""
	square = CIRCLE(16.0)([32,8])
	square = PROD([square,Q(0.5)])
	square = TEXTURE("Texture/road_texture.jpg")(square)
	neighbourhood = STRUCT([neighbourhood,T([1,2,3])([275,36,3.5]),square])
	VIEW(neighbourhood)
	return neighbourhood

ggpl_suburban_housing_neighbourhood()