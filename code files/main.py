#Made by Pradyun Beerla

#pip install tkinter
'''Note : There are some other digital assests that you will require before running this code. Check them in the 'Digital Assets' folder'''

from tkinter import *
from tkinter import colorchooser,messagebox,filedialog
import PIL.ImageGrab as ImageGrab
import win32api
from extra_assets import *

root = Tk()
root.title("MetaPaint")
root.iconbitmap("metapaint.ico")
root.state('zoomed')
root.config(background="white")
mousecords = Label(root, bg='white')
mousecords.place(x=10, y=662)

class paint():
	def __init__(self):
		self.justErased = False
		self.pen_color = "black"
		self.eraser_color = "white"
		self.saveImg = False
		self.doPaint = True
		self.squareDraw = False
		self.colour_frame = LabelFrame(root, text='Color Palette',font= ('arial',15), bd=7, relief=RIDGE,bg='white')
		self.colour_frame.place(x=1100, y=5, width=170, height=90)
		colors = ['red', 'yellow', 'green', 'blue', 'violet', 'dark blue', 'black', 'grey', 'orange', 'magenta', 'pink', 'purple']
		i=0
		j=0
		for color in colors:
			Button(self.colour_frame, bg=color,bd=2,relief=RIDGE, width=2, command=lambda col=color:self.select_color(col)).grid(row=i, column=j, padx=1, pady=2)
			j+=1
			if j==6:
				j=0
				i=1

		self.menubar = Menu(root)
		self.menu1 = Menu(root, tearoff=0)
		self.menu1.add_command(label="Save File", command=self.save_paint)
		self.menu1.add_separator()
		self.menu1.add_command(label="Exit", command=root.destroy)
		self.menubar.add_cascade(label="File", menu=self.menu1)
		self.menu2 = Menu(self.menubar, tearoff=0)
		self.menu2.add_command(label="Undo", command=self.undo)
		self.menubar.add_cascade(label="Options", menu=self.menu2)

		root.config(menu=self.menubar)

		self.eraser = Button(root, text='Eraser',bd=4,bg='white', command=self.erase, width=8, relief=RIDGE)
		self.eraser.place(x=1017, y=20)

		self.clear = Button(root, text='Clear',bd=4,bg='white', command=lambda : self.canvas.delete("all"), width=8, relief=RIDGE)
		self.clear.place(x=1017, y=64)

		self.save = Button(root, text='Save',bd=4,bg='white', command=self.save_paint, width=8, relief=RIDGE)
		self.save.place(x=927, y=64)

		self.canvas_button = Button(root, text='Background',bd=4,bg='white', command=self.canvas_color, width=9, relief=RIDGE)
		self.canvas_button.place(x=927, y=20)

		self.pensize_frame = LabelFrame(root, text='Size', bd=5, bg='white', font=('arial', 15, 'bold'), relief=RIDGE)
		self.pensize_frame.place(x=700, y=10, height=80, width=205)

		self.pensize = Scale(self.pensize_frame, orient=HORIZONTAL, from_ = 1, to = 10, length=170, bg='white')
		self.pensize.set(1)
		self.pensize.grid(row=0, column=0, padx=10)
 
		self.canvas = Canvas(root, bg='white', bd=5, relief=GROOVE, height=545, width=1330, cursor="pencil")
		self.canvas.place(x=10,y=105)

		self.squareImg = PhotoImage(file="square.png")
		self.square = Button(root,bd=4, image=self.squareImg, command=self.makeSquare)
		self.square.place(x=630, y=8, height=45, width=45)

		self.paintImg = PhotoImage(file="brush.png")
		self.paint_button = Button(root, image=self.paintImg, bd=4, command=self.startPaint)
		self.paint_button.place(x=580, y=55)

		self.circleImg = PhotoImage(file="circle.png")
		self.circle_button = Button(root, image=self.circleImg, bd=4, command=self.drawCircle)
		self.circle_button.place(x=580, y=8, height=45, width=45)

		self.lineImg = PhotoImage(file="line.png")
		self.line_button = Button(root, text='Line', bd=4, command=self.drawLine, image=self.lineImg)
		self.line_button.place(x=530, y=8, height=45, width=45)

		self.undoImg = PhotoImage(file="undo.png")
		self.undo_button = Button(root, image=self.undoImg, bd=4, command=self.undo)
		self.undo_button.place(x=470, y=8, height=45, width=45)

		createMessage(self.eraser, text = 'Eraser\n\n'
							'This tool can erase anything\n'
							'drawn on the canvas with your\n'
							'preferred size')

		createMessage(self.clear, text = 'Clear\n\n'
							'This function clears\n'
							'anything drawn on the screen\n'
							'and resets the board\n\n'
							'Keyboard Binding - Ctrl+D')

		createMessage(self.save, text = 'Save\n\n'
							'This saves your drawn\n'
							'screen into a JPG image file\n\n'
							'Keyboard Binding - Ctrl+S')

		createMessage(self.canvas_button, text = 'Background\n\n'
							'This tool changes and fills\n'
							'your entire screen background\n'
							'to your preferred solid color')

		createMessage(self.square, text = 'Square\n\n'
							'Draw a square of preferred\n'
							'size and color')

		createMessage(self.paint_button, text = 'Draw\n\n'
							'Paint and scribble anything on screen\n'
							'with preferred brush color')

		createMessage(self.circle_button, text = 'Circle\n\n'
							'Draw a circle of preferred\n'
							'size and color')

		createMessage(self.line_button, text = 'Line\n\n'
							'Draw straight lines with any\n'
							'length and your preferred color')

		createMessage(self.undo_button, text = 'Undo\n\n'
							'You can undo your last\n'
							'changes done on the\n'
							'screen with this tool\n\n'
							'Keyboard Binding - Ctrl+Z')

		root.protocol("WM_DELETE_WINDOW", self.onClose)

		self.canvas.bind("<B1-Motion> ",self.paint)
		root.bind("<Control-z>", self.undo_starter)
		root.bind("<Control-s>", self.save_paint_starter)
		root.bind("<Control-d>", self.clearScreen)

		self.stack = []
		self.drawnlines = []

	def save_paint_starter(self, event):
		self.save_paint()

	def clearScreen(self, event):
		self.canvas.delete("all")

	def undo_starter(self, event):
		self.undo()

	def undo(self):
		if len(self.stack) != 0:
			a = self.stack.pop()
			self.canvas.delete(a)

	def drawLine(self):
		self.canvas.config(cursor='cross')
		self.canvas.bind("<ButtonPress-1>", self.on_button_press_line)
		self.canvas.bind("<B1-Motion>", self.on_move_press_line)
		self.canvas.bind("<ButtonRelease-1>", self.on_button_release_line)

		self.x = self.y = 0

		self.circle1 = None

		self.start_x1 = None
		self.start_y1 = None


	def drawCircle(self):
		self.canvas.config(cursor='tcross')
		self.canvas.bind("<ButtonPress-1>", self.on_button_press_circle)
		self.canvas.bind("<B1-Motion>", self.on_move_press_circle)
		self.canvas.bind("<ButtonRelease-1>", self.on_button_release_circle)
		self.x = self.y = 0

		self.circle = None

		self.start_x = None
		self.start_y = None

	def makeSquare(self):
		self.canvas.config(cursor='plus')
		self.canvas.bind("<ButtonPress-1>", self.on_button_press)
		self.canvas.bind("<B1-Motion>", self.on_move_press)
		self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
		self.x = self.y = 0

		self.rect = None

		self.start_x = None
		self.start_y = None

	def on_button_press_line(self, event):
		self.start_x1 = event.x
		self.start_y1 = event.y
		if self.justErased == True:
			self.rect1 = self.canvas.create_line(self.x, self.y, 1, 1, width=self.pensize.get()*2, fill='black')
			self.justErased = False
		else:
			self.rect1 = self.canvas.create_line(self.x, self.y, 1, 1, width=self.pensize.get()*2, fill=self.pen_color)
		self.stack.append(self.rect1)

	def on_move_press_line(self, event):
		rectX1, rectY1 = (event.x, event.y)
		self.canvas.coords(self.rect1, self.start_x1, self.start_y1, rectX1, rectY1)
 
	def on_button_release_line(self, event):
		pass

	def on_button_press_circle(self, event):
	    self.start_x = event.x
	    self.start_y = event.y
	    if self.justErased == True:
	    	self.rect = self.canvas.create_oval(self.x, self.y, 1, 1, fill="", width=self.pensize.get()*2, outline='black')
	    	self.justErased = False
	    else:
	    	self.rect = self.canvas.create_oval(self.x, self.y, 1, 1, fill="", width=self.pensize.get()*2, outline=self.pen_color)	
	    self.stack.append(self.rect)
	def on_move_press_circle(self, event):
	    rectX, rectY = (event.x, event.y)
	    self.canvas.coords(self.rect, self.start_x, self.start_y, rectX, rectY)    

	def on_button_release_circle(self, event):
		pass

	def startPaint(self):
		self.canvas.config(cursor='pencil')
		self.pen_color = self.pen_color
		self.canvas.bind("<B1-Motion> ",self.paint)

	def on_button_press(self, event):
	    self.start_x = event.x
	    self.start_y = event.y
	    if self.justErased == True:
	    	self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, tags='rect', fill="", width=self.pensize.get()*2, outline='black')
	    	self.justErased = False
	    else:
	    	self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, tags='rect', fill="", width=self.pensize.get()*2, outline=self.pen_color)
	    self.stack.append(self.rect)

	def on_move_press(self, event):
	    rectX, rectY = (event.x, event.y)
	    self.canvas.coords(self.rect, self.start_x, self.start_y, rectX, rectY)    

	def on_button_release(self, event):
	    pass

	def paint(self, event):
		x1, y1 = (event.x-2),(event.y-2)
		x2, y2 = (event.x+2),(event.y+2)
		if self.justErased == True:
			self.drawLine = self.canvas.create_oval(x1, y1, x2, y2, fill='black', outline='black', width=self.pensize.get()*4)
			self.justErased = False
		else:
			self.drawLine = self.canvas.create_oval(x1, y1, x2, y2, fill=self.pen_color, outline=self.pen_color, width=self.pensize.get()*4)
		self.drawnlines.append(self.drawLine)
	def select_color(self, col):
		self.pen_color = col

	def erase(self):
		self.justErased = True
		self.canvas.bind("<B1-Motion> ",self.paint)
		self.pen_color = self.eraser_color
		self.canvas.config(cursor='dotbox')

	def canvas_color(self):
		color = colorchooser.askcolor()
		self.canvas.config(background=color[1])
		self.eraser_color = color[1]

	def save_paint(self):
		try:
			filename = filedialog.asksaveasfilename(title='Save File As', filetypes=(('JPG Files', '*.jpg'),('All Files', '*.*')), defaultextension='.jpg')
			x = root.winfo_rootx() + self.canvas.winfo_x()
			y = root.winfo_rooty() + self.canvas.winfo_y()

			x1 = x + self.canvas.winfo_width()
			y1 = y + self.canvas.winfo_height()

			ImageGrab.grab().crop((x, y, x1, y1)).save(filename)
			messagebox.showinfo('MetaPaint', 'Image has been saved in ' + str(filename))
			self.saveImg = True

		except:
			messagebox.showerror("MetaPaint", "Something went wrong\nUnable to save file")

	def onClose(self):
		if self.saveImg == False:
			respo = messagebox.askokcancel("MetaPaint", "Any unsaved changes may be lost", icon="warning")
			if respo == 1:
				root.quit()

			else:
				pass

		else:
			root.quit()

def mousepos():
	x, y = win32api.GetCursorPos()
	mousecords.config(text=f'x : {x}, y : {y}')
	mousecords.after(1, mousepos)

if __name__ == '__main__':
	paint()
	mousepos()
	root.mainloop()

#THE END
