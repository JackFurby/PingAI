import pygame, sys
from pygame.locals import *
import copy

sys.path.insert(0, 'api/')
sys.path.insert(0, 'nn/')
import api
import nn


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


class NNAgent(api.Agent):
	def __init__(self, network):
		api.Agent.__init__(self)
		self.nn = nn.NeuralNetwork(network)
	
	def step(self, gamestate):
		ball = gamestate["ball"]
		xvel = 0 if ball["xvel"] < 0 else 1
		yvel = 0 if ball["yvel"] < 0 else 1
		up, down = self.nn.calculate_output_layer([ball["x"], ball["y"], xvel, yvel, self.bat_y])
		
		if up > 0.5 and down < 0.5:
			self.action = api.Action.UP
		elif up < 0.5 and down < 0.5:
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
	
	keys = pygame.key.get_pressed()
	if not keys[K_SPACE]:
		return

	screen.fill(BLACK)

	pygame.draw.rect(screen, WHITE, ( 0, (agent_a.bat_y - agent_a.bat_height) * HEIGHT, 10, agent_a.bat_height * 2 * HEIGHT ), 0)
	pygame.draw.rect(screen, WHITE, ( WIDTH-10, (agent_b.bat_y - agent_b.bat_height) * HEIGHT, 10, agent_b.bat_height * 2 * HEIGHT ), 0)

	pygame.draw.rect(screen, WHITE, ( (gamestate["ball"]["x"] * WIDTH) - 10, (gamestate["ball"]["y"] * HEIGHT) - 10, 20, 20), 0)

	pygame.display.update()
	clock.tick(60)

def main():
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

	#agent_a = KeyboardAgent(K_w, K_s)
	#agent_b = KeyboardAgent(K_UP, K_DOWN)
	#agent_b = NaiveAIAgent()
	agents = [NNAgent(nn.random_weights([5, 10, 2], 1)) for _ in range(0, 10)]
	
	while True:
		next_gen = []
		total_hits = 0
		for a, b in zip(agents[::2], agents[1::2]):
			game = api.Game(a, b)
			winner, hits = game.play(renderer=pygame_render)
			print("Game ended after {} hits".format(hits))
			total_hits += hits
			next_gen.append(winner)
		
		agents = []
		
		for agent in next_gen + next_gen:
			child = NNAgent(copy.deepcopy(agent.nn.weights))
			child.nn.mutate(0.1)
			agents.append(child)
		
		print("### Total hits this generation: {} ###".format(total_hits))


if __name__ == "__main__":
	main()
