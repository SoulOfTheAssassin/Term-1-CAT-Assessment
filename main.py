import random
import pygame
import sys
from triplesdictionary import triples

pygame.init()
app_clock = pygame.time.Clock()


def remove(string):
    var = str(string)
    var = var.replace('[', '')
    var = var.replace(']', '')
    return var

def hypotenuse(x, y):
    x = x ** 2  
    y = y ** 2
    e = x + y
    e = e ** 0.5
    return int(e)

def distance(p1x, p1y, dx, dy):  #
    xdistance = dx - p1x                                               
    ydistance = dy - p1y                                                 
    p1_distance = hypotenuse(xdistance, ydistance)                 
    distance = round(p1_distance, 1)
    return distance

def pos_to_neg(x):
    return 0-x

def difference(x1, x2):
    if x1 < x2:
        placeholderx = x2 - x1
    elif x1 > x2:
        placeholderx = x1 - x2
    elif x1 == x2:
        placeholderx = x1
    return placeholderx

def midpoint(x1, y1, x2, y2):
    x = (x1 + x2)/2                            
    y = (y1 + y2)/2  
    return [x, y]

def gradient(x1, y1, x2, y2):
    var = (y2 - y1)/(x2 - x1)
    var = round(var, 1)
    return var

def printstats(name, x, y):
    print(f'\n\n{name} Information')
    print(f'{name} Coordinates: {x}, {y}')


def create_app_window(width, height):
    print(f'\nWelcome. The plane goes from -{width/2} to {width/2} in both the x and y directions')
    pygame.display.set_caption("App Name TBD")           # Email me with a suggestion of what we should name this app/game. 
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
p1mid = []
p2mid = []

sizex = int(input('What size plane do you want (x)? '))
sizey = int(input('What size plane do you want (y)? '))

#this is the code to find the midpoint between player 1 and destination
# 1: x difference  2: x midpoint  3: y difference  4: y midpoint  5: actual distance  6: distance to midpoint

p1dict = {
    'Name': 'Player 1',
    'X': random.randint(pos_to_neg(sizex),sizex),
    'Y': random.randint(pos_to_neg(sizey),sizey),
    'Pygame Coords': None,
    'Colour': 'red',
}

p2dict = {
    'Name': 'Player 2',
    'X': random.randint(pos_to_neg(sizex),sizex),
    'Y': random.randint(pos_to_neg(sizey), sizey),
    'Pygame Coords': None,
    'Colour': 'blue',
}

destinationdict = {
    'Name': 'Destination',
    'X': random.randint(pos_to_neg(sizex), sizex),
    'Y': random.randint(pos_to_neg(sizey), sizey),
    'Pygame Coords': None,
    'Colour': 'black',
}

directions = { #angels of directions
   1: (0, 45),
   2: (45, 90),
   3: (90, 135),
   4: (135, 180),
   5: (180, 225),
   6: (225, 270),
   7: (270, 315),
   8: (315, 360)
}

p1_to_destination = distance(p1dict['X'], p1dict['Y'], destinationdict['X'], destinationdict['Y'])
p2_to_destination = distance(p2dict['X'], p2dict['Y'], destinationdict['X'], destinationdict['Y'])
players_distance = distance(p1dict['X'], p1dict['Y'], p2dict['X'], p2dict['Y'])

grad_p1_destination = gradient(p1dict['X'], p1dict['Y'], destinationdict['X'], destinationdict['Y'])
grad_p2_destination = gradient(p2dict['X'], p2dict['Y'], destinationdict['X'], destinationdict['Y'])
grad_players = gradient(p1dict['X'], p1dict['Y'], p2dict['X'], p2dict['Y'])

mid_p1_destination = midpoint(p1dict['X'], p1dict['Y'], destinationdict['X'], destinationdict['Y'])
mid_p2_destination = midpoint(p2dict['X'], p2dict['Y'], destinationdict['X'], destinationdict['Y'])
players_mid = midpoint(p1dict['X'], p1dict['Y'], p2dict['X'], p2dict['Y'])

mid_p2_destination = remove(mid_p2_destination)
mid_p1_destination = remove(mid_p1_destination)
players_mid = remove(players_mid)

app_surf, app_surf_rect = create_app_window(sizex, sizey)

initialise_entities(sizex, sizey)
#player 1 stats
printstats(p1dict['Name'], p1dict['X'], p1dict['Y'])
print(f'Distance to Destination: {p1_to_destination}')
print(f'Distance to Player 2: {players_distance}')
print(f'Gradient with Destination: {grad_p1_destination}')
print(f'Gradient with Player 2: {grad_players}')
print(f'Midpoint Coords with Destination: {mid_p1_destination}')
print(f'Midpoint Coords with Player 2: {players_mid}')
print('\n')
#player 2 stats
printstats(p2dict['Name'], p2dict['X'], p2dict['Y'])
print(f'Distance to Destination: {p2_to_destination}')
print(f'Distance to Player 2: {players_distance}')
print(f'Gradient with Destination: {grad_p2_destination}')
print(f'Gradient with Player 2: {grad_players}')
print(f'Midpoint Coords with Destination: {mid_p2_destination}')
print(f'Midpoint Coords with Player 2: {players_mid}')
print('\n')
#destination stats
printstats(destinationdict['Name'], destinationdict['X'], destinationdict['Y'])
print(f'Distance to Player 1: {p1_to_destination}')
print(f'Distance to Player 2: {p2_to_destination}')
print(f'Gradient with Player 1: {grad_p1_destination}')
print(f'Gradient with Player 2: {grad_p2_destination}')
print(f'Midpoint Coords with Player 1: {mid_p1_destination}')
print(f'Midpoint Coords with Player 2: {mid_p2_destination}')
print('\n')
# turns = 1
# win = False
# while win != True:                             # The gameplay happens in here. Infinite loop until the user quits or a player wins"
#    for event in pygame.event.get():    # scan through all 'events' happening to the window such as mouse clicks and key presses
#        if event.type == pygame.QUIT:   # must have this else the user can't quit!
#            pygame.quit()
#            sys.exit()
#        if turns == 1:     # if the left button was pressed, ask for player 1 new coordinates (for you, you must ask for distance and direction!)
#            requested_direction = input("Player ONE: Enter the direction you would like to go: ") # You neeed to ask for distance and direction
#            requested_distance = int(input("Player ONE: Enter the distance tou would like to go: "))
#            p1dict['Cartesian Coords'] = (requested_distance, requested_direction)
#            p1dict['Pygame Coords'] = conv_cartesian_to_pygame_coords(requested_distance, requested_direction)
#            turns = 2
#        elif turns == 2:    # if the right buttom was pressed, as for player two's request (you must has for distance and direction)
#            requested_distance, requested_direction = input("Enter new coordinates for Player TWO: e.g. 60, -155: ").split(",") # You need to ask for distance and direction
#            requested_distance = int(requested_distance)
#            p2dict['Cartesian Coords'] = (requested_distance, requested_direction)
#            p2dict['Pygame Coords'] = conv_cartesian_to_pygame_coords(requested_distance, requested_direction)
#                # If you plan to use some or all of my code in your investigation, email me with the subject line of you want to name the game. Be creative :)
           
#    app_surf_update(destinationdict, p1dict, p2dict)    # call the function to update the app surface with the new coordinates. Send it the entities
#    refresh_window()            # now refresh the window so that our changes are visible. Loop back to while True.