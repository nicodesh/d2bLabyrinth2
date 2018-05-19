# -*-coding:Utf-8 -*

""" Server of Roboc Game. You have to execute this file to launch the server. """

from server.rserver import *


# ----------------------------------------------------------
# Choose the Map !
# ----------------------------------------------------------

the_map = False # No map so far

# The admin has to choose a maze to launch a new map.
the_maze = choose_the_maze()
the_map = RobocMap(the_maze)
print("Max of robots: {}".format(the_map.free_space))

# ----------------------------------------------------------
# Launch the server
# ----------------------------------------------------------

launch_server('', 12800, the_map)

# ----------------------------------------------------------
# The game is over
# ----------------------------------------------------------

print("\n")
print("La partie est terminée, le serveur a été clôturé. ")