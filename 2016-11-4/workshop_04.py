from pyplasm import *
import math
from ast import literal_eval

"""round the vertices of the structure"""
def round_vertices(verts):
	for v in verts:
		v[0]=math.fabs(round(v[0],2))
		v[1]=math.fabs(round(v[1],2))
		v[2]=math.fabs(round(v[2],2))

"""create the hpc object as parameter to the ggpl function"""
def create_hpc(verts,cells):
	roof =MKPOL([verts,cells,None])
	return roof

"""replace the cells writing the correct number of the vertices in each tuple"""
def replace_cells(cells,dictionary):
	for cell in cells:
		for element in cell:
			for key,val in dictionary.items():
				if element in val:
					index = cell.index(element)
					cell[index] = int(key)

"""set an integer as a key for a vertex"""
def find_key(dictionary, key):
	i=1
	for k in dictionary.keys():
		if k==key:
			return i;
		i+=1
	return 0

"""check the position of the upper vertices of the roof"""
"""if these vertices have the x or y coordinate in common with"""
"""the coordinates of the vertices of the basement or intermediate ones then return true"""
def check_coordinates(cell,verticesList):
	check=False	
	verticesInCell=[]
	for el in cell:
		vert=verticesList[el-1]	
		verticesInCell.append(vert)

	temp=verticesInCell[0]
	xValueTemp = temp[0]
	yValueTemp=temp[1]
	for v in verticesInCell:
		if v[1]==yValueTemp or v[0]==xValueTemp:
			check=True
		else:
			return False
	return check


"""this function creates a roof from an hpc object passed as parameter"""
def ggpl_roof_builder(hpcObject):
	"""create the skeleton of the object"""
	roofSkeleton = SKEL_2(hpcObject)
	"""extracts the vertices and the cells of the object and stores them in a list"""
	structureInfo= UKPOL(roofSkeleton)
	"""save the cells in a different list used fot the computations"""
	cells = structureInfo[1]
	"""initialize dictionary for the vertices of the structure in order to delete the duplicates"""
	dictionary = {}
	"""same procedure done for the cells"""
	verts =structureInfo[0]
	"""round vertices of the structure"""
	round_vertices(verts)
	"""counter utilised for different computations"""
	i=1
	"""for each vertex transform its value in a string and put it as key in the dictionary"""
	"""the values of the dictionary are the values assumed by the vertex"""
	"""the UKPOL keeps counting the same vertex giving it multiple numbers"""
	for v in verts:
		key=','.join(map(str,v))
		if not key in dictionary.keys():
			dictionary[','.join(map(str,v))] = [i]
		else:
			dictionary.get(','.join(map(str,v))).append(i)

		i+=1
	i=1
	"""helper dictionary"""
	vertsDictionary = {}
	"""initialize verts, in this list the procedure will put the vertices without duplicates"""
	verts=[]
	"""upper vertices of the roof stored as numbers, the 1 vertex, the 2 and so on"""
	highVerts =[]
	"""upper vertices stored as tuples"""
	highVertsV = []
	"""basement vertices stored as tuples"""
	downVertsV = []
	"""creates the lists above putting the basement vertices in a list and the other ones in another"""
	for key in dictionary.keys():
		vertsDictionary[str(i)] = dictionary.get(key)
		v = literal_eval(key)
		verts.append(v)
		x,y,z = v
 		if z>0:
 			highVerts.append(find_key(dictionary,','.join(map(str,v))))
 			highVertsV.append(v)
 		else:
 			downVertsV.append(v)

		i+=1
	"""replace the consecutive numbers of the vertices in the cell with the right id of the vertex"""	
	replace_cells(cells,vertsDictionary)
	"""creates the roof from the the computed vertices and cells"""		
 	roof = MKPOL([verts,cells,None])
 	"""creates the beams of the roof """
 	roof = OFFSET([.1,.1,.1])(SKEL_1(roof))
 	"""check what are the rising faces of the roof"""
 	up_cells=[]
 	for index in highVerts:
		for cell in cells:
			if index in cell and not check_coordinates(cell,verts) and not cell in up_cells:
				up_cells.append(cell)
 	"""creates the faces of the roof"""										
 	upboundary_cells = MKPOL([verts,up_cells,None])
 	"""assemble the final roof"""
 	roof = STRUCT([roof,upboundary_cells])
 	VIEW(roof)
 	return roof



if __name__ == '__main__':
	#gable roof
	#verts = [[0,0,0],[8,0,0],[8,8,0],[0,8,0],[0,4,4],[8,4,4]]
	#hip roof
	#verts = [[0,0,0],[8,0,0],[8,8,0],[0,8,0],[2,4,4],[6,4,4]]
	#gable and hip roof cells
	#cells=[[1,4,5],[2,6,3],[3,4,5,6],[1,2,5,6],[1,4,3,2]]
	#mansard
	#verts = [[0,0,0],[8,0,0],[8,8,0],[0,8,0],[2,2,4],[2,6,4],[6,2,4],[6,6,4]]
	#cells=[[1,4,5,6],[2,7,3,8],[3,4,8,6],[1,2,5,7],[1,4,3,2],[7,8,5,6]]
	#gambrel
	verts = [[0,0,0],[2,0,3],[2,8,3],[0,8,0],[6,0,6],[6,8,6],[10,0,3],[10,8,3],[12,0,0],[12,8,0]]
	cells=[[1,2,3,4],[2,3,6,5],[5,6,8,7],[7,8,10,9],[1,4,9,10],[1,2,5,7,9],[3,4,6,8,10]]
	hpcObject=create_hpc(verts,cells)
	ggpl_roof_builder(hpcObject)

