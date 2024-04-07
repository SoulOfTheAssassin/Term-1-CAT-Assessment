import random
import pygame
import sys
import math
from triplesdictionary import triples

pygame.init()
app_clock = pygame.time.Clock()

def hypotenuse(x, y):
    x = x ** 2  
    y = y ** 2
    e = x + y
    e = math.sqrt(e)
    return e

def pos_to_neg(x):
    return 0-x

def middle(px, destinationx, py, destinationy):
    middle = []
    if px < destinationx:
        placeholderx = destinationx - px
    elif px > destinationx:
        placeholderx = px - destinationx
    elif px == destinationx:
        placeholderx = px

    middle.append(placeholderx)
 
    placeholderx = placeholderx / 2

    if px < destinationx:
        placeholderx = px + placeholderx
    elif px > destinationx:
        placeholderx = destinationx + placeholderx
    elif px == destinationx:
        placeholderx = 0

    middle.append(placeholderx)


    if py < destinationy:
        placeholdery = destinationy - py
    elif py > destinationy:
        placeholdery = py - destinationy
    elif py == destinationy:
        placeholdery = py

    middle.append(placeholdery)
        
    placeholdery = placeholdery / 2

    if py < destinationy:
        placeholdery = py + placeholdery
    elif py > destinationy:
        placeholdery = destinationy + placeholdery
    elif py == destinationy:
        placeholdery = 0

    middle.append(placeholdery)
    
    return middle

def create_app_window(width, height):
    print(f'\nWelcome. The plane goes from -{width/2} to {width/2} in both the x and y directions')
    pygame.display.set_caption("<App Name> TBD")           # Email me with a suggestion of what we should name this app/game. 
    app_dimensions = (width + 10, height + 10)             # to give a bit of margin. -400 to 400 both ways
    app_surf = pygame.display.set_mode(app_dimensions)     # create the main display surface for us to draw on
    app_surf_rect = app_surf.get_rect()                    # get a rectangle with important coordinates of the display surface.
    return app_surf, app_surf_rect # so that they can be used outside the function. At the moment they are local variables

def app_surf_update(destinationdict, p1dict, p2dict):
    app_surf.fill('white') # fill the display surface with white background colour

    # draw the x-axis and the y-axis
    # pygame.draw.line() needs the display surfaceto draw on, colour of the line, starting coordinates and ending coordinates
    pygame.draw.line(app_surf, 'grey',(0,app_surf_rect.height/2),(app_surf_rect.width,app_surf_rect.height/2),width=1)
    pygame.draw.line(app_surf, 'grey',(app_surf_rect.width/2, 0),(app_surf_rect.width/2,app_surf_rect.height),width=1)
    
    # draw destination
    # pygame.draw.circle() needs the surface to draw on, colour, coordinates, circle radius and line width
    pygame.draw.circle(app_surf, 'black',destinationdict['Pygame Coords'], radius = 3, width = 3)

    # draw player one and player two
    pygame.draw.circle(app_surf, p1dict['Colour'], p1dict['Pygame Coords'], radius = 3, width = 2)
    pygame.draw.circle(app_surf, p2dict['Colour'], p2dict['Pygame Coords'], radius = 3, width = 2)

def refresh_window():
    pygame.display.update() # refresh the screen with what we drew inside the app_surf_update() function
    app_clock.tick(24)      # tell pygame to refresh the screen 24 times per second

def conv_cartesian_to_pygame_coords(x,y):
    # pygame's coordinate system has the origin at the top left corner which is weird (they have good reasons for this)
    # x values increase to the right and y values increase going DOWN which is backwards!
    # we need to move the x coordinate to the center which is easy - just add half a window width
    # for the y coordinate, we need to first negate it, then move it down half a window height
    pygame_x = x + app_surf_rect.width / 2
    pygame_y = -y + app_surf_rect.height /2
    return(pygame_x, pygame_y)              # return the 'weird' coordinates that pygame can use

def initialise_entities(x, y):
    # initially set the requested coordinates to random values
    # each time you call randint() you get new random coords
    p1_rand_x, p1_rand_y = random.randint(pos_to_neg(x),x), random.randint(pos_to_neg(y),y)
    p1dict['Cartesian Coords'] = (p1_rand_x, p1_rand_y)     # store the random cartesian coordinates
    p1dict['Pygame Coords'] = conv_cartesian_to_pygame_coords(p1_rand_x, p1_rand_y) # convert and store pygame coordinates

    p2_rand_x, p2_rand_y = random.randint(pos_to_neg(x),x), random.randint(pos_to_neg(y),y)
    p2dict['Cartesian Coords'] = (p2_rand_x, p2_rand_y)
    p2dict['Pygame Coords'] = conv_cartesian_to_pygame_coords(p2_rand_x, p2_rand_y)

    dest_rand_x, dest_rand_y = random.randint(pos_to_neg(x),x), random.randint(pos_to_neg(y),y)
    destinationdict['Cartesian Coords'] = (dest_rand_x, dest_rand_y)
    destinationdict['Pygame Coords'] = conv_cartesian_to_pygame_coords(dest_rand_x, dest_rand_y)
    # no need to return entities. They are dictionaries so the function can modify them directly (see the Python Functions tutorial on Connect Notices)




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
p1mid = middle(p1x, destinationx, p1y, destinationy)
p2mid = middle(p2x, destinationx, p2y, destinationy)

print(p1mid)
print(p2mid)

#math
placeholderx = p1mid[0]
placeholdery = p1mid[2]

p1mid.append(hypotenuse(placeholderx, placeholdery))

placeholderx = p1mid[1]
placeholdery = p1mid[3]

p1mid.append(hypotenuse(placeholderx, placeholdery))

print(p1mid)


print(pos_to_neg(3))



p1dict = {
    'Name': 'Player 1',
    'Cartesian Coords': None,
    'Pygame Coords': None,
    'Colour': 'red',
}

p2dict = {
    'Name': 'Player 2',
    'Cartesian Coords': None,
    'Pygame Coords': None,
    'Colour': 'blue',
}

destinationdict = {
    'Name': 'Destination',
    'Cartesian Coords': None,
    'Pygame Coords': None,
    'Colour': 'black',
}






app_surf, app_surf_rect = create_app_window(sizex, sizey)

initialise_entities(sizex, sizey)

while True:                             # The gameplay happens in here. Infinite loop until the user quits or a player wins"
   for event in pygame.event.get():    # scan through all 'events' happening to the window such as mouse clicks and key presses
       if event.type == pygame.QUIT:   # must have this else the user can't quit!
           pygame.quit()
           sys.exit()
       if event.type == pygame.MOUSEBUTTONDOWN:    # if a mouse button is down
           left_button, middle_button, right_button = pygame.mouse.get_pressed()   # get the state of the mouse buttons
           if left_button == True:     # if the left button was pressed, ask for player 1 new coordinates (for you, you must ask for distance and direction!)
               requested_x, requested_y = input("Enter new coordinates for Player ONE: e.g. 60, -155: ").split(",") # You neeed to ask for distance and direction
               requested_x = int(requested_x)
               requested_y = int(requested_y)
               p1dict['Cartesian Coords'] = (requested_x, requested_y)
               p1dict['Pygame Coords'] = conv_cartesian_to_pygame_coords(requested_x, requested_y)
           if right_button == True:    # if the right buttom was pressed, as for player two's request (you must has for distance and direction)
               requested_x, requested_y = input("Enter new coordinates for Player TWO: e.g. 60, -155: ").split(",") # You need to ask for distance and direction
               requested_x = int(requested_x)
               requested_y = int(requested_y)
               p2dict['Cartesian Coords'] = (requested_x, requested_y)
               p2dict['Pygame Coords'] = conv_cartesian_to_pygame_coords(requested_x, requested_y)
               # If you plan to use some or all of my code in your investigation, email me with the subject line of you want to name the game. Be creative :)
           
   app_surf_update(destinationdict, p1dict, p2dict)    # call the function to update the app surface with the new coordinates. Send it the entities
   refresh_window()            # now refresh the window so that our changes are visible. Loop back to while True.