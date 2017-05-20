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

key_pressed = 0 #ensures multiple click events don't occur in a single click for textareas


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

def rad_btn(border_color, active_color, hover_color, x, y, action=None, group={}, width=25, height=25, thick=3):
	global rad_clicked #ensures multiple click events don't occur in a single click
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	if (x + width > mouse[0] > x) and (y + height > mouse[1] > y): #checks to see if mouse is over btn
		if click[0] == 1 and action != None and rad_clicked == 0: #btn clicked
			rad_clicked = 1
			if group[action]: #changes btn status
				group[action] = False
			else:
				group[action] = True
	if group[action]: #btn selected
		pygame.draw.rect(screen, active_color, (x,y,width,height), thick)
	else: #btn not selected
		pygame.draw.rect(screen, border_color, (x,y,width,height), thick)
	if click[0] == 0:
		rad_clicked = 0

def text_obj(text, font, color, background_color, x=-1, y=-1, offset_x=0, offset_y=0): #text for menus e.g. titles
	if x == -1 and y == -1: #text in center of window
		text = font.render(text, True, color, background_color)
		text_width = text.get_rect().width
		text_height = text.get_rect().height
		screen.blit(text,((WIDTH / 2.0) - (text_width / 2.0) + offset_x,(HEIGHT / 2.0) - (text_height / 2.0) + offset_y))
	else: #text top right in position of x and y
		text = font.render(text, True, color, background_color)
		screen.blit(text,(x, y))


class textarea(object):

	def __init__(self, border_color=grey, active_color=red, box_color=white, text_color=black, x=0, y=0, max_char=10, text_type=small_font, in_text="example", width=150, height=25, thick=3):
		self.border_color = border_color
		self.active_color = active_color
		self.box_color = box_color
		self.text_color = text_color
		self.x = x
		self.y = y
		self.max_char = max_char
		self.text_type = text_type
		self.in_text = in_text
		self.width = width
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
			screen.blit(starting_text,(self.x+3, self.y+3))

	def textarea(self): #un selected textarea
		pygame.draw.rect(screen, self.box_color, (self.x,self.y,self.width,self.height))
		pygame.draw.rect(screen, self.border_color, (self.x,self.y,self.width,self.height), self.thick)
		text_list = []
		for char in self.in_text: #sets max character lengh
			if len(text_list) < self.max_char:
				text_list.append(char)
		starting_text = self.text_type.render("".join(text_list), True, self.text_color)
		screen.blit(starting_text,(self.x+3, self.y+3))

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
		elif event.type == KEYUP:
			key_pressed = 0

	def get_text(self):
		return self.in_text

	def text_area_selection(self):
		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()
		width, height = self.get_dim() #gets width and height for textarea
		x, y = self.get_pos() #gets x and y for textarea
		if (x + width > mouse[0] > x) and (y + height > mouse[1] > y): #checks to see if mouse is over textarea
			if click[0] == 1: #textarea selected
				#pygame.time.wait(150) #wait stops multiple clicks
				self.set_active(textareas)
		elif click[0] == 1: #textarea not selected
			self.set_active_false()
		if self.get_state() == True:
			self.active_textarea()
		else:
			self.textarea()

#textareas for use in menus
connect_ip = textarea(grey, red, white, black, 350, 210, 15, small_font, "IP address", 180, 25, 3)
host_games = textarea(grey, red, white, black, 230, 210, 3, small_font, "10", 50, 25, 3)

textareas = [connect_ip, host_games]

#radio button groups
global rad_btns_stats
rad_btns_stats = {"host":False, "client":True}

def main_menu():
	#setting and position of title
	title_text = text_obj("PingAI", large_font, white, black, -1, -1)

	#buttons
	button('Single player', med_font, white, black, red, 150, 300, "singleplayer")
	button('Multiplayer', med_font, white, black, red, 150, 350, "multiplayer")
	button("Exit", small_font, red, black, white, 570, 440, "exit")


def multiplayer_menu():
	current_menu = "multi"

	#text for menu
	title_text = text_obj("Multiplayer", large_font, white, black, -1, -1, 0, -150)
	host_text = text_obj("Host", small_font, white, black, 80, 155)
	client_text = text_obj("Client", small_font, white, black, 385, 155)
	ip_address_text = text_obj("IP address: {}".format(socket.gethostbyname(socket.gethostname())), small_font, white, black, 45, 185)
	game_number_text = text_obj("number of games:", small_font, white, black, 45, 215)
	connect_to_text = text_obj("Connect to:", small_font, white, black, 350, 185)

	#buttons
	button('Main menu', med_font, white, black, red, 45, 430, "main")
	button("Exit", small_font, red, black, white, 570, 440, "exit")
	button("Play", med_font, white, black, red, 560, 360, "play")

	#radio buttons
	rad_btn(white, red, grey, 45, 150, "host", rad_btns_stats)
	rad_btn(white, red, grey, 350, 150, "client", rad_btns_stats)

	#textareas
	textareas[0].text_area_selection() #allows textarea to render
	textareas[1].text_area_selection()
	if textareas[0].get_state(): #allows text update when textarea is selected
		textareas[0].update_text()
	elif textareas[1].get_state():
		textareas[1].update_text()


def updateMenu():
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
	updateMenu()
	clock.tick(30)
