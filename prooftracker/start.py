
import sys
import os

from .classes import App, ZenonProof, GoelandProof
from .utils import analyze

OPTIONS = {
	'-solver'       : (1, 'Zenon'),
	'-file'         : (1, None),
	'-aux'          : (1, None),
	'--aux'         : (0, False),
	'--elements'    : (0, False),
	'--debug'       : (0, False),
	'--dev'         : (0, False),
	'--clean'       : (0, False),
	'--unwind'      : (0, False), 
	'--slow'        : (0, False),
	'--help'        : (0, False),
	'-depth'        : (1, None),
	'-nb-rules'     : (1, None),
	'-max-recursion': (1, 6),
	'-max-width'    : (1, 500),
	'--collapse'    : (1, False)
}

class UserError(BaseException):
	pass

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
	app.proof.update_depths()
	cond = []
	if not options['--unwind']:
		cond += [lambda node: 'target' not in node.properties]
	if options['-depth'] is not None:
		cond += [lambda node: node.depth < int(options['-depth'])]
	if options['-nb-rules'] is not None:
		cond += [lambda node: node.properties['nb_rules'] < int(options['-nb-rules'])]
	if cond:
		app.proof.root.apply(lambda node: node.properties.update({'nb_rules': (0 if node.parent is None else node.parent.properties['nb_rules']+(1 if node.properties['text'].startswith('next_branch') else 0))}))
		def rec(node):
			for child in list(node.children):
				checks = list(map(lambda i: i(child), cond))
				if not all(checks):
					node.children.remove(child)
					app.proof.nodes.remove(child)
				rec(child)
		rec(app.proof.root)
		app.proof.noded_steps = list(map(lambda step: tuple(filter(lambda node: node in app.proof.nodes, step)), app.proof.noded_steps))
	app.proof.nodes.sort(key=lambda node: node.index)
	app.proof.update_depths()
	app.proof.update_coords(app.font)
	if options['--elements']:
		import tkinter as tk
		w = tk.Tk()
		w.title('Elements')
		t = tk.Text(w, font=["Helvetica", 12])
		for key, val in app.proof.elements.items():
			s = str(key)+' : '+val
			lim = 50
			if len(s) > lim:
				s = s[:lim]+'...'
			t.insert(tk.END, s+'\n')
		t.pack(fill=tk.BOTH, expand=True)
	app.display(margin=10, lines=True, focus=app.proof.root)
	if options['--dev']:
		from mylib import idle
		idle('#end of lirmm', globals(), locals())

def start(args: [str]):
	options = analyze(args, OPTIONS)
	if options['-aux'] or options['--aux']:
		from .auxruns import auxrun
		auxrun(options)
	elif options['--help']:
		display_help(options)
	else:
		try:
			init(options)
		except UserError as err:
			print(str('\n').join(err.args))

def display_help(options):
	print('no documentation yet')