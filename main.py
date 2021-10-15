# **********************************************************************
#-----------------------------------------------------------------------
#*********************  WELCOME TO SOKOBAN SOLVER  *********************
#@@@@@  Authors: QUACH MINH TUAN - TO THANH PHONG - VO ANH NGUYEN  @@@@@
#-----------------------------------------------------------------------
# **********************************************************************


#-----------------
# Importing Modules
#-----------------
import pygame
import time
from pygame.locals import *
import os
import psutil
from queue import Queue
from copy import copy, deepcopy
from datetime import datetime
import math
from sortedcontainers import SortedList
import numpy as np
from scipy.optimize import linear_sum_assignment

#-----------------
# Setting Pygame
#-----------------
FPS = 60  # Frames per second
WIDTH = 700
HEIGHT = 1100
successes, failures = pygame.init()
print("{0} successes and {1} failures".format(successes, failures))
pygame.display.set_caption("Sokoban Solver")
surface = pygame.display.set_mode((HEIGHT,WIDTH))
clock = pygame.time.Clock()


#---------------------
# Setup Colors 
#---------------------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY_LIGHT = (231, 231, 231)
ORANGE = '#ff631c'
BLUE_LIGHT = (40, 53, 88)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
YELLOW_LIGHT = (255, 255, 51)
BROWN = (210, 105, 30)
PINK = (204, 0, 255)
GREEN_LIGHT = (0, 255, 140)
GREEN = (0, 255, 0)
GREEN_DARK = (0, 255, 0)


#---------------------
# Font Setup
#---------------------
menuFont = pygame.font.SysFont("CopperPlate Gothic", 60, bold = True)  
helpFont = pygame.font.SysFont("Comic Sans MS", 25)      
wordFont = pygame.font.SysFont("CopperPlate Gothic", 25)  
recordFont = pygame.font.SysFont("Comic Sans MS", 17)  
mapFont = pygame.font.SysFont("Comic Sans MS", 20, bold = True)   
levelFont = pygame.font.SysFont("Comic Sans MS", 25, bold = True)  
buttonFont = pygame.font.SysFont("CopperPlate Gothic", 18, bold = True)


#---------------------
# Global Variables
#---------------------
numsRow = 8 
numsCol = 8 

numsUnit = max(numsCol, numsRow)
lengthSquare = int(WIDTH/numsUnit)

offsetX = lengthSquare * (numsUnit - numsCol)/2 
offsetY = lengthSquare * (numsUnit - numsRow)/2 

map_list = ['MINI COSMOS', 'MICRO COSMOS']
map_index = 0
level = 0
mode = 0
win = 0
step = 1
timeTook = 0
pushed = 0
startTime = 0
stepNode = 0
visualized = 0
moves = []
history = 0
name = ''
actions = []
ptr = -1
itemMemory = psutil.Process(os.getpid()).memory_info().rss/(1024*1024)

#---------------------
# Setup Items 
#---------------------
background = pygame.image.load("Items/background.jpg")
background = pygame.transform.scale(background, (WIDTH, WIDTH))

wall = pygame.image.load('Items/wall.png')
wall = pygame.transform.scale(wall, (lengthSquare, lengthSquare))

box = pygame.image.load('Items/box.png')
box = pygame.transform.scale(box, (lengthSquare, lengthSquare))

goal = pygame.image.load('Items/goal.png')
goal = pygame.transform.scale(goal, (lengthSquare, lengthSquare))

player_ = pygame.image.load('Items/player.png')
player_ = pygame.transform.scale(player_, (lengthSquare, lengthSquare))

up_arrow = pygame.image.load("Items/up_arrow.png")
up_arrow = pygame.transform.scale(up_arrow, (20, 20))

down_arrow = pygame.image.load("Items/down_arrow.png")
down_arrow = pygame.transform.scale(down_arrow, (20, 20))

pick_button = pygame.image.load("Items/choose.png")
pick_button = pygame.transform.scale(pick_button, (98, 41))

change = pygame.image.load("Items/change.png")
change = pygame.transform.scale(change, (32, 32))

visualize_button = pygame.image.load("Items/visualizebutton.png")

restart_button = pygame.image.load("Items/restart.png")
restart_button = pygame.transform.scale(restart_button, (105, 40))

undo_button = pygame.image.load("Items/undo.png")
undo_button = pygame.transform.scale(undo_button, (35, 35))

redo_button = pygame.image.load("Items/redo.png")
redo_button = pygame.transform.scale(redo_button, (35, 35))


#---------------------
# Setup Rectangles
#---------------------
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


#---------------------
# Setup Displays
#---------------------
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

def display_record():
	recordText = recordFont.render("The solution has been recorded in Results folder", True, RED)
	surface.blit(recordText, [700 + 10, 0 + 612])

def display_title_step_3(color = RED):
	step3Text = helpFont.render("3. Happy Hacking!!!", True, color)
	surface.blit(step3Text, [700 + 10, 0 + 365])

def display_title_content_step_3(color = BROWN):
	statusText = helpFont.render("Status:", True, color)
	surface.blit(statusText, [700 + 26, 0 + 455])

	if not (mode >= 2 and win == 0):
		attemptedText = helpFont.render("Time:", True, color)
		stepText = helpFont.render("Step:", True, color)
		pushedText = helpFont.render("Pushed:", True, color)

		surface.blit(attemptedText, [700 + 30, 0 + 493])
		surface.blit(stepText, [700 + 30, 0 + 530])
		surface.blit(pushedText, [700 + 30, 0 + 570])

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
	surface.blit(statusText, [700 + 127, 0 + 458])

	if not (mode >= 2 and win == 0):
		timeText = helpFont.render("{:0.6f} s".format(timeTook), True, GREEN_LIGHT)
		stepText = helpFont.render(f"{stepNode}", True, GREEN_LIGHT)
		pushedText = helpFont.render(f"{pushed}", True, GREEN_LIGHT)

		surface.blit(timeText, [700 + 110, 0 + 493])
		surface.blit(stepText, [700 + 135, 0 + 530])
		surface.blit(pushedText, [700 + 135, 0 + 570])

def display_restart():
	surface.blit(restart_button, [700 + 160, 0 + 410])

def display_visualize():
	surface.blit(visualize_button, [700 + 135, 0 + 647])

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
	if step == 3:
		display_undo()
		display_redo()
		display_restart()
		display_title_content_step_3()
		display_content_step_3()

		if mode > 1 and win == 1:
			display_visualize()
	
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
		display_step_1(GREEN_DARK, 0)
		display_step_2(GREEN_DARK, mode = mode)
		if win == 0:
			display_step_3(YELLOW, mode = mode)
		elif win == 1:
			display_step_3(GREEN_DARK, mode = mode)
			display_record()

def draw_board():
	draw_menu()

	for point in walls:
		surface.blit(wall, [offsetX + lengthSquare * point[0], offsetY + lengthSquare * point[1]])
	
	for point in paths:
		pygame.draw.rect(surface, WHITE, [offsetX + lengthSquare * point[0], offsetY + lengthSquare * point[1], lengthSquare, lengthSquare])

	# # Debug dead_squares
	# for point in dead_squares:
	# 	pygame.draw.rect(surface, RED, [offsetX + lengthSquare * point[0], offsetY + lengthSquare * point[1], lengthSquare, lengthSquare])

	for point in goals:
		surface.blit(goal, [offsetX + lengthSquare * point[0], offsetY + lengthSquare * point[1]])

	point = player
	surface.blit(player_, [offsetX + lengthSquare * point[0], offsetY + lengthSquare * point[1]])

	for point in boxes:
		surface.blit(box, [offsetX + lengthSquare * point[0], offsetY + lengthSquare * point[1]])

	display_title()
	pygame.display.flip()



#-----------------
# Refresh Data
#-----------------
def reset_data():
	global numsCol, numsRow, numsUnit, lengthSquare, offsetX, offsetY, wall, box, goal, player_, walls, goals, boxes, paths, player, name, distanceToGoal, dead_squares, actions, ptr
	
	wall = pygame.image.load('Items/wall.png')
	box = pygame.image.load('Items/box.png')
	goal = pygame.image.load('Items/goal.png')
	player_ = pygame.image.load('Items/player.png')
	name = "./Testcases/{}/{}.txt".format(map_list[map_index], level+1)
	walls, goals, boxes, paths, player, numsRow, numsCol = set_value(name)
	distanceToGoal, dead_squares = set_distance()
	actions = []
	ptr = -1

	numsUnit = max(numsCol, numsRow)
	lengthSquare = int(WIDTH/numsUnit)

	offsetX = lengthSquare * (numsUnit - numsRow)/2 
	offsetY = lengthSquare * (numsUnit - numsCol)/2 

	wall = pygame.transform.scale(wall, (lengthSquare, lengthSquare))
	box = pygame.transform.scale(box, (lengthSquare, lengthSquare))
	goal = pygame.transform.scale(goal, (lengthSquare, lengthSquare))
	player_ = pygame.transform.scale(player_, (lengthSquare, lengthSquare))

def init_data():
	global move, win, step, timeTook, pushed, startTime, stepNode, map_index, level, board, numsRow, numsCol, numsUnit, lengthSquare, offsetX, offsetY, visualized, actions
	
	mode = 0
	win = 0
	step = 1
	timeTook = 0
	pushed = 0
	startTime = 0
	stepNode = 0
	visualized = 0
	actions = []
	reset_data()


#------------------------
# Setting Data Structures and Functionalities
#------------------------
class Direction:
	'''
	vector: we can define it as object of class Point that we have define above, so that we can add 2 Point or double it for checking
	char: character represent for its direction, that we can print results
	'''
	def __init__(self, vector, char):
		self.vector = vector
		self.char = char

	def get_char(self):
		return self.char

# We set the coordinate from top-left corner and x-axis and y-axis as default
L = Direction((-1, 0), 'L')
R = Direction((1, 0), 'R')
U = Direction((0, -1), 'U')
D = Direction((0, 1), 'D')
directions = [U, L, D, R] # clock-wise



#$$ Rule for moving in SOKOBAN map, the rules below will apply for 4 directions: UP, DOWN, LEFT, RIGHT
# Rule 1: If the forward cell is empty, we literally can move
# Rule 2: If the forward cell has a wall, we can not move
# Rule 3: If the forward cell has a box:
	# Rule 3.1: If the forward of forward cell has a box or a wall, we can not move 
	# Rule 3.2: If the forward of forward cell not contains a box or a wall, we can move forward and push the box forward 

def set_available_moves(player, boxes): 
	# Setup attribute available_moves as a list storing legal moves up to date which is a subset of directions list (<= 4 elements)
	# Available moves <=> Rule 1 + Rule 3.2
	available_moves = []
	for direction in directions:
		if (player[0] + direction.vector[0], player[1] + direction.vector[1]) not in walls:
			# forward cell can be a box or empty
			if (player[0] + direction.vector[0], player[1] + direction.vector[1]) in boxes:
				# forward cell contains a box
				if ((player[0] + 2*direction.vector[0], player[1] + 2*direction.vector[1]) not in walls) and ((player[0] + 2*direction.vector[0], player[1] + 2*direction.vector[1]) not in boxes):
					available_moves.append(direction)
			else:
				# forward cell is empty
				available_moves.append(direction)
	return available_moves

# Move the player with direction but the argument make sure direction in the available_moves 
def move(player, boxes, direction):	
	temp = (player[0] + direction.vector[0], player[1] + direction.vector[1])
	is_pushed = 0
	res = True
	boxes = set(boxes)
	if temp in boxes:
		is_pushed = 1
		boxes.remove(temp)
		boxes.add((player[0] + 2*direction.vector[0], player[1] + 2*direction.vector[1]))
		
		if (player[0] + 2*direction.vector[0], player[1] + 2*direction.vector[1]) in dead_squares:
			res = False
	boxes = tuple(boxes) 
	player = temp
	return res, is_pushed, player, boxes

def is_win(goals, boxes):
	return goals.issubset(boxes)

def undo():
	global player, boxes, ptr, stepNode, pushed
	if ptr > -1:
		move = actions[ptr]
		boxes = set(boxes)
		if move[1] == 1:
			pushed -= 1
			boxes.remove((player[0] + move[0].vector[0], player[1] + move[0].vector[1]))
			boxes.add(player)
		boxes = tuple(boxes)
		player = (player[0] - move[0].vector[0], player[1] - move[0].vector[1])
		stepNode -= 1
		ptr -= 1

def redo():
	global player, boxes, ptr, stepNode, pushed
	if ptr < len(actions) - 1:
		_, is_pushed, player, boxes = move(player, boxes, actions[ptr + 1][0])
		ptr += 1
		stepNode += 1
		pushed += is_pushed

def set_distance():
	distanceToGoal = dict()
	dead_squares = set()
	for goal in goals:
		distanceToGoal[goal] = dict()
		for path in paths:
			distanceToGoal[goal][path] = 1e9
	queue = Queue()
	for goal in goals:
		distanceToGoal[goal][goal] = 0
		queue.put(goal)
		while not queue.empty():
			position = queue.get()
			for direction in directions:
				boxPosition = (position[0] + direction.vector[0], position[1] + direction.vector[1])
				playerPosition = (position[0] + 2*direction.vector[0], position[1] + 2*direction.vector[1])
				if boxPosition in paths:
					if distanceToGoal[goal][boxPosition] == 1e9:
						if (boxPosition not in walls) and (playerPosition not in walls):
							distanceToGoal[goal][boxPosition] = distanceToGoal[goal][position] + 1
							queue.put(boxPosition)
	# Add dead squares
	for path in paths:
		ok = 1
		for goal in goals:	
			if distanceToGoal[goal][path] != 1e9:
				ok = 0
				break
		if ok == 1:
			dead_squares.add(path)
	return distanceToGoal, dead_squares

def minimum_cost(step, boxes):
	# Minimum of matching all distances from all goals to all boxes (Assignment Problem) using Hungarian Algorithm
	temp = []
	for goal in goals:
		for box in boxes:
			## Using Manhattan distance
			# temp.append(abs(goal[0] - box[0]) + abs(goal[1] - box[1])) 

			## Using DistanceToGoal 2d-array
			temp.append(distanceToGoal[goal][box])

	arr = np.array(temp)
	# Make matrix with row is goal and colum is box
	cost = arr.reshape(len(goals), len(boxes))
	row_ind, col_ind = linear_sum_assignment(cost) # Hungarian Algorithm
	return cost[row_ind, col_ind].sum() + step # f(n) = g(n) + h(n)

def set_value(filename):
	walls = set() # set of Point()
	goals = set()
	boxes = []
	paths = set()
	player = None
	x = 0
	y = 0
	with open(filename, 'r') as f:
		read_data = f.read()
		lines = read_data.split('\n')	
		for line in lines:
			x = 0
			for char in line:
				if char == '#': # Wall
					walls.add((x,y))
				elif char == 'x': # Box
					boxes.append((x,y))
					paths.add((x,y))
				elif char == '?': # Goal
					goals.add((x,y))
					paths.add((x,y))
				elif char == '@': # Player
					player = (x,y)
					paths.add((x,y))
				elif char == '-': # Player and Goal
					goals.add((x,y))
					player = (x,y)
					paths.add((x,y))
				elif char == '+': # Box and Goal
					goals.add((x,y))
					boxes.append((x,y))
					paths.add((x,y))
				elif char == '.': # Path - avaiable move
					paths.add((x,y))
				x += 1
			y += 1
	return walls, goals, tuple(boxes), paths, player, x, y


#----------------------
# Exporting The Results
#----------------------
def print_results(board, gen, rep, expl, memo, dur):
	if mode == 2:
		print("\n-- Algorithm: Breadth first search --")
	elif mode == 3:
		print("\n-- Algorithm: A star --")
	print("Sequence: ", end="")
	for ch in board.history_moves:
		print(ch.direction.char, end=" ")
	print("\nNumber of steps: " + str(board.step))
	print("Nodes generated: " + str(gen))
	print("Nodes repeated: " + str(rep))
	print("Nodes explored: " + str(expl))
	print("Memory: ", str(memo), " MB")  # in megabytes
	print('Duration: ' + str(dur) + ' secs')

def line_prepender(filename, algo, sol, ste, gen, rep, expl, memo, dur):
	if not os.path.exists('Results'):
		os.mkdir('Results')
	if not os.path.exists(filename):
		open(filename, 'w+')
	with open(filename, 'r+') as f:
		content = f.read()
		f.seek(0, 0)
		dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S %p")
		f.write("Datatime (UTC+7): " + dt_string + '\n')
		f.write("Problem: " + name.split('./')[-1] + '\n')
		f.write("Algorithm: " + algo + '\n')
		f.write("Solution: " + sol + '\n')
		f.write("Number of steps: " + str(ste) + '\n')
		f.write("Nodes generated: " + str(gen) + '\n')
		f.write("Nodes repeated: " + str(rep) + '\n')
		f.write("Nodes explored: " + str(expl) + '\n')
		f.write("Memory: " + str(memo) + ' MB' + '\n')
		f.write("Duration: " + str(dur) + " secs" + '\n')
		f.write("\n\n")
		f.write("===================================================" + '\n')
		f.write("===================================================" + '\n')
		f.write("\n\n")
		f.write(content)

def add_history(algo, sol, ste, gen, rep, expl, memo, dur):
	line_prepender('Results/history_log.txt', algo, sol, ste, gen, rep, expl, memo, dur)
	line_prepender('Results/Solution_{}_test {}'.format(name.split('/')[2], name.split('/')[3]), algo, sol, ste, gen, rep, expl, memo, dur)

def get_history_moves(actions):
	return ", ".join(list(map(lambda move: move[0].char, actions)))


#-----------------
# Setting Alogorithms
#-----------------
def bfs(curr_player, curr_boxes):
	global win, timeTook, startTime
	node_repeated = 0
	node_generated = 0
	frontier = Queue()
	explored = set()
	frontier.put((curr_player, curr_boxes, 0, 0, []))

	node_generated += 1
	explored.add((curr_player, curr_boxes))
	startTime = time.time()
	while True:
		if frontier.empty():
			print("Solution not found\n")
			return (0, 0, 0, 0, [])

		(now_player, now_boxes, steps, push, actions) = frontier.get()
		moves = set_available_moves(now_player,now_boxes)
		for m in moves:
			res, is_pushed, new_player, new_boxes = move(now_player, now_boxes, m)
			if (new_player, new_boxes) not in explored and res == True:
				explored.add((new_player, new_boxes))
				if is_win(goals, new_boxes):							
					timeTook = time.time() - startTime
					win = 1
					memo_info = psutil.Process(os.getpid()).memory_info().rss/(1024*1024) - itemMemory
					add_history("Breadth First Search", get_history_moves(actions + [(m,is_pushed)]), steps + 1, node_generated, node_repeated, len(explored), memo_info, timeTook)
					return (node_generated + 1, steps + 1, timeTook, memo_info, actions + [(m,is_pushed)])
				frontier.put((new_player, new_boxes, steps+1, push + is_pushed, actions + [(m,is_pushed)]))
			else:
				node_repeated += 1
			node_generated += 1
	

def A_star(curr_player, curr_boxes):
	global win, timeTook, startTime
	node_repeated = 0
	node_generated = 0
	frontier = SortedList(key=lambda x: minimum_cost(x[2], x[1]))
	explored = set()
	frontier.add((curr_player, curr_boxes, 0, 0, []))
	node_generated += 1
	explored.add((curr_player, curr_boxes))
	startTime = time.time()
	while True:
		if len(frontier) == 0:
			print("Solution not found\n")
			return (0, 0, 0, 0, [])

		(now_player, now_boxes, steps, push, actions) = frontier.pop(0)
		moves = set_available_moves(now_player,now_boxes)
		for m in moves:
			res, is_pushed, new_player, new_boxes = move(now_player, now_boxes, m)
			if (new_player, new_boxes) not in explored and res == True:
				explored.add((new_player, new_boxes))
				if is_win(goals, new_boxes):
					timeTook = time.time() - startTime
					win = 1
					memo_info = psutil.Process(os.getpid()).memory_info().rss/(1024*1024) - itemMemory
					add_history("A star", get_history_moves(actions + [(m,is_pushed)]), steps + 1, node_generated, node_repeated, len(explored), memo_info, timeTook)
					return (node_generated + 1,steps + 1, timeTook, memo_info, actions + [(m,is_pushed)])
				frontier.add((new_player, new_boxes, steps + 1, push + is_pushed, actions + [(m,is_pushed)]))
			else:
				node_repeated += 1
			node_generated += 1


#-----------------
# Run Program
#-----------------
if __name__ == '__main__':
	name = "./Testcases/{}/{}.txt".format(map_list[0],1)
	walls, goals, boxes, paths, player, _, _ = set_value(name)
	distanceToGoal, dead_squares = set_distance()
	
	while True:
		clock.tick(FPS)
		if is_win(goals, boxes) == True and mode == 1:
			win = 1
			# This result has been recorded in Results folder
			if history == 0:
				add_history("Manually", get_history_moves(actions), stepNode, 0, 0, 0, 0, timeTook)
				history = 1

		if step == 3 and win == 0 and mode == 1:
			timeTook = time.time() - startTime

		if step == 3 and mode == 2 and win == 0:
			(node_created, steps, times, memo, moves) = bfs(player, boxes)

		if step == 3 and mode == 3 and win == 0:
			(node_created, steps, times, memo, moves) = A_star(player, boxes)

		if len(moves) > 0 and visualized == 1:
			(_, is_pushed, player, boxes) = move(player, boxes, moves[0][0])
			actions.append(moves[0])
			moves.pop(0)
			stepNode += 1
			pushed += is_pushed
			ptr += 1
			time.sleep(0.3)
			

		for event in pygame.event.get():
			keys_pressed = pygame.key.get_pressed()
			if event.type == pygame.QUIT or keys_pressed[pygame.K_q]:
				pygame.quit()

			if event.type == pygame.KEYDOWN:
				if step == 3:
					if mode == 1 and win == 0:
						if event.key == pygame.K_w or event.key == pygame.K_UP:
							if U in set_available_moves(player, boxes):
								if ptr + 1 < len(actions):
									actions = actions[0:(ptr+1)]
								(_, is_pushed, player, boxes) = move(player, boxes, U)
								stepNode += 1
								pushed += is_pushed
								ptr += 1
								actions.append((U, is_pushed))
						elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
							if D in set_available_moves(player, boxes):
								if ptr + 1 < len(actions):
									actions = actions[0:(ptr+1)]
								(_, is_pushed, player, boxes) = move(player, boxes, D)
								stepNode += 1
								pushed += is_pushed
								ptr += 1
								actions.append((D, is_pushed))
						elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
							if L in set_available_moves(player, boxes):
								if ptr + 1 < len(actions):
									actions = actions[0:(ptr+1)]
								(_, is_pushed, player, boxes) = move(player, boxes, L)
								stepNode += 1
								pushed += is_pushed
								ptr += 1
								actions.append((L, is_pushed))
						elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
							if R in set_available_moves(player, boxes):
								if ptr + 1 < len(actions):
									actions = actions[0:(ptr+1)]
								(_, is_pushed, player, boxes) = move(player, boxes, R)
								stepNode += 1
								pushed += is_pushed
								ptr += 1
								actions.append((R, is_pushed))

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
						continue
					if A_rect.collidepoint(x,y):
						mode = 3
						step = 3
						continue

				if step == 3:
					if mode == 1:
						if restart_rect.collidepoint(x,y):
							init_data()
							step = 1
						if undo_rect.collidepoint(x,y):
							undo()
						if redo_rect.collidepoint(x,y):
							redo()
					if mode == 2:
						#Bfs
						if restart_rect.collidepoint(x,y):
							init_data()
							step = 1
						if win == 1:
							if visualized == 0:
								if visualize_rect.collidepoint(x,y):
									visualized = 1
							else:
								if undo_rect.collidepoint(x,y):
									undo()
								if redo_rect.collidepoint(x,y):
									redo()
					if mode == 3:
						# A_star
						if restart_rect.collidepoint(x,y):
							init_data()
							step = 1
						if win == 1:
							if visualized == 0:
								if visualize_rect.collidepoint(x,y):
									visualized = 1
							else:
								if undo_rect.collidepoint(x,y):
									undo()
								if redo_rect.collidepoint(x,y):
									redo()

		draw_board()
		pygame.display.update()