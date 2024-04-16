import random
import pygame
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
    print('Please enter move in format: distance <space> direction.') 
    print('The distance and direction must be natural numbers.') 
    print("The distance must be 5 or larger.")  
    print("The direction must to be from 1-8.") 
    while True: 
        move = input("Enter your move: ").strip() 
        try: 
            move=move.split(" ") # To get the distance and direction
        except:
            print("Please enter in format: distance <space> direction. ")
            continue
        try:
            distance=int(move[0])
            direction=int(move[1])
        except:
            print("The distance and direction need to be natural numbers.")
            continue
        if direction > 8 or direction < 1:
            print("The direction has to be 1-8.")
        elif distance < 0:
            print("The distance cannot be negative.")
        elif distance < 5:
            print("The distance must be 5 or larger. ")
        else:
            print("Move was successful.")
            return distance, direction


colours = ['grey', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
p1colour = 'red'
p2colour = 'blue'
npccolour = 'green'
npctoggle = False
functionloop = True
sizex = 400
sizey = 400
functionlist = ['planesize', 'togglenpc', 'playersize', 'playercolour', 'help', 'printsettings', 'start']
print('Here are a list of functions: ')
print('PlaneSize: adjust the size of the plane.')
print('ToggleNPC: Toggle the NPC.')
print('PlayerSize: adjust the size of the players.')
print('PlayerColour: change the player colours.')
print('PrintSettings: prints all current settings.')
print('Help: prints the rules.')
print('Start: starts the game.')
while functionloop:
    function = input('Enter function: ').lower()
    while function not in functionlist:
        print('This is not a valid function. Please try again. ')
        function = input('Enter function: ')
    if function == 'planesize':
        while True:
            try:
                sizex = int(input('Enter X of Cartesian Plane: '))
            except:
                print('This is not a valid input. Please input using a natural number. ')
            else: 
                break
        while True:
            try:
                sizey = int(input('Enter Y of Cartesian Plane: '))
            except:
                print('This is not a valid input. Please input using a natural number. ')
            else: 
                break
    elif function == 'playercolour':
        while True:
            try:
                playernum = int(input('Please choose which player: '))
            except:
                print('Use a single number.')
            else:
                break
        print(f'Here is a printout of the colour list: {colours}')
        if playernum == 1:
            p1colour = input('Please choose a colour: ').lower()
            while p1colour not in colours:
                print('Please select a colour from the list above.')
                p1colour = input('Please choose a colour: ').lower()
        elif playernum == 2:
            p2colour = input('Please choose a colour: ').lower()
            while p2colour not in colours:
                print('Please select a colour from the list above.')
                p2colour = input('Please choose a colour: ').lower()
        elif playernum == 3:
            npccolour = input('Please choose a colour: ').lower()
            while npccolour not in colours:
                print('Please select a colour from the list above.')
                npccolour = input('Please choose a colour: ').lower()
    elif function == 'start':
        functionloop = False
    elif function == 'togglenpc':
        if npctoggle == True:
            npctoggle = False
        elif npctoggle == False:
            npctoggle = True
    elif function == 'help':
        print('''
To win, you must land on the destination or another player.
You can only use primitive pythagorean triples.
''')
    elif function == 'printsettings':
        print()
        print(f'NPC Toggled: {npctoggle}')
        print(colored('Player ONE', p1colour) + f' colour: {p1colour}')
        print(colored('Player TWO', p2colour) + f' colour: {p2colour}')
        print(colored('NPC', npccolour) + f' colour: {npccolour}')
        print()


p1dict = {
    'Name': 'Player ONE',
    'X': random.randint(pos_to_neg(sizex),sizex),
    'Y': random.randint(pos_to_neg(sizey),sizey),
    'Pygame Coords': None,
    'Colour': p1colour,
    'Num': 1,
}

p2dict = {
    'Name': 'Player TWO',
    'X': random.randint(pos_to_neg(sizex),sizex),
    'Y': random.randint(pos_to_neg(sizey), sizey),
    'Pygame Coords': None,
    'Colour': p2colour,
    'Num': 2,
}

destdict = {
    'Name': 'Destination',
    'X': random.randint(pos_to_neg(sizex), sizex),
    'Y': random.randint(pos_to_neg(sizey), sizey),
    'Pygame Coords': None,
    'Colour': 'black',
    'Num': None,
}

npcdict = {
    'Name': 'Destination',
    'X': random.randint(pos_to_neg(sizex), sizex),
    'Y': random.randint(pos_to_neg(sizey), sizey),
    'Pygame Coords': None,
    'Colour': npccolour,
    'Num': 3,
    'Toggle': npctoggle,
}

app_surf, app_surf_rect = create_app_window(sizex*2, sizey*2)

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
playerturns = 1
win = False
direction = ''
refresh_window()
while win != True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           pygame.quit()
           sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if playerturns == 1:
                print(colored('Player ONE:', p1dict['Colour']))
                dist, direction = inputcheck()
                moveplayer(dist, direction, p1dict)
                p1dict['Pygame Coords'] = conv_cartesian_to_pygame_coords(p1dict['X'], p1dict['Y'])
                win = checkwin(p1dict, p2dict, destdict, p1dict['Num'])
                if win == "Player ONE":
                    print('The winner is: ' + colored(p1dict['Name'], p1dict['Colour']))
                playerturns = 2
            elif playerturns == 2:
                print(colored('Player TWO:', p2dict['Colour']))
                dist, direction = inputcheck()
                moveplayer(dist, direction, p2dict)
                p2dict['Pygame Coords'] = conv_cartesian_to_pygame_coords(p2dict['X'], p2dict['Y'])
                win = checkwin(p1dict, p2dict, destdict, p2dict['Num'])
                if win == "Player TWO":
                    print('The winner is: ' + colored(p2dict['Name'], p2dict['Colour']))
                playerturns = 1
           
    app_surf_update(destdict, p1dict, p2dict)
    refresh_window()
    