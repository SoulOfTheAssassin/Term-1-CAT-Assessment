import random
import pygame
import time
import sys
from termcolor import colored
from triplesdictionary import triples
from playsound import playsound

pygame.init()
app_clock = pygame.time.Clock()
pygame.mixer.init()



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

def npc_move(distance:float, gradient:float, npc_x, destination_x) -> str: # calculates the move for the npc and returns str in the format distance<space>direction.
# actual movement (direction)
    try:
        if gradient >= 0:
            if gradient >= 1:
                direction = "2" if npc_x < destination_x else "6"
            else:
                direction = "1" if npc_x < destination_x else "5"
        else:
            if gradient <= -1:
                direction = "7" if npc_x < destination_x else "3"
            else:
                direction = "8" if npc_x < destination_x else "4"
    except:
        direction = "3"
    distance = round(distance)
    if distance > size * 2:
        distance = size * 2
    return str(distance) + " " + direction

def pos_to_neg(x):
    return 0-x

def slowprint(str, speed):
    for char in str:
        print(char, end='')
        sys.stdout.flush()
        time.sleep(speed)
    time.sleep(1)
    print()
    
def slowinput(str, speed):
    for char in str:
        print(char, end='')
        sys.stdout.flush()
        time.sleep(speed)
    c = input()
    return c

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
    slowprint(colored(f'{name}', colour) + ' Information', 0.03)
    slowprint(colored(f'{name}', colour) + f' Coordinates: {x}, {y}', 0.03)

def create_app_window(width, height):
    slowprint(f'\nWelcome. The plane goes from -{width/2} to {width/2} in both the x and y directions', 0.03)
    pygame.display.set_caption("Gam ov Gradiante")           
    app_dimensions = (width + 10, height + 10)
    app_surf = pygame.display.set_mode(app_dimensions)
    app_surf_rect = app_surf.get_rect()
    print()
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
    slowprint('Please enter move in format: distance <space> direction.', 0.03) 
    slowprint('The distance and direction must be natural numbers.', 0.03) 
    slowprint("The distance must be 5 or larger.", 0.03)  
    slowprint("The direction must to be from 1-8.", 0.03) 
    while True: 
        move = slowinput("Enter your move: ", 0.03)
        move = move.strip()
        try: 
            move=move.split(" ") # To get the distance and direction
        except:
            slowprint("Please enter in format: distance <space> direction. ", 0.03)
            continue
        try:
            distance=int(move[0])
            direction=int(move[1])
        except:
            slowprint("The distance and direction need to be natural numbers.", 0.03)
            continue
        if direction > 8 or direction < 1:
            slowprint("The direction has to be 1-8.", 0.03)
        elif distance < 0:
            slowprint("The distance cannot be negative.", 0.03)
        elif distance < 5:
            slowprint("The distance must be 5 or larger. ", 0.03)
        else:
            slowprint("Move was successful.", 0.03)
            return distance, direction


functionloop = True
colours = ['grey', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
music = 'off'
songs = [1, 2, 3, 4, 5, 6,  'off']
p1colour = 'red'
p2colour = 'blue'
npccolour = 'green'
npctoggle = False
size = 800
sizes = [1,2,3,4,5,6,7,8,9,10]
playersize = 5.0
functionlist = ['planesize', 'togglenpc', 'playersize', 'playercolour', 'help', 'printsettings', 'start', 'quit', 'music']
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
Music: select a music track.
PrintSettings: prints all current settings.
Help: prints the rules.
Start: starts the game.''', 0.01)
while functionloop:
    function = slowinput('Enter function: ', 0.03)
    function = function.lower()
    while function not in functionlist:
        slowprint('This is not a valid function. Please try again. ', 0.03)
        function = slowinput('Enter function: ', 0.03)
        function = function.lower()
    if function == 'planesize':
        while True:
            try:
                size = int(slowinput('Enter Y of Cartesian Plane: ', 0.03))
            except:
                slowprint('This is not a valid input. Please input using a natural number. ', 0.03)
            else: 
                break
    elif function == 'playercolour':
        while True:
            try:
                playernum = int(slowinput('Please choose which player: ', 0.03))
            except:
                slowprint('Please use a single number.', 0.03)
            else:
                break
        slowprint(f'Here is a printout of the colour list: ' + colored('grey', 'grey')+ ', ' + colored('red', 'red') + ', ' + colored('green', 'green') + ', ' + colored('yellow', 'yellow') + ', ' + colored('blue', 'blue') + ', ' + colored('magenta', 'magenta') + ', ' + colored('cyan', 'cyan') + ', ' + colored('white', 'white') + '.', 0.03)
        print()
        if playernum == 1:
            p1colour = slowinput('Please choose a colour: ', 0.03).lower()
            while p1colour not in colours:
                slowprint('Please select a colour from the list above.', 0.03)
                p1colour = slowinput('Please choose a colour: ', 0.03).lower()
        elif playernum == 2:
            p2colour = slowinput('Please choose a colour: ', 0.03).lower()
            while p2colour not in colours:
                slowprint('Please select a colour from the list above.', 0.03)
                p2colour = slowinput('Please choose a colour: ', 0.03).lower()
        elif playernum == 3:
            npccolour = slowinput('Please choose a colour: ', 0.03).lower()
            while npccolour not in colours:
                slowprint('Please select a colour from the list above.', 0.03)
                npccolour = slowinput('Please choose a colour: ', 0.03).lower()
    elif function == 'start':
        if music == 'off':
            continue
        elif music == 1:
            pygame.mixer.music.load('Song1.wav')
        elif music == 2:
            pygame.mixer.music.load('Song2.wav')
        elif music == 3:
            pygame.mixer.music.load('Song3.wav')
        elif music == 4:
            pygame.mixer.music.load('Song4.wav')
        elif music == 5:
            pygame.mixer.music.load('The Pi Song  (Memorize 100 Digits Of π) _ SCIENCE SONGS.wav')
        elif music == 6:
            pygame.mixer.music.load('Spanish or Vanish (full song) from Duolingo On Ice.wav')
        if music == int(music):
            pygame.mixer.music.play()
        functionloop = False
    elif function == 'togglenpc':
        if npctoggle == True:
            npctoggle = False
        elif npctoggle == False:
            npctoggle = True
        slowprint(f'NPC Toggled: {npctoggle}', 0.03)
    elif function == 'help':
        slowprint('''
Two players are required to play this game. 
To win, you must land on the destination or another player.
You can only use primitive pythagorean triples.
''', 0.03)
    elif function == 'playersize':
        playersize = slowinput('Please choose a size from 1-10: ', 0.03)
        while playersize not in sizes:
            playersize = slowinput('Please choose a number from 1-10: ', 0.03)
        playersize = int(playersize)
    elif function == 'printsettings':
        print()
        slowprint(colored('NPC', str(npccolour)) + f' Toggled: {npctoggle}', 0.03)
        slowprint(colored('Player ONE', str(p1colour)) + f' colour: {p1colour}', 0.03)
        slowprint(colored('Player TWO', str(p2colour)) + f' colour: {p2colour}', 0.03)
        slowprint(colored('NPC', str(npccolour)) + f' colour: {npccolour}', 0.03)
        slowprint(f'Plane Size: {size} by {size}', 0.03)
        slowprint(f'Player Size: {playersize}', 0.03)
        slowprint(f'Music Track: {music}', 0.03)
        print()
    elif function == 'music':
        slowprint('Here is the list of songs: ' + remove(songs), 0.03)
        music = int(slowinput('Select a music track: ', 0.03))
        while music not in songs:
            music = int(slowinput('Select a music track: ', 0.03))


p1dict = {
    'Name': 'Player ONE',
    'X': random.randint(1,size),
    'Y': random.randint(1,size),
    'Pygame Coords': None,
    'Colour': p1colour,
    'Num': 1,
}

p2dict = {
    'Name': 'Player TWO',
    'X': random.randint(1,size),
    'Y': random.randint(1, size),
    'Pygame Coords': None,
    'Colour': p2colour,
    'Num': 2,
}

destdict = {
    'Name': 'Destination',
    'X': random.randint(1, size),
    'Y': random.randint(1, size),
    'Pygame Coords': None,
    'Colour': 'black',
    'Num': None,
}

npcdict = {
    'Name': 'Destination',
    'X': random.randint(1, size),
    'Y': random.randint(1, size),
    'Pygame Coords': None,
    'Colour': npccolour,
    'Num': 3,
    'Toggle': npctoggle,
}

app_surf, app_surf_rect = create_app_window(size, size)

initialise_entities()

directions = [1,2,3,4,5,6,7,8]
 # math
p1_to_destination = distance(p1dict['X'], p1dict['Y'], destdict['X'], destdict['Y'])
p2_to_destination = distance(p2dict['X'], p2dict['Y'], destdict['X'], destdict['Y'])
players_distance = distance(p1dict['X'], p1dict['Y'], p2dict['X'], p2dict['Y'])
npc_to_destination = distance(destdict['X'], destdict['Y'], npcdict['X'], npcdict['Y'])
npc_to_p1 = distance(p1dict['X'], p1dict['Y'], npcdict['X'], npcdict['Y'])
npc_to_p2 = distance(p2dict['X'], p2dict['Y'], npcdict['X'], npcdict['Y'])

grad_p1_destination = gradient(p1dict['X'], p1dict['Y'], destdict['X'], destdict['Y'])
grad_p2_destination = gradient(p2dict['X'], p2dict['Y'], destdict['X'], destdict['Y'])
grad_players = gradient(p1dict['X'], p1dict['Y'], p2dict['X'], p2dict['Y'])
npc_grad_destination = gradient(destdict['X'], destdict['Y'], npcdict['X'], npcdict['Y'])
npc_grad_p1 = gradient(p1dict['X'], p1dict['Y'], npcdict['X'], npcdict['Y'])
npc_grad_p2 = gradient(p2dict['X'], p2dict['Y'], npcdict['X'], npcdict['Y'])

mid_p1_destination = midpoint(p1dict['X'], p1dict['Y'], destdict['X'], destdict['Y'])
mid_p2_destination = midpoint(p2dict['X'], p2dict['Y'], destdict['X'], destdict['Y'])
players_mid = midpoint(p1dict['X'], p1dict['Y'], p2dict['X'], p2dict['Y'])
npc_destination_mid = midpoint(destdict['X'], destdict['Y'], npcdict['X'], npcdict['Y'])
npc_p1_mid = midpoint(p1dict['X'], p1dict['Y'], npcdict['X'], npcdict['Y'])
npc_p2_mid = midpoint(p2dict['X'], p2dict['Y'], npcdict['X'], npcdict['Y'])

mid_p2_destination = remove(mid_p2_destination)
mid_p1_destination = remove(mid_p1_destination)
players_mid = remove(players_mid)
npc_destination_mid = remove(npc_destination_mid)
npc_p1_mid = remove(npc_p1_mid)
npc_p2_mid = remove(npc_p2_mid)


app_surf_update(destdict, p1dict, p2dict)
p = ['y', 'n']
pr = slowinput('Would you like to print stats?(y/n) ', 0.03).lower()
while pr not in p:
    slowprint('Please enter y or n.', 0.03)
    pr = slowinput('Would you like to print stats?(y/n) ', 0.03).lower()
if pr == 'y':
    #player 1 stats
    printstats(p1dict['Name'], p1dict['X'], p1dict['Y'], 'red')

    # print(f'Distance to Destination: {p1_to_destination}')
    # print(f'Midpoint Coords with Destination: {mid_p1_destination}')
    # print(f'Gradient with Destination: {grad_p1_destination}')
    # print(f'Distance to Player 2: {players_distance}')
    # print(f'Midpoint Coords with Player 2: {players_mid}')
    # print(f'Gradient with Player 2: {grad_players}')

    slowprint(f'''Distance to Destination: {p1_to_destination}
    Midpoint Coords with Destination: {mid_p1_destination}
    Gradient with Destination: {grad_p1_destination}
    Distance to Player TWO: {players_distance}
    Midpoint Coords with Player TWO: {players_mid}
    Gradient with Player TWO: {grad_players}
    ''', 0.03)

    #player 2 stats
    printstats(p2dict['Name'], p2dict['X'], p2dict['Y'], p2dict['Colour'])
    slowprint(f'''Distance to Destination: {p2_to_destination}
    Midpoint Coords with Destination: {mid_p2_destination}
    Gradient with Destination: {grad_p2_destination}
    Distance to Player ONE: {players_distance}
    Midpoint Coords with Player ONE: {players_mid}
    Gradient with Player ONE: {grad_players}
    ''', 0.03)

    if npctoggle:
        printstats(npcdict['Name'], npcdict['X'], npcdict['Y'], npcdict['Colour'])
        slowprint(f'''Distance to Destination: {npc_to_destination}
    Midpoint Coords with Destination: {npc_destination_mid}
    Gradient with Destination: {npc_grad_destination}
    Distance to Player ONE: {npc_to_p1}
    Midpoint Coords with Player ONE: {npc_p1_mid}
    Gradient with Player ONE: {npc_grad_p1}
    Distance to Player TWO: {npc_to_p2}
    Midpoint Coords with Player TWO: {npc_p2_mid}
    Gradient with Player TWO: {npc_grad_p2}
    ''', 0.03)


    # print(f'Distance to Destination: {p2_to_destination}')
    # print(f'Distance to Player 2: {players_distance}')
    # print(f'Gradient with Destination: {grad_p2_destination}')
    # print(f'Gradient with Player ONE: {grad_players}')
    # print(f'Midpoint Coords with Player ONE: {mid_p2_destination}')
    # print(f'Midpoint Coords with Player ONE: {players_mid}')
    # print('\n')


    #destination stats
    printstats(destdict['Name'], destdict['X'], destdict['Y'], 'grey')
    slowprint(f'Distance to Player ONE: {p1_to_destination}', 0.03)
    slowprint(f'Distance to Player TWO: {p2_to_destination}', 0.03)
    slowprint(f'Gradient with Player ONE: {grad_p1_destination}', 0.03)
    slowprint(f'Gradient with Player TWO: {grad_p2_destination}', 0.03)
    slowprint(f'Midpoint Coords with Player ONE: {mid_p1_destination}', 0.03)
    slowprint(f'Midpoint Coords with Player TWO: {mid_p2_destination}', 0.03)
    ('\n')
    
    
playerturns = 1
win = False
direction = ''
refresh_window()
slowprint('You must click every time for each move.', 0.03)
while win != True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           pygame.quit()
           sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if playerturns == 1:
                print()
                slowprint(colored('Player ONE:', p1dict['Colour']), 0.03)
                dist, direction = inputcheck()
                moveplayer(dist, direction, p1dict)
                p1dict['Pygame Coords'] = conv_cartesian_to_pygame_coords(p1dict['X'], p1dict['Y'])
                win = checkwin(p1dict, p2dict, destdict, p1dict['Num'])
                if win == "Player ONE":
                    slowprint('The winner is: ' + colored(p1dict['Name'], p1dict['Colour']), 0.03)
                playerturns = 2
            elif playerturns == 2:
                print()
                slowprint(colored('Player TWO:', p2dict['Colour']), 0.03)
                dist, direction = inputcheck()
                moveplayer(dist, direction, p2dict)
                p2dict['Pygame Coords'] = conv_cartesian_to_pygame_coords(p2dict['X'], p2dict['Y'])
                win = checkwin(p1dict, p2dict, destdict, p2dict['Num'])
                if win == "Player TWO":
                    slowprint('The winner is: ' + colored(p2dict['Name'], p2dict['Colour']), 0.03)
                playerturns = 1
            if npctoggle:
                slowprint(colored('NPC:', npcdict['Colour']), 0.03)
                slowprint('''Please enter move in format: distance <space> direction.
The distance and direction must be natural numbers.
The distance must be 5 or larger.
The direction must to be from 1-8.''', 0.03)
                npcdistance, npcdirection = npc_move(npc_to_destination, npc_grad_destination, npcdict['X'], destdict['X'])
                for char in f'Enter your move: ':
                    print(char, end='')
                    sys.stdout.flush()
                    time.sleep(0.03)
                time.sleep(1)
                slowprint(npcdistance + npcdirection, 0.03)
                # win = checkwin()
                
                
           
    app_surf_update(destdict, p1dict, p2dict)
    refresh_window()
    