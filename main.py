import pygame
import os
import psutil

successes, failures = pygame.init()
print("{0} successes and {1} failures".format(successes, failures))

# SOKOBAN solver

# screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
FPS = 60  # Frames per second.

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY_LIGHT = (231,231,231)
# RED = (255, 0, 0), GREEN = (0, 255, 0), BLUE = (0, 0, 255).




pygame.display.set_caption("Sokoban Solver")
surface = pygame.display.set_mode((600,600))

board = []

# How to calculate the time and space complexity
# Find max of length width and height: Hope 12x12
# width and height of box (50x50), default: (16x16)

numsRow = 8 #maybe change
numsCol = 8

numsUnit = max(numsCol, numsRow)

lengthSquare = int(600/numsUnit)

# offset

background = pygame.image.load("Items/background.jpg")
background = pygame.transform.scale(background, (600, 600))

wall = pygame.image.load('Items/wall.png')
wall = pygame.transform.scale(wall, (lengthSquare, lengthSquare))

box = pygame.image.load('Items/box.png')
box = pygame.transform.scale(box, (lengthSquare, lengthSquare))

goal = pygame.image.load('Items/goal.png')
goal = pygame.transform.scale(goal, (lengthSquare, lengthSquare))

player = pygame.image.load('Items/player.png')
player = pygame.transform.scale(player, (lengthSquare, lengthSquare))

def display_background():
	surface.blit(background, [0, 0])

# We want to dogde many if else as much as possible because it will cause more errors when coding.
# -> So we can assume that L,R,U,D as a Point (+-1, 0), (0, +-1)

# We can use a tuple with 2 variable (x,y) as coordinate of graph but it still need some way to interact with other points

# We create a Data Structure of each point, bacause we need some interaction between point to point such as add 2 point for moving left current point + (0,-1), double point for checking avaiable move, equation for set checking duplicate

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
		self.history_moves = [] # List of tuple (Direction, Boolean), Bool for saving we pushed the boxes or not
		self.available_moves = []
		self.walls = set() # Consider set or 2d-array for time and space-complexity and since the fixed property
		self.goals = set()
		self.boxes = set()
		self.paths = set()
		self.player = None
		self.cost = 1e9  # used for heuristic search: A* algorithm
		# set_available_moves()

	def clear_value(self):
		self.walls.clear()
		self.goals.clear()
		self.boxes.clear()
		self.paths.clear()
		self.player = None
		self.cost = 1e9

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
		if direction in self.available_moves:
			temp = self.player + direction.vector
			if temp in self.boxes:
				# We push the box forward, so we need to remove the current position and add the forward position
				self.boxes.remove(temp)
				self.boxes.add(temp + direction.vector)
				self.history_moves.append(Move(direction, 1))
			else:
				self.history_moves.append(Move(direction, 0))

			self.player = temp
		self.set_available_moves()


	def undo(self, direction):
		if len(history_moves) > 0:
			move = history_moves[-1]
			if move.pushed == 1:
				self.boxes.remove(self.player + direction)
				self.boxes.add(self.player)

			self.player = self.player - direction
			history_moves.pop()
		self.set_available_moves()

	# def dfs(): => In same class or more function ?? 
	# def a_star():

	

	def is_win(self):
		if self.goals.issubset(self.boxes):
			return True
		else:
			return False

	def set_value(self, filename):
		with open(filename, 'r') as f:
			read_data = f.read()
			lines = read_data.split('\n')
			x = 0
			y = 0
			for line in lines:
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
					elif char == '.': # Path - avaiable move
						self.add_path(x,y)
				
					x += 1
				x = 0
				y += 1

		self.set_available_moves()

# We need a DS can have more Direction
# Point = (x,y), simple add, print, double, __eq__
#  Direction = ((x,y), 'char') 

# Move_available = directions = [U,D,L,R]

# add filename
#do not convert it into number, just character to set

# We have 2 options: use matrix for saving, hash table with Time: O(1), Space: O(n*m), => Hard to control overlap position: player vs goal and box vs goal
# or using Set for hash Time: O(logn), Space(m*n)

# Fixed: background + wall + path + goal 
# Variable: player + box + (goal + box) => Use flag

# state = set(), used for check duplicate with O(logn)

board = Board()
board.set_value("test_2.txt")

# how to center it

def draw_board(board):

	display_background()
	

	for point in board.walls:
		surface.blit(wall, [lengthSquare * point.x, lengthSquare * point.y])
	
	for point in board.paths:
		pygame.draw.rect(surface, WHITE, [lengthSquare * point.x, lengthSquare * point.y, lengthSquare, lengthSquare])

	

	for point in board.goals:
		surface.blit(goal, [lengthSquare * point.x, lengthSquare * point.y])

	point = board.player
	surface.blit(player, [lengthSquare * point.x, lengthSquare * point.y])

	for point in board.boxes:
		surface.blit(box, [lengthSquare * point.x, lengthSquare * point.y])

	# print()
	# i = 1
	# j = 1
	# pygame.draw.rect(surface, GRAY_LIGHT, [lengthSquare * i, lengthSquare * j, lengthSquare, lengthSquare])

				
	# i = 0
	# j = 2
	
	
	pygame.display.flip()


def main():
	global board
	while True:
		clock.tick(FPS)

		for event in pygame.event.get():
			keys_pressed = pygame.key.get_pressed()
			if event.type == pygame.QUIT or keys_pressed[pygame.K_q]:
				pygame.quit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_w or event.key == pygame.K_UP:
					board.move(U)
				elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
					print("adfasd")
					board.move(D)
				elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
					board.move(L)
				elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
					board.move(R)

		draw_board(board)

		pygame.display.update()

if __name__ == '__main__':
	main()