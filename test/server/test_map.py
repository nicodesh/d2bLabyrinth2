# -*-coding:Utf-8 -*

""" This module contains all Map tests. That's the main test, because to test a map,
you need to create all other objects : a Robot and a Maze. All this elements interact between each other. """

import unittest
from server.map import *
from server.maze import *
from server.robot import *

class test_map(unittest.TestCase):
	""" Class to test the Roboc Map Module. """

	def test_win(self):
		""" Test of win method. """

		with open("cartes/facile.txt") as f:
			maze_file = f.read()

		the_maze = RobocMaze(maze_file) # Create a new maze
		the_map = RobocMap(the_maze) # Create a new map
		winner_robot = RobocRobot(0, 0) # Create a new Robot
		the_map.add_robot(winner_robot) # Add the robot

		#Force him to win
		the_map.robots[0].x = 9
		the_map.robots[0].y = 5
		
		self.assertEqual(winner_robot, the_map.win())

	def test_in_the_area(self):
		""" Test of in_the_area method. """

		with open("cartes/facile.txt") as f:
			maze_file = f.read()

		the_maze = RobocMaze(maze_file) # Create a new maze
		the_map = RobocMap(the_maze) # Create a new map
		winner_robot = RobocRobot(0, 0) # Create a new Robot
		the_map.add_robot(winner_robot) # Add the robot

		self.assertEqual(the_map.in_the_area(-1,-1), False) # Robot is out (negative coordinates)
		self.assertEqual(the_map.in_the_area(4,4), True) # Robot is in
		self.assertEqual(the_map.in_the_area(11,1), False) # Robot is out on x
		self.assertEqual(the_map.in_the_area(1,11), False) # Robot is out on y

	def test_add_robot(self):
		""" Test of add_robot method. Try to see if there is no collision, even with the max number of robots. """

		with open("cartes/prison.txt") as f:
			maze_file = f.read()

		the_maze = RobocMaze(maze_file) # Create a new maze
		the_map = RobocMap(the_maze) # Create a new map
		winner_robot = RobocRobot(0, 0) # Create a new Robot

		i = 0
		while (i < the_map.free_space):
			the_map.add_robot(RobocRobot(0,0))
			i += 1

	def test_play(self):
		""" Test of "play" method of a Roboc Map. """

		with open("cartes/prison.txt") as f:
			maze_file = f.read()

		the_maze = RobocMaze(maze_file) # Create a new maze
		the_map = RobocMap(the_maze) # Create a new map
		a_robot = RobocRobot(0, 0) # Create a new Robot
		the_map.add_robot(a_robot) # Add the robot to the party

		# We force the Roboc Robots coordinates
		test_x = 18
		test_y = 1

		a_robot.x = test_x
		a_robot.y = test_y

		# Play against the wall
		a_robot.add_command_in_queue("COMMAND:E|1")
		the_map.play(the_map.robots[0])
		self.assertEqual(a_robot.x, test_x) # Coordinates are supposed to be still the same
		self.assertEqual(a_robot.y, test_y) # Coordinates are supposed to be still the same

		# Play normally
		a_robot.add_command_in_queue("COMMAND:S|1")
		the_map.play(the_map.robots[0])
		test_y += 1
		self.assertEqual(a_robot.x, test_x) # Coordinates are supposed to be still the same
		self.assertEqual(a_robot.y, test_y) # Coordinates are supposed to be still the same

		# Play with repetition
		a_robot.add_command_in_queue("COMMAND:S|10")
		while len(a_robot.commands_queue) > 0:
			the_map.play(the_map.robots[0])
		test_y += 10
		self.assertEqual(a_robot.x, test_x) # Coordinates are supposed to be still the same
		self.assertEqual(a_robot.y, test_y) # Coordinates are supposed to be still the same

		# Break a wall
		self.assertEqual(the_map.maze[test_y][test_x+1], "O") # Verify if it's a wall as expected.
		a_robot.add_command_in_queue("COMMAND:PE|1")
		the_map.play(the_map.robots[0])
		self.assertEqual(the_map.maze[test_y][test_x+1], ".") # Verify if now it's a door.

		# Build a wall
		self.assertEqual(the_map.maze[test_y][test_x+1], ".") # Verify if it's a door as expected.
		a_robot.add_command_in_queue("COMMAND:ME|1")
		the_map.play(the_map.robots[0])
		self.assertEqual(the_map.maze[test_y][test_x+1], "O") # Verify if now it's a wall.

# Launch the test
if __name__=='__main__':
    try:
        unittest.main()
    except SystemExit as inst:
        if inst.args[0] is True: # raised by sys.exit(True) when tests failed
            raise