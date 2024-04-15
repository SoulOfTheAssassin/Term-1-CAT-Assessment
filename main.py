import random
import pygame
import sys
from termcolor import colored
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

def printstats(name, x, y, colour):
    print(colored(f'{name}', colour) + ' Information')
    print(colored(f'{name}', colour) + f' Coordinates: {x}, {y}')


def create_app_window(width, height):
    print(f'\nWelcome. The plane goes from -{width/2} to {width/2} in both the x and y directions')
    pygame.display.set_caption("<App Name> TBD")           
    app_dimensions = (width + 10, height + 10)
    app_surf = pygame.display.set_mode(app_dimensions)
    app_surf_rect = app_surf.get_rect()
    return app_surf, app_surf_rect

def app_surf_update(destdict, p1dict, p2dict):
    app_surf.fill('white')
    pygame.draw.line(app_surf, 'grey',(0,app_surf_rect.height/2),(app_surf_rect.width,app_surf_rect.height/2),width=1)
    pygame.draw.line(app_surf, 'grey',(app_surf_rect.width/2, 0),(app_surf_rect.width/2,app_surf_rect.height),width=1)
    pygame.draw.circle(app_surf, 'black',destdict['Pygame Coords'], radius = 3, width = 3)
    pygame.draw.circle(app_surf, 'black',destdict['Pygame Coords'], radius = 10, width = 1)
    pygame.draw.circle(app_surf, p1dict['Colour'], p1dict['Pygame Coords'], radius = 3, width = 2)
    pygame.draw.circle(app_surf, p2dict['Colour'], p2dict['Pygame Coords'], radius = 3, width = 2)
    pygame.draw.circle(app_surf, p1dict['Colour'], p1dict['Pygame Coords'], radius = 10, width = 1)
    pygame.draw.circle(app_surf, p2dict['Colour'], p2dict['Pygame Coords'], radius = 10, width = 1)

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

def initialise_entities():
    p1dict['Pygame Coords'] = conv_cartesian_to_pygame_coords(p1dict['X'], p1dict['Y']) # convert and store pygame coordinates
    p2dict['Pygame Coords'] = conv_cartesian_to_pygame_coords(p2dict['X'], p2dict['Y'])
    destdict['Pygame Coords'] = conv_cartesian_to_pygame_coords(destdict['X'], destdict['Y'])




sizex = int(input('What size plane do you want (x)? '))
sizey = int(input('What size plane do you want (y)? '))

#this is the code to find the midpoint between player 1 and destination
# 1: x difference  2: x midpoint  3: y difference  4: y midpoint  5: actual distance  6: distance to midpoint

p1dict = {
    'Name': 'Player ONE',
    'X': random.randint(pos_to_neg(sizex),sizex),
    'Y': random.randint(pos_to_neg(sizey),sizey),
    'Pygame Coords': None,
    'Colour': 'red',
}

p2dict = {
    'Name': 'Player TWO',
    'X': random.randint(pos_to_neg(sizex),sizex),
    'Y': random.randint(pos_to_neg(sizey), sizey),
    'Pygame Coords': None,
    'Colour': 'blue',
}

destdict = {
    'Name': 'Destination',
    'X': random.randint(pos_to_neg(sizex), sizex),
    'Y': random.randint(pos_to_neg(sizey), sizey),
    'Pygame Coords': None,
    'Colour': 'black',
}

app_surf, app_surf_rect = create_app_window(sizex*2, sizey*2)

initialise_entities()

angles = { #angels of directions
   1: (0, 45),
   2: (45, 90),
   3: (90, 135),
   4: (135, 180),
   5: (180, 225),
   6: (225, 270),
   7: (270, 315),
   8: (315, 360)
}

directions = [1,2,3,4,5,6,7,8]
 # math
p1_to_destination = distance(p1dict['X'], p1dict['Y'], destdict['X'], destdict['Y'])
p2_to_destination = distance(p2dict['X'], p2dict['Y'], destdict['X'], destdict['Y'])
players_distance = distance(p1dict['X'], p1dict['Y'], p2dict['X'], p2dict['Y'])

grad_p1_destination = gradient(p1dict['X'], p1dict['Y'], destdict['X'], destdict['Y'])
grad_p2_destination = gradient(p2dict['X'], p2dict['Y'], destdict['X'], destdict['Y'])
grad_players = gradient(p1dict['X'], p1dict['Y'], p2dict['X'], p2dict['Y'])

mid_p1_destination = midpoint(p1dict['X'], p1dict['Y'], destdict['X'], destdict['Y'])
mid_p2_destination = midpoint(p2dict['X'], p2dict['Y'], destdict['X'], destdict['Y'])
players_mid = midpoint(p1dict['X'], p1dict['Y'], p2dict['X'], p2dict['Y'])

mid_p2_destination = remove(mid_p2_destination)
mid_p1_destination = remove(mid_p1_destination)
players_mid = remove(players_mid)


app_surf_update(destdict, p1dict, p2dict)
#player 1 stats
printstats(p1dict['Name'], p1dict['X'], p1dict['Y'], 'red')
print(f'Distance to Destination: {p1_to_destination}')
print(f'Distance to Player 2: {players_distance}')
print(f'Gradient with Destination: {grad_p1_destination}')
print(f'Gradient with Player 2: {grad_players}')
print(f'Midpoint Coords with Destination: {mid_p1_destination}')
print(f'Midpoint Coords with Player 2: {players_mid}')
print('\n')
#player 2 stats
printstats(p2dict['Name'], p2dict['X'], p2dict['Y'], p2dict['Colour'])
print(f'Distance to Destination: {p2_to_destination}')
print(f'Distance to Player 2: {players_distance}')
print(f'Gradient with Destination: {grad_p2_destination}')
print(f'Gradient with Player 2: {grad_players}')
print(f'Midpoint Coords with Destination: {mid_p2_destination}')
print(f'Midpoint Coords with Player 2: {players_mid}')
print('\n')
#destination stats
printstats(destdict['Name'], destdict['X'], destdict['Y'], 'grey')
print(f'Distance to Player 1: {p1_to_destination}')
print(f'Distance to Player 2: {p2_to_destination}')
print(f'Gradient with Player 1: {grad_p1_destination}')
print(f'Gradient with Player 2: {grad_p2_destination}')
print(f'Midpoint Coords with Player 1: {mid_p1_destination}')
print(f'Midpoint Coords with Player 2: {mid_p2_destination}')
print('\n')
turns = 1
win = False
direction = ''
refresh_window()
while win != True:                             # The gameplay happens in here. Infinite loop until the user quits or a player wins"
   for event in pygame.event.get():    # scan through all 'events' happening to the window such as mouse clicks and key presses
       if event.type == pygame.QUIT:   # must have this else the user can't quit!
           pygame.quit()
           sys.exit()
       if turns == 1:     # if the left button was pressed, ask for player 1 new coordinates (for you, you must ask for distance and direction!)
           print(colored('Player ONE:', p1dict['Colour']))
           while True:
                try:
                    dist, direction = int(input('Please enter the distance and direction you wish to travel in the format <distance>, <direction>: ')).split(',')
                except ValueError:
                    print('Please use integers in the format <distance>, <direction>.')
                else:
                    break
           turns = 2
           
       elif turns == 2:    # if the right buttom was pressed, as for player two's request (you must has for distance and direction)
           dist, direction = input("Enter new coordinates for Player TWO: e.g. 60, -155: ").split(",") # You need to ask for distance and direction
           dist = int(dist)
           p2dict['Cartesian Coords'] = (dist, direction)
           p2dict['Pygame Coords'] = conv_cartesian_to_pygame_coords(dist, direction)
           turns = 1
               # If you plan to use some or all of my code in your investigation, email me with the subject line of you want to name the game. Be creative :)
           
   app_surf_update(destdict, p1dict, p2dict)    # call the function to update the app surface with the new coordinates. Send it the entities
   refresh_window()            # now refresh the window so that our changes are visible. Loop back to while True.