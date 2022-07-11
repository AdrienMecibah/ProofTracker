
import os

import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *

from .classes import method
from .utils import join, BASE_DIR


@method
def __init__(self, font):
	super(type(self), self).__init__()
	do(unpackingmap(self.__setattr__, type(self).attributes.items()))
	self.canvas = None
	self.hs = None
	self.vs = None
	self.pressed = False
	self.app = None


@method
def prep(self):
	if False:
		def f(ev, delta):
			self.app.stage += delta
			self.app.draw(self.app.stage)
		self.bind('<space>', lambda ev: f(ev, 1))
		self.bind('<Shift-space>', lambda ev: f(ev, -1))
	self.title(self.app.title)
	self.geometry('600x400')
	#self.iconbitmap(join(BASE, 'Win', self.iconfile))
	self.grid_rowconfigure(0, weight=1)
	self.grid_columnconfigure(0, weight=1)
	self.canvas = tk.Canvas(self, scrollregion=tuple(self.scrollregion))
	self.canvas.grid(row=0, column=0, sticky='nswe')
	self.hs = tk.Scrollbar(self, orient=HORIZONTAL, command=self.canvas.xview)
	self.hs.grid(row=1, column=0, sticky='we')
	self.vs = tk.Scrollbar(self, orient=VERTICAL, command=self.canvas.yview)
	self.vs.grid(row=0, column=1, sticky='ns')
	self.canvas.configure(xscrollcommand=self.hs.set, yscrollcommand=self.vs.set)
	self.do_bindings()

@method
def scroll_to(self, node, safe=False):
	if safe and node.canvas_id is None:
		if self.app.options['--debug']:
			print('fails on', node.properties['text'][:30])
		return
	c = self.canvas.bbox('all')
	n = self.canvas.bbox(node.canvas_id)
	x = (n[0])/(c[2]-c[0])
	y = 1-(n[1])/(c[3]-c[1])
	self.canvas.xview_moveto(x)
	self.canvas.yview_moveto(y)
	if self.app.options['--debug']:
		print('success focus on', node.properties['text'][:30], ':', x, y)