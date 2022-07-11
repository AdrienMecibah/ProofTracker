
from .classes import method, Proof

@method
def __init__(self, proof_type, options, fontname="Helvetica", fontsize=15):
	if not issubclass(proof_type, Proof):
		return TypeError('proof_type parameter is not a Proof')
	self.proof = proof_type()
	self.proof.app = self
	self.win = None
	self.font = [fontname, fontsize]
	self.default_font = [fontname, fontsize]
	self.title = 'Graphic'
	self.options = options
	self.stage = 0

@method
def display(self, margin=5, lines=True, focus=None):
	self.win = Win(self.font)
	self.win.app = self
	self.win.prep()
	self.stage = 1
	if self.options['--slow']:
		self.draw(1, margin, lines, focus=focus)
	else:
		self.draw(len(self.proof.noded_steps), margin, lines, focus=focus)
	self.win.mainloop()

@method
def click(self, node, **kwargs):
	if self.options['--slow']:
		if any(map(lambda child: child.visible, node.children)):
			node.apply(lambda node: setattr(node, 'visible', False))
			node.apply(lambda node: setattr(node, 'collapsed', bool(node.children)))
			node.visible = True
		else:
			for child in node.children:
				child.visible = True	
			node.collapsed = False		
	else:
		node.collapsed = not node.collapsed
		if node.collapsed:
			node.apply(lambda n: setattr(n, 'collapsed', False))
			node.apply(lambda n: setattr(n, 'visible', False))
			node.collapsed = True
			node.visible = True
		else:
			node.apply(lambda n: setattr(n, 'collapsed', False))
			node.apply(lambda n: setattr(n, 'visible', True))
			node.collapsed = False
			node.visible = True
	self.proof.update_coords(self.font)
	self.draw(**kwargs)

@method
def draw(self, step=None, margin=5, lines=False, focus=None):
	if step is None:
		step = self.stage 
	nodes = self.proof.nodes
	self.win.canvas.delete('all')
	if self.options['--unwind']:
		for st in self.proof.noded_steps[:max(0, step-1)]:
			for node in st:
				if not node.visible:
					continue
				if node.properties.get('unwinding') is True:
					target = node.properties.get('target')
					if target is not None:
						self.win.canvas.create_line(
							int(node.left-margin), int(node.top+node.height/2),
							int(node.left-node.height/2-2*margin), int(node.top+node.height/2),
							width = 1.5,
							fill = 'red',
							)
						self.win.canvas.create_line(
							int(node.left-node.height/2-2*margin), int(node.top+node.height/2),
							int(target.left-target.height/2-2*margin), int(target.top+target.height/2),
							width = 1.5,
							fill = 'red',
							)
						self.win.canvas.create_line(
							int(target.left-target.height/2-2*margin), int(target.top+target.height/2),
							int(target.left-margin), int(target.top+target.height/2),
							width = 1.5,
							fill = 'red',
							arrow = 'last',
							)	
	if lines and False:
		for st in self.proof.noded_steps[:max(0, step-1)]:
			for node in st:
				for child in node.children:
					if not child.visible:
						continue
					self.win.canvas.create_line(
						int(node.left+node.width/2), int(node.top-margin),
						int(child.left+child.width/2), int(child.top+child.height+margin),
						width = 2,
						arrow = 'last',
						)
	i = 0
	for st in self.proof.noded_steps[:max(0, step)]:
		for node in st:
			if not node.visible:
				continue
			i += 1
			fl = 'SkyBlue1'
			if node.properties.get('type') == 'inst':
				opt = dict(
					fill = fl if node.collapsed else 'white',
					dash = (1, 1),
					)
			else:# node.properties['type'] == 'action':
				opt = dict(
					fill = fl if node.collapsed else ('green3' if 'next_branch' in node.properties['text'] else 'lightgray'),
					)
			tmp = self.win.canvas.create_rectangle(
				int(node.left-margin), int(node.top-margin),
				int(node.left+node.width+margin), int(node.top+(1*node.height)+margin),
				**opt
				)
			node.canvas_id = tmp
			j = node.index
			if self.options['--debug']:
				self.win.canvas.tag_bind(tmp, '<ButtonPress-3>', lambda ev, n=node: print(n))
			if self.options['--collapse']:
				self.win.canvas.tag_bind(tmp, '<ButtonPress-1>', lambda ev, n=node: self.click(n, step=step, margin=margin, lines=lines))
			font = self.font#(self.font[0], int(self.font[1]))
			tmp = self.win.canvas.create_text(
				int(node.left), int(node.top),
				anchor = 'nw',
				text = ('' if True else str({node.index})+' ')+(node.properties['text']),
				tag = 'text',
				font = (font[0], int(font[1])),
				)
			if node.parent is not None:
				self.win.canvas.create_line(
					int(node.parent.left+node.parent.width/2), int(node.parent.top-margin),
					int(node.left+node.width/2), int(node.top+node.height+margin),
					width = 2,
					arrow = 'last',
					)
			if self.options['--debug']:
				self.win.canvas.tag_bind(tmp, '<ButtonPress-3>', lambda ev, n=node: print(n))
			if self.options['--collapse']:
				self.win.canvas.tag_bind(tmp, '<ButtonPress-1>', lambda ev, n=node: self.click(n, step=step, margin=margin, lines=lines))
	self.win.canvas.configure(scrollregion=self.win.canvas.bbox('all'))
	if focus is not None and focus.canvas_id is not None:
		self.win.scroll_to(focus)
	else:
		try:
			f = list(sorted(self.proof.noded_steps[step-1], key=lambda node: node.top))[0]
			if self.options['--dev']:
				print(f.properties['text'][:30])
			self.win.scroll_to(f, safe=False)
		except:
			import traceback; traceback.print_exc()
			if self.options['--dev']:
				from mylib import idle; idle('#fail scroll_to', globals(), locals())
			else:
				exit()
	if self.options['--dev']:
		from mylib import idle
		idle("#end of draw", globals(), locals())