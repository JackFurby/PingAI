import pygame, simplepygame
from pygame.locals import *

WIDTH = 640
HEIGHT = 480
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption("PongAI")
clock = pygame.time.Clock()
white = (255, 255, 255)
black = (0, 0, 0)

#text for menu(s)
mainTitle = 'PingAI'
subHeading = 'press enter to play...'

#text properties for menu(s)
titleFont = pygame.font.Font('freesansbold.ttf', 100) #font for main title
subFont = pygame.font.Font('freesansbold.ttf', 30) #font for sub heading

def updateTitle():
	keys = pygame.key.get_pressed()

	if keys[K_RETURN]:
		simplepygame.mainLoop()

	screen.fill((0, 0, 0)) # clear the screen with black

	titleText = titleFont.render(mainTitle, True, white, black) #main title
	textWidth = titleText.get_rect().width
	textHeight = titleText.get_rect().height
	screen.blit(titleText,((WIDTH / 2.0) - (textWidth / 2.0),(HEIGHT / 2.0) - (textHeight / 2.0)))

	subTitleText = subFont.render(subHeading, True, white, black) #sub heading
	subTextWidth = subTitleText.get_rect().width
	subTextHeight = subTitleText.get_rect().height
	screen.blit(subTitleText,((WIDTH / 2.0) - (subTextWidth / 2.0),(HEIGHT / 2.0) - (subTextHeight / 2.0) + 80))


	pygame.display.update()

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

	updateTitle()

	clock.tick(30)
