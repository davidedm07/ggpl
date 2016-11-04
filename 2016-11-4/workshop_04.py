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

def ggpl_roof_builder(hpcObject):
	roofSkeleton = SKEL_2(hpcObject)
	structureInfo= UKPOL(roofSkeleton)
	cells = structureInfo[1]
	print cells
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
	print dictionary
	i=1
	vertsDictionary = {}
	verts=[]
	for key in dictionary.keys():
		vertsDictionary[str(i)] = dictionary.get(key)
		verts.append(literal_eval(key))
		i+=1

	replace_cells(cells,vertsDictionary)		
	#verts= []				
	#for key in dictionary.keys():
	#	verts.append(literal_eval(key))

 	roof = MKPOL([verts,cells,None])
 	roof = OFFSET([.1,.1,.1])(SKEL_1(roof))
 	highVerts =[]
 	for vertex in verts:
 		x,y,z = vertex
 		if z>0:
 			highVerts.append(find_key(dictionary,','.join(map(str,vertex))))
 	

 	if not highVerts:
 			highVerts=verts
 	up_cells=[]
 	for cell in cells:
 		for i in range(len(highVerts)):
 			#if highVerts[i] in cell:
 			#	up_cells.append(cell)
 			if all(x in cell for x in highVerts):
 				up_cells.append(cell)				
 	upboundary_cells = MKPOL([verts,up_cells,None])
 	roof = STRUCT([roof,upboundary_cells])
 	VIEW(roof)



if __name__ == '__main__':
	#verts = [[0,0,0],[8,0,0],[8,8,0],[0,8,0],[0,4,4],[8,4,4]]
	verts = [[0,0,0],[8,0,0],[8,8,0],[0,8,0],[0,4,4],[8,4,4]]
	cells=[[1,4,5],[2,6,3],[3,4,5,6],[1,2,5,6],[1,4,3,2]]
	hpcObject=create_hpc(verts,cells)
	ggpl_roof_builder(hpcObject)

