import vpython
from vpython import *
import numpy as np

x1, y1, z1, x2, y2, z2 = np.load('..\\data\\3Dpen.npy')
ball1 = vpython.sphere(color = color.green, radius = 0.3, make_trail=True, retain=20)
ball2 = vpython.sphere(color = color.blue, radius = 0.3, make_trail=True, retain=20)
rod1 = cylinder(pos=vector(0,0,0),axis=vector(0,0,0), radius=0.05)
rod2 = cylinder(pos=vector(0,0,0),axis=vector(0,0,0), radius=0.05)
base  = box(pos=vector(0,-4.25,0),axis=vector(1,0,0),
            size=vector(10,0.5,10) )
s1 = cylinder(pos=vector(0,-3.99,0),axis=vector(0,-0.1,0), radius=0.8, color=color.gray(luminance=0.7))
s2 = cylinder(pos=vector(0,-3.99,0),axis=vector(0,-0.1,0), radius=0.8, color=color.gray(luminance=0.7))

print('Start')
i = 0
while True:
    rate(30)
    i = i + 1
    i = i % len(x1)
    ball1.pos = vector(x1[i], z1[i], y1[i])
    ball2.pos = vector(x2[i], z2[i], y2[i])
    rod1.axis = vector(x1[i], z1[i], y1[i])
    rod2.pos = vector(x1[i], z1[i], y1[i])
    rod2.axis = vector(x2[i]-x1[i], z2[i]-z1[i], y2[i]-y1[i])
    s1.pos = vector(x1[i], -3.99, y1[i])
    s2.pos = vector(x2[i], -3.99, y2[i])