# -*-coding:Utf-8 -*

"""This Maze module contains all Maze class and functions."""

import os
import pickle
from server.map import *

def choose_the_maze():
	""" Display the mazes and ask the admin which maze he wants to play. """

	print("Voici les différentes cartes que vous pouvez jouer :")
	print("")
	maze_number = 0
	for i, f_name in enumerate(os.listdir("cartes")):
		if f_name.endswith(".txt"):
			maze_number += 1
			print("{0:} - {1:}".format(maze_number, f_name))
	print("")

	# Ask the admin for the map he wants to play
	maze_choice = -1
	while maze_choice < 0 or maze_choice > maze_number:
		maze_choice = input("Laquelle souhaitez-vous jouer ? (numéro de carte) : ")
		try:
			maze_choice = int(maze_choice)
		except ValueError:
			maze_choice = -1
	
	# Load the maze file the admin wants to play
	maze_number = 0
	for i, f_name in enumerate(os.listdir("cartes")):
		if f_name.endswith(".txt"):
			maze_number += 1
			if (maze_number == maze_choice):
				f_path = os.path.join("cartes", f_name)
				with open(f_path) as f:
					maze_file = f.read()

	# Create the maze object
	the_maze = RobocMaze(maze_file)
	return the_maze

class RobocMaze:
	"""
	This class returns a RobocMaze object from a Maze string, typically retrieved from a Maze file.
	The walls will be modelized with a list object.

	Args:
		maze_string (str) : A string maze, certainly extracted from a .txt file.

	"""
	def __init__(self, maze_string):
		self.walls = self.create_walls(maze_string)

	def create_walls(self, maze_string):
		""" Return the walls, modelized in a list. """

		walls = [[]]
		line = 0
		self.free_space = 0
		for x in maze_string:
			if x == " ":
				self.free_space += 1
			if x == "\n":
				walls.append([])
				line += 1
			elif x == "X":
				walls[line].append(" ") # If a robot is in the Maze, we delete it. Mouahahah.
				self.free_space += 1
			elif (x.upper() in ['.', 'U', 'O', ' ']):
				walls[line].append(x)
		return walls