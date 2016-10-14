from larlib import *
from pyplasm import *

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
  VIEW(structure)
   
def main():
  """specify the parameters for the function buildStructure"""
  buildStructure((1,1),[10,20,40],(1,1),[2,4,6])


if __name__ == '__main__':
   main()

   
    
  