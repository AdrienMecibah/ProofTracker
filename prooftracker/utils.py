
import os
import json
import sys

try:
	from .strictlymine import *
except:
	pass

class Object(object):
	@staticmethod
	def from_dict(attributes):
		return Object(**attributes)
	def __init__(self, **kwargs):
		for item in kwargs.items():
			setattr(self, *item)

BASE_DIR = BASE = os.path.dirname(__file__)
		
unpackingmap = lambda fun, iterable: map(
	lambda item: fun(*item), 
	iterable
	)
unpackingfilter = lambda fun, iterable: filter(
	lambda item: fun(*item), 
	iterable
	)

do = lambda mapobject: [list(mapobject), None][1]
domap = lambda callable, iterable: [do(map(callable, iterable)), None][1]

def join(*args: [str], sep: str=os.sep) -> str:
	return sep.join(args)

def dumps(obj: {int, str, list, dict}) -> str:
	return json.dumps(obj, indent=4)

def dodump(obj):
	print(dumps(obj))


def analyze(args, options):
	result = {}
	count = 0
	idx = 0
	while idx < len(args):
		is_option = False
		for name, (nb, default) in options.items():
			if name == args[idx]:
				if nb:
					value = []
					for _ in range(nb):
						idx += 1
						if idx == len(args) or args[idx] in options:
							raise ValueError()
						value += [args[idx]]
					result[name] = value[0] if len(value) == 1 else value
				else:
					result[name] = True
				idx += 1
				is_option = True
				break
		if not is_option:
			result[count] = args[idx]
			idx += 1
			count += 1
	for name, (nb, default) in list(options.items()):
		if name not in result:
			result[name] = default
	return result