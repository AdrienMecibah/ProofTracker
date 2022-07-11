
import tkinter
import os

from .utils import join, BASE_DIR

def method(function):
	function.instance_method = True
	return function

def get_methods(folder_name, glb, lcl):
	for name in os.listdir(join(BASE_DIR, folder_name)):
		if not name.endswith('.py'):
			continue
		with open(join(BASE_DIR, folder_name, name)) as f:
			code = f.read()
		tmp = {}
		try:
			exec(code, glb, tmp)
		except BaseException as exc:
			print(join(folder_name, name))
			raise exc
		glb.update(tmp)
		for name, obj in list(tmp.items()):
			if not (type(obj) in (classmethod, staticmethod) or (callable(obj) and 'instance_method' in dir(obj) and obj.instance_method is True)):
				tmp.pop(name)
		lcl.update(tmp)

class Proof:
	get_methods('Proof', globals(), locals())


class GoelandProof(Proof):
	get_methods('GoelandProof', globals(), locals())


class ZenonProof(Proof):
	get_methods('ZenonProof', globals(), locals())
	formula_repr_transformation = {
		'!=' : '!=',
		'-.' : '-',
		'/\\': '^',
		'\\/': 'v',
		}



class Node(object):
	get_methods('Node', globals(), locals())
	attributes = {}



class Win(tkinter.Tk):
	get_methods('Win', globals(), locals())
	attributes = {
		'win_title': 'Graphic',
		'scrollregion': [0, 0, 1000, 1000],
		'iconfile': 'crossref.ico',
		}
	bindings = {}


class App(object):
	get_methods('App', globals(), locals())
	attributes = {}