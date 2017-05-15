import pygame, sys
from pygame.locals import *

WIDTH = 640
HEIGHT = 480

screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption("PongAI")
clock = pygame.time.Clock()

ball = {
	"x": WIDTH/2,
	"y": HEIGHT/2,
	"xvel": 10,
	"yvel": 10,
	"r": 10
}

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
	screen.fill((0, 0, 0)) # clear the screen with black
	pygame.draw.rect(screen, (0xFF, 0xFF, 0xFF), (ball["x"]-ball["r"], ball["y"]-ball["r"], ball["r"]*2, ball["r"]*2), 0)
	ball["x"] += ball["xvel"]
	ball["y"] += ball["yvel"]
	if (ball["xvel"] > 0 and ball["x"] + ball["r"] > WIDTH) or (ball["xvel"] < 0 and ball["x"] - ball["r"] < 0):
		ball["xvel"] *= -1
	if (ball["yvel"] > 0 and ball["y"] + ball["r"] > HEIGHT) or (ball["yvel"] < 0 and ball["y"] - ball["r"] < 0):
		ball["yvel"] *= -1
	pygame.display.update()
	clock.tick(60)
