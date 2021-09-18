

from main import check_one_digit
from os import truncate
from queue import Queue
from copy import copy, deepcopy
from time import time

class MyQueue:

    '''
    Custom FIFO queue that keeps track of a queue in a list
    '''

    def __init__(self):
        self.q = []

    def push(self, x):
        ''' inserts at the beginning of the list '''
        self.q.insert(0, x)

    def pop(self):
        ''' removes the first item in the list '''
        return self.q.pop(0)

    def isEmpty(self):
        ''' checks for empty list '''
        if len(self.q) == 0:
            return True

    def __len__(self):
        ''' overriding len() '''
        return len(self.q)



class Point:
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

    # 
    # def __hash__(self):
    #     return hash((self.x, self.y))
    

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
		print("(" + str(self.x) + "," + str(self.y) + ")")
    
class Direction:
	'''
	vector: we can define it as object of class Point that we have define above, so that we can add 2 Point or double it for checking
	char: in character, that we can print or add the 
	'''
	def __init__(self, vector, char):
		self.vector = vector
		self.char = char

	def get_char(self):
		return self.char

class Move:
	def __init__(self, direction, pushed):
		self.direction = direction # a object of class Direction
		self.pushed = pushed # boolean value for pushed or not

# We set the coordinate from top-left corner and x-axis and y-axis is default
L = Direction(Point(-1, 0), 'L') # a point or vector and a character that represent for each direction
R = Direction(Point(1, 0), 'R')
U = Direction(Point(0, -1), 'U')
D = Direction(Point(0, 1), 'D')
directions = [U, D, L, R]

class Board:
	# Use what DataStructure for saving wall, goal, box, player
	# Set for finding and adding operator with time complexity O(logn), with already function such as union(), issubset(),..
	def __init__(self):
		# self.dir_list = dir_list  # list of directions for solution
		self.name = ''
		self.history_moves = [] # List of tuple (Direction, Boolean), Bool for saving we pushed the boxes or not
		self.available_moves = []
		self.walls = set() # Consider set or 2d-array for time and space-complexity and since the fixed property
		self.goals = set()
		self.boxes = set()
		self.paths = set()
		self.player = None
		self.step = 0
		self.pushed = 0
		self.ptr = -1
		self.x = -1
		self.y = -1
		self.ptr = 0
		self.cost = 1e9  # used for heuristic search: A* algorithm
		# set_available_moves()

	def clear_value(self):
		self.name = ''
		self.history_moves = [] # List of tuple (Direction, Boolean), Bool for saving we pushed the boxes or not
		self.available_moves = []
		self.walls = set() # Consider set or 2d-array for time and space-complexity and since the fixed property
		self.goals = set()
		self.boxes = set()
		self.paths = set()
		self.player = None
		self.step = 0
		self.pushed = 0
		self.ptr = -1
		self.x = -1
		self.y = -1
		self.ptr = 0
		self.cost = 1e9  # used for heuristic search: A* algorithm

	def __eq__(self, other):
		return (self.walls == other.walls) and (self.goals == other.goals) and (self.boxes == other.boxes) and (self.player == other.player)

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

	def direction_in_available(self,m):
		for i in self.available_moves:
			if (i.get_char() == m.get_char()): return True
		return False
	

	# Rule for moving in SOKOBAN map, the rules below will apply for 4 directions: UP, DOWN, LEFT, RIGHT
	# Rule 1: If the forward cell is empty, we literally can move
	# Rule 2: If the forward cell has a wall, we can not move
	# Rule 3: If the forward cell has a box:
		# Rule 3.1: If the forward of forward cell has a box or a wall, we can not move 
		# Rule 3.2: If the forward of forward cell not contains a box or a wall, we can move forward and push the box forward 

	# Only use this function if we have 
	def set_available_moves(self): 
		# return a list a legal move up to date which is a subset of directions list (<= 4 elements)
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


	# --- We think about this not just for solving a game, we can play it by control the keyboard. So if when we have illegal move, just cost O(logn)
	


	def move(self, direction):
		# print("adfbaksd
		# self.player.x += 1
		# print(direction.vector.x)
		# move the player with direction but the argument make sure direction in the available_moves() 
		if (self.direction_in_available(direction)):
			self.ptr += 1
			if self.ptr < len(self.history_moves):
				# Cut the list
				self.history_moves = self.history_moves[0:self.ptr]
			temp = self.player + direction.vector
			self.step += 1
			if temp in self.boxes:
				# We push the box forward, so we need to remove the current position and add the forward position
				self.pushed += 1
				self.boxes.remove(temp)
				self.boxes.add(temp + direction.vector)
				self.history_moves.append(Move(direction, 1))
			else:
				self.history_moves.append(Move(direction, 0))

			self.player = temp
		self.set_available_moves()


	def undo(self):
		if self.ptr > 0:
			self.ptr -= 1
			move = self.history_moves[self.ptr]
			if move.pushed == 1:
				self.pushed -= 1
				self.boxes.remove(self.player + move.direction.vector)
				self.boxes.add(self.player)

			self.player = self.player - move.direction.vector
			self.step -= 1
			# self.history_moves.pop()
		self.set_available_moves()


	def redo(self):
		if self.ptr < len(self.history_moves):
			self.move(self.history_moves[self.ptr])
			self.ptr += 1

	# def dfs(): => In same class or more function ?? 
	# def a_star():


	def is_win(self):
		if self.goals.issubset(self.boxes):
			return True
		else:
			return False

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
					elif char == '-':
						self.add_goal(x,y)
						self.add_player(x,y)
						self.add_path(x,y)
					elif char == '+':
						self.add_goal(x,y)
						self.add_box(x,y)
						self.add_path(x,y)
					elif char == '.': # Path - avaiable move
						self.add_path(x,y)
				
					x += 1
				y += 1
		self.set_available_moves()
		return (x,y)


board = Board()
board.set_value("test_1.txt")


def print_results(board, gen, rep, fre, expl, dur):
	print("1. Breadth first search:")
	print("Sequence: ",end="")
	for ch in board.history_moves:
		print(ch.direction.char,end=" ")
	print()
	print(len(board.history_moves))
	print('Duration: ' + str(dur) + 'secs')

def equalSet(child,explored):
	for ele in explored:
		if (child.__eq__(ele)): return True
	return False

def print_player(node):
	node.player.get_point()

def print_box(node):
	for i in node.boxes:
		i.get_point()
		print(" ",end = '')


def print_status(node):
	for m in node.available_moves:
		print(m.get_char(),end=" ")
	print()
	print("Position of player",end = "")
	print_player(node)
	print("Position of box", end="")
	print_box(node)
	print()



# implementation of BFS
# is_win(): Check goal state
# move(L,R,U,D): Choices for moving
# board.available_moves: Create a list of available_moves
# OUTPUT:-> print() to a file named result.txt
def bfs(board):
	start = time()
	
	if (board.is_win()):
		end = time()
		print_results(board,1,0,0,0,end-start)
		return 
	frontier = MyQueue()
	explored = set()
	frontier.push(board)
	stayed_Searching = True

	i = 0
	while stayed_Searching:
		if (i == 18): 
			print("Debug session")
		i = i + 1
		if frontier.isEmpty():
			print("Solution not found\n")
			print(i)
			return
		print("Start loop " + str(i) + " at node: ",end="")
		
		node = frontier.pop()
		moves = node.available_moves
		explored.add(node)

		print_status(node)

		print("child from loop " + str(i))
		for m in moves:
			child = deepcopy(node)
			child.move(m)
			if (child not in explored): #(child not in frontier):
				if (child.is_win()):
					end = time()
					print_results(child,0,0,0,0,end-start)	
					return child
				frontier.push(child)
				print_status(child)
		print()
	print(i)

				

bfs(board)



