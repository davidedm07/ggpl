import csv
from pyplasm import *
#DIFFERENCE
def ggpl_house_builder():
		with open("muri_esterni.lines", "rb") as csvfile:
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
		externalWalls = PROD([externalWalls,Q(3)])
		externalWalls = TEXTURE("external_walls.jpg")(externalWalls)
		pavement = TEXTURE("parquet_texture.jpg")(pavement)
		with open("muri_interni.lines", "rb") as csvfile:
			csvReader = csv.reader(csvfile,delimiter=",")
			internalWalls_list = []
			for row in csvReader :
				internalWalls_list.append(POLYLINE([[float(row[0]),float(row[1])],[float(row[2]),float(row[3])]]))
		internalWalls = STRUCT(internalWalls_list)
		internalWalls = S([1,2])([xScale,yScale])(internalWalls)
		internalWalls = OFFSET([.2,.2])(internalWalls)
		internalWalls = PROD([internalWalls,Q(3)])
		
		with open("porte.lines", "rb") as csvfile:
			csvReader = csv.reader(csvfile,delimiter=",")
			listDoors = []
			cuboid = []
			cont = 0
			for row in csvReader:
				cont += 1
				cuboid.append([float(row[0]),float(row[1])])
				if cont == 4:
					listDoors.append(MKPOL([cuboid,[[1,2,3,4]],None]))
					cuboid = []
					cont = 0
		with open("finestre.lines", "rb") as csvfile:
			csvReader = csv.reader(csvfile,delimiter=",")
			listWindows = []
			cuboid = []
			cont = 0
			for row in csvReader:
				cont += 1
				cuboid.append([float(row[0]),float(row[1])])
				if cont == 4:
					listWindows.append(MKPOL([cuboid,[[1,2,3,4]],None]))
					cuboid = []
					cont = 0			

			doors = STRUCT(listDoors)
			doors = S([1,2])([xScale, yScale])(doors)
			windows = STRUCT(listWindows)
			windows = S([1,2])([xScale, yScale])(windows)
        	doors = OFFSET([.2,.2])(doors)
        	doors = PROD([doors, Q(3)])
        	V#IEW(doors)
        	internalWalls = DIFFERENCE([internalWalls,doors])
        	internalWalls = TEXTURE("internal_walls.jpg")(internalWalls)
        	walls = STRUCT([internalWalls,externalWalls])
        	internalWalls = DIFFERENCE([internalWalls,doors])
		house = STRUCT([walls,pavement])
		VIEW(house)

ggpl_house_builder()