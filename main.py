import random
import pygame
import time
import sys
from termcolor import colored
from triplesdictionary import triples

pygame.init()
app_clock = pygame.time.Clock()


def remove(list):
    var = str(list)
    var = var.replace('[', '')
    var = var.replace(']', '')
    return var

def hypotenuse(x, y):
    x = x ** 2  
    y = y ** 2
    e = x + y
    e = e ** 0.5
    return int(e)

def distance(px, py, dx, dy):  #
    xdistance = dx - px                                               
    ydistance = dy - py                                                 
    p1_distance = hypotenuse(xdistance, ydistance)                 
    distance = round(p1_distance, 1)
    return distance

def pos_to_neg(x):
    return 0-x

def slowprint(str, speed):
    for char in str:
        print(char, end='')
        sys.stdout.flush()
        time.sleep(speed)
    time.sleep(1)
    
# def slowinput(string, speed):
#     for char in string:
#         input = print(char, end='')
#         sys.stdout.flush()
#         time.sleep(speed)
#     time.sleep(1)
#     return str(input)

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
    try:
        var = (y2 - y1)/(x2 - x1)
    except ZeroDivisionError:
        return "Undefined"
    var = round(var, 1)
    return var

def printstats(name, x, y, colour):
    print(colored(f'{name}', colour) + ' Information')
    print(colored(f'{name}', colour) + f' Coordinates: {x}, {y}')

def create_app_window(width, height):
    print(f'\nWelcome. The plane goes from -{width/2} to {width/2} in both the x and y directions')
    pygame.display.set_caption("Gam ov Gradiante")           
    app_dimensions = (width + 10, height + 10)
    app_surf = pygame.display.set_mode(app_dimensions)
    app_surf_rect = app_surf.get_rect()
    return app_surf, app_surf_rect

def app_surf_update(destdict, p1dict, p2dict):
    app_surf.fill('white')
    pygame.draw.line(app_surf, 'grey',(0,app_surf_rect.height/2),(app_surf_rect.width,app_surf_rect.height/2),width=1)
    pygame.draw.line(app_surf, 'grey',(app_surf_rect.width/2, 0),(app_surf_rect.width/2,app_surf_rect.height),width=1)
    pygame.draw.circle(app_surf, 'black',destdict['Pygame Coords'], radius = 3, width = 3)
    pygame.draw.circle(app_surf, 'black',destdict['Pygame Coords'], radius = playersize, width = 1)
    pygame.draw.circle(app_surf, p1dict['Colour'], p1dict['Pygame Coords'], radius = 3, width = 2)
    pygame.draw.circle(app_surf, p2dict['Colour'], p2dict['Pygame Coords'], radius = 3, width = 2)
    pygame.draw.circle(app_surf, p1dict['Colour'], p1dict['Pygame Coords'], radius = playersize, width = 1)
    pygame.draw.circle(app_surf, p2dict['Colour'], p2dict['Pygame Coords'], radius = playersize, width = 1)

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

def moveplayer(distance, direction, dictionary):
    iffound = False
    while iffound == False:
        for triple in triples:
            if triple[2] == distance:
                a = triple[0]
                b = triple[1]
                iffound = True
                break
        if iffound == False:
            distance = distance - 1
    if direction == 1:
        dictionary['X'] += b
        dictionary['Y'] += a
    elif direction == 2:
        dictionary['X'] += a
        dictionary['Y'] += b
    elif direction == 3:
        dictionary['X'] -= a
        dictionary['Y'] += b
    elif direction == 4:
        dictionary['X'] -= b
        dictionary['Y'] += a
    elif direction == 5:
        dictionary['X'] -= b
        dictionary['Y'] -= a
    elif direction == 6:
        dictionary['X'] -= a
        dictionary['Y'] -= b
    elif direction == 7:
        dictionary['X'] += a
        dictionary['Y'] -= b
    elif direction == 8:
        dictionary['X'] += b
        dictionary['Y'] -= a

def checkwin(dictionary1, dictionary2, dictionary3, lastmove):
     if dictionary1['X'] == dictionary2['X'] and dictionary1['Y'] == dictionary2['Y']:
         win = True
     elif dictionary1['X'] == dictionary3['X'] and dictionary1['Y'] == dictionary3['Y']:
         win = True
     elif dictionary3['X'] == dictionary2['X'] and dictionary3['Y'] == dictionary2['Y']:
         win = True
     else: 
         return False
     if win: 
         if lastmove == 1:
             return "Player ONE"
         elif lastmove == 2:
             return "Player TWO"
         elif lastmove == 3:
             return "NPC"

def inputcheck():
    slowprint('Please enter move in format: distance <space> direction.', 0.085) 
    slowprint('The distance and direction must be natural numbers.', 0.085) 
    slowprint("The distance must be 5 or larger.", 0.085)  
    slowprint("The direction must to be from 1-8.", 0.085) 
    while True: 
        move = input("Enter your move: ")
        move = move.strip()
        try: 
            move=move.split(" ") # To get the distance and direction
        except:
            slowprint("Please enter in format: distance <space> direction. ", 0.085)
            continue
        try:
            distance=int(move[0])
            direction=int(move[1])
        except:
            slowprint("The distance and direction need to be natural numbers.", 0.085)
            continue
        if direction > 8 or direction < 1:
            slowprint("The direction has to be 1-8.", 0.085)
        elif distance < 0:
            slowprint("The distance cannot be negative.", 0.085)
        elif distance < 5:
            slowprint("The distance must be 5 or larger. ", 0.085)
        else:
            slowprint("Move was successful.", 0.085)
            return distance, direction


colours = ['grey', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
p1colour = 'red'
p2colour = 'blue'
npccolour = 'green'
npctoggle = False
functionloop = True
sizex = 800
sizey = 800
size = [1,2,3,4,5,6,7,8,9,10]
playersize = 5.0
functionlist = ['planesize', 'togglenpc', 'playersize', 'playercolour', 'help', 'printsettings', 'start', 'quit']
# slowprint('Here are a list of functions: ', 0.03)
# print()
# slowprint('PlaneSize: adjust the size of the plane.', 0.03)
# print()
# slowprint('ToggleNPC: Toggle the NPC.', 0.03)
# print()
# slowprint('PlayerSize: adjust the size of the players.', 0.03)           this is backup code
# print()
# slowprint('PlayerColour: change the player colours.', 0.03)
# print()
# slowprint('PrintSettings: prints all current settings.', 0.03)
# print()
# slowprint('Help: prints the rules.', 0.03)
# print()
# slowprint('Start: starts the game.', 0.03)
# print()
slowprint('''Here are a list of functions: 
PlaneSize: adjust the size of the plane.
ToggleNPC: Toggle the NPC.
PlayerSize: adjust the size of the players.
PlayerColour: change the player colours.
PrintSettings: prints all current settings.
Help: prints the rules.
Start: starts the game.
''', 0.05)
while functionloop:
    function = input('Enter function: ')
    function = function.lower()
    while function not in functionlist:
        slowprint('This is not a valid function. Please try again. ', 0.03)
        function = input('Enter function: ')
        function = function.lower()
    if function == 'planesize':
        while True:
            try:
                sizex = int(input('Enter X of Cartesian Plane: '))
            except:
                slowprint('This is not a valid input. Please input using a natural number. ', 0.085)
            else: 
                break
        while True:
            try:
                sizey = int(input('Enter Y of Cartesian Plane: '))
            except:
                slowprint('This is not a valid input. Please input using a natural number. ', 0.085)
            else: 
                break
    elif function == 'playercolour':
        while True:
            try:
                playernum = int(input('Please choose which player: '))
            except:
                slowprint('Please use a single number.', 0.085)
            else:
                break
        slowprint(f'Here is a printout of the colour list: ' + colored('grey', 'grey')+ ', ' + colored('red', 'red') + ', ' + colored('green', 'green') + ', ' + colored('yellow', 'yellow') + ', ' + colored('blue', 'blue') + ', ' + colored('magenta', 'magenta') + ', ' + colored('cyan', 'cyan') + ', ' + colored('white', 'white') + '.', 0.03)
        print()
        if playernum == 1:
            p1colour = input('Please choose a colour: ').lower()
            while p1colour not in colours:
                slowprint('Please select a colour from the list above.', 0.085)
                p1colour = input('Please choose a colour: ').lower()
        elif playernum == 2:
            p2colour = input('Please choose a colour: ').lower()
            while p2colour not in colours:
                slowprint('Please select a colour from the list above.', 0.085)
                p2colour = input('Please choose a colour: ').lower()
        elif playernum == 3:
            npccolour = input('Please choose a colour: ').lower()
            while npccolour not in colours:
                slowprint('Please select a colour from the list above.', 0.085)
                npccolour = input('Please choose a colour: ').lower()
    elif function == 'start':
        functionloop = False
    elif function == 'togglenpc':
        if npctoggle == True:
            npctoggle = False
        elif npctoggle == False:
            npctoggle = True
        slowprint(f'NPC Toggled: {npctoggle}', 0.085)
    elif function == 'help':
        slowprint('''
Two players are required to play this game. 
To win, you must land on the destination or another player.
You can only use primitive pythagorean triples.
''', 0.085)
    elif function == 'playersize':
        playersize = input('Please choose a size from 1-10: ')
        while playersize not in size:
            playersize = input('Please choose a number from 1-10: ')
        playersize = int(playersize)
    elif function == 'printsettings':
        print()
        slowprint(colored('NPC', npccolour) + f' Toggled: {npctoggle}', 0.085)
        slowprint(colored('Player ONE', p1colour) + f' colour: {p1colour}', 0.085)
        slowprint(colored('Player TWO', p2colour) + f' colour: {p2colour}', 0.085)
        slowprint(colored('NPC', npccolour) + f' colour: {npccolour}', 0.085)
        slowprint(f'Plane Size: {sizex*2} by {sizey*2}', 0.085)
        slowprint(f'Player Size: {playersize}', 0.085)
        print()


p1dict = {
    'Name': 'Player ONE',
    'X': random.randint(1,sizex),
    'Y': random.randint(1,sizey),
    'Pygame Coords': None,
    'Colour': p1colour,
    'Num': 1,
}

p2dict = {
    'Name': 'Player TWO',
    'X': random.randint(1,sizex),
    'Y': random.randint(1, sizey),
    'Pygame Coords': None,
    'Colour': p2colour,
    'Num': 2,
}

destdict = {
    'Name': 'Destination',
    'X': random.randint(1, sizex),
    'Y': random.randint(1, sizey),
    'Pygame Coords': None,
    'Colour': 'black',
    'Num': None,
}

npcdict = {
    'Name': 'Destination',
    'X': random.randint(1, sizex),
    'Y': random.randint(1, sizey),
    'Pygame Coords': None,
    'Colour': npccolour,
    'Num': 3,
    'Toggle': npctoggle,
}

app_surf, app_surf_rect = create_app_window(sizex, sizey)

initialise_entities()

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
import sys
import time


# print(f'Distance to Destination: {p1_to_destination}')
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
playerturns = 1
win = False
direction = ''
refresh_window()
print('You must click every time for each move.')
while win != True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           pygame.quit()
           sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if playerturns == 1:
                print()
                print(colored('Player ONE:', p1dict['Colour']))
                dist, direction = inputcheck()
                moveplayer(dist, direction, p1dict)
                p1dict['Pygame Coords'] = conv_cartesian_to_pygame_coords(p1dict['X'], p1dict['Y'])
                win = checkwin(p1dict, p2dict, destdict, p1dict['Num'])
                if win == "Player ONE":
                    print('The winner is: ' + colored(p1dict['Name'], p1dict['Colour']))
                playerturns = 2
            elif playerturns == 2:
                print()
                print(colored('Player TWO:', p2dict['Colour']))
                dist, direction = inputcheck()
                moveplayer(dist, direction, p2dict)
                p2dict['Pygame Coords'] = conv_cartesian_to_pygame_coords(p2dict['X'], p2dict['Y'])
                win = checkwin(p1dict, p2dict, destdict, p2dict['Num'])
                if win == "Player TWO":
                    print('The winner is: ' + colored(p2dict['Name'], p2dict['Colour']))
                playerturns = 1
#             if npctoggle:
#                 npcmovex = 
#                 npcmovey = 
#                 print()
#                 print(colored('NPC:', npcdict['Colour']))
#                 print('''Please enter move in format: distance <space> direction.
# The distance and direction must be natural numbers.
# The distance must be 5 or larger.
# The direction must to be from 1-8.''')
#                 print(f'Enter your move: {npcmovex} {npcmovey}')
           
    app_surf_update(destdict, p1dict, p2dict)
    refresh_window()
    