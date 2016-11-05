from pyplasm import *
import math
from ast import literal_eval

def round_vertex(verts):
	for v in verts:
		v[0]=math.fabs(round(v[0],2))
		v[1]=math.fabs(round(v[1],2))
		v[2]=math.fabs(round(v[2],2))

def create_hpc(verts,cells):
	roof =MKPOL([verts,cells,None])
	return roof


def replace_cells(cells,dictionary):
	for cell in cells:
		for element in cell:
			for key,val in dictionary.items():
				if element in val:
					index = cell.index(element)
					cell[index] = int(key)


def find_key(dictionary, key):
	i=1
	for k in dictionary.keys():
		if k==key:
			return i;
		i+=1
	return 0

def check_coordinates(v,listVerts):
	xV,yV,zV = v
	for i in range(len(listVerts)):
		x,y,z = listVerts[i]
		if xV==x or yV==y:
			return True
		else:
			return False 

def ggpl_roof_builder(hpcObject):
	roofSkeleton = SKEL_2(hpcObject)
	structureInfo= UKPOL(roofSkeleton)
	cells = structureInfo[1]
	dictionary = {}
	verts =structureInfo[0]
	round_vertex(verts)
	i=1
	for v in verts:
		key=','.join(map(str,v))
		if not key in dictionary.keys():
			dictionary[','.join(map(str,v))] = [i]
		else:
			dictionary.get(','.join(map(str,v))).append(i)

		i+=1
	i=1
	vertsDictionary = {}
	verts=[]
	highVerts =[]
	highVertsV = []
	for key in dictionary.keys():
		vertsDictionary[str(i)] = dictionary.get(key)
		v = literal_eval(key)
		verts.append(v)
		x,y,z = v
 		if z>0:
 			highVerts.append(find_key(dictionary,','.join(map(str,v))))
 			highVertsV.append(v)
		i+=1
	replace_cells(cells,vertsDictionary)		
 	roof = MKPOL([verts,cells,None])
 	roof = OFFSET([.1,.1,.1])(SKEL_1(roof))

 	if not highVerts:
 			highVerts=verts
 	up_cells=[]
 	for cell in cells:
 		for i in range(len(highVerts)):
 			if check_coordinates(highVertsV[i],verts):
 				if all(x in cell for x in highVerts):
 					up_cells.append(cell)
 			else:
 				if highVerts[i] in cell:
 					up_cells.append(cell)
 							
 	upboundary_cells = MKPOL([verts,up_cells,None])
 	roof = STRUCT([roof,upboundary_cells])
 	VIEW(roof)



if __name__ == '__main__':
	#verts = [[0,0,0],[8,0,0],[8,8,0],[0,8,0],[0,4,4],[8,4,4]]
	verts = [[0,0,0],[8,0,0],[8,8,0],[0,8,0],[2,4,4],[6,4,4]]
	cells=[[1,4,5],[2,6,3],[3,4,5,6],[1,2,5,6],[1,4,3,2]]
	hpcObject=create_hpc(verts,cells)
	ggpl_roof_builder(hpcObject)

