# -*-coding:Utf-8 -*

""" Roboc Client Module. Contains all functions to run the RobocRobot application client side. """

import socket
import sys
import re
import os
from threading import Thread, RLock

my_lock = RLock()
client_is_on = True

# --------------------------------------------------------
# Thread class listening the client inputs
# --------------------------------------------------------

class ListenClient(Thread):
	"""
	Thread listening input in order to send a message to the Roboc Server.
	
	Args:
		socket (socket) : Socket connected to the server.

	"""
	def __init__(self, socket):
		Thread.__init__(self)
		self.socket = socket

	def run(self):
		msg_to_send = "".encode()
		global client_is_on

		while client_is_on == True:
			
			command_from_input = input("") # Listen the input entry
			
			if command_from_input.upper() == "Q":
				stop_client(self.socket)

			else:
				try:
					command_to_send = re.sub(r"[0-9]+.*", r"", command_from_input) # Catch the command 
					repeat = re.sub(r"[a-zA-Z]+", r"", command_from_input) # Catch the repeat (numbers after the command)
					try:
						repeat = int(repeat)
						command_to_send = 'COMMAND:' + command_to_send + "|" + str(repeat)
					except:
						command_to_send = 'COMMAND:' + command_to_send

					self.socket.send(command_to_send.encode())
				except:
					pass

# --------------------------------------------------------
# Thread class listening the server messages
# --------------------------------------------------------

class ListenServer(Thread):
	"""
	Thread listening the Server in order to get new maps and messages. 
	
	Args:
		socket (socket object) : socket connected to the server.

	"""
	def __init__(self, socket):
		Thread.__init__(self)
		self.socket = socket

	def run(self):
		global client_is_on
		while client_is_on == True:
			try:
				msg_received = self.socket.recv(1024).decode() # Receipt the message

				if msg_received != "": # Or else if the message is not empty
					msg_received = msg_received.split("MSG:") # Split messages
					for m_received in msg_received:

						# --------------------------------------------------
						# Map to display
						# --------------------------------------------------
						if (m_received[0:4] == "MAP:"):
							os.system('cls' if os.name == 'nt' else "printf '\033c'")
							print(m_received[4:])

						# --------------------------------------------------
						# Information to display
						# --------------------------------------------------
						elif (m_received[0:4] == "INF:"):
							print(m_received[4:])

						# --------------------------------------------------
						# The server tell us we have to quit, snif snif :'(
						# --------------------------------------------------
						elif (m_received == "Q"):
							stop_client(self.socket)
			except:
				pass

# --------------------------------------------------------
# Function launching the client and making the connexion
# --------------------------------------------------------

def launch_client(host, port):
	"""
	Launch the client application.

	Args:
		host (str) : the host of the server.
		port (int) : the port of the server.

	"""

	print("Trying to connect...")
	try:
		my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # New socket, IPV4 / TCP
		my_socket.connect((host, port))

	except ConnectionRefusedError:
		print("Erreur - Connexion refusée. Veuillez vous assurer que le serveur est lancé.")

	else:

		print("Connexion établie avec le serveur sur le port {0:}.".format(port))

		# Create the threads
		listen_client = ListenClient(my_socket)
		listen_server = ListenServer(my_socket)

		# Launch the threads
		listen_client.start()
		listen_server.start()

		# Join the threads
		listen_client.join()
		listen_server.join()

# --------------------------------------------------------
# Stop the client
# --------------------------------------------------------

def stop_client(socket):
	"""
	Stop the client and close the socket.

	Args:
		socket (socket) : The socket connected to the Server.

	"""

	global client_is_on

	with my_lock: # Prevent two closings at the same time
		if (client_is_on == True):
			client_is_on = False # Close the game in local
			socket.send("Q".encode())
			socket.close() # Close connexion
			print("\nLa partie est terminée. Appuyez sur n'importe quelle touche pour quitter.")