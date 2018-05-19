# -*-coding:Utf-8 -*

""" Client of Roboc Game. You have to execute this file with python3 to play. """

from client.rclient import *

print("Bienvenue sur l'application Roboc !")
launch_client("localhost", 12800) # Launch a party in local. The port has to be the same as the Roboc Server.