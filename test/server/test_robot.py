# -*-coding:Utf-8 -*

""" Module to test the RobocRobot Module. """

import unittest
from server.robot import *

class test_robot(unittest.TestCase):
	""" Test to try the class Robot Roboc. """

	def test_robot(self):
		""" Try to create a Roboc Robot. """

		x = 1
		y = 2

		myrobot = RobocRobot(x, y)
		myrobot.add_command_in_queue("COMMAND:O|24")		

		self.assertIs(type(myrobot), RobocRobot) # Test the type
		self.assertEqual(myrobot.x, x) # Test the X coordonate
		self.assertEqual(myrobot.y, y) # Test the Y coordonate
		self.assertIn("O", myrobot.commands_queue)

# Launch the test
if __name__=='__main__':
    try:
        unittest.main()
    except SystemExit as inst:
        if inst.args[0] is True: # raised by sys.exit(True) when tests failed
            raise