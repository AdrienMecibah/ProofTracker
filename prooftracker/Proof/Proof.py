
from .classes import method

@method
def __init__(self):
	self.elements = []
	self.root = None
	self.nodes = []
	self.app = None

@method
def load_file(self, *args, **kwargs):
	raise BaseException('Should have been implemented by subclass')

@method
def update_depths(self):
	self.root.apply(lambda node: setattr(node, 'depth', (0 if node.parent is None else node.parent.depth+1)))

@method
def update_coords(self, font):
	self.update_depths()
	hspacing = 250
	vspacing = 100
	max_height = 1000
	max_width = int(self.app.options['-max-width'])
	...
	nodes = list(filter(lambda node: node.visible, self.nodes))
	largest = dict(map(lambda key: (key, -hspacing), set(map(lambda node: node.depth, nodes))))
	heights = dict(map(lambda key: (key, 0), set(map(lambda node: node.depth, nodes))))
	levels = dict(map(lambda key: (key, []), set(map(lambda node: node.depth, nodes))))
	w = tk.Tk()
	cv = tk.Canvas(w)
	cv.pack()
	for node in nodes:
		tag = cv.create_text(0, 0, anchor='nw', text=(node.properties['text']), font=(font[0], int(font[1])))
		l, t, r, b = cv.bbox(tag)
		node.width = (r-l)
		node.height = (b-t)
		if node.width > max_width or b-t > max_height:
			text = ''
			i = 0
			while i < 100000:
				text += node.properties['text'][i]
				cv.itemconfigure(tag, text=text+'...')
				l, t, r, b = cv.bbox(tag)
				if r-l > max_width or b-t > max_height:
					break
				i += 1
			else:
				raise ValueError()
			text = text[:-1]
			node.width = (r-l)
			node.height = (b-t)
			node.properties['text'] = text + '...'
	w.destroy()
	del w
	for node in nodes:
		largest[node.depth] += node.width + hspacing
		heights[node.depth] = max((heights[node.depth], min(node.height, max_height))) # + self.vertical_spacing
		if node not in levels[node.depth]:
			levels[node.depth] += [node]
	deepest = max(largest)
	altitude = sum(heights.values()) + vspacing * (deepest)
	for dp, level in levels.items():
		for node in level:
			node.top = altitude - heights[dp]
		altitude += -(heights[dp]+vspacing)
	interest = list(filter(lambda node: largest[node.depth] == max(largest.values()), nodes))
	assert interest
	handled = []
	lat = hspacing
	for node in interest:
		node.left = lat
		lat += node.width + hspacing
		handled += [node]
	middle = lambda node: node.left + node.width / 2
	def up(node):
		if node.children:
			if len(node.children) % 2:
				mid = node.children[len(node.children)//2]
				mid.left = middle(node) - mid.width/2
				lat = mid.left
				c = len(node.children)//2 - 1
				while c >= 0:
					lat += -(hspacing+node.children[c].width)
					node.children[c].left = lat
					c += -1
				c = len(node.children)//2 + 1
				lat = mid.left + mid.width + hspacing
				while c < len(node.children):
					node.children[c].left = lat
					lat += node.children[c].width + hspacing
					c += 1
			else:
				lat = middle(node) + hspacing/2
				c = len(node.children)//2 - 1
				while c >= 0:
					lat += -(hspacing+node.children[c].width)
					node.children[c].left = lat
					c += -1
				lat = middle(node) - hspacing/2
				c = len(node.children)//2
				while c < len(node.children):
					lat += node.children[c].width + hspacing
					node.children[c].left = lat
					c += 1
			for child in node.children:
				up(child)
	def down(node):
		if node is not None:
			handled.append(node)
			if len(node.children) % 2:
				mid = node.children[len(node.children)//2]
				node.left = middle(mid) - node.width / 2
			elif len(node.children):
				midleft = node.children[len(node.children)//2-1]
				midright = node.children[len(node.children)//2]
				node.left = (middle(midleft) + middle(midright)) / 2 - node.width
			down(node.parent)
	for node in interest:
		down(node)
		up(node)


@method
def update_coords(self, font):
	self.update_depths()
	hspacing = 250
	vspacing = 100
	max_height = 300
	max_width = int(self.app.options['-max-width'])
	...
	w = tk.Tk()
	cv = tk.Canvas(w)
	cv.pack()
	for node in self.nodes:
		tag = cv.create_text(0, 0, anchor='nw', text=(node.properties['text']), font=(font[0], int(font[1])))
		l, t, r, b = cv.bbox(tag)
		node.width = (r-l)
		node.height = (b-t)
		if node.width > max_width or b-t > max_height:
			text = ''
			i = 0
			while i < 100000:
				text += node.properties['text'][i]
				cv.itemconfigure(tag, text=text+'...')
				l, t, r, b = cv.bbox(tag)
				if r-l > max_width or b-t > max_height:
					break
				i += 1
			else:
				raise ValueError()
			text = text[:-1]
			node.width = (r-l)
			node.height = (b-t)
			node.properties['text'] = text + '...'
	w.destroy()
	del w
	...
	grid = {}
	def f(node, x, y):
		grid[node] = (x, y)
		a = 0
		while (x+a, y+1) in grid.values():
			a += 1
		for i, child in enumerate(node.children):
			f(child, x+a+i, y+1)
		...
	f(self.root, 0, 0)
	width = max(map(lambda coord: coord[0], grid.values()))
	height = max(map(lambda coord: coord[1], grid.values()))
	grid = dict(map(lambda key: (key, (grid[key][0], height-grid[key][1])), grid))
	largest = dict(map(lambda x: (x, 0), range(width+1)))
	for x in range(width+1):
		for node in self.nodes:
			if grid[node][0] == x:
				largest[x] = max(largest[x], node.width)
	tallest = dict(map(lambda y: (y, 0), range(height+1)))
	for y in range(height+1):
		for node in self.nodes:
			if grid[node][1] == y:
				tallest[y] = max(tallest[y], node.height)
	#try:#from mylib import idle; idle('#coords', globals(), locals())
	for node, (x, y) in grid.items():
		node.properties['grid'] = (x, y)
		node.left = -hspacing
		for a in range(x):
			node.left += hspacing + largest[x]
		node.left += largest[x] - node.width/2
		node.top = -vspacing
		for b in range(y):
			node.top += vspacing + tallest[x]
		node.top -= tallest[y]-node.height/2
	