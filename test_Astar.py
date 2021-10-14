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
		self.walls = set() # set of Point()
		self.goals = set()
		self.boxes = set()
		self.paths = set()
		self.lose = -1
		self.player = None
		self.step = 0
		self.distanceToGoal = dict() # Nested dictionary
		self.dead_squares = set()

	def clear_value(self):
		self.name = ''
		self.walls = set()
		self.goals = set()
		self.boxes = set()
		self.paths = set()
		self.lose = -1
		self.player = None
		self.step = 0
		self.distanceToGoal = dict()
		self.dead_squares = set()

	def __eq__(self, other):
		return self.boxes.issubset(other.boxes) and self.player == other.player

	def __key(self):
		return (self.name)

	def __hash__(self):
		return hash(self.__key())




	#$$ Rule for moving in SOKOBAN map, the rules below will apply for 4 directions: UP, DOWN, LEFT, RIGHT
	# Rule 1: If the forward cell is empty, we literally can move
	# Rule 2: If the forward cell has a wall, we can not move
	# Rule 3: If the forward cell has a box:
		# Rule 3.1: If the forward of forward cell has a box or a wall, we can not move 
		# Rule 3.2: If the forward of forward cell not contains a box or a wall, we can move forward and push the box forward 

	def set_available_moves(self): 
		# Setup attribute available_moves as a list storing legal moves up to date which is a subset of directions list (<= 4 elements)
		# Available moves <=> Rule 1 + Rule 3.2
		available_moves = set()
		for direction in directions:
			if self.player + direction.vector not in self.walls:
				# forward cell can be a box or empty
				if self.player + direction.vector in self.boxes:
					# forward cell contains a box
					if (self.player + direction.vector.double() not in self.walls) and (self.player + direction.vector.double() not in self.boxes):
						available_moves.add(direction)
				else:
					# forward cell is empty
					available_moves.add(direction)
		return available_moves

	# Move the player with direction but the argument make sure direction in the available_moves 
	def move(self, direction):	
		temp = self.player + direction.vector
		self.step += 1
		if temp in self.boxes:
			self.boxes.remove(temp)
			self.boxes.add(temp + direction.vector)
			
			if self.lose == -1:
				if (temp + direction.vector) in self.dead_squares:
					self.lose = 0
		
		self.player = temp
		

	def is_win(self):
		return self.goals.issubset(self.boxes)

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
		return cost[row_ind, col_ind].sum() + self.step # f(n) = g(n) + h(n)

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
		self.set_distance()
		return (x,y)


board = Board()

map_list = ['MINI COSMOS', 'MICRO COSMOS']
proc1 = psutil.Process(os.getpid())
itemMemory = proc1.memory_info().rss/(1024*1024)

def board_move(curr_board, direction):
	curr_board.move(direction)
	return curr_board

def bfs(curr_board):
	startTime = time.time()
	node_generated = 0
	node_repeated = 0

	frontier = Queue()
	explored = set()
	frontier.put(curr_board)
	stayed_Searching = True

	node_generated += 1
	explored.add(curr_board)
	i = 0
	while stayed_Searching:
		i = i + 1
		if time.time() - startTime > 600:
			return (0, 0, 0)
		if frontier.empty():
			print("Solution not found\n")
			return (0, 0, 0)
		node = frontier.get()
		moves = node.set_available_moves()

		for m in moves:
			child = deepcopy(node)
			child.move(m)
			if (child not in explored) and child.lose == -1:
				explored.add(child)
				if (child.is_win()):
					end = time.time() - startTime
					process = psutil.Process(os.getpid())
					memo_info = process.memory_info().rss/(1024*1024) - itemMemory
					return (child.step, end, memo_info)
				frontier.put(child)
			else:
				node_repeated += 1
			node_generated += 1



def A_star(curr_board):
	startTime = time.time()
	node_generated = 0
	node_repeated = 0

	frontier = SortedList(key=lambda board: board.minimum_cost())
	explored = set()
	frontier.add(curr_board)
	stayed_Searching = True

	node_generated += 1
	explored.add(board)
	i = 0
	while stayed_Searching:
		i = i + 1
		if time.time() - startTime > 600:
			return (0, 0, 0)
		if len(frontier) == 0:
			print("Solution not found\n")
			return (0, 0, 0)
		node = frontier.pop(0)
		moves = node.set_available_moves()

		for m in moves:
			child = deepcopy(node)
			child.move(m)
			if (child not in explored) and child.lose == -1:
				explored.add(child)
				if (child.is_win()):
					end = time.time() - startTime
					process = psutil.Process(os.getpid())
					memo_info = process.memory_info().rss/(1024*1024) - itemMemory
					return (child.step, end, memo_info)
				frontier.add(child)
			else:
				node_repeated += 1
			node_generated += 1


def main_BFS():
	i = -1
	if not os.path.exists("BFS.csv"):
		f = open("BFS.csv", 'w+')
		f.write("Map,Level,Algorithm,Status,Step,Time (s),Memory (MB)\n")
		f.close()
		i = 0
	else:
		# load file:
		f = open("BFS.csv", "r")
		contents = f.read()
		i = len(contents.split('\n')) - 2
		f.close()
	
	print("Loading BFS algorithm results from testcase {}".format(i+1))

	for j in range(i, 80):
		board.set_value("./Testcases/{}/{}.txt".format(map_list[int(j/40)], j%40+1))
		print("\nSolving testcase {}: ".format(j+1))
		(step, time, memo) = bfs(board)
		
		f = open("BFS.csv", 'a+')
		if step == 0:
			f.write("{},{},BFS,Time Limit Exceeded,???,???,??? \n".format(map_list[int(j/40)], j%40+1))
			print("Results testcase {}. Time Limit Exceeded.".format(j+1))
		else:
			f.write("{},{},BFS,Completed,{},{:0.3f},{:0.3f}\n".format(map_list[int(j/40)], j%40+1, step, time, memo))
			print("Results testcase {}. Completed, Step: {}, Time: {:0.3f} s, Memory: {:0.3f} MB\n".format(j+1, step, time, memo))
		f.close()

	print("\nSolving BFS algorithm results Completed")


def main_Astar():
	i = -1
	if not os.path.exists("A_star.csv"):
		f = open("A_star.csv", 'w+')
		f.write("Map,Level,Algorithm,Status,Step,Time (s),Memory (MB)\n")
		f.close()
		i = 0
	else:
		# load file:
		f = open("A_star.csv", "r")
		contents = f.read()
		i = len(contents.split('\n')) - 2
		f.close()
	
	print("Loading A-star algorithm results from testcase {}".format(i+1))

	for j in range(i, 80):
		board.set_value("./Testcases/{}/{}.txt".format(map_list[int(j/40)], j%40+1))
		print("\nSolving testcase {}: ".format(j+1))
		(step, time, memo) = A_star(board)
		
		f = open("A_star.csv", 'a+')
		if step == 0:
			f.write("{},{},A_star,Time Limit Exceeded,???,???,??? \n".format(map_list[int(j/40)], j%40+1))
			print("Results testcase {}. Time Limit Exceeded.".format(j+1))
		else:
			f.write("{},{},A_star,Completed,{},{:0.3f},{:0.3f}\n".format(map_list[int(j/40)], j%40+1, step, time, memo))
			print("Results testcase {}. Completed, Step: {}, Time: {:0.3f} s, Memory: {:0.3f} MB\n".format(j+1, step, time, memo))
		f.close()

	print("\nSolving A-star algorithm results Completed")

if __name__ == '__main__':
	main_Astar()