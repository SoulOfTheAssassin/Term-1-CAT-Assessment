import random
import pygame
import sys
from triplesdictionary import triples
from functions import *

size = []
x = []
y = []
placeholderx = ''
placeholdery = ''

placeholderx = int(input('What size plane do you want (x)? '))
placeholdery = int(input('What size plane do you want (y)? '))

size.append(placeholderx)
size.append(placeholdery)
print(size)
sizex = int(size[0])
sizey = int(size[1])
for i in range(3):
    x.append(random.randint(1, sizex))
    y.append(random.randint(1, sizey))
    
p1x = x[0]
p1y = y[0]
p2x = x[1]
p2y = y[1]
destinationx = x[2]
destinationy = y[2]

print(p1x)
print(p1y)
print(p2x)
print(p2y)
print(destinationx)
print(destinationy)

#for triple in range(len(triples)):
#   print('foo')

#this is the code to find the midpoint between player 1 and destination
# 1: x difference  2: x midpoint  3: y difference  4: y midpoint  5: actual distance  6: distance to midpoint
p1mid = mid(p1x, destinationx, p1y, destinationy)
p2mid = mid(p2x, destinationx, p2y, destinationy)

print(p1mid)
print(p2mid)



app_surf, app_surf_rect = create_app_window(sizex, sizey)