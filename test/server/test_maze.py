# -*-coding:Utf-8 -*

""" Module to test the Maze Module. """

import unittest
from server.maze import *

class test_maze(unittest.TestCase):
	""" Class to test the creation of a Maze from a file. """

	def test_maze(self):
		""" Test the Maze Creation. """

		with open("cartes/facile.txt") as f:
			maze_file = f.read()

		# Create the maze
		the_maze = RobocMaze(maze_file)

		# Test the types
		self.assertIs(type(the_maze), RobocMaze) # Maze Object
		self.assertIs(type(the_maze.walls), list) # Walls of the maze (list type)

		# Test there is no Robot in the Maze.
		for row in the_maze.walls:
			self.assertNotIn("X", row)

# Launch the test
if __name__=='__main__':
    try:
        unittest.main()
    except SystemExit as inst:
        if inst.args[0] is True: # raised by sys.exit(True) when tests failed
            raise