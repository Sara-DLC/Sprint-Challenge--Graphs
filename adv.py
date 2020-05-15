from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# DFT to find all paths and reverse back
# BFT to find shortest paths
# Memoization/recursion to store already visited paths?
# List all potential paths and return the index of the list using index method


def reversed_path(directions):
    # if no directions are there return nothing
    if directions is None:
        return None
    # List all potential path cardinal directions
    potential_path = ["n", "e", "s", "w"]
    # return index of the path
    return potential_path[(potential_path.index(directions) + 2) % 4]


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)


'''
Keep a list of prev, possible, and max path traversal
append to the previous path, the current room the player is in and wait for input
while the length of the previous path is 0 add that vertex to the previous path list
if the vertex(room) id is not in the possible path list add it to our list
is the last path is not none add the room id to the last path
if the length of the possible path is the same of the length of the graph break out of the loop
do a check if room exists, if it does and the room id is not in our list add it to our possible path
if the length of our exists is 0, randomize direction, get the room it's pointing to, the possible path direction, save and add the previous path, and the traversal path direction
otherwise add the traversal path as the last path and pop it off.
'''
previous_path = []
possible_path = {}

previous_path.append((player.current_room, None, None, 0))

while len(previous_path) > 0:
    node = previous_path[-1]
    room = node[0]
    last_path = node[1]

    if room.id not in possible_path:
        possible_path[room.id] = set()

    if last_path is not None:
        possible_path[room.id].add(last_path)

    if len(possible_path) == len(room_graph):
        break

    room_exists = room.get_exits()
    possible_exists = [
        i for i in room_exists if i not in possible_path[room.id]]

    if len(possible_exists) > 0:

        direction = random.choice(possible_exists)
        room_to = room.get_room_in_direction(direction)
        possible_path[room.id].add(direction)
        previous_path.append((room_to, reversed_path(direction)))
        traversal_path.append(direction)
    else:
        traversal_path.append(last_path)
        previous_path.pop(-1)


for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
