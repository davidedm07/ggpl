from pyplasm import *
from larlib import *
import csv

def buildStructure((px,py),distance_pillars,(by,bz),distance_beams):

  """first pillar of the structure"""
  first_pillar = CUBOID([px,py,distance_beams[-1]])
  """ length of the array of the distances among pillars"""
  length_pillars = len(distance_pillars)
  """ length of the array of the distances among beams"""
  length_beams = len(distance_beams)
  """ assign the first pillar as the temporary structure"""
  structure = first_pillar 
  """ adding beams for every pillar"""
  for i in range(length_pillars):
    beam = CUBOID([distance_pillars[i],by,bz]) 
    for j in range(length_beams):
      """the last beam has to be a little higher than the others"""
      if j == length_beams-1:
        last_beam = CUBOID([distance_pillars[i]+px,by,bz])
        structure = STRUCT([structure,T(3)(distance_beams[j]),last_beam])
        """the other beams all have the same heigth""" 
      else:
        structure = STRUCT([structure,T(3)(distance_beams[j]),beam])
    """closure pillar"""      
    pillar =  CUBOID([px,py,distance_beams[-1]])
    """ concatenation of the temporary structures"""
    structure = STRUCT([structure,T(1)(distance_pillars[i]),pillar])
    """end loop"""

    """display the final structure"""

  return structure  
  
   

def ggpl_bone_structure(file_name):
	"""read csv file"""
	with open(file_name, 'rb') as csvfile:
		reader = csv.reader(csvfile)
		odd = []
		even = []
		i=0
		"""put the odd lines in a list called odd and the even ones in a list called even"""
		for row in reader:
			if i%2==1:
				odd.append(row)
				i=i+1
			elif i%2==0:
				even.append(row)
				i=i+1

	"""reset the value of the variable i"""
	i=0
	"""scan every line of the list even and takes the parameters"""
	for row in even:
		"""dimensions of a pillar"""
		(px,py)=(float(row[0]),float(row[1]))
		"""initialize the array for the distances among pillars"""
		distance_pillars = []
		"""put the cursor on the right spot"""
		j=3
		"""scan the file until it finds the close bracket which closes the array"""
		while row[j]!="]":
			"""put the data in the array"""
			distance_pillars.append(float(row[j]))
			j=j+1
		"""dimension of a beam taken from the file"""
		(by,bz)= (float(row[j+1]),float(row[j+2]))
		"""put the cursor on the right spot"""
		j= j+4
		"""istanciate the array for the distances among the beams"""
		distance_beams = []
		"""scan the file as done before"""
		while row[j]!="]":
			distance_beams.append(float(row[j]))
			j=j+1		
		"""create the first structure putting the connection beams"""
		if i==0:
			structure=buildStructure((px,py),distance_pillars,(by,bz),distance_beams)
			"""assign the right value to the distance between  2 2D structures"""
			"""this distance will be used as the length of the connection beams"""
			partialDistance = float(odd[0][0])
			"""create the x coordinate of the connection beam"""
			xBeam = QUOTE([float(row[0])])
			l=[]
			z=0
			cont = 0
			"""create the right number of connection beams"""
			for el in distance_beams:
				"""need to reset the coordinates system in order to put the
				right distance between the connection beams"""
				if z==0:
					distance = -(el-cont)
					z += 1
				else:
					distance = -(el-cont-float(row[0]))
					z +=1
				"""putting the calculated values in the list"""
				l.append(distance)
				cont = el
				l.append(float(row[1]))
			"""creating the z coordinate of the beams"""
			zBeam = QUOTE(l)
			yBeam = QUOTE([float(odd[0][0])])
			xyBeam = PROD([xBeam,yBeam])
			"""creating the 3D beam"""
			beam = PROD([xyBeam,zBeam])
			partialBeam = STRUCT([beam,T(1)(1),beam])
			"""creating a struct of beams put in the right spot according to the pillars"""
			for y in range(len(distance_pillars)):
				partialBeam = STRUCT([partialBeam,T(1)(distance_pillars[y]),beam])
			"""create the 2D structure with the connection beams"""
			firstStructure=STRUCT([structure,T(2)(1),partialBeam])
			partialStructure=firstStructure	
			"""last 2D structure to close the final result"""
		elif i== len(even)-1:
			partialStructure= STRUCT([partialStructure,T(2)(partialDistance),structure])
			"""create the intermediate structures"""
		else:
			partialStructure= STRUCT([partialStructure,T(2)(partialDistance),firstStructure])
			m=0
			partialDistance=0
			"""summing the fistance between the 2D structures"""
			while m<= i:
				partialDistance += float(odd[m][0])
				m+=1
		i= i+1
	"""display the result"""
	VIEW(partialStructure)
		



if __name__ == '__main__':
	ggpl_bone_structure("frame_data_460009.csv")