# -*-coding:Utf-8 -*

""" This module contains the RobocRobot class. """

class RobocRobot:
	""" Create a Roboc Robot.

		Args:
			x: (int) X Coordinate.
			y: (int) Y Coordinate.
			socket: (socket) Optionnal. The player socket associated to the Robot.

	"""

	def __init__(self, x, y, socket=""):
		self.x = x
		self.y = y
		self.socket = socket
		self.commands_queue = []

	def add_command_in_queue(self, command):
		"""
		Add a new command in the queue of the robot.
		When it's time to play for him, the server will check
		if a command is ready to play in this list.

		Args:
			command (str) : The command. Format: COMMAND:NAME|REPETITION. For instance COMMAND:N|4

		"""

		command_splited = command.split("|")
		command_name = command_splited[0][8:]
		try:
			i = int(command_splited[1])
		except:
			i = 1
		while i > 0:
			self.commands_queue.append(command_name) # Command added.
			i -= 1