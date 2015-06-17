from tkinter import *
import time
import random

n, m = 10, 10 				#n - row and height , m - column and width!!!
n, m = map(int, input().split())

randomn = n
randomm = m

colorconst = 2

VELOCITY = 100

COLORS = ['0','1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']

number_of_pushings = 0
number_of_random_pushings = 0

matrix = []
for i in range(n):
	matrix.append([0]*m)
random_matrix = []
for i in range(n):
	random_matrix.append([0]*m)

WANT_TO_CHECK_RANDOM_PUSHING = False
CHECK_FOR_STOPPING_THE_LOOP = None
CHECK_FOR_STOPPING_THE_RANDOM_LOOP = None
PUSHES_PER_DRAWING = 1
total_sand = 0
sandy = 0

random_pushing_matrix = None

#ФУНКЦИИ ДОБАВЛЕНИЯ/УБИРАНИЯ ПЕСКА

def add_sand(event):					#добавляет песок в клетки по щелчку левой кнопкой мыши
	global WIDTH, HEIGHT, m, n, matrix, sandy, total_sand, WANT_TO_CHECK_RANDOM_PUSHING
	c = event.widget
	x = event.x
	y = event.y
	x /= const
	y /= const
	x = int(x) - 1
	y = int(y) - 1
	if x < m and y < n:
		#root = Tk()
		#text = Text(root, height=7, width=7,font='Arial 14',wrap = WORD)
		#text.pack()
		#def get_sand(event):
		#	global sandy
		#	sandy = text.get('1.0', END)
		#root.bind('<Button-3>', get_sand)
		#print(sandy)
		if WANT_TO_CHECK_RANDOM_PUSHING == True:
			random_matrix[y][x] += sandy
		matrix[y][x] += sandy
		total_sand += sandy
		matrix_square(x, y, matrix[y][x])

def remove_sand(event):					#убирает песок из клетки по щелчку правой кнопкой мыши
	global WIDTH, HEIGHT, m, n, matrix, total_sand, WANT_TO_CHECK_RANDOM_PUSHING
	c = event.widget
	x = event.x 
	y = event.y 
	x /= const
	y /= const
	x = int(x) - 1
	y = int(y) - 1
	if x < m and y < n:
		if WANT_TO_CHECK_RANDOM_PUSHING == True:
			random_matrix[y][x] = 0
		total_sand -= matrix[y][x]
		matrix[y][x] = 0
		matrix_square(x, y, matrix[y][x])

def remove_all(event):
	global WIDTH, HEIGHT, m, n, matrix, number_of_pushings, total_sand, WANT_TO_CHECK_RANDOM_PUSHING
	for i in range(n):
		for k in range(m):
			if WANT_TO_CHECK_RANDOM_PUSHING == True:
				matrix[i][k] = 0
			matrix[i][k] = 0
	number_of_pushings = 0
	total_sand = 0
	draw_matrix()

def getV(root):
	global sandy
	a = scale1.get()
	sandy = a
	print("Текущее значение количества песчинок:", a)

#ФУНКЦИИ РИСОВАНИЯ МАТРИЦЫ

def convert_from_hex_to_de(a):				
	global COLORS
	hexad = ''
	while a > 0:
		hexad = COLORS[a%16] + hexad
		a //= 16
	return hexad

def colour_square(a):
	global colorconst, COLORS
	mycolor = '#'
	#a *= 32000
	color = a
	a //= colorconst
	a = 255 - a
	a = convert_from_hex_to_de(a)
	while len(a) < 2:
		a = '0' + a
	a *= 3
	#while len(a) < 6:
	#	a += 'f' 
	mycolor += a[:6]
	#if a == 0:
	#	a = 'white'
	if color == 1:
		mycolor = 'cyan'
	elif color == 2:
		mycolor = 'steel blue'
	elif color == 3:
		mycolor = 'blue'
	elif color == 4:
		mycolor = 'red'
	return mycolor

def matrix_square(x, y, a):
	global n, m, const, WIDTH, HEIGHT
	x += 1
	y += 1
	x *= const
	y *= const
	a = colour_square(a)
	c.create_rectangle(x, y, x + const, y + const, outline = "black", fill = a)

def draw_matrix():
	global matrix, n, m
	c.delete(*c.find_all())
	for i in range(n):
		for k in range(m):
			matrix_square(k, i, matrix[i][k])

def get_pushed(root):
	global PUSHES_PER_DRAWING
	a = pushes_scale.get()
	PUSHES_PER_DRAWING = a

#ФУНКЦИИ РАССЫПАНИЯ ПЕСКА

def check_size(matrix, n, m):
	#print('hello')
	counter = 0
	#print_matrix(matrix)
	#print(n, m)
	for i in range(n):
		if matrix[i][0] >= 4 or matrix[i][m-1] >= 4:
			#print('cool', i, k)
			counter += 1
	for k in range(m):
		if matrix[0][k] >= 4 or matrix[n-1][k] >= 4:
			counter += 1
	counter = check_counter(counter)
	if counter == 1:
		for p in range(n):
			matrix[p].append(0)
		for p in range(n):
			matrix[p].insert(0, 0)
		matrix.insert(0, [0]*(m + 2))
		matrix.append([0]*(m+2))
		m += 2
		n += 2
	return matrix, n, m
	#print_matrix(matrix)

def check_counter(a):
	if a > 0:
		a = 1
	return a
	
def push_sand():
	global n, m, matrix, CHECK_FOR_STOPPING_THE_LOOP
	counter = 0
	memento = None
	for i in range(n):
		for k in range(m):
			if matrix[i][k] >= 4:
				matrix[i][k] -= 4
				matrix[i+1][k] += 1
				matrix[i-1][k] += 1
				matrix[i][k-1] += 1
				matrix[i][k+1] += 1
				counter += 1
				memento = k
				break
		if memento != None:
			break

	#print_matrix(matrix)
	if counter == 0:
		CHECK_FOR_STOPPING_THE_LOOP = False

def push_sand2():
	global n, m, matrix, number_of_pushings, CHECK_FOR_STOPPING_THE_LOOP
	pushed_sand = []
	timea = time.clock()
	counter = 0
	for i in range(n):
		for k in range(m):
			if matrix[i][k] >= 4:
				pushed_sand.append([i, k])
				counter += 1
	for p in range(len(pushed_sand)):
		i, k = pushed_sand[p][0], pushed_sand[p][1]
		matrix[i][k] -= 4
		matrix[i+1][k] += 1
		matrix[i-1][k] += 1
		matrix[i][k+1] += 1
		matrix[i][k-1] += 1
	timeb = time.clock()
	number_of_pushings += counter
	#print(timeb-timea)
	if counter == 0:
		CHECK_FOR_STOPPING_THE_LOOP = False

#ДОПФУНКЦИИ

def print_matrix(matrix):
	for i in range(len(matrix)):
		print(matrix[i], end = '\n')
	print('wellwellwell')

def renew_const():
	global n, m, const
	const = 500//(max(m,n))

def draw_colors():
	global colorconst
	for i in range(0, 255*colorconst, 5):
		#print(colour_square(i))
		anotherc.create_rectangle(0, i, 20, i+5, fill = colour_square(i))

def print_number_of_pushings(event):
	global number_of_pushings, number_of_random_pushings
	number_of_pushings_button['text'] = 'Number of pushings: ' + str(number_of_pushings) + '; number of random pushings: ' + str(number_of_random_pushings)

#def round1(i, n):
#	if i <= n//2:
#		return 0
#	else:
#		return n-1

#ФУНКЦИИ ЗАЦИКЛИВАНИЯ

def keep_on_pushing():
	global CHECK_FOR_STOPPING_THE_LOOP,CHECK_FOR_STOPPING_THE_RANDOM_LOOP, number_of_pushings, PUSHES_PER_DRAWING, matrix, random_matrix, n, m, randomn, randomm
	renew_const()
	draw_matrix()
	if CHECK_FOR_STOPPING_THE_LOOP != False:
		for i in range(PUSHES_PER_DRAWING):
			matrix, n, m = check_size(matrix, n, m)
			push_sand2()
	if CHECK_FOR_STOPPING_THE_RANDOM_LOOP != False:
		button_for_checking_random_pushing['text'] = 'Being checked'
		random_matrix, randomn, randomm = check_size(random_matrix, randomn, randomm)
		random_push_sand()
	elif CHECK_FOR_STOPPING_THE_LOOP == False:
		the_truth = check_if_they_are_the_same()
		if the_truth == True:
			button_for_checking_random_pushing['text'] = 'THEY ARE TOTALLY THE SAME'
		else:
			button_for_checking_random_pushing['text'] = 'THEY ARE DIFFERENT! nooooo'
	
#			break
	#counter = push_sand()					#работает, но в разы медленнее, чем push_sand2()
	#print(number_of_pushings)
	check_the_stop_button()
	c.after(VELOCITY, keep_on_pushing)

def check_the_stop_button():
	global CHECK_FOR_STOPPING_THE_LOOP
	if CHECK_FOR_STOPPING_THE_LOOP == False:
		but2['text'] = 'START'
	else:
		but2['text'] = 'STOP'


def stop_the_loop(event):
	global CHECK_FOR_STOPPING_THE_LOOP, CHECK_FOR_STOPPING_THE_RANDOM_LOOP
	if CHECK_FOR_STOPPING_THE_LOOP == None:
		CHECK_FOR_STOPPING_THE_LOOP = False
	else:
		CHECK_FOR_STOPPING_THE_LOOP = None
	if CHECK_FOR_STOPPING_THE_RANDOM_LOOP == None:
		CHECK_FOR_STOPPING_THE_RANDOM_LOOP = False
	else:
		CHECK_FOR_STOPPING_THE_RANDOM_LOOP = None

def loop(event):
	CHECK_FOR_STOPPING_THE_LOOP = None

	keep_on_pushing()

#RANDOMISING

def random_push_sand():
	global randomn, randomm, random_matrix, number_of_random_pushings, CHECK_FOR_STOPPING_THE_RANDOM_LOOP
	pushed_sand = []
	#timea = time.clock()
	#counter = 0
	for i in range(randomn):
		for k in range(randomm):
			if random_matrix[i][k] >= 4:
				pushed_sand.append([i, k])
				#counter += 1
	if len(pushed_sand) != 0:
		pushing_this_one = random.randint(0, len(pushed_sand)- 1)
		#print(pushed_sand, pushing_this_one)
		i, k = pushed_sand[pushing_this_one][0], pushed_sand[pushing_this_one][1]
		random_matrix[i][k] -= 4
		random_matrix[i+1][k] += 1
		random_matrix[i-1][k] += 1
		random_matrix[i][k+1] += 1
		random_matrix[i][k-1] += 1
	#timeb = time.clock()
		number_of_random_pushings += 1
	#print(timeb-timea)
		#print_matrix(random_matrix)
	elif len(pushed_sand) == 0:
		CHECK_FOR_STOPPING_THE_RANDOM_LOOP = False

def check_if_they_are_the_same():
	global matrix, random_matrix, number_of_pushings, number_of_random_pushings
	ret = True
	if len(matrix) == len(random_matrix):
		for i in range(len(matrix)):
			if len(matrix[i]) == len(random_matrix[i]):
				for k in range(len(matrix[i])):
					if matrix[i][k] != random_matrix[i][k]:
						ret = False
			else:
				ret = False
	else:
		ret = False
	return ret


def randomize_it(event):
	global WANT_TO_CHECK_RANDOM_PUSHING, CHECK_FOR_STOPPING_THE_RANDOM_LOOP, matrix, random_matrix
	#random_matrix = matrix
	button_for_checking_random_pushing['text'] = 'Being checked'
	WANT_TO_CHECK_RANDOM_PUSHING = True
	CHECK_FOR_STOPPING_THE_RANDOM_LOOP = True


const = 500//(max(m,n))

WIDTH = (m+1)*const
HEIGHT = (n+1)*const

#BUTTONS SCALES CANVAS

root = Tk()
c = Canvas(root, width = WIDTH, height = HEIGHT)
anotherc = Canvas(root, width = 20, height = 255*colorconst)
but = Button(root, text = "PUSH SAND", bg="white",fg = "black") 
but2 = Button(root, text = "STOP", bg="white",fg = "black")
scale1 = Scale(root, orient=VERTICAL, length=510, from_=0, to=510, tickinterval = 50, resolution = 5)
pushes_scale = Scale(root, orient=HORIZONTAL, length=500, from_=1, to = 30, tickinterval = 2, resolution = 1)
button1 = Button(root, text="Change sand number", bg="white",fg = "black")
pushes_button = Button(root, text = 'Change pushes speed', bg="white",fg = "black")
number_of_pushings_button = Button(root, text = 'Number of pushings: 0; number of random pushings: 0', bg="white",fg = "black")
button_for_checking_random_pushing = Button(root, text = 'I want to check random pushing', bg="white",fg = "black")

#BINDING

c.bind("<Button-1>", add_sand)
c.bind('<Button-3>', remove_sand)
but.bind('<Button-1>', loop)
but.bind('<Button-3>', remove_all)
but2.bind('<Button-1>', stop_the_loop)
pushes_button.bind('<Button-1>', get_pushed)
button1.bind("<Button-1>",getV)
number_of_pushings_button.bind('<Button-1>', print_number_of_pushings)
button_for_checking_random_pushing.bind('<Button-1>', randomize_it)

#PACKING
but2.pack(side = 'left')
but.pack(side = 'left')
anotherc.pack(side = 'right')
scale1.pack(side = 'right')
button1.pack(side = 'right')
pushes_scale.pack(side = 'bottom')
pushes_button.pack(side = 'bottom')
button_for_checking_random_pushing.pack()
number_of_pushings_button.pack()
c.pack(side = 'top')

draw_matrix()
draw_colors()



but2.pack(side = 'left')
anotherc.pack(side = 'right')
scale1.pack(side = 'right')
button1.pack(side = 'right')
pushes_scale.pack(side = 'bottom')
pushes_button.pack(side = 'bottom')
but.pack()
c.pack()

root.mainloop()
