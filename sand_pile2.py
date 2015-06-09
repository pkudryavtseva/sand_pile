from tkinter import *
import time

n, m = 10, 10 				#n - row and height , m - column and width!!!
n, m = map(int, input().split())


matrix = []
for i in range(n):
	matrix.append([0]*m)

#sandy = 0

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
		sand = int(input())
		matrix[y][x] += sand
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
	global WIDTH, HEIGHT, m, n, matrix
	for i in range(n):
		for k in range(m):
			matrix[i][k] = 0
	draw_matrix()

def colour_square(a):
	if a == 0:
		a = 'white'
	elif a == 1:
		a = 'cyan'
	elif a == 2:
		a = 'steel blue'
	elif a == 3:
		a = 'blue'
	else:
		a = 'red'
	return a


def matrix_square(x, y, a):
	global n, m, const, WIDTH, HEIGHT
	x += 1
	y += 1
	x *= const
	y *= const
	a = colour_square(a)
	c.create_rectangle(x, y, x + const, y + const, outline = "black", fill = a)



def print_matrix(matrix):
	for i in range(len(matrix)):
		print(matrix[i], end = '\n')
	print('wellwellwell')
def round1(i, n):
	if i <= n//2:
		return 0
	else:
		return n-1
def check_counter(a):
	if a > 0:
		a = 1
	return a
def check_size():
	global n, m, matrix
	#print('hello')
	counter = 0
	for i in range(n):
		for k in range(m):
			if matrix[i][k] >= 4:
				#print('cool', i, k)
				if i == 0 or i == n-1 or k == 0 or k == m-1:
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
	



def push_sand():
	global n, m, matrix
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
		return False

def push_sand2():
	global n, m, matrix
	pushed_sand = []
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
	if counter == 0:
		return False




def draw_matrix():
	global matrix
	c.delete(*c.find_all())
	for i in range(n):
		for k in range(m):
			matrix_square(k, i, matrix[i][k])

def keep_on_pushing(event):
	counter = None
	while counter != False:
		draw_matrix()
		check_size()
		#counter = push_sand()					#работает, но в разы медленнее, чем push_sand2()
		counter = push_sand2()


WIDTH = 100*m
HEIGHT = 100*n
const = 20 - (n + m)//4
c = Canvas(width = WIDTH, height = HEIGHT)




root = Tk()
but = Button(root, text="SAND", width = 30,height = 5, bg="white",fg="black") 
but.pack()
draw_matrix()
c.bind("<Button-1>", add_sand)
c.bind('<Button-3>', remove_sand)
root.bind('<Button-1>', keep_on_pushing)
root.bind('<Button-3>', remove_all)



c.pack()
c.mainloop()
