import pygame, simplepygame, sys, socket
sys.path.insert(0, 'api/')
import apitest
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
grey = (150, 150, 150)

large_font = pygame.font.Font('freesansbold.ttf', 100) #font for main title
med_font = pygame.font.Font('freesansbold.ttf', 30) #font for sub heading
small_font = pygame.font.Font('freesansbold.ttf', 20) #font for small text

current_menu = "main" #menu the user is on

rad_btns_stats = {"host":False, "client":True}

key_pressed = 0


def button(text, text_type, text_color, background_color, active_color, x, y, action=None): #this makes a btn, code works but needs tidying up
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	button_object = text_type.render(text, True, text_color, background_color) #makes text (used to get width and height)
	button_width = button_object.get_rect().width
	button_height = button_object.get_rect().height
	if (x + button_width > mouse[0] > x) and (y + button_height > mouse[1] > y): #checks to see if mouse is over text
		button_object = text_type.render(text, True, active_color, background_color)
		if click[0] == 1 and action != None: #check for button press
			if action == "singleplayer":
				apitest.spec()
			elif action == "multiplayer":
				global current_menu
				current_menu = "multi"
			elif action == "main":
				global current_menu
				current_menu = "main"
			elif action == "exit":
				sys.exit()
			elif action == "play":
				simplepygame.mainLoop() #change this to start multiplayer game and / or server
	else:
		button_object = text_type.render(text, True, text_color, background_color) #button not presses or hover
	screen.blit(button_object,(x,y))

def rad_btn(border_color, active_color, hover_color, x, y, action=None, width=25, height=25, thick=3):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	if (x + width > mouse[0] > x) and (y + height > mouse[1] > y): #checks to see if mouse is over btn
		if click[0] == 1 and action != None: #btn clicked
			pygame.time.wait(150) #wait stopps multiple clicks
			global rad_btns_stats
			if rad_btns_stats[action]: #changes btn status
				rad_btns_stats[action] = False
			else:
				rad_btns_stats[action] = True
	if rad_btns_stats[action]: #btn selected
		pygame.draw.rect(screen, active_color, (x,y,width,height), thick)
	else: #btn not selected
		pygame.draw.rect(screen, border_color, (x,y,width,height), thick)

class textarea(object):

	def __init__(self, border_color=grey, active_color=red, box_color=white, text_color=black, x=0, y=0, max_char=10, text_type=small_font, in_text="example", height=25, thick=3):
		self.border_color = border_color
		self.active_color = active_color
		self.box_color = box_color
		self.text_color = text_color
		self.x = x
		self.y = y
		self.max_char = max_char
		self.text_type = text_type
		self.in_text = in_text
		self.width = max_char*15
		self.height = height
		self.thick = thick
		self.active = False

	def active_textarea(self): #selected textarea
			pygame.draw.rect(screen, self.box_color, (self.x,self.y,self.width,self.height))
			pygame.draw.rect(screen, self.active_color, (self.x,self.y,self.width,self.height), self.thick)
			text_list = []
			for char in self.in_text: #sets max character lengh
				if len(text_list) < self.max_char:
					text_list.append(char)
			starting_text = self.text_type.render("".join(text_list), True, self.text_color)
			screen.blit(starting_text,(self.x+5, self.y+5))

	def textarea(self): #un selected textarea
		pygame.draw.rect(screen, self.box_color, (self.x,self.y,self.width,self.height))
		pygame.draw.rect(screen, self.border_color, (self.x,self.y,self.width,self.height), self.thick)
		text_list = []
		for char in self.in_text: #sets max character lengh
			if len(text_list) < self.max_char:
				text_list.append(char)
		starting_text = self.text_type.render("".join(text_list), True, self.text_color)
		screen.blit(starting_text,(self.x+5, self.y+5))

	def get_pos(self): #returns x and y
		return (self.x, self.y)

	def get_dim(self): #returns width and height
		return (self.width, self.height)

	def get_state(self): #returns state
		return self.active

	def set_active(self, all_textareas): #deselect all textareas and selects one user clicked
		for textarea in all_textareas:
			textarea.set_active_false()
		self.active = True

	def set_active_false(self): #deselects text area
		self.active = False

	def update_text(self):
		global key_pressed
		text_list = []
		for char in self.in_text: #sets max character lengh
			if len(text_list) <= self.max_char:
				text_list.append(char)
		if event.type == KEYDOWN  and key_pressed == 0:
			key_pressed = 1
			if event.key == K_BACKSPACE:
				text_list = text_list[0:-1]
			elif event.key <=127:
				text_list.append(chr(event.key))
			self.in_text = "".join(text_list)
		if event.type == KEYUP:
			key_pressed = 0

	def get_text(self):
		return self.in_text

def text_area_selection(textarea_in):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	width, height = textarea_in.get_dim() #gets width and height for textarea
	x, y = textarea_in.get_pos() #gets x and y for textarea
	if (x + width > mouse[0] > x) and (y + height > mouse[1] > y): #checks to see if mouse is over textarea
		if click[0] == 1: #textarea selected
			#pygame.time.wait(150) #wait stops multiple clicks
			textarea_in.set_active(textareas)
	elif click[0] == 1: #textarea not selected
		textarea_in.set_active_false()
	if textarea_in.get_state() == True:
		textarea_in.active_textarea()
	else:
		textarea_in.textarea()

#textareas for use in menus
connect_ip = textarea(grey, red, white, black, 350, 210, 15, small_font, "IP address", 25, 3)
host_games = textarea(grey, red, white, black, 230, 210, 3, small_font, "10", 25, 3)

textareas = [connect_ip, host_games]

def main_menu():
	#setting and position of title
	title_text = large_font.render('PingAI', True, white, black)
	title_text_width = title_text.get_rect().width
	title_text_height = title_text.get_rect().height
	screen.blit(title_text,((WIDTH / 2.0) - (title_text_width / 2.0),(HEIGHT / 2.0) - (title_text_height / 2.0)))

	#buttons
	button('Single player', med_font, white, black, red, 150, 300, "singleplayer")
	button('Multiplayer', med_font, white, black, red, 150, 350, "multiplayer")
	button("Exit", small_font, red, black, white, 570, 440, "exit")


def multiplayer_menu():
	current_menu = "multi"

	#setting and position of title and text
	title_text = large_font.render("Multiplayer", True, white, black)
	title_text_width = title_text.get_rect().width
	title_text_height = title_text.get_rect().height
	screen.blit(title_text,((WIDTH / 2.0) - (title_text_width / 2.0),(HEIGHT / 2.0) - (title_text_height / 2.0) - 150))

	host_text = small_font.render("Host", True, white, black)
	screen.blit(host_text,(80, 155))

	client_text = small_font.render("Client", True, white, black)
	screen.blit(client_text,(385, 155))

	ip_address_text = small_font.render("IP address: {}".format(socket.gethostbyname(socket.gethostname())), True, white, black)
	screen.blit(ip_address_text,(45, 185))

	ip_address_text = small_font.render("number of games:", True, white, black)
	screen.blit(ip_address_text,(45, 215))

	ip_address_text = small_font.render("Connect to:", True, white, black)
	screen.blit(ip_address_text,(350, 185))

	#buttons
	button('Main menu', med_font, white, black, red, 45, 430, "main")
	button("Exit", small_font, red, black, white, 570, 440, "exit")
	button("Play", med_font, white, black, red, 560, 360, "play")

	#radio buttons
	rad_btn(white, red, grey, 45, 150, "host")
	rad_btn(white, red, grey, 350, 150, "client")

	#textareas
	text_area_selection(textareas[0]) #allows textarea to render
	text_area_selection(textareas[1])
	if textareas[0].get_state(): #allows text update when textarea is selected
		textareas[0].update_text()
	elif textareas[1].get_state():
		textareas[1].update_text()


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
