from pyplasm import *
import math

def ggpl_stair(dx,dy,dz):
    #get steps dimensions
    stepX=dx/2
    stepY=dy/10 #suppose the platform big long as four steps
    stepZ=dz/7
 	
    #counter for height and distance
    countH=stepZ
    countD=stepY
    #building single step
    step=CUBOID([stepX,stepY,stepZ])
    st=step
    #cycle for creating first group of stairs
    while countH<(stepZ*6):
        add_step=T(2)(countD)(step)
        countD+=stepY
        st=STRUCT([st,T(3)(countH),add_step])
        countH+=stepZ
 
    # creating the platform and using T transform
    platform=CUBOID([dx,4*stepY,stepZ])
    platform=T(2)(countD)(platform)
    platform = TEXTURE("Texture/external_walls.jpg")(platform)
    pillar = CUBOID([.4,.4,dz])
    pillar = TEXTURE("Texture/cement_texture.jpg")(pillar)
    #adding platform to struct
    st = TEXTURE("Texture/stair_texture.jpg")(st)
    stair=STRUCT([st,T(3)(countH),platform])
    stair = STRUCT([stair,T(2)(dy-4*stepY),pillar])
    stair = STRUCT([stair,T([1,2])([dx-0.4,dy-4*stepY]),pillar])
    box = SKEL_1(CUBOID([dx,dy,dz]))

    return stair	
	