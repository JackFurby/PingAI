import pygame, simplepygame, sys
from pygame.locals import *

WIDTH = 640
HEIGHT = 480
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption("PongAI")
clock = pygame.time.Clock()
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

large_font = pygame.font.Font('freesansbold.ttf', 100) #font for main title
med_font = pygame.font.Font('freesansbold.ttf', 30) #font for sub heading
small_font = pygame.font.Font('freesansbold.ttf', 15) #font for small text

current_menu = "main" #menu the user is on

def button(text, text_type, text_color, background_color, active_color, rel_x, rel_y, action=None):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	button_object = text_type.render(text, True, text_color, background_color)
	button_width = button_object.get_rect().width
	button_height = button_object.get_rect().height
	text_x = (WIDTH / 2.0) - (button_width / 2.0) + rel_x
	text_y = (HEIGHT / 2.0) - (button_height / 2.0) + rel_y
	if (text_x + button_width > mouse[0] > text_x) and (text_y + button_height > mouse[1] > text_y):
		button_object = med_font.render(text, True, active_color, black)
		if click[0] == 1 and action != None:
			if action == "singleplayer":
				simplepygame.mainLoop()
			elif action == "multiplayer":
				global current_menu
				current_menu = "multi"
			elif action == "exit":
				sys.exit()
	else:
		button_object = med_font.render(text, True, text_color, black)
	screen.blit(button_object,(text_x,text_y))

def main_menu():
	#setting and position of title
	title_text = large_font.render('PingAI', True, white, black)
	title_text_width = title_text.get_rect().width
	title_text_height = title_text.get_rect().height
	screen.blit(title_text,((WIDTH / 2.0) - (title_text_width / 2.0),(HEIGHT / 2.0) - (title_text_height / 2.0)))

	#buttons
	button('Single player', med_font, white, black, red, -120, 80, "singleplayer")
	button('Multiplayer', med_font, white, black, red, 120, 80, "multiplayer")
	button("Exit", small_font, red, black, white, 240, 200, "exit")


def multiplayer_menu():
	current_menu = "multi"
	#text for multiplayer menu
	multi_title = 'Multiplayer'

	#setting and position of title
	title_text = large_font.render(multi_title, True, white, black)
	title_text_width = title_text.get_rect().width
	title_text_height = title_text.get_rect().height
	screen.blit(title_text,((WIDTH / 2.0) - (title_text_width / 2.0),(HEIGHT / 2.0) - (title_text_height / 2.0) - 150))

def updateTitle():
	keys = pygame.key.get_pressed()

	screen.fill((0, 0, 0)) # clear the screen with black

	if current_menu == "main":
		main_menu()
	elif current_menu == "multi":
		multiplayer_menu()

	pygame.display.update()

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

	updateTitle()

	clock.tick(30)
