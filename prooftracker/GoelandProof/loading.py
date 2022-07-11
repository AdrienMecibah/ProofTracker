
from .utils import *
from .classes import method

@method
def load_file(self, file: str):
	with open(file, 'r', encoding='utf-8') as f:
		file = json.load(f)
	root = tmp(file) # Demander à Julie d'expliquer l'output
	self.root = root
	self.nodes = [root] + self.root.apply(list, list.__add__)
	self.noded_steps = list(map(lambda node: (node, ), self.nodes))

def tmp(file):
	from .classes import Node
	do(map(lambda el: el.update({'Children': []}), file))
	file = list(map(Object.from_dict, file))
	elements = dict(map(lambda el: (el.Name, el), list(reversed(file))))
	for el in file:
		if el.Name not in elements[el.Father].Children and el.Father != el.Name:
			elements[el.Father].Children += [el.Name]
	for el in elements.values():
		print(el.Name, ':', (el.Children))
	children = []
	for el in elements.values():
		children += list(filter(lambda child: child not in children, el.Children))
	roots = list(filter(lambda el: el.Name not in children, elements.values()))
	assert len(roots) == 1
	root = roots[0]
	def r(content, node):
		content[node] = {}
		for c in node.Children:
			r(content[node], elements[c])
	d = {}
	r(d, root)
	el_to_node = lambda el: {'properties': {'text': str(' ; ').join(filter(lambda s: s not in ('{}', ), el.Forms.split(' ; ')))}}
	def r(els, parent):
		for el, ch in els.items():
			node = Node(parent=parent, **el_to_node(el))
			node.parent = parent
			parent.children += [node]
			r(ch, node)
	root = Node(**el_to_node(root))
	r(d, root)
	return root