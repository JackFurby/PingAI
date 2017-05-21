import pygame, sys
from pygame.locals import *

import api, cv2, os
import pyscreenshot as ImageGrab
import numpy as np



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

			#save keys pressed for screenshots
			text_file = open("/Users/jack/Documents/programming/pingAILearning/keys.txt", "w")
			text_file.write(str(key_record))
			text_file.close()

			pygame.quit()
			sys.exit()

	screen.fill(BLACK)

	pygame.draw.rect(screen, WHITE, ( 0, (agent_a.bat_y - agent_a.bat_height) * HEIGHT, 10, agent_a.bat_height * 2 * HEIGHT ), 0)
	pygame.draw.rect(screen, WHITE, ( WIDTH-10, (agent_b.bat_y - agent_b.bat_height) * HEIGHT, 10, agent_b.bat_height * 2 * HEIGHT ), 0)

	pygame.draw.rect(screen, WHITE, ( (gamestate["ball"]["x"] * WIDTH) - 10, (gamestate["ball"]["y"] * HEIGHT) - 10, 20, 20), 0)

	pygame.display.update()

	#takes screenshot and key input
	global run_number
	global key_record
	global training_output
	global file_name
	run_number += 1
	if run_number % 10 == 0: #only take record every half a second



		pygame.image.save(screen, "/Users/jack/Documents/programming/pingAILearning/pic/screenshot" + str(run_number) + ".png")


		screen_save = cv2.imread("/Users/jack/Documents/programming/pingAILearning/pic/screenshot" + str(run_number) + ".png",0)
		#screen_save = np.fromstring(pygame.image.tostring(screen, "RGB"), dtype='uint8')
		#screen_save = ImageGrab.grab(bbox=(0,40,WIDTH,HEIGHT)) # X1,Y1,X2,Y2
		#screen_save = cv2.cvtColor(screen_save,cv2.COLOR_BGR2GRAY)
		screen_save = cv2.resize(screen_save, (100, 100))


		keys = pygame.key.get_pressed()
		pressed_key = [0,0,0]
		if keys[K_w]:
			pressed_key = [1,0,0]
			key_record.append(pressed_key)
		elif keys[K_s]:
			pressed_key = [0,1,0]
			key_record.append(pressed_key)
		else:
			pressed_key = [0,0,1]
			key_record.append(pressed_key)
		training_output.append([screen_save,pressed_key])

		if len(training_output) % 500 == 0:
			print(len(training_output))
			np.save(file_name, training_output)

	clock.tick(60)

def spec():
	global screen
	global BLACK
	global WHITE
	global WIDTH
	global HEIGHT
	global clock

	global run_number
	global key_record
	global training_output
	global file_name
	file_name = '/Users/jack/Documents/programming/pingAILearning/training_output.npy'
	if os.path.isfile(file_name):
		training_output = list(np.load(file_name))
	else:
		training_output = []

	WIDTH = 640
	HEIGHT = 480
	WHITE = (0xFF, 0xFF, 0xFF)
	BLACK = (0x00, 0x00, 0x00)

	run_number = 0
	key_record = []
	training_output = []

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
