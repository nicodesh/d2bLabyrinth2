# -*-coding:Utf-8 -*

""" Roboc Server Module. Contain all functions to make the server work. """

import socket
import select
from server.map import *
from server.maze import *

def launch_server(host, port, the_map):
	"""
	Launch the server. Listen on the specified host and port.
	First, the server waits for new players.
	Then, the server waits for a player sending "c" to launch the game.

	Args:
		host (str) : The host of the server connexion. Probably "localhost".
		port (int) : The port of the server connexion.
		the_map (RobocMap object) : The Roboc Map associated to this new party.
	
	"""

	# ----------------------------------------------------------
	# Server Activation
	# ----------------------------------------------------------

	my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # New socket, IPV4 / TCP
	my_socket.bind((host, port)) # Which host and port
	my_socket.listen(5) # Start listening, queue max 5 connexions

	print("Serveur activé. Le serveur écoute à présent le port {0:}".format(port))

	keep_going = True # The game is now
	party_open = True # Players can still join the game
	connected_clients = [] # No player so far
	player_to_play = -1 # Nobody has to play so far

	while keep_going: # The server is running

		# -----------------------------------------------------------
		# New client connexions
		# -----------------------------------------------------------

		if party_open and (the_map.free_space - len(the_map.robots) > 0) : # Still listening for new connexions
			try:
				connexions_queue, wlist, xlist = select.select([my_socket], [], [], 0.05)
			except select.error:
				pass

			for connexion in connexions_queue:
				new_connexion, new_connexion_infos = connexion.accept()
				connected_clients.append(new_connexion)

				new_robot = RobocRobot(0, 0, new_connexion) # Create a new Robot
				the_map.add_robot(new_robot) # Add the new robot to the map
				
				print("New connexion : ", new_connexion)
				print("Free slots: {}".format(the_map.free_space - len(the_map.robots)))
				new_connexion.send("MSG:INF:Bienvenue sur le serveur !".encode())
				
				if (len(connected_clients) == 1):
					new_connexion.send("MSG:INF:Vous êtes pour l'instant tout seul.".encode())
				
				elif (len(connected_clients) > 1):
					for c_c in connected_clients:
						c_c.send("MSG:INF:{} joueurs connectés. Tapez C pour lancer la partie, Q pour l'arrêter.".format(len(connected_clients)).encode())


		clients_waiting = []
		try:
			clients_waiting, wlist, xlist = select.select(connected_clients, [], [], 0.05)
		except select.error:
			pass

		else:
			for client_waiting in clients_waiting:
				msg = client_waiting.recv(1024).decode()

				if msg.upper() == "Q": # Players can stop the party whenever they want.
					keep_going = False

				# If the game has not started yet, players can launch the game.
				if party_open == True:
					if msg.upper() == "COMMAND:C":
						if len(the_map.robots) > 1:
							party_open = False
							# The game is starting now! So let's display the map for everybody
							the_map.display()
							player_to_play += 1

						else:
							client_waiting.send("MSG:INF:Il n'y pas encore assez de joueurs pour démarrer.".encode())

				else: # New connections not accepted, we are playing so we're just listening for playing commands
					for robot in the_map.robots: # We try to identify the robot matching with the client message.
						if robot.socket == client_waiting:
							robot_speaking = robot
					
					if (msg[:8] == "COMMAND:"):
						print("Commande reçue : {}".format(msg))
						robot_speaking.add_command_in_queue(msg) # We add the command in the robot commands queue

			if party_open == False:
				if the_map.play(the_map.robots[player_to_play]) == True: # If there was a command in the robot commands queue
					the_map.display() # Display the map for everybody
					# Check if someone won
					if the_map.win() != False:
						for r in the_map.robots:
							if r == the_map.win():
								r.socket.send("MSG:INF:Congratz, you win!".encode())
							else:
								r.socket.send("MSG:INF:Sorry, you lose!".encode())
						keep_going = False
					else:
						if (player_to_play < len(the_map.robots)-1): # Find the next one to play
							player_to_play += 1
						else: # Reset the list if it was the last one.
							player_to_play = 0

	for client in connected_clients:
		client.send("MSG:Q".encode())
		client.close()

	my_socket.close()