# -*-coding:Utf-8 -*

""" Map Module of Roboc. Contain the RobocMap class, which is the main class of the game. """

import os
import pickle
import random
from server.robot import *

#-------------------------------------------------------------------------
# RobocMap Class
#-------------------------------------------------------------------------

class RobocMap:
	""" Class creating a new game. A map is a maze with robots.
	All commands and stuff are controlled by this class.
	It's kind of the god class of the game ;)

	Args:
		maze (RobocMaze object). The maze which should be used as map in the Game.

	"""
	def __init__(self, maze):
		self.commands = ["Q", "N", "S", "E", "O", "MN", "MS", "ME", "MO", "PN", "PS", "PE", "PO"]
		self.sizex = len(maze.walls[0])
		self.sizey = len(maze.walls)
		self.maze = maze.walls
		self.robots = []
		self.free_space = maze.free_space

	def play(self, robot):
		"""
		Execute the first command in the commands list of the robot.

		Args:
			robot (RobocRobot object) : the robot which is going to play.

		"""
		try:
			c = robot.commands_queue.pop(0).upper()
		except:
			return False
		
		x = int(robot.x)
		y = int(robot.y)

		if (c in ("N", "MN", "PN")): # To the North! (Move, wall or door)
			y -= 1
		elif (c in ("S", "MS", "PS")): # To the South! (Move, wall or door)
			y += 1
		elif (c in ("E", "ME", "PE")): # To the East! (Move, wall or door)
			x += 1
		elif (c in ("O", "MO", "PO")): # To the West! (Move, wall or door)
			x -= 1

		if (c in ("N", "S", "E", "O")): # It's a move.
			if self.in_the_area(x, y): # We are still in the Map
				if (self.maze[y][x] in [" ", ".", "U"]): # It's a legal move.
					legal_move = True
					for other_robot in self.robots:
						if other_robot.x == x and other_robot.y == y:
							legal_move = False
							break
					if legal_move:
						robot.x = x
						robot.y = y

		elif (c in ("MN", "MS", "ME", "MO")): # It's a door closing.
			if (self.maze[y][x] == "."): # It's a legal door closing.
				self.maze[y][x] = "O" # We close the door

		elif (c in ("PN", "PS", "PE", "PO")): # It's a door opening.
			if (self.maze[y][x] == "O"): # It's a legal door opening.
				self.maze[y][x] = "." # We open the door

		return True

	def display(self):
		""" Send to map to all players. """

		for robot in self.robots: # Parse each robot
			map_str = "MSG:MAP:"
			for i, row in enumerate(self.maze): # Construct the map for the robot
				line = ""
				for j, x in enumerate(row):
					for r in self.robots: # Verify if a robot is here
						if (i, j) == (r.y, r.x): # A robot is here and...
							if r == robot: #... It's himself
								x = "X"
							else: # ... It's a competitor
								x = "x"
					line += x # Add the character to the line
				map_str += line + "\n" # Add the line to the map
			robot.socket.send(map_str.encode())

	def add_robot(self, robot):
		"""
		Add a new robot to the map. We have to place it at a random place.

		Args:
			robot (RobocRobot object) : the robot to add.

		"""

		# Finding a place for the robot. Free space, without any other robot.
		while (self.maze[robot.y][robot.x] != " "):
			robot.x = random.randrange(0, self.sizex)
			robot.y = random.randrange(0, self.sizey)
			for old_gangsta in self.robots:
				if (robot.x, robot.y) == (old_gangsta.x, old_gangsta.y):
					robot.x = 0
					robot.y = 0

		# Finally, adding it to the map.
		self.robots.append(robot)

	def in_the_area(self, x, y):
		"""
		Determine if the coordinates are in the Map.

		Args:
			x (int) : x coordonate
			y (int) : y coordonate

		"""

		if x < 0 or y < 0:
			return False

		elif self.sizex <= x or self.sizey <= y:
			return False

		else:
			return True

	def win(self):
		""" Look for a winner. Return the winner RobocRobot if it exists, otherwise return False. """
		
		for robot in self.robots:
			if self.maze[robot.y][robot.x] == "U":
				return robot # We've got a winner!!!

		return False # No winner for this time!
