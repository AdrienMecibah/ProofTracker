
from .classes import method

@method
def __init__(self, parent=None, properties=None, children=None, index=-1, depth=-1, debug=False, auto_affect_children = False,):
	do(unpackingmap(self.__setattr__, type(self).attributes.items()))
	self.parent = parent
	self.children = [] if children is None else children
	self.properties = {} if properties is None else properties
	self.index = index
	self.depth = depth
	self.width = -1.0
	self.height = -1.0
	self.left = -1.0
	self.mid = -1.0
	self.top = -1.0
	self.visible = True
	self.collapsed = False
	self.canvas_id = None
	if debug:
		print('new node with index', index)
	if auto_affect_children and parent is not None:
		parent.children.append(self)

@method
def __getitem__(self, key):
	return self.children[key]

@method
def __repr__(self):
	return str(self)

@method
def __len__(self):
	return len(self.children)

@method
def __iter__(self):
	return iter(self.children)

@method
def __repr__(self):
	return str(self)

@method
def __str__(self):
	return '<'+type(self).__name__+' index=' + str(self.index)+' depth=' + str(self.depth) +' properties=' + str(self.properties)+' geometry=' + str(+self) + ' children:[' + str(len(self.children)) + '] canvas_id='+str(self.canvas_id)+'>'

@method
def __pos__(self):
	str = lambda x: int(x).__str__()
	return str(self.width)+'x'+str(self.height)+'+'+str(self.left)+'+'+str(self.top)