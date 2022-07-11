
from .classes import *
from .utils import *

import os


# Choose the default function to call if `--auxrun` argument is specified and not `-auxrun` ───────┐
#                                                                                                  ↓        
def auxrun(options): globals()[options['-auxrun']](options) if options['-auxrun'] is not None else info(options) 

# ──────────────────────────────────────────────────────────────────────────────────────────────────

def init(options):
	sys.setrecursionlimit(10**(options['-max-recursion']))
	file = options['-file'] 
	if file is None:
		raise UserError('No file specified')
	elif not os.path.exists(file):
		raise UserError('File "'+file+'" does not exist')
	if options['-solver'] is None:
		raise UserError('No solver specified with -solver')
	elif options['-solver'].lower() in ('z', 'zen', 'zenon'):
		proof_type = ZenonProof
	elif options['-solver'].lower() in ('g', 'go', 'goeland', 'goéland'):
		proof_type = GoelandProof
	else:
		raise UserError('Unkwnon solver "'+options['-solver']+'"')
	app = App(proof_type, options)
	app.proof.load_file(file)
	app.proof.update_coords(app.font)
	app.display(margin=10, lines=True)


def prgl(options):
	import sys
	sys.setrecursionlimit(10**6)
	file = options['-file'] 
	assert file is not None
	from .classes import App, GoelandProof
	app = App(GoelandProof, options)
	app.proof.load_file(file)
	app.proof.update_coords(app.font)
	app.display(margin=10, lines=True)
	

def to_dot(options):
	file = options['-file'] 
	assert file is not None
	app = App(ZenonProof)
	app.proof.load_file(file)
	result = 'digraph G {\nrankdir=BT;\n'
	result += app.proof.root.apply(
		lambda node: \
			str(node.index)+' [shape=record,style=filled,label="{'+     
			(node.properties['text'] \
			if type(	node) == Action else \
			str('|').join(node.properties['lines']))+
			'}"];\n',
		str.__add__,
		)
	result += app.proof.root.apply(
		lambda node: str().join(map(
			lambda child: '    '+str(node.index)+'-->'+str(child.index)+'\n',
			node.children,
			)),
		str.__add__,
		)
	result += '}'
	print(result)


def info(options):
	print(os)
	output = {}
	def rec(folder):
		nonlocal output
		result = 0
		for name in os.listdir(folder):
			path = join(folder, name)
			if os.path.isdir(path):
				result += rec(path)
				continue
			if not path.endswith('.py'):
				continue
			with open(path, encoding='UTF-8') as f:
				if options['--clean']:
					nb = len(list(filter(bool, f.read().split('\n'))))
				else:
					nb = len(f.read().split('\n'))
			result += nb
			output[path] = nb
		return result	
	total = rec(os.path.dirname(__file__))
	indent = max(map(len, output.keys()))
	longuest = max(map(lambda nb: len(str(nb)), output.values()))
	for p, nb in output.items():
		print(p, end='')
		print(str(' ')*(indent-len(p)), end=' +')
		print(str(' ')*(longuest-len(str(nb))), end='')
		print(nb)
	print(str(' ')*(indent+len(' +')+longuest-len('=')-len(str(total)))+'='+str(total))


def test_lzf(options):
	file = options['-file'] 
	assert file is not None
	app = App(ZenonProof)
	app.proof.load_file(file)
	for step in app.proof.steps[:4]:
		print(repr(step))
	print('end of test')


def test_apply_method(options):
	def generate(lim, lv=1):
		import random
		node = {'children': [], 'properties': {'val': random.randrange(8, 21)}} 
		if lim <= lv:
			return node
		for c in range(2):#random.randrange(1, 4)):
			node['children'].append(generate(lim, lv=lv+1))
		return node
	app = App()
	app.filters.append(lambda node: type(node['properties'].get('val')) == int)
	app.load(generate(3))
	mx = app.apply(lambda node: print(node.depth*str('    '), node, sep=''))
	mx = app.apply(lambda node: node.properties['val'], max)