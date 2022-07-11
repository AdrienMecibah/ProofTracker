
from .utils import *
from .classes import method


@method
def do_bindings(self):
	self.canvas.bind('<ButtonPress-1>', self.move_start)
	self.canvas.bind('<B1-Motion>', self.move_move)
	self.canvas.bind('<ButtonPress-2>', self.pressed2)
	self.canvas.bind('<Motion>', self.move_move2)
	#linux scroll
	self.canvas.bind('<Button-4>', self.zoomerP)
	self.canvas.bind('<Button-5>', self.zoomerM)
	#windows scroll
	self.canvas.bind('<Control-MouseWheel>', self.zoomer)
	# Hack to make zoom work on Windows
	self.bind_all('<Control-MouseWheel>', self.zoomer)
	...
	self.bind('<space>', lambda ev: self.test(ev, +1))
	self.bind('<Shift-space>', lambda ev: self.test(ev, -1))


@method
def test(self, event=None, incr=1):
	self.app.proof.noded_steps = list(filter(bool, self.app.proof.noded_steps))
	if self.app.options['--slow'] and 0 <= self.app.stage+incr < len(self.app.proof.noded_steps):
		if self.app.options['--debug']:
			print(self.app.stage, '->', self.app.stage+incr)
		self.app.stage += incr
		self.app.draw(lines=True, margin=10)


@method
def move_start(self, event):
	self.canvas.scan_mark(event.x, event.y)

@method
def move_move(self, event):
	self.canvas.scan_dragto(event.x, event.y, gain=1)

@method
def pressed2(self, event):
	self.pressed
	self.pressed = not self.pressed
	self.canvas.scan_mark(event.x, event.y)

@method
def move_move2(self, event):
	if self.pressed:
		self.canvas.scan_dragto(event.x, event.y, gain=1)

#windows zoom
@method
def zoomer(self,event):
	if (event.delta > 0):
		self.canvas.scale('all', event.x, event.y, 1.1, 1.1)
		self.app.font[1] = self.app.font[1] * 1.1
	elif (event.delta < 0):
		self.canvas.scale('all', event.x, event.y, 0.9, 0.9)
		self.app.font[1] = self.app.font[1] * 0.9
	self.canvas.configure(scrollregion = self.canvas.bbox('all'))
	for child_widget in self.canvas.find_withtag('text'):
		self.canvas.itemconfigure(child_widget, font=(self.app.font[0], int(self.app.font[1])))
	#print(self.app.font[1])

#linux zoom
@method
def zoomerP(self,event):
	self.canvas.scale('all', event.x, event.y, 1.1, 1.1)
	self.canvas.configure(scrollregion = self.canvas.bbox('all'))
@method
def zoomerM(self,event):
	self.canvas.scale('all', event.x, event.y, 0.9, 0.9)
	self.canvas.configure(scrollregion = self.canvas.bbox('all'))