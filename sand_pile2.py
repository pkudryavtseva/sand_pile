from tkinter import *
import time

n, m = 10, 10 				#n - row and height , m - column and width!!!
n, m = map(int, input().split())

colorconst = 2

VELOCITY = 100

COLORS = ['0','1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']

number_of_pushings = 0

matrix = []
for i in range(n):
	matrix.append([0]*m)

CHECK_FOR_STOPPING_THE_LOOP = None

sandy = 0

#ФУНКЦИИ ДОБАВЛЕНИЯ/УБИРАНИЯ ПЕСКА

def add_sand(event):
	global WIDTH, HEIGHT, m, n, matrix, sandy
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
		matrix[y][x] += sandy
		matrix_square(x, y, matrix[y][x])

def remove_sand(event):
	global WIDTH, HEIGHT, m, n, matrix
	c = event.widget
	x = event.x 
	y = event.y 
	x /= const
	y /= const
	x = int(x) - 1
	y = int(y) - 1
	if x < m and y < n:
		matrix[y][x] = 0
		matrix_square(x, y, matrix[y][x])

def remove_all(event):
	global WIDTH, HEIGHT, m, n, matrix, number_of_pushings
	for i in range(n):
		for k in range(m):
			matrix[i][k] = 0
	number_of_pushings = 0
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

#ФУНКЦИИ РАССЫПАНИЯ ПЕСКА

def check_size():
	global n, m, matrix
	#print('hello')
	counter = 0
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
	print(timeb-timea)
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

#def round1(i, n):
#	if i <= n//2:
#		return 0
#	else:
#		return n-1

#ФУНКЦИИ ЗАЦИКЛИВАНИЯ

def keep_on_pushing():
	global CHECK_FOR_STOPPING_THE_LOOP, number_of_pushings
	renew_const()
	draw_matrix()
	
	if CHECK_FOR_STOPPING_THE_LOOP != False:
		check_size()
		push_sand2()
#		break
	#counter = push_sand()					#работает, но в разы медленнее, чем push_sand2()
	#print(number_of_pushings)
	c.after(VELOCITY, keep_on_pushing)

def stop_the_loop(event):
	global CHECK_FOR_STOPPING_THE_LOOP
	if CHECK_FOR_STOPPING_THE_LOOP == None:
		CHECK_FOR_STOPPING_THE_LOOP = False
	else:
		CHECK_FOR_STOPPING_THE_LOOP = None

def loop(event):
	CHECK_FOR_STOPPING_THE_LOOP = None
	keep_on_pushing()


const = 500//(max(m,n))

WIDTH = (m+1)*const
HEIGHT = (n+1)*const

root = Tk()
c = Canvas(root, width = WIDTH, height = HEIGHT)
anotherc = Canvas(root, width = 20, height = 255*colorconst)
but = Button(root, text = "PUSH SAND", width = 30,height = 5, bg="white",fg = "black") 
but2 = Button(root, text = "STOP", width = 30,height = 5, bg="white",fg = "black")

draw_matrix()
draw_colors()

c.bind("<Button-1>", add_sand)
c.bind('<Button-3>', remove_sand)
but.bind('<Button-1>', loop)
but.bind('<Button-3>', remove_all)
but2.bind('<Button-1>', stop_the_loop)

scale1 = Scale(root, orient=VERTICAL, length=510, from_=0, to=510, tickinterval = 50, resolution = 5)
button1 = Button(root, text="New sand number")

button1.bind("<Button-1>",getV)

but2.pack(side = 'left')
anotherc.pack(side = 'right')
scale1.pack(side = 'right')
button1.pack(side = 'right')
but.pack()
c.pack()

root.mainloop()
