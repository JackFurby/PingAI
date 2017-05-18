import pygame, sys
from pygame.locals import *

import api


class KeyboardAgent(api.Agent):
	def __init__(self, up_key, down_key):
		api.Agent.__init__(self)
		self.up_key = up_key
		self.down_key = down_key

	def step(self, gamestate):
		keys = pygame.key.get_pressed()

		if keys[self.up_key] and not keys[self.down_key]:
			self.action = api.Action.UP
		elif not keys[self.up_key] and keys[self.down_key]:
			self.action = api.Action.DOWN
		else:
			self.action = api.Action.NONE


class NaiveAIAgent(api.Agent):
	def step(self, gamestate):
		if gamestate["ball"]["y"] < self.bat_y:
			self.action = api.Action.UP
		else:
			self.action = api.Action.DOWN


def pygame_render(gamestate, agent_a, agent_b):
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

	screen.fill(BLACK)

	pygame.draw.rect(screen, WHITE, ( 0, (agent_a.bat_y - agent_a.bat_height) * HEIGHT, 10, agent_a.bat_height * 2 * HEIGHT ), 0)
	pygame.draw.rect(screen, WHITE, ( WIDTH-10, (agent_b.bat_y - agent_b.bat_height) * HEIGHT, 10, agent_b.bat_height * 2 * HEIGHT ), 0)

	pygame.draw.rect(screen, WHITE, ( (gamestate["ball"]["x"] * WIDTH) - 10, (gamestate["ball"]["y"] * HEIGHT) - 10, 20, 20), 0)

	pygame.display.update()
	clock.tick(60)

def spec():
	global screen
	global BLACK
	global WHITE
	global WIDTH
	global HEIGHT
	global clock

	WIDTH = 640
	HEIGHT = 480
	WHITE = (0xFF, 0xFF, 0xFF)
	BLACK = (0x00, 0x00, 0x00)

	screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
	pygame.display.set_caption("PongAI")

	pygame.init()
	clock = pygame.time.Clock()

	agent_a = KeyboardAgent(K_w, K_s)
	#agent_b = KeyboardAgent(K_UP, K_DOWN)
	agent_b = NaiveAIAgent()

	game = api.Game(agent_a, agent_b)
	game.play(renderer=pygame_render)


if __name__ == "__main__":
	spec()
