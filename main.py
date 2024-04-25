import random
import pygame
import time
import sys
from termcolor import colored
from triplesdictionary import triples


pygame.init()
app_clock = pygame.time.Clock()
pygame.mixer.init()



def remove(list): #function for printing lists
    var = str(list)
    var = var.replace('[', '')
    var = var.replace(']', '')
    return var

def hypotenuse(x:int, y:int): #function for finding length of hypotenuse
    x = x ** 2  
    y = y ** 2
    e = x + y
    e = e ** 0.5
    return int(e)

def distance(px:int, py:int, dx:int, dy:int): #function for finding distance between 2 points
    xdistance = dx - px                                               
    ydistance = dy - py                                                 
    p1_distance = hypotenuse(xdistance, ydistance) #uses hypotenuse funcion                 
    distance = round(p1_distance, 1)
    return distance

def npc_move(distance:float, gradient:float, npc_x:int, destination_x:int) -> str: # function for finding the npc move
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

def slowprint(str:str, speed:float): #function for type printing
    for char in str:
        print(char, end='')
        sys.stdout.flush()
        time.sleep(speed)
    time.sleep(1)
    print()
    
def slowinput(str:str, speed:float): #function for type inputing
    for char in str:
        print(char, end='')
        sys.stdout.flush()
        time.sleep(speed)
    i = input()
    return i

def midpoint(x1:int, y1:int, x2:int, y2:int): #function to find midpoint
    x = (x1 + x2)/2                            
    y = (y1 + y2)/2  
    return [x, y]

def gradient(x1:int, y1:int, x2:int, y2:int): #function to find gradient
    try:
        var = (y2 - y1)/(x2 - x1)
    except ZeroDivisionError:
        return "Undefined"
    var = round(var, 1)
    return var

def printstats(dict:dict): #code to print stats
    slowprint(colored(f'{dict['Name']}', dict['Colour']) + ' Information', 0.03)
    slowprint(colored(f'{dict['Name']}', dict['Colour']) + f' Coordinates: {dict['X']}, {dict['Y']}', 0.03)

def create_app_window(width:int, height:int): #mr kigodi function
    slowprint(f'\nWelcome. The plane goes from -{width} to {width} in both the x and y directions.', 0.03)
    pygame.display.set_caption("Gam ov Gradiante")           
    app_dimensions = (width + 10, height + 10)
    app_surf = pygame.display.set_mode(app_dimensions)
    app_surf_rect = app_surf.get_rect()
    print()
    return app_surf, app_surf_rect

def app_surf_update(destdict:dict, p1dict:dict, p2dict:dict, npcdict:dict, npctoggle:bool):#mr kigodi function
    app_surf.fill('white')
    pygame.draw.line(app_surf, 'grey',(0,app_surf_rect.height/2),(app_surf_rect.width,app_surf_rect.height/2),width=1)
    pygame.draw.line(app_surf, 'grey',(app_surf_rect.width/2, 0),(app_surf_rect.width/2,app_surf_rect.height),width=1)
    pygame.draw.circle(app_surf, 'black',destdict['Pygame Coords'], radius = 3, width = 3)
    pygame.draw.circle(app_surf, 'black',destdict['Pygame Coords'], radius = float(buffersize), width = 1)
    pygame.draw.circle(app_surf, p1dict['Colour'], p1dict['Pygame Coords'], radius = 3, width = 2)
    pygame.draw.circle(app_surf, p2dict['Colour'], p2dict['Pygame Coords'], radius = 3, width = 2)
    pygame.draw.circle(app_surf, p1dict['Colour'], p1dict['Pygame Coords'], radius = float(buffersize), width = 1)
    pygame.draw.circle(app_surf, p2dict['Colour'], p2dict['Pygame Coords'], radius = float(buffersize), width = 1)
    if npctoggle:
        pygame.draw.circle(app_surf, npcdict['Colour'], npcdict['Pygame Coords'], radius = 3, width = 1)
        pygame.draw.circle(app_surf, npcdict['Colour'], npcdict['Pygame Coords'], radius = float(buffersize), width = 1)
    

def refresh_window():#mr kigodi function
    pygame.display.update()
    app_clock.tick(24)

def conv_cartesian_to_pygame_coords(x:int,y:int):#mr kigodi function
    pygame_x = x + app_surf_rect.width / 2
    pygame_y = -y + app_surf_rect.height /2
    return(pygame_x, pygame_y)

def initialise_entities():#mr kigodi function
    p1dict['Pygame Coords'] = conv_cartesian_to_pygame_coords(p1dict['X'], p1dict['Y'])
    p2dict['Pygame Coords'] = conv_cartesian_to_pygame_coords(p2dict['X'], p2dict['Y'])
    destdict['Pygame Coords'] = conv_cartesian_to_pygame_coords(destdict['X'], destdict['Y'])
    npcdict['Pygame Coords'] = conv_cartesian_to_pygame_coords(npcdict['X'], npcdict['Y'])

def moveplayer(distance:int, direction:int, dictionary:dict): #function to move players
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
    if direction == 1: #edits dictionary
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

def checkwin(dictionary1:dict, dictionary2:dict, dictionary3:dict, npc:dict, buffer:float, lastmove:int): #function to check win
    if distance(dictionary1['X'], dictionary1['Y'], dictionary2['X'], dictionary2['Y']) <= buffer:
        win = True
    elif distance(dictionary1['X'], dictionary1['Y'], dictionary3['X'], dictionary3['Y']) <= buffer:
        win = True
    elif distance(dictionary1['X'], dictionary1['Y'], npc['X'], npc['Y']) <= buffer:
        win = True
    elif distance(dictionary3['X'], dictionary3['Y'], dictionary2['X'], dictionary2['Y']) <= buffer:
        win = True
    elif distance(dictionary3['X'], dictionary3['Y'], npc['X'], npc['Y']) <= buffer:
        win = True
    else: 
        return False
    if win: 
        if lastmove == 1:
            slowprint('Congratulations! Player ONE wins!', 0.05)
        elif lastmove == 2:
            slowprint('Congratulations! Player TWO wins!', 0.05)
        elif lastmove == 3:
            slowprint('Unlucky... The NPC beat you...', 0.05)
        return True

def inputcheck(): #function to input move
    slowprint('Please enter move in format: distance <space> direction.', 0.03) 
    while True: 
        move = slowinput("Enter your move: ", 0.03)
        move = move.strip()
        try: 
            move=move.split(" ") 
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

playagain = 'y'

while playagain == 'y': #play again loop
    functionloop = True
    colours = ['grey', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white', 'quit']
    music = 'off'
    songs = ['1', '2', '3', '4', '5', '6', 'off', 'quit']
    p1colour = 'red'
    p2colour = 'blue'
    npccolour = 'green'
    npctoggle = False
    size = 800
    buffersize = 5.0
    functionlist = ['planesize', 'togglenpc', 'buffersize', 'playercolour', 'help', 'printsettings', 'start', 'quit', 'music']
    playerlist = ['1', '2', '3']
    playernum = ''
    slowprint('''Here are a list of functions: 
PlaneSize: adjust the size of the plane.
ToggleNPC: Toggle the NPC.
BufferSize: adjust the size of the player buffer.
PlayerColour: change the player colours.
Music: select a music track.
PrintSettings: prints all current settings.
Help: prints the rules.
Start: starts the game.
Quit: quits the program.''', 0.01)
    while functionloop:
        function = slowinput('Enter function: ', 0.03)
        function = function.lower()
        while function not in functionlist:
            slowprint('This is not a valid function. Please try again. ', 0.03)
            function = slowinput('Enter function: ', 0.03)
            function = function.lower()
            if function in functionlist:
                break
        if function == 'planesize': #changes plane size
            while True:
                try:
                    size = int(slowinput('Enter size of Cartesian Plane: ', 0.03))
                except:
                    slowprint('This is not a valid input. Please input using a natural number. ', 0.03)
                else: 
                    break
        elif function == 'playercolour':#changes colour of a player
            playernum = slowinput('Please choose a player: ', 0.04)     
            while playernum not in playerlist:
                playernum = slowinput('Please choose a player: ', 0.04)                
            slowprint(f'Here is a printout of the colour list: ' + colored('grey', 'grey')+ ', ' + colored('red', 'red') + ', ' + colored('green', 'green') + ', ' + colored('yellow', 'yellow') + ', ' + colored('blue', 'blue') + ', ' + colored('magenta', 'magenta') + ', ' + colored('cyan', 'cyan') + ', ' + colored('white', 'white') + '.', 0.03)
            print()
            if playernum == '1':
                p1colour = slowinput('Please choose a colour: ', 0.03).lower()
                while p1colour not in colours:
                    slowprint('Please select a colour from the list above.', 0.03)
                    p1colour = slowinput('Please choose a colour: ', 0.03).lower()
            elif playernum == '2':
                p2colour = slowinput('Please choose a colour: ', 0.03).lower()
                while p2colour not in colours:
                    slowprint('Please select a colour from the list above.', 0.03)
                    p2colour = slowinput('Please choose a colour: ', 0.03).lower()
            elif playernum == '3':
                npccolour = slowinput('Please choose a colour: ', 0.03).lower()
                while npccolour not in colours:
                    slowprint('Please select a colour from the list above.', 0.03)
                    npccolour = slowinput('Please choose a colour: ', 0.03).lower()
        elif function == 'start':#starts game
            if music.isnumeric():
                if music == '1':
                    pygame.mixer.music.load('Song1.wav')
                elif music == '2':
                    pygame.mixer.music.load('Song2.wav')
                elif music == '3':
                    pygame.mixer.music.load('Song3.wav')
                    slowprint('Song by ASAPScience', 0.04)
                elif music == '4':
                    pygame.mixer.music.load('Song4.wav')
                    slowprint('Song by Sheet Music Boss', 0.04)
                elif music == '5':
                    pygame.mixer.music.load('Song5.wav')
                    slowprint('Song by ASAPScience', 0.04)
                elif music == '6':
                    pygame.mixer.music.load('Song6.wav')
                    slowprint('Song by Sean', 0.04)
                pygame.mixer.music.play()
            else:
                pygame.mixer.music.unload()
            functionloop = False
            break
        elif function == 'togglenpc':#toggles npc
            if npctoggle == True:
                npctoggle = False
            elif npctoggle == False:
                npctoggle = True
            slowprint(f'NPC Toggled: {npctoggle}', 0.03)
        elif function == 'help':#prints rules
            slowprint('''
Two players are required to play this game. 
To win, you must land on the destination or another player.
You can only use primitive pythagorean triples.
Your move must be in format: distance <space> direction.
Direction must be 1-8.
Distance cannot be less than 5.
''', 0.03)
        elif function == 'buffersize': #changes size of buffer
            playersize = slowinput('Please choose a size from 1-10: ', 0.03)
            while playersize not in sizes:
                playersize = slowinput('Please choose a number from 1-10: ', 0.03)
            if playersize == 'quit':
                sys.exit()
            else:
                playersize = int(playersize)
        elif function == 'printsettings': #prints all settings
            print()
            slowprint(colored('NPC', str(npccolour)) + f' Toggled: {npctoggle}', 0.03)#type: ignore
            slowprint(colored('Player ONE', str(p1colour)) + f' colour: {p1colour}', 0.03) # type: ignore
            slowprint(colored('Player TWO', str(p2colour)) + f' colour: {p2colour}', 0.03) # type: ignore
            slowprint(colored('NPC', str(npccolour)) + f' colour: {npccolour}', 0.03) # type: ignore
            slowprint(f'Plane Size: {size} by {size}', 0.03)
            slowprint(f'Buffer Size: {playersize}', 0.03)
            slowprint(f'Music Track: {music}', 0.03)
            print()
        elif function == 'music': #selects music
            slowprint('Here are the list of options: ' + remove(songs) + '.', 0.03)
            music = slowinput('Select a music track: ', 0.03)
            while music not in songs:
                music = slowinput('Select a music track: ', 0.03)
            if music == 'quit':
                exit()
        elif function == 'quit':
            exit()
        elif function == 'buffersize':
            try:
                buffer = int(input('Please enter a buffer size: '))
            except:
                print('Please enter a positive integer. ')

    sise = size/2
    sise = int(-sise)

#DICTIONARIES
    p1dict = {
        'Name': 'Player ONE',
        'X': random.randint(sise, int(size/2)),
        'Y': random.randint(sise, int(size/2)),
        'Pygame Coords': None,
        'Colour': p1colour,
        'Num': 1,
    }

    p2dict = {
        'Name': 'Player TWO',
        'X': random.randint(sise, int(size/2)),
        'Y': random.randint(sise, int(size/2)),
        'Pygame Coords': None,
        'Colour': p2colour,
        'Num': 2,
    }

    destdict = {
        'Name': 'Destination',
        'X': random.randint(sise, int(size/2)),
        'Y': random.randint(sise, int(size/2)),
        'Pygame Coords': None,
        'Colour': 'black',
        'Num': None,
    }

    npcdict = {
        'Name': 'NPC',
        'X': random.randint(sise, int(size/2)),
        'Y': random.randint(sise, int(size/2)),
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


    app_surf_update(destdict, p1dict, p2dict, npcdict, npctoggle)
    #OPTION TO PRINT STATS
    options = ['y', 'n']
    pr = slowinput('Would you like to print stats?(y/n) ', 0.03).lower()
    while pr not in options:
        slowprint('Please enter y or n.', 0.03)
        pr = slowinput('Would you like to print stats?(y/n) ', 0.03).lower()
    if pr == 'y':
        #player 1 stats
        printstats(p1dict)
        slowprint(f'''Distance to Destination: {p1_to_destination}
Midpoint Coords with Destination: {mid_p1_destination}
Gradient with Destination: {grad_p1_destination}
Distance to Player TWO: {players_distance}
Midpoint Coords with Player TWO: {players_mid}
Gradient with Player TWO: {grad_players}
''', 0.03)

        #player 2 stats
        printstats(p2dict)
        slowprint(f'''Distance to Destination: {p2_to_destination}
Midpoint Coords with Destination: {mid_p2_destination}
Gradient with Destination: {grad_p2_destination}
Distance to Player ONE: {players_distance}
Midpoint Coords with Player ONE: {players_mid}
Gradient with Player ONE: {grad_players}
''', 0.03)
#npc stats
        if npctoggle:
            printstats(npcdict)
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
        #destination stats
        printstats(destdict)
        slowprint(f'''Distance to Player ONE: {p1_to_destination}
Distance to Player TWO: {p2_to_destination}
Gradient with Player ONE: {grad_p1_destination}
Gradient with Player TWO: {grad_p2_destination}
Midpoint Coords with Player ONE: {mid_p1_destination}
Midpoint Coords with Player TWO: {mid_p2_destination}
''', 0.03)
        
        
    musicagain = 'y'    
        
#GAME LOOP
    playerturns = 1
    win = False
    refresh_window()
    slowprint('You must click every time for each move.', 0.03)
    while win != True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if playerturns == 1: #player 1 turn
                    print()
                    slowprint(colored('Player ONE:', p1dict['Colour']), 0.03)
                    dist, direction = inputcheck()
                    moveplayer(dist, direction, p1dict)
                    p1dict['Pygame Coords'] = conv_cartesian_to_pygame_coords(p1dict['X'], p1dict['Y'])
                    win = checkwin(p1dict, p2dict, destdict, npcdict, buffersize, p1dict['Num'])
                    playerturns = 2
                elif playerturns == 2:#PLAYER 2
                    print()
                    slowprint(colored('Player TWO:', p2dict['Colour']), 0.03)
                    dist, direction = inputcheck()
                    moveplayer(dist, direction, p2dict)
                    p2dict['Pygame Coords'] = conv_cartesian_to_pygame_coords(p2dict['X'], p2dict['Y'])
                    win = checkwin(p1dict, p2dict, destdict, npcdict, buffersize, p2dict['Num'])
                    if npctoggle:#checks whether npc is on, if yes then give npc a turn, else back to p1
                        playerturns = 3
                    else:
                        playerturns = 1
                elif playerturns == 3:#npc turn
                    print()
                    slowprint(colored('NPC:', npcdict['Colour']), 0.03)
                    slowprint('Please enter move in format: distance <space> direction.', 0.03)
                    npcmove = npc_move(npc_to_destination, float(npc_grad_destination), npcdict['X'], destdict['X'])
                    npcmove1 = npcmove.split(' ')
                    print(npcmove1)
                    npcdistance = int(npcmove1[0])
                    npcdirection = int(npcmove1[1])
                    moveplayer(npcdistance, npcdirection, npcdict)
                    for char in f'Enter your move: ':#makes it so it looks like npc is inputting
                        print(char, end='')
                        sys.stdout.flush()
                        time.sleep(0.03)
                    time.sleep(1)
                    slowprint(npcmove, 0.03)
                    slowprint('Move was successful.', 0.03)
                    win = checkwin(p1dict, p2dict, destdict, npcdict, buffersize, npcdict['Num'])
                    playerturns = 1
            if music != 'off': #checks whether music is on
                if musicagain == 'y'
                    if pygame.mixer.music.get_busy() == False:#checks whether music is playing
                        musicagain = slowinput('Would you like to play music again? (y/n) ', 0.04)
                        while musicagain not in options:
                            slowprint('Please select y or n.', 0.04)
                            musicagain = slowinput('Would you like to music play again? (y/n) ', 0.04)
                        if musicagain == 'y':
                            pygame.mixer.music.play()
                        else:
                            pygame.mixer.music.unload()

                    
            app_surf_update(destdict, p1dict, p2dict, npcdict, npctoggle)
            refresh_window()
        
    playagain = slowinput('Would you like to play again? (y/n) ', 0.05).lower()#checks whether player wants to play again
    while playagain not in options:
        slowprint('Please enter y or n.', 0.06) #if yes then they loop back to the beginning
        playagain = slowinput('Would you like to play again? (y/n) ', 0.05).lower()

pygame.quit()
sys.exit() #if not then the quit