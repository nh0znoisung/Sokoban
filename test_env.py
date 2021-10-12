import time
import os
import psutil
from queue import Queue
from copy import copy, deepcopy
from datetime import datetime
import math
from sortedcontainers import SortedList
import numpy as np
from scipy.optimize import linear_sum_assignment
import pandas as pd


class Point:
	'''
	(self.x, self.y): works as a coordinate on board 
	=> It works like a tuple (x,y) but more extended with some function to interact with other Points such as add, double, subtract,...
	'''
	def __init__(self):
		self.x = -1
		self.y = -1

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __eq__(self, point):
		if self.x == point.x and self.y == point.y:
			return True
		else:
			return False
	# Magic method: https://www.python-course.eu/python3_magic_methods.php
	def __add__(self, point):
		x = self.x + point.x
		y = self.y + point.y
		return Point(x, y)

	def __sub__(self, point):
		x = self.x - point.x
		y = self.y - point.y
		return Point(x, y)

	def double(self):
		return Point(self.x*2, self.y*2)

	# Error unhashable type
	def __key(self):
		return (self.x, self.y)

	def __hash__(self):
		return hash(self.__key())

	def get_point(self):
		print("(" + str(self.x) + "," + str(self.y) + ")", end = " ")
	
class Direction:
	'''
	vector: we can define it as object of class Point that we have define above, so that we can add 2 Point or double it for checking
	char: character represent for its direction, that we can print results
	=>  We want to dogde many if else as much as possible because it will cause more errors when coding.
	=>  Such as when we go Left, we just add current Point with Point(-1,0),...
	'''
	def __init__(self, vector, char):
		self.vector = vector
		self.char = char

	def get_char(self):
		return self.char

class Move:
	def __init__(self, direction, pushed):
		self.direction = direction # a object of class Direction
		self.pushed = pushed # boolean value for checking box is pushed or not

# We set the coordinate from top-left corner and x-axis and y-axis as default
L = Direction(Point(-1, 0), 'L')
R = Direction(Point(1, 0), 'R')
U = Direction(Point(0, -1), 'U')
D = Direction(Point(0, 1), 'D')
directions = [U, L, D, R] # clock-wise

class Board:
	# Use set() DataStructure for saving wall, goal, box, player
	# set() in Python is implemented as hashmap with finding and adding or deleting operator just cost time complexity O(1), in worst-case it still cost O(n) since hashing collision
	# set() is the same as 2d-array in time and space complexity, but it's convenient that it's support function such as union(), issubset(),..
	def __init__(self):
		self.name = ''
		self.history_moves = [] # List of tuple Move()
		self.available_moves = []
		self.walls = set() # set of Point()
		self.goals = set()
		self.boxes = set()
		self.paths = set()
		self.lose = -1
		self.player = None
		self.step = 0
		self.pushed = 0
		self.ptr = -1
		self.x = -1
		self.y = -1
		self.cost = 1e9  # used for heuristic search: A* algorithm
		self.distanceToGoal = dict() # Nested dictionary
		self.dead_squares = set()

	def clear_value(self):
		self.name = ''
		self.history_moves = []
		self.available_moves = []
		self.walls = set()
		self.goals = set()
		self.boxes = set()
		self.paths = set()
		self.lose = -1
		self.player = None
		self.step = 0
		self.pushed = 0
		self.ptr = -1
		self.x = -1
		self.y = -1
		self.cost = 1e9
		self.distanceToGoal = dict()
		self.dead_squares = set()

	def __eq__(self, other):
		return self.walls == other.walls and self.goals == other.goals and self.boxes == other.boxes and self.player == other.player

	def __key(self):
		return (self.name)

	def __hash__(self):
		return hash(self.__key())

	def add_wall(self, x, y):
		self.walls.add(Point(x,y))

	def add_goal(self, x, y):
		self.goals.add(Point(x,y))

	def add_box(self, x, y):
		self.boxes.add(Point(x,y))

	def add_path(self, x, y):
		self.paths.add(Point(x,y))

	def add_player(self, x, y):
		self.player = Point(x,y)

	def get_history_moves(self):
		return ", ".join(list(map(lambda move: move.direction.char, self.history_moves)))

	#$$ Rule for moving in SOKOBAN map, the rules below will apply for 4 directions: UP, DOWN, LEFT, RIGHT
	# Rule 1: If the forward cell is empty, we literally can move
	# Rule 2: If the forward cell has a wall, we can not move
	# Rule 3: If the forward cell has a box:
		# Rule 3.1: If the forward of forward cell has a box or a wall, we can not move 
		# Rule 3.2: If the forward of forward cell not contains a box or a wall, we can move forward and push the box forward 

	def set_available_moves(self): 
		# Setup attribute available_moves as a list storing legal moves up to date which is a subset of directions list (<= 4 elements)
		# Available moves <=> Rule 1 + Rule 3.2
		self.available_moves = []
		for direction in directions:
			if self.player + direction.vector not in self.walls:
				# forward cell can be a box or empty
				if self.player + direction.vector in self.boxes:
					# forward cell contains a box
					if self.player + direction.vector.double() not in self.walls.union(self.boxes):
						self.available_moves.append(direction)
				else:
					# forward cell is empty
					self.available_moves.append(direction)

	def direction_in_available(self, m):
		for i in self.available_moves:
			if (i.get_char() == m.get_char()):
				return True
		return False

	# Move the player with direction but the argument make sure direction in the available_moves 
	def move(self, direction, redo = False, move = True):	
		if (self.direction_in_available(direction)):
			self.ptr += 1
			if move == True:
				if self.ptr < len(self.history_moves):
					# Cut the list
					self.history_moves = self.history_moves[0:self.ptr]
				if self.ptr <= self.lose:
					self.lose = -1 
			temp = self.player + direction.vector
			
			self.step += 1
			if temp in self.boxes:
				# We push the box forward, so we need to remove the current position and add the forward position
				self.pushed += 1
				self.boxes.remove(temp)
				self.boxes.add(temp + direction.vector)
				if redo == False:
					self.history_moves.append(Move(direction, 1))

				# Check lose or not
				if self.lose == -1:
					curr_box = temp + direction.vector
					if curr_box in self.dead_squares:
						self.lose = self.ptr
			else:
				if redo == False:
					self.history_moves.append(Move(direction, 0))
			self.player = temp
		self.set_available_moves()
		self.minimum_cost()

	def undo(self):
		if self.ptr > -1:
			move = self.history_moves[self.ptr]
			if move.pushed == 1:
				self.pushed -= 1
				self.boxes.remove(self.player + move.direction.vector)
				self.boxes.add(self.player)

			self.player = self.player - move.direction.vector
			self.step -= 1
			self.ptr -= 1
		self.set_available_moves()
		self.minimum_cost()

	def redo(self):
		if self.ptr < len(self.history_moves) - 1:
			self.move(self.history_moves[self.ptr + 1].direction, redo = True, move = False)

	def is_lose(self):
		if self.lose != -1:
			if self.ptr >= self.lose:
				return True
		return False

	def is_win(self):
		if self.goals.issubset(self.boxes):
			return True
		else:
			return False

	def set_distance(self):
		for goal in self.goals:
			self.distanceToGoal[goal] = dict()
			for path in self.paths:
				self.distanceToGoal[goal][path] = math.inf
		queue = Queue()
		for goal in self.goals:
			self.distanceToGoal[goal][goal] = 0
			queue.put(goal)
			while not queue.empty():
				position = queue.get()
				for direction in directions:
					boxPosition = position + direction.vector
					playerPosition = position + direction.vector.double()
					if boxPosition in self.paths:
						if self.distanceToGoal[goal][boxPosition] == math.inf:
							if (boxPosition not in self.walls) and (playerPosition not in self.walls):
								self.distanceToGoal[goal][boxPosition] = self.distanceToGoal[goal][position] + 1
								queue.put(boxPosition)
		# Add dead squares
		for path in self.paths:
			ok = 1
			for goal in self.goals:	
				if self.distanceToGoal[goal][path] != math.inf:
					ok = 0
					break
			if ok == 1:
				self.dead_squares.add(path)

	def minimum_cost(self):
		# Minimum of matching all distances from all goals to all boxes (Assignment Problem) using Hungarian Algorithm
		temp = []
		for goal in self.goals:
			for box in self.boxes:
				## Using Manhattan distance
				# temp.append(abs(goal.x - box.x) + abs(goal.y - box.y)) 

				## Using DistanceToGoal 2d-array
				if self.distanceToGoal[goal][box] == math.inf:
					temp.append(1e9)
				else:
					temp.append(self.distanceToGoal[goal][box])

		arr = np.array(temp)
		# Make matrix with row is goal and colum is box
		cost = arr.reshape(len(self.goals), len(self.boxes))
		row_ind, col_ind = linear_sum_assignment(cost) # Hungarian Algorithm
		self.cost = cost[row_ind, col_ind].sum() + len(self.history_moves) # f(n) = g(n) + h(n)

	def set_value(self, filename):
		self.clear_value()
		self.name = filename
		x = 0
		y = 0
		with open(filename, 'r') as f:
			read_data = f.read()
			lines = read_data.split('\n')	
			for line in lines:
				x = 0
				for char in line:
					if char == '#': # Wall
						self.add_wall(x,y)
					elif char == 'x': # Box
						self.add_box(x,y)
						self.add_path(x,y)
					elif char == '?': # Goal
						self.add_goal(x,y)
						self.add_path(x,y)
					elif char == '@': # Player
						self.add_player(x,y)
						self.add_path(x,y)
					elif char == '-': # Player and Goal
						self.add_goal(x,y)
						self.add_player(x,y)
						self.add_path(x,y)
					elif char == '+': # Box and Goal
						self.add_goal(x,y)
						self.add_box(x,y)
						self.add_path(x,y)
					elif char == '.': # Path - avaiable move
						self.add_path(x,y)
					x += 1
				y += 1
		self.set_available_moves()
		self.set_distance()
		self.minimum_cost()
		return (x,y)


board = Board()
map_list = ['MINI COSMOS', 'MICRO COSMOS']

def main():
	i = -1
	if not os.path.exists("env.csv"):
		f = open("env.csv", 'w+')
		f.write("Map,Level,Boxes,Paths\n")
		f.close()
		i = 0
	else:
		# load file:
		f = open("env.csv", "r")
		contents = f.read()
		i = len(contents.split('\n')) - 2
		f.close()
	
	print("Loading from testcase {}".format(i+1))

	for j in range(i, 80):
		board.set_value("./Testcases/{}/{}.txt".format(map_list[int(j/40)], j%40+1))
		print("\nSolving testcase {}".format(j+1))
		(boxes,paths) = (len(board.boxes), len(board.paths))
		
		f = open("env.csv", 'a+')
		f.write("{},{},{},{}\n".format(map_list[int(j/40)], j%40+1, boxes, paths))
		f.close()

if __name__ == '__main__':
	main()
