import pygame, sys
from pygame.locals import *
import random

WIDTH = 640
HEIGHT = 480
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption("PongAI")
clock = pygame.time.Clock()
white = 255, 255, 255
myfont = pygame.font.SysFont("monospace", 15)

balls = []

for _ in range(20):
	ball = {
		"x": random.randrange(0, WIDTH),
		"y": random.randrange(0, HEIGHT),
		"xvel": 10 * (random.randrange(0, 2)-0.5),
		"yvel": 10 * (random.randrange(0, 2)-0.5),
		"r": 10, #radius of ball
		"color": (random.randrange(0, 0xFF), random.randrange(0, 0xFF), random.randrange(0, 0xFF))
	}
	balls.append(ball)

bat_l = {
	"x": 5,
	"y": HEIGHT/2,
	"width": 5, # actually, half the width and height
	"height": 50,
	"color": white,
	"speed": 8
}

bat_r = bat_l.copy()
bat_r["x"] = WIDTH - bat_r["x"]


def update():
	keys = pygame.key.get_pressed()
	
	if keys[K_s] and bat_l["y"] < HEIGHT - bat_l["height"]:
		bat_l["y"] += bat_l["speed"]
	if keys[K_w] and bat_l["y"] > bat_l["height"]:
		bat_l["y"] -= bat_l["speed"]

	if keys[K_DOWN] and bat_r["y"] < HEIGHT - bat_r["height"]:
		bat_r["y"] += bat_r["speed"]
	if keys[K_UP] and bat_r["y"] > bat_r["height"]:
		bat_r["y"] -= bat_r["speed"]
	deleted  = []
	for ball in balls:

		# bat_l collision
		#if (abs(ball["y"] - bat_l["y"]) < (bat_l["height"] + ball["r"])) and (abs(ball["x"] - bat_l["x"]) < (bat_l["width"] + ball["r"])):
		#	ball["xvel"] *= -1

		# wall collision
		x2 = ball["x"] + ball["xvel"]
		y2 = ball["y"] + ball["yvel"]
		
		if x2 < 0:
			yint = -(ball["yvel"]/ball["xvel"]) * ball["x"] + ball["y"]
			if bat_l["y"] - bat_l["height"] < yint < bat_l["y"] + bat_l["height"]: # bounce
				x2 = -x2
				ball["xvel"] *= -1
			else: # don't bounce
				deleted.append(ball)
		elif x2 > WIDTH:
			yint = (ball["yvel"]/-ball["xvel"]) * (WIDTH - ball["x"]) + ball["y"]
			if bat_r["y"] - bat_r["height"] < yint < bat_r["y"] + bat_r["height"]: # bounce
				x2 = WIDTH - (x2-WIDTH)
				ball["xvel"] *= -1
			else: # don't bounce
				deleted.append(ball)
		if y2 < 0 or y2 > HEIGHT:
			ball["yvel"] *= -1
		
		ball["x"] = x2
		ball["y"] = y2

	for ball in deleted:
		balls.remove(ball)

def render():
	screen.fill((0, 0, 0)) # clear the screen with black
	pygame.draw.rect(screen, bat_l["color"], (bat_l["x"]-bat_l["width"], bat_l["y"]-bat_l["height"], bat_l["width"]*2, bat_l["height"]*2), 0)
	pygame.draw.rect(screen, bat_r["color"], (bat_r["x"]-bat_r["width"], bat_r["y"]-bat_r["height"], bat_r["width"]*2, bat_r["height"]*2), 0)

	for ball in balls:
		pygame.draw.rect(screen, ball["color"], (ball["x"]-ball["r"], ball["y"]-ball["r"], ball["r"]*2, ball["r"]*2), 0)

	score = myfont.render("Some text", 1, white)
	screen.blit(score, (320, 240))
	640
480

	pygame.display.update()

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

	update()
	render()

	clock.tick(60)
