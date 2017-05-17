import pygame
from pygame.locals import *

WIDTH = 640
HEIGHT = 480
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption("PongAI")
white = (255, 255, 255)
black = (0, 0, 0)

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
