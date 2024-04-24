import pygame

pygame.mixer.init()

pygame.mixer.music.load('Song1.wav')
pygame.mixer.music.play()
endmusic = pygame.mixer.music.set_endevent(10)

print(endmusic)