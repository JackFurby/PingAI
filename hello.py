import pygame, sys
from pygame.locals import *
import random

WIDTH = 640
HEIGHT = 480

screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption("PongAI")
clock = pygame.time.Clock()

balls = []

for _ in range(500):
	ball = {
		"x": random.randrange(0, WIDTH),
		"y": random.randrange(0, HEIGHT),
		"xvel": random.randrange(-10, 10),
		"yvel": random.randrange(-10, 10),
		"r": 10,
		"color": (random.randrange(0, 0xFF), random.randrange(0, 0xFF), random.randrange(0, 0xFF))
	}
	balls.append(ball)

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
	screen.fill((0, 0, 0)) # clear the screen with black
	
	for ball in balls:
		pygame.draw.rect(screen, ball["color"], (ball["x"]-ball["r"], ball["y"]-ball["r"], ball["r"]*2, ball["r"]*2), 0)
		ball["x"] += ball["xvel"]
		ball["y"] += ball["yvel"]
		if (ball["xvel"] > 0 and ball["x"] + ball["r"] > WIDTH) or (ball["xvel"] < 0 and ball["x"] - ball["r"] < 0):
			ball["xvel"] *= -1
		if (ball["yvel"] > 0 and ball["y"] + ball["r"] > HEIGHT) or (ball["yvel"] < 0 and ball["y"] - ball["r"] < 0):
			ball["yvel"] *= -1
	
	pygame.display.update()
	clock.tick(60)
