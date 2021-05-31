# -*- coding: utf-8 -*-
from writer import *

#注意: x为上下 +x为向右 [-65,65]
#y为左右，+y为向右 [-65,65]
#z为前后，+z为靠近镜头

outmap=[]

a=makeBall_opaq(outmap,position=[-60.,30.,0.],color=[0,255,0])
# a=makeBall_mirror(a,position=[-45.,30.,0.])
# a=makeBall_transparent(a,position=[-40.,30.,20.])
# a=drawLine(outmap=[],ball="s",fromPoint=[60.,30.],toPoint=[-60.,-30.],z=0,number=6,color="random")
# a=drawSin(outmap,ball="op",fromPoint=[60.,30.],toPoint=[-60.,-30.],factor=20,number=10,color="random")
# a=drawCic(outmap,ball="op",centerPoint=[0.,0.],color="random",jiaodu=40)

outAndRend(a,bg=[217,237,244],size=1280)