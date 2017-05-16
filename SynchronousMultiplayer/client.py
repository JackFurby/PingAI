import socket
import pygame, sys
from pygame.locals import *
import json

WIDTH = 640
HEIGHT = 480
TCP_PORT = 1337
pygame.init()


if len(sys.argv) != 2:
	print("Error: Specify an IP address.")
	exit()

screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption("PongAI")
white = (255, 255, 255)
myfont = pygame.font.SysFont("monospace", 32)

ball = {}
bat_l = {}
bat_r = {}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((sys.argv[1], TCP_PORT))
sfile = s.makefile()


def update():
	keys = pygame.key.get_pressed()

	if keys[K_DOWN] and not keys[K_UP]:
		s.send(b"D")
	elif keys[K_UP] and not keys[K_DOWN]:
		s.send(b"U")
	else: 
		s.send(b" ")


	state = sfile.readline()
	print(state)
	bat_l, bat_r, ball = json.loads(state) 
	print(bat_l)

	return bat_l, bat_r, ball
	

def render(bat_l, bat_r, ball):
	print(bat_l)
	screen.fill((0, 0, 0)) # clear the screen with black
	pygame.draw.rect(screen, white, (bat_l["x"]-bat_l["width"], bat_l["y"]-bat_l["height"], bat_l["width"]*2, bat_l["height"]*2), 0)
	pygame.draw.rect(screen, white, (bat_r["x"]-bat_r["width"], bat_r["y"]-bat_r["height"], bat_r["width"]*2, bat_r["height"]*2), 0)

	pygame.draw.rect(screen, white, (ball["x"]-ball["r"], ball["y"]-ball["r"], ball["r"]*2, ball["r"]*2), 0)

	score = myfont.render("{} : {}".format(bat_l["score"], bat_r["score"]) , 1, white)
	screen.blit(score, (280, 240))
	

	pygame.display.update()

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

	bat_l, bat_r, ball = update()
	render(bat_l, bat_r, ball)