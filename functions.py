import pygame
import sys

def hypotenuse(x, y):
    x = x ** 2  
    y = y ** 2
    e = x + y
    return e



def mid(px, destinationx, py, destinationy):
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

def app_surf_update(destination, player_one, player_two):
    app_surf.fill('white') # fill the display surface with white background colour

    # draw the x-axis and the y-axis
    # pygame.draw.line() needs the display surfaceto draw on, colour of the line, starting coordinates and ending coordinates
    pygame.draw.line(app_surf, 'grey',(0,app_surf_rect.height/2),(app_surf_rect.width,app_surf_rect.height/2),width=1)
    pygame.draw.line(app_surf, 'grey',(app_surf_rect.width/2, 0),(app_surf_rect.width/2,app_surf_rect.height),width=1)
    
    # draw destination
    # pygame.draw.circle() needs the surface to draw on, colour, coordinates, circle radius and line width
    pygame.draw.circle(app_surf, 'black',destination['pygame_coords'], radius = 3, width = 3)

    # draw player one and player two
    pygame.draw.circle(app_surf, player_one['colour'], player_one['pygame_coords'], radius = 3, width = 2)
    pygame.draw.circle(app_surf, player_two['colour'], player_two['pygame_coords'], radius = 3, width = 2)

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
    # initially set the requested coordinates to random values
    # each time you call randint() you get new random coords
    p1_rand_x, p1_rand_y = random.randint(-400,400), random.randint(-400,400)
    player_one['cartesian_coords'] = (p1_rand_x, p1_rand_y)     # store the random cartesian coordinates
    player_one['pygame_coords'] = conv_cartesian_to_pygame_coords(p1_rand_x, p1_rand_y) # convert and store pygame coordinates

    p2_rand_x, p2_rand_y = random.randint(-400,400), random.randint(-400,400)
    player_two['cartesian_coords'] = (p2_rand_x, p2_rand_y)
    player_two['pygame_coords'] = conv_cartesian_to_pygame_coords(p2_rand_x, p2_rand_y)

    dest_rand_x, dest_rand_y = random.randint(-400,400), random.randint(-400,400)
    destination['cartesian_coords'] = (dest_rand_x, dest_rand_y)
    destination['pygame_coords'] = conv_cartesian_to_pygame_coords(dest_rand_x, dest_rand_y)
    # no need to return entities. They are dictionaries so the function can modify them directly (see the Python Functions tutorial on Connect Notices)