from enum import Enum
import random


class Action(Enum):
	UP = "U"
	DOWN = "D"
	NONE = " "


"""
This class is a template. Extensions of this class should implement the "step" method
"""
class Agent:
	def __init__(self):
		self.score = 0
		self.bat_y = 0.5 # this value is a fraction of the screen height
		self.bat_height = 0.08
		self.action = Action.NONE
	
	"""
	This method should modify the `action` field to represent the desired action.
	"""
	def step(self, gamestate):
		raise NotImplementedError


class Game:
	def __init__(self, agent_a, agent_b, options=None):
		self.agent_a = agent_a
		self.agent_b = agent_b
		self.total_hits = 0
		
		self.options = {
			"final_score": 7,
			"bat_speed": 0.006,
			"ball_speed": 0.015
		}
		
		self.gamestate = {
			"ball": {
				"x": 0.1,
				"y": 0.5,
				"xvel": self.options["ball_speed"] * 0.4,
				"yvel": self.options["ball_speed"] * (random.randrange(0, 2)-0.5),
			}
		}
	
	def step(self):
		self.agent_a.step(self.gamestate)
		flipped = self.gamestate.copy() # The other agent will have a mirrored perception of the game state
		flipped["ball"] = flipped["ball"].copy()
		flipped["ball"]["x"] = 1 - flipped["ball"]["x"]
		flipped["ball"]["xvel"] *= -1
		self.agent_b.step(flipped)
		
		for agent in [self.agent_a, self.agent_b]:
			if agent.action == Action.UP:
				agent.bat_y -= self.options["bat_speed"]
				agent.bat_y = max(agent.bat_height, agent.bat_y)
			elif agent.action == Action.DOWN:
				agent.bat_y += self.options["bat_speed"]
				agent.bat_y = min(1 - agent.bat_height, agent.bat_y)
		
		ball = self.gamestate["ball"]
		x2 = ball["x"] + ball["xvel"]
		y2 = ball["y"] + ball["yvel"]
		
		if x2 < 0:
			ball["xvel"] *= -1
			if self.agent_a.bat_y - self.agent_a.bat_height < y2 < self.agent_a.bat_y + self.agent_a.bat_height: # bounce
				x2 = -x2
				self.total_hits += 1
			else: # don't bounce
				self.agent_b.score += 1
				x2 = 0.1
				y2 = self.agent_b.bat_y
		elif x2 > 1:
			ball["xvel"] *= -1
			if self.agent_b.bat_y - self.agent_b.bat_height < y2 < self.agent_b.bat_y + self.agent_b.bat_height: # bounce
				x2 = 2-x2
				self.total_hits += 1
			else: # don't bounce
				self.agent_a.score += 1
				x2 = 0.9
				y2 = self.agent_a.bat_y
		if y2 < 0 or y2 > 1:
			ball["yvel"] *= -1
		
		ball["x"] = x2
		ball["y"] = y2

	def play(self, renderer=None):
		while max(self.agent_a.score, self.agent_b.score) < self.options["final_score"]:
			self.step()
			
			if renderer is not None:
				renderer(self.gamestate, self.agent_a, self.agent_b)
		
		if self.agent_a.score > self.agent_b.score:
			return self.agent_a, self.total_hits
		else:
			return self.agent_b, self.total_hits
