# def new_board(filename):
# 	e = []
# 	with open(filename, 'r') as f:
# 		read_data = f.read()
# 		lines = read_data.split('\n')
# 		for line in lines:
# 			tmp = []
# 			for char in line:
# 				if char == ' ': # space
# 					tmp.append(0)
# 				elif char == '#': # wall
# 					tmp.append(1)
# 				elif char == 'x': # box
# 					tmp.append(2)
# 				elif char == '?': #goal
# 					tmp.append(3)
# 				elif char == '@': # man
# 					tmp.append(4)
# 			e.append(tmp)
# 	return e

# board = new_board('test_1.txt')

# for i in range(len(board)):
# 	for j in range(len(board[0])):
# 		if board[i][j] == 1:
# 			print("adfas")

###########################################
# Calculate the time and space complexity
# import os
# import psutil
# import time
# start = time.time()
# process = psutil.Process(os.getpid())
# print(process.memory_info().rss/(1024*1024))  # in megabytes
# print(time.time() - start)

##############################################

# class Board:
# 	# Use what DataStructure for saving wall, goal, box, player
# 	def __init__(self):
# 		# self.dir_list = dir_list  # list of directions for solution
# 		self.walls = set()
# 		self.goals = set()
# 		self.boxes = set()
# 		self.paths = set()
# 		self.player = None
# 		self.cost = 1  # used for heuristic search: A* algorithm

# 	def add_wall(self, x, y):
# 		self.walls.add((x,y))

# 	def add_goal(self, x, y):
# 		self.goals.add((x,y))

# 	def add_box(self, x, y):
# 		self.boxes.add((x,y))

# 	def add_path(self, x, y):
# 		self.paths.add((x,y))

# 	def add_player(self, x, y):
# 		self.player = (x,y)

	
# 	def is_win(self):
# 	    if self.goals.issubset(self.boxes):
# 	        return True
# 	    else:
# 	        return False

# 	def set_value(self, filename):
# 		with open(filename, 'r') as f:
# 			read_data = f.read()
# 			lines = read_data.split('\n')
# 			x = 0
# 			y = 0
# 			for line in lines:
# 				for char in line:
# 					if char == '#': # Wall
# 						self.add_wall(x,y)
# 					elif char == 'x': # Box
# 						self.add_box(x,y)
# 					elif char == '?': # Goal
# 						self.add_goal(x,y)
# 					elif char == '@': # Player
# 						self.add_player(x,y)
# 					elif char == '.': # Path - avaiable move
# 						self.add_path(x,y)
				
# 					x += 1
# 				x = 0
# 				y += 1

# board = Board()
# board.set_value("test_1.txt")
# cnt = 0
# for i,j in board.paths:
# 	cnt += 1
# 	print("({},{})".format(i,j))

# print(cnt)

# 


# class Point:
# 	def __init__(self):
# 		self.x = -1
# 		self.y = -1

# 	def __init__(self, x, y):
# 		self.x = x
# 		self.y = y

# 	def __eq__(self, point):
# 		if self.x == point.x and self.y == point.y:
# 			return True
# 		else:
# 			return False

#     # # Error unhashable type
#     # def __hash__(self):
#     #     return hash((self.x, self.y))
	

# 	# Magic method: https://www.python-course.eu/python3_magic_methods.php
# 	def __add__(self, point):
# 		x = self.x + point.x
# 		y = self.y + point.y
# 		return Point(x, y)

# 	def __sub__(self, point):
# 		x = self.x - point.x
# 		y = self.y - point.y
# 		return Point(x, y)

# 	def double(self):
# 		return Point(self.x*2, self.y*2)

#     # def __key(self):
#     #     return (self.x, self.y)

#     # def __hash__(self):
#     #     return hash(self.__key())

#     def add(self):
#     	return self.x + self.y
print("adfasd")
class A:
	def __init(self,a,b,c):
		self.attr_a = a
		self.attr_b = b
		self.attr_c = c


	# def __key(self):
	#     return (self.attr_a, self.attr_b, self.attr_c)

	# def __hash__(self):
	#     return hash(self.__key())

	# def __eq__(self, other):
	#     if isinstance(other, A):
	#         return self.__key() == other.__key()
	#     return NotImplemented

	def add(self):
		return self.attr_a + self.attr_c
	def print(self):
		return "asdfasd"


a = A()
print(a)
