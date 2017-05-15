import pygame, sys
from pygame.locals import *
import random

WIDTH = 640
HEIGHT = 480

screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption("PongAI")
clock = pygame.time.Clock()
white = 255, 255, 255

balls = []

for _ in range(20):
	ball = {
		"x": random.randrange(0, WIDTH),
		"y": random.randrange(0, HEIGHT),
		"xvel": random.randrange(-10, 10),
		"yvel": random.randrange(-10, 10),
		"r": 10,
		"color": (random.randrange(0, 0xFF), random.randrange(0, 0xFF), random.randrange(0, 0xFF))
	}
	balls.append(ball)

bat = {
	"x": 30,
	"y": HEIGHT/2,
	"width": 10, # actually, half the width and height
	"height": 50,
	"color": white,
	"speed": 3
}

def update():
	keys = pygame.key.get_pressed()
	if keys[K_DOWN] and bat["y"] < HEIGHT - bat["height"]:
		bat["y"] += bat["speed"]
	if keys[K_UP] and bat["y"] > bat["height"]:
		bat["y"] -= bat["speed"]
	
	for ball in balls:
		ball["x"] += ball["xvel"]
		ball["y"] += ball["yvel"]
		
		# bat collision
		if (abs(ball["y"] - bat["y"]) < (bat["height"] + ball["r"])) and (abs(ball["x"] - bat["x"]) < (bat["width"] + ball["r"])):
			ball["xvel"] *= -1
		
		# wall collision
		if (ball["xvel"] > 0 and ball["x"] + ball["r"] > WIDTH) or (ball["xvel"] < 0 and ball["x"] - ball["r"] < 0):
			ball["xvel"] *= -1
		if (ball["yvel"] > 0 and ball["y"] + ball["r"] > HEIGHT) or (ball["yvel"] < 0 and ball["y"] - ball["r"] < 0):
			ball["yvel"] *= -1

def render():
	screen.fill((0, 0, 0)) # clear the screen with black
	pygame.draw.rect(screen, bat["color"], (bat["x"]-bat["width"], bat["y"]-bat["height"], bat["width"]*2, bat["height"]*2), 0)
	
	for ball in balls:
		pygame.draw.rect(screen, ball["color"], (ball["x"]-ball["r"], ball["y"]-ball["r"], ball["r"]*2, ball["r"]*2), 0)
	
	pygame.display.update()

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
	
	update()
	render()
	
	clock.tick(60)
