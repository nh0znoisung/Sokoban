import pygame
import time
from pygame.locals import *
import os
import psutil

successes, failures = pygame.init()
print("{0} successes and {1} failures".format(successes, failures))

# SOKOBAN solver

# screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
FPS = 60  # Frames per second.

WIDTH = 700
HEIGHT = 1100

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY_LIGHT = (231,231,231)
ORANGE = '#ff631c'
BLUE_LIGHT = (40, 53, 88) # menu
RED = (255,0,0) # end
BLUE = (0, 0, 255) #line
YELLOW = (255, 255, 0) # title
YELLOW_LIGHT = (255,255,51)
BROWN = (210,105,30)
PINK = (204, 0, 255) # start
GREEN_LIGHT = (0, 255, 140) # node
GREEN = (0, 255, 0)
GREEN_DARK = (0, 255, 0)
# RED = (255, 0, 0), , BLUE = (0, 0, 255).

menuFont = pygame.font.SysFont("CopperPlate Gothic", 60, bold = True)  
helpFont = pygame.font.SysFont("Comic Sans MS", 25)      
wordFont = pygame.font.SysFont("CopperPlate Gothic",25)  
mapFont = pygame.font.SysFont("Comic Sans MS", 20, bold = True)   
levelFont = pygame.font.SysFont("Comic Sans MS", 25, bold = True)  
buttonFont = pygame.font.SysFont("CopperPlate Gothic", 18, bold = True)
# statusFont = pygame.font.SysFont("CopperPlate Gothic",25)    


pygame.display.set_caption("Sokoban Solver")
surface = pygame.display.set_mode((HEIGHT,WIDTH))

numsRow = 8 #maybe change
numsCol = 8 

numsUnit = max(numsCol, numsRow)
lengthSquare = int(WIDTH/numsUnit)

offsetX = lengthSquare * (numsUnit - numsCol)/2 
offsetY = lengthSquare * (numsUnit - numsRow)/2 




background = pygame.image.load("Items/background.jpg")
background = pygame.transform.scale(background, (WIDTH, WIDTH))

wall = pygame.image.load('Items/wall.png')
wall = pygame.transform.scale(wall, (lengthSquare, lengthSquare))

box = pygame.image.load('Items/box.png')
box = pygame.transform.scale(box, (lengthSquare, lengthSquare))

goal = pygame.image.load('Items/goal.png')
goal = pygame.transform.scale(goal, (lengthSquare, lengthSquare))

player = pygame.image.load('Items/player.png')
player = pygame.transform.scale(player, (lengthSquare, lengthSquare))

up_arrow = pygame.image.load("Items/up_arrow.png")
up_arrow = pygame.transform.scale(up_arrow, (20, 20))

down_arrow = pygame.image.load("Items/down_arrow.png")
down_arrow = pygame.transform.scale(down_arrow, (20, 20))

pick_button = pygame.image.load("Items/choose.png")
pick_button = pygame.transform.scale(pick_button, (98, 41))

change = pygame.image.load("Items/change.png")
change = pygame.transform.scale(change, (32, 32))

visualize_button = pygame.image.load("Items/visualizebutton.png")
# visualize_button = pygame.transform.scale(visualize_button, (98, 41))

restart_button = pygame.image.load("Items/restart.png")
restart_button = pygame.transform.scale(restart_button, (105, 40))

undo_button = pygame.image.load("Items/undo.png")
undo_button = pygame.transform.scale(undo_button, (35, 35))

redo_button = pygame.image.load("Items/redo.png")
redo_button = pygame.transform.scale(redo_button, (35, 35))



up_arrow_rect = Rect(600 + 245, 0 + 200, 20, 20)
down_arrow_rect = Rect(600 + 245, 0 + 220, 20, 20)
change_rect = Rect(600 + 367, 0 + 155, 32, 32)
pick_rect = Rect(600 + 400, 0 + 178, 98, 41)
self_rect = Rect(700 + 40, 305, 110, 48)
bfs_rect = Rect(700 + 165, 305, 95, 48)
A_rect = Rect(700 + 275, 305, 95, 48)
restart_rect = Rect(700 + 160, 0 + 410, 105, 40)
visualize_rect = Rect(700 + 135, 0 + 650, 161, 34)
undo_rect = Rect(700 + 90, 0 + 410, 50, 40)
redo_rect = Rect(700 + 285, 0 + 410, 50, 40)

def display_title():
    menuText = menuFont.render("SOKOBAN", True, ORANGE)
    surface.blit(menuText, [700 + 35, 0 + 20])

def display_background():
	surface.blit(background, [0, 0])

def display_title_step_1(color = RED):
	step1Text = helpFont.render("1. Choose your round", True, color)
	surface.blit(step1Text, [700 + 10, 0 + 105])

def display_up_arrow():
	surface.blit(up_arrow, [600 + 245, 0 + 200])

def display_down_arrow():
	surface.blit(down_arrow, [600 + 245, 0 + 220])

def display_change():
	surface.blit(change, [600 + 367, 0 + 155])

def display_pick_button():
	surface.blit(pick_button, [600 + 400, 0 + 178])

def display_title_content_1(color = BROWN):
	statusText = helpFont.render("Map:", True, color)
	attemptedText = helpFont.render("Level:", True, color)
	surface.blit(statusText, [700 + 30, 0 + 152])
	surface.blit(attemptedText, [700 + 30, 0 + 200])

def display_map(color = GRAY_LIGHT):
	mapText = mapFont.render(f"{map_list[map_index]}", True, color)
	surface.blit(mapText, [700 + 95, 0 + 155])

def check_one_digit(n):
	if len(str(n)) == 1:
		return True
	return False

def display_level(color = GRAY_LIGHT):
	# Check if 2 digits
	levelText = levelFont.render(f"{level + 1}", True, color)
	if check_one_digit(level):
		surface.blit(levelText, [700 + 115, 0 + 200])
	else:
		surface.blit(levelText, [700 + 105, 0 + 200])


def display_help():
	helpText = levelFont.render("(1-40)", True, BROWN)
	surface.blit(helpText, [700 + 185, 0 + 200])





def display_title_step_2(color = RED):
	step2Text = helpFont.render("2. Choose your gameplay", True, color)
	surface.blit(step2Text, [700 + 10, 0 + 252])


def display_button_self():
	pygame.draw.rect(surface, BLACK, pygame.Rect(700 + 40, 305, 110, 48),  0, 6)
	step7Text = buttonFont.render("Manually", True, GREEN)
	surface.blit(step7Text, [700 + 45, 318])

def display_button_BFS():
	pygame.draw.rect(surface, BLACK, pygame.Rect(700 + 165, 305, 95, 48),  0, 6)
	step7Text = buttonFont.render("BFS", True, PINK)
	surface.blit(step7Text, [700 + 190, 318])

def display_button_A():
	pygame.draw.rect(surface, BLACK, pygame.Rect(700 + 275, 305, 95, 48),  0, 6)
	step7Text = buttonFont.render("A*", True, YELLOW_LIGHT)
	surface.blit(step7Text, [700 + 313, 318])




def display_title_step_3(color = RED):
	step3Text = helpFont.render("3. Happy Hacking!!!", True, color)
	surface.blit(step3Text, [700 + 10, 0 + 365])

def display_title_content_step_3(color = BROWN):
	statusText = helpFont.render("Status:", True, color)
	attemptedText = helpFont.render("Time:", True, color)
	stepText = helpFont.render("Step:", True, color)
	pushedText = helpFont.render("Pushed:", True, color)
	surface.blit(statusText, [700 + 26, 0 + 455])
	surface.blit(attemptedText, [700 + 30, 0 + 503])
	surface.blit(stepText, [700 + 30, 0 + 550])
	surface.blit(pushedText, [700 + 30, 0 + 600])


def display_content_step_3():
	status_str = ""
	if win == -1:
		status_str = ""
		status_col = YELLOW
	if win == 0:
		status_str = "Solving . . ."
		status_col = (255,255,51)
	elif win == 2:
		status_str = "No solution"
		status_col = RED
	elif win == 1:
		status_str = "Win !!@@!!"
		status_col = GREEN_DARK

	statusText = wordFont.render(f"{status_str}", True, status_col)
	timeText = helpFont.render("{:0.3f} s".format(timeTook), True, GREEN_LIGHT)
	stepText = helpFont.render(f"{stepNode}", True, GREEN_LIGHT)
	pushedText = helpFont.render(f"{pushed}", True, GREEN_LIGHT)

	surface.blit(statusText, [700 + 127, 0 + 458])
	surface.blit(timeText, [700 + 110, 0 + 503])
	surface.blit(stepText, [700 + 135, 0 + 550])
	surface.blit(pushedText, [700 + 135, 0 + 600])


def display_restart():
	surface.blit(restart_button, [700 + 160, 0 + 410])

def display_visualize():
	print("asdf")
	surface.blit(visualize_button, [700 + 135, 0 + 650])

def display_undo():
	pygame.draw.rect(surface, RED, pygame.Rect(700 + 90, 0 + 410, 50, 40),  0, 20)
	surface.blit(undo_button, [700 + 95, 0 + 410])

def display_redo():
	pygame.draw.rect(surface, RED, pygame.Rect(700 + 285, 0 + 410, 50, 40),  0, 20)
	surface.blit(redo_button, [700 + 292, 0 + 410])

def display_step_1(col = RED, mode = -1):
	display_title_step_1(color = col)
	if mode == -1:
		display_up_arrow()
		display_down_arrow()
		display_change()
		display_pick_button()
		display_title_content_1()
		display_map()
		display_level()
		display_help()
	else:
		display_title_content_1()
		display_map(RED)
		display_level(RED)

def display_step_2(col = RED, mode = 0):
	display_title_step_2(color = col)
	if mode == 0:
		display_button_self()
		display_button_BFS()
		display_button_A()
	elif mode == 1:
		display_button_self()
	elif mode == 2:
		display_button_BFS()
	elif mode == 3:
		display_button_A()


def display_step_3(col = RED, mode = 0):
	display_title_step_3(color = col)
	# display_visualize()
	# print(mode)
	if mode == 2 or mode == 3:
		display_visualize()		
		display_undo()
		display_redo()
		display_restart()
		display_title_content_step_3()
		display_content_step_3()
	if mode == 1:
		display_undo()
		display_redo()
		display_restart()
		display_title_content_step_3()
		display_content_step_3()

	
# status = 0, time = 0, step = 0, pushed = 0
def draw_menu():
	pygame.draw.rect(surface, BLUE_LIGHT, [700, 0, 1050, 700])

	display_background()
	if step == 1:
		display_step_1(YELLOW, -1)
		display_step_2(mode = -1)
		display_step_3()
	elif step == 2:
		display_step_1(GREEN_DARK, 0)
		display_step_2(YELLOW, mode = 0)
		display_step_3()
	elif step == 3:
		if win == 0:
			display_step_1(GREEN_DARK, 0)
			# print(mode)
			display_step_2(GREEN_DARK, mode = mode)
			display_step_3(YELLOW, mode = mode)
		else:
			display_step_1(GREEN_DARK, 0)
			display_step_2(GREEN_DARK, mode = mode)
			display_step_3(GREEN_DARK, mode = mode)
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


# filename = ""
board = Board()
# board.set_value(filename)

# Goal + player = (-)
# Goal + box = (+)
# win = True



def reset_data():
	global board, numsCol, numsRow, numsUnit, lengthSquare, offsetX, offsetY, wall, box, goal, player
	
	wall = pygame.image.load('Items/wall.png')
	box = pygame.image.load('Items/box.png')
	goal = pygame.image.load('Items/goal.png')
	player = pygame.image.load('Items/player.png')
	numsRow, numsCol = board.set_value("./Testcases/{}/{}.txt".format(map_list[map_index], level+1))

	numsUnit = max(numsCol, numsRow)
	lengthSquare = int(WIDTH/numsUnit)

	print(numsCol, numsRow, numsUnit) #Debug

	offsetX = lengthSquare * (numsUnit - numsRow)/2 
	offsetY = lengthSquare * (numsUnit - numsCol)/2 

	wall = pygame.transform.scale(wall, (lengthSquare, lengthSquare))
	box = pygame.transform.scale(box, (lengthSquare, lengthSquare))
	goal = pygame.transform.scale(goal, (lengthSquare, lengthSquare))
	player = pygame.transform.scale(player, (lengthSquare, lengthSquare))

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



# How to calculate the time and space complexity
# Find max of length width and height: Hope 12x12
# width and height of box (50x50), default: (16x16)


# 

# how to center it
map_list = ['MINI COSMOS', 'MICRO COSMOS']
map_index = 0
level = 0

reset_data()
# reset_data("./Testcases/Mini Cosmos/6.txt")

def init_data():
	global move, win, step, timeTook, pushed, startTime, stepNode, map_index, level, board, numsRow, numsCol, numsUnit, lengthSquare, offsetX, offsetY
	mode = 0
	win = 0
	step = 1
	timeTook = 0
	pushed = 0
	startTime = 0
	stepNode = 0

	# map_index = 0
	# level = 0
	# board = Board()
	# 
	board.clear_value()
	reset_data()


def draw_board(board):
	draw_menu()

	for point in board.walls:
		surface.blit(wall, [offsetX + lengthSquare * point.x, offsetY + lengthSquare * point.y])
	
	for point in board.paths:
		pygame.draw.rect(surface, WHITE, [offsetX + lengthSquare * point.x, offsetY + lengthSquare * point.y, lengthSquare, lengthSquare])

	

	for point in board.goals:
		surface.blit(goal, [offsetX + lengthSquare * point.x, offsetY + lengthSquare * point.y])

	point = board.player
	surface.blit(player, [offsetX + lengthSquare * point.x, offsetY + lengthSquare * point.y])

	for point in board.boxes:
		surface.blit(box, [offsetX + lengthSquare * point.x, offsetY + lengthSquare * point.y])

	display_title()

	pygame.display.flip()


mode = 0
win = 0
step = 1
timeTook = 0
pushed = 0
startTime = 0
stepNode = 0



def main():
	global board, level, map_index, step, mode, win, stepNode, timeTook, startTime, pushed
	while True:
		clock.tick(FPS)
		print(len(board.history_moves))
		if board.is_win() == True:
			win = 1
		if win == 0:
			timeTook = time.time() - startTime
		for event in pygame.event.get():
			keys_pressed = pygame.key.get_pressed()
			if event.type == pygame.QUIT or keys_pressed[pygame.K_q]:
				pygame.quit()



			if event.type == pygame.KEYDOWN:
				if step == 3:
					if mode == 1 and win == 0:
						if event.key == pygame.K_w or event.key == pygame.K_UP:
							board.move(U)
							stepNode = board.step
							pushed = board.pushed
						elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
							board.move(D)
							stepNode = board.step
							pushed = board.pushed
						elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
							board.move(L)
							stepNode = board.step
							pushed = board.pushed
						elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
							board.move(R)
							stepNode = board.step
							pushed = board.pushed

			if event.type == pygame.MOUSEBUTTONDOWN:
				x, y = event.pos

				if step == 1:
					if up_arrow_rect.collidepoint(x, y):
						level = (level + 1)%40
						reset_data()
					if down_arrow_rect.collidepoint(x,y):
						level = (level+39)%40
						reset_data()
					if change_rect.collidepoint(x,y):
						map_index = 1 - map_index
						reset_data()
					if pick_rect.collidepoint(x,y):
						step = 2

				if step == 2:
					if self_rect.collidepoint(x,y):
						mode = 1
						step = 3
						startTime = time.time()
					if bfs_rect.collidepoint(x,y): 
						mode = 2
						step = 3
						# bfs(board) => Change global win into 1, board = goal_board with new_board
						# stepNode = board.step
						# pushed = board.pushed
						startTime = time.time()
					if A_rect.collidepoint(x,y):
						mode = 3
						step = 3
						startTime = time.time()
						# a_star(board)

				if step == 3:
					if restart_rect.collidepoint(x,y):
						init_data()
						step = 1
					if undo_rect.collidepoint(x,y):
						board.undo()
						stepNode = board.step
						pushed = board.pushed	
					if redo_rect.collidepoint(x,y):
						board.redo()
						stepNode = board.step
						pushed = board.pushed
					if mode > 1:
						if visualize_rect.collidepoint(x,y):
							continue

		draw_board(board)
		pygame.display.update()

if __name__ == '__main__':
	main()