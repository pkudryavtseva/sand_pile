from tkinter import *
import time
import random

 				#n - row and height , m - column and width!!!
mode = None
while mode != 1 and mode != 2:
		print('Введите режим работы, 1 для рассыпания песка, 2 для проверки случайного пересыпания:')
		mode = int(input())
n, m = 0, 0
while  n < 10 or m < 10 or n > 100 or m > 100:
		print('Введите количество столбцов и строк через пробел в 1 строку (от 10 до 100):')
		try:
			n, m = map(int, input().split())
		except:
			n,m = 0,0

first_n = n
first_m = m



colorconst = 2

VELOCITY = 1

COLORS = ['0','1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']

number_of_pushings = 0

matrix = []
for i in range(n):
	matrix.append([0]*m)


CHECK_FOR_STOPPING_THE_LOOP = False
CHECK_FOR_STOPPING_THE_RANDOM_LOOP = None
PUSHES_PER_DRAWING = 1
total_sand = 0
sandy = 100
print("Текущее значение количества песчинок: 10")



#ФУНКЦИИ ДОБАВЛЕНИЯ/УБИРАНИЯ ПЕСКА

def add_sand(event):					#добавляет песок в клетки по щелчку левой кнопкой мыши
	global WIDTH, HEIGHT, m, n, matrix, sandy, total_sand
	c = event.widget
	x = event.x
	y = event.y
	x /= const
	y /= const
	x = int(x) - 1
	y = int(y) - 1
	if x < m and y < n and y > 1 and x > 1:
		#root = Tk()
		#text = Text(root, height=7, width=7,font='Arial 14',wrap = WORD)
		#text.pack()
		#def get_sand(event):
		#	global sandy
		#	sandy = text.get('1.0', END)
		#root.bind('<Button-3>', get_sand)
		#print(sandy)
		if mode == 2:
			random_matrix[y][x] += sandy
			matrix_square(x, y, random_matrix[y][x], random_c)
		matrix[y][x] += sandy
		total_sand += sandy
		matrix_square(x, y, matrix[y][x], c)
		

def remove_sand(event):					#убирает песок из клетки по щелчку правой кнопкой мыши
	global WIDTH, HEIGHT, m, n, matrix, total_sand, random_matrix
	c = event.widget
	x = event.x 
	y = event.y 
	x /= const
	y /= const
	x = int(x) - 1
	y = int(y) - 1
	if x < m and y < n and y > 1 and x > 1:
		total_sand -= matrix[y][x]
		matrix[y][x] = 0
		if mode == 2:
			random_matrix[x][y] = 0
		matrix_square(x, y, matrix[y][x], c)

def remove_all(event):
	global WIDTH, HEIGHT, m, n, matrix, number_of_pushings, total_sand, mode, first_m, first_n, const, random_matrix, randomm, randomn, CHECK_FOR_STOPPING_THE_LOOP
	if mode == 2:
		global but
	number_of_pushings = 0
	total_sand = 0
	n = first_n
	m = first_m
	matrix = []
	for i in range(n):
		matrix.append([0]*m)
	const = 500//(max(m,n))
	WIDTH = (m+1)*const
	HEIGHT = (n+1)*const
	draw_matrix(matrix, first_n, first_m, c)
	if mode == 2:
		random_matrix = []
		randomn = first_n
		randomm = first_m
		for i in range(randomn):
			random_matrix.append([0]*randomm)

		draw_matrix(random_matrix, first_n, first_m, random_c)
		if CHECK_FOR_STOPPING_THE_LOOP != False:
			but = Button(root, text = "PUSH SAND", bg="white",fg = "black") 
			but.bind('<Button-1>', loop)
			but.pack(side = 'top')

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

def colour_square(a):		#по данному числу определяет цвет, который ему сопоставляется
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

def matrix_square(x, y, a, c):		#рисует одну клетку решеткия, используя столбец и строку клетки в матрице, значение это клетки и холст, на котором нужно рисовать
	global n, m, const, WIDTH, HEIGHT
	x += 1
	y += 1
	x *= const
	y *= const
	a = colour_square(a)
	c.create_rectangle(x, y, x + const, y + const, outline = "black", fill = a)

def draw_matrix(matrix, n, m, c):		#рисует всю решетку
	c.delete(*c.find_all())
	for i in range(n):
		for k in range(m):
			matrix_square(k, i, matrix[i][k], c)

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

def renew_const(const, n, m):
	const = 500//(max(m,n))
	return const

def draw_colors():
	global colorconst
	for i in range(0, 255*colorconst, 5):
		#print(colour_square(i))
		anotherc.create_rectangle(0, i, 20, i+5, fill = colour_square(i))

def print_number_of_pushings(event):
	global number_of_pushings, number_of_random_pushings
	number_of_pushings_button['text'] = 'Number of pushings: ' + str(number_of_pushings)
	if mode == 2:
		number_of_pushings_button['text'] += '; number of random pushings:' + str(number_of_random_pushings)

#def round1(i, n):
#	if i <= n//2:
#		return 0
#	else:
#		return n-1

#ФУНКЦИИ ЗАЦИКЛИВАНИЯ

def push_once(event):
	global CHECK_FOR_STOPPING_THE_LOOP,CHECK_FOR_STOPPING_THE_RANDOM_LOOP, const, number_of_pushings, PUSHES_PER_DRAWING, matrix, random_matrix, n, m, randomn, randomm
	matrix, n, m = check_size(matrix, n, m)
	push_sand2()
	check_the_stop_button()
	const = renew_const(const, n, m)
	draw_matrix(matrix, n, m, c)
	change_button()
	CHECK_FOR_STOPPING_THE_LOOP = False

def keep_on_pushing():		#зацикливает пересыпание песка
	global VELOCITY, mode, CHECK_FOR_STOPPING_THE_LOOP,CHECK_FOR_STOPPING_THE_RANDOM_LOOP, number_of_pushings, PUSHES_PER_DRAWING, matrix, random_matrix, n, m, randomn, randomm, mode, const

	for i in range(PUSHES_PER_DRAWING):
		if CHECK_FOR_STOPPING_THE_LOOP != False:
			matrix, n, m = check_size(matrix, n, m)
			push_sand2()
		else:
			break
	const = renew_const(const, n, m)
	draw_matrix(matrix, n, m, c)
#	if CHECK_FOR_STOPPING_THE_RANDOM_LOOP != False:
#		button_for_checking_random_pushing['text'] = 'Being checked'
#		random_matrix, randomn, randomm = check_size(random_matrix, randomn, randomm)
#		random_push_sand()
#	elif CHECK_FOR_STOPPING_THE_LOOP == False:
#		the_truth = check_if_they_are_the_same()
#		if the_truth == True:
#			button_for_checking_random_pushing['text'] = 'THEY ARE TOTALLY THE SAME'
#		else:
#			button_for_checking_random_pushing['text'] = 'THEY ARE DIFFERENT! nooooo'	
#			break
	#counter = push_sand()					#работает, но в разы медленнее, чем push_sand2()
	#print(number_of_pushings)
	if mode == 1:
		check_the_stop_button()
		change_button()
	if CHECK_FOR_STOPPING_THE_LOOP != False:
		c.after(VELOCITY, keep_on_pushing)
	elif mode == 2:
		but = Button(root, text = "FINISHED", bg="white",fg = "black") 
		but.pack(side = 'top')
		VELOCITY = 1
		keep_on_random_pushing()

def check_the_stop_button():
	global CHECK_FOR_STOPPING_THE_LOOP
	if CHECK_FOR_STOPPING_THE_LOOP == False:
		but['text'] = 'PUSH SAND'
	else:
		but['text'] = 'STOP'

def change_button():
	if CHECK_FOR_STOPPING_THE_LOOP == None:
		but.bind('<Button-1>', stop_the_loop)
	else:
		but.bind('<Button-1>', loop)

def stop_the_loop(event):
	global CHECK_FOR_STOPPING_THE_LOOP#, CHECK_FOR_STOPPING_THE_RANDOM_LOOP
	if CHECK_FOR_STOPPING_THE_LOOP == None:
		CHECK_FOR_STOPPING_THE_LOOP = False
	else:
		CHECK_FOR_STOPPING_THE_LOOP = None
	#if CHECK_FOR_STOPPING_THE_RANDOM_LOOP == None:
	#	CHECK_FOR_STOPPING_THE_RANDOM_LOOP = False
	#else:
	#	CHECK_FOR_STOPPING_THE_RANDOM_LOOP = None

def loop(event):		#зацикливает пересыпания песка
	global CHECK_FOR_STOPPING_THE_LOOP, mode
	CHECK_FOR_STOPPING_THE_LOOP = None
	but.bind('<Button-1>', stop_the_loop)
	keep_on_pushing()
	if mode == 2:
		but.destroy()

#RANDOMISING

def keep_on_random_pushing():		#зацикливает случайные пересыпания
	global randomn, randomm, random_matrix, number_of_random_pushings, CHECK_FOR_STOPPING_THE_RANDOM_LOOP, random_const
	random_const = renew_const(random_const, randomn, randomm)
	random_matrix, randomn, randomm = check_size(random_matrix, randomn, randomm)
	random_push_sand()
	random_const = renew_const(random_const, randomn, randomm)
	draw_matrix(random_matrix, randomn, randomm, random_c)
	if CHECK_FOR_STOPPING_THE_RANDOM_LOOP != False:
		random_c.after(VELOCITY, keep_on_random_pushing)
	else:
		the_truth = check_if_they_are_the_same()
		if the_truth == True:
			button_for_checking_random_pushing['text'] = 'THEY ARE TOTALLY THE SAME'
		else:
			button_for_checking_random_pushing['text'] = 'THEY ARE DIFFERENT! nooooo'

def random_push_sand():			#осуществляет одно случайное пересыпание
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
		pushing_this_one = random.randint(0, len(pushed_sand) - 1)
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

def check_if_they_are_the_same():		#проверка того, что конечные состояния совпадают
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


def pack_for_just_doing_it():			#функция, создающая окно для визуализации пересыпания
	#BUTTONS SCALES CANVAS
	global root, c, anotherc, but, but_clear, scale1, pushes_scale, button1, pushes_button, number_of_pushings_button, matrix, n, m, CHECK_FOR_STOPPING_THE_RANDOM_LOOP, CHECK_FOR_STOPPING_THE_LOOP
	global WIDTH, HEIGHT, const
	const = 500//(max(m,n))
	WIDTH = 550
	HEIGHT = 550
	root = Tk()
	c = Canvas(root, width = WIDTH, height = HEIGHT)
	anotherc = Canvas(root, width = 20, height = 255*colorconst)
	but = Button(root, text = "PUSH SAND", bg="white",fg = "black") 
	but_clear = Button(root, text = "CLEAR", bg="white",fg = "black")
	scale1 = Scale(root, orient=VERTICAL, length=510, from_=0, to=510, tickinterval = 50, resolution = 5)
	pushes_scale = Scale(root, orient=HORIZONTAL, length=500, from_=1, to = 100, tickinterval = 10, resolution = 1)
	button1 = Button(root, text="Change sand number", bg="white",fg = "black")
	pushes_button = Button(root, text = 'Change pushes speed', bg="white",fg = "black")
	number_of_pushings_button = Button(root, text = 'Number of pushings: 0', bg="white",fg = "black")
	#button_for_checking_random_pushing = Button(root, text = 'I want to check random pushing', bg="white",fg = "black")

	#BINDING

	c.bind("<Button-1>", add_sand)
	c.bind('<Button-3>', remove_sand)
	but.bind('<Button-1>', loop)
	but.bind('<Button-3>', push_once)
	but_clear.bind('<Button-1>', remove_all)
	pushes_button.bind('<Button-1>', get_pushed)
	button1.bind("<Button-1>",getV)
	number_of_pushings_button.bind('<Button-1>', print_number_of_pushings)
	#button_for_checking_random_pushing.bind('<Button-1>', randomize_it)

	#PACKING

	but_clear.pack(side = 'left')
	but.pack(side = 'left')
	anotherc.pack(side = 'right')
	scale1.pack(side = 'right')
	button1.pack(side = 'right')
	pushes_scale.pack(side = 'bottom')
	pushes_button.pack(side = 'bottom')
	#button_for_checking_random_pushing.pack()
	number_of_pushings_button.pack()
	c.pack(side = 'top')

	draw_matrix(matrix, n, m, c)
	draw_colors()

	root.mainloop()


def pack_for_checking_random():			#функция, создающая два окна, в одном из них визуализируется случайное пересыпание, в другом - обычное
	#BUTTONS SCALES CANVAS FOR IT
	global root, c, anotherc, but, but_clear, scale1, pushes_scale, button1, pushes_button, number_of_pushings_button, random_root, random_c, random_pushes_scale, random_number_of_pushings_button
	global randomn, randomm, number_of_random_pushings, random_matrix, WIDTH, HEIGHT, const, RANDOMHEIGHT, RANDOMWIDTH, random_const, button_for_checking_random_pushing
	randomn = n
	randomm = m
	number_of_random_pushings = 0

	random_matrix = []
	for i in range(n):
		random_matrix.append([0]*m)
	const = 500//(max(m,n))
	random_const = 500//(max(randomm,randomn))

	WIDTH = 550
	HEIGHT = 550
	RANDOMWIDTH = 550
	RANDOMHEIGHT = 550

	root = Tk()
	c = Canvas(root, width = WIDTH, height = HEIGHT)
	anotherc = Canvas(root, width = 20, height = 255*colorconst)
	but = Button(root, text = "PUSH SAND", bg="white",fg = "black") 
	but_clear = Button(root, text = "CLEAR", bg="white",fg = "black")
	scale1 = Scale(root, orient=VERTICAL, length=510, from_=0, to=510, tickinterval = 50, resolution = 5)
	pushes_scale = Scale(root, orient=HORIZONTAL, length=500, from_=1, to = 30, tickinterval = 2, resolution = 1)
	button1 = Button(root, text="Change sand number", bg="white",fg = "black")
	pushes_button = Button(root, text = 'Change pushes speed', bg="white",fg = "black")
	number_of_pushings_button = Button(root, text = 'Number of pushings: 0; number of random pushings: 0', bg="white",fg = "black")

	#BUTTONS SCALES CANVAS FOR RANDOM
	random_root = Tk()
	random_c = Canvas(random_root, width = RANDOMWIDTH, height = RANDOMHEIGHT)
	button_for_checking_random_pushing = Button(random_root, text = 'Being checked')

	#BINDING

	c.bind("<Button-1>", add_sand)
	c.bind('<Button-3>', remove_sand)
	but.bind('<Button-1>', loop)
	but.bind('<Button-3>', push_once)
	but_clear.bind('<Button-1>', remove_all)
	pushes_button.bind('<Button-1>', get_pushed)
	button1.bind("<Button-1>",getV)
	number_of_pushings_button.bind('<Button-1>', print_number_of_pushings)

	#PACKING

	but_clear.pack(side = 'left')
	anotherc.pack(side = 'right')
	scale1.pack(side = 'right')
	button1.pack(side = 'right')
	pushes_scale.pack(side = 'bottom')
	pushes_button.pack(side = 'bottom')
	number_of_pushings_button.pack(side = 'top')
	c.pack(side = 'top')
	but.pack(side = 'top')
	random_c.pack()
	button_for_checking_random_pushing.pack(side = 'bottom')

	draw_matrix(matrix, n, m, c)
	draw_matrix(random_matrix, randomn, randomm, random_c)
	draw_colors()

	root.mainloop()
if mode == 1:
	pack_for_just_doing_it()
elif mode == 2:
	pack_for_checking_random()
