
from .classes import *

@method
def load_file(self, file: str):
	try:
		steps = []
		if type(file) == str:
			import os
			if not os.path.exists(file):
				raise FileExistsError(file)
			self.app.title = str().join(os.path.basename(file).split(os.extsep)[:-1])
			if os.extsep not in os.path.basename(file):
				self.app.title = os.path.basename(file)
			with open(file, encoding='utf-8') as f:
				text = f.read()
		else:
			raise TypeError('file parameter must be type str')
		text = str('\n').join(map(lambda line: line[line.index(' #adding'):] if ' #adding' in line else line, text.split('\n')))+'\n'
		file_starter = '----\n'
		text = text[text.index(file_starter)+len(file_starter):]
		text = text.replace(': ####', ':\n####')
		text = text.replace('###>', '')
		while ' \n' in text:
			text = text.replace(' \n', '\n')
		elements = {}
		i = 0
		while i < len(text):
			if text[i] == '[':
				key = ''
				val = ''
				i += 1
				while i < len(text) and text[i] not in ('/', ']'):
					key += text[i]
					i += 1
				assert i < len(text)
				assert key.isdigit()
				while i < len(text) and text[i] != ']':
					i += 1
				assert i < len(text)
				i += 1
				while i < len(text) and not (text[i:i+3] ==', [' or text[i] == '\n'):
					val += text[i]
					i += 1
				assert i < len(text)
				#idle(globals(), locals())
				if f not in elements:
					elements[int(key)] = type(self).represent_element_formula(val)
			i += 1
		#elements = list(sorted(set(map(int, filter(str.isdigit, elements)))))
		action_starter = '\n####'
		actions = list(map(lambda a: a[1:], text.split(action_starter)))[1:]
		for idx, an in enumerate(actions):
			lines = an.split('\n')
			assert lines
			op = lines[0][:lines[0].index(':')]
			assert op in ('refute', 'next_branch', 'unwind')
			els = []
			news = []
			rule = None
			if not an[an.index(':')+1:].replace(' ', ''):
				pass 
			elif op == 'refute':
				lines[0] = lines[0][len(op):]
				for line in lines:
					if '-->' in line:
						news += [int(line.split('-->')[0], 16)]
					elif '[' in line:
						el = ''
						i = line.index('[') + 1
						while i < len(line) and line[i] != ']':
							el += line[i]
							i += 1
						assert i < len(line)
						els += [el]
			elif op in ('next_branch', 'unwind'):
				lines[0] = lines[0][len(op):]
				rule = lines[0][:lines[0].index(',')]
				while rule.startswith(' '):
					rule = rule[1:]
				lines[0] = lines[0][lines[0].index(','):]
				content = str('\n').join(filter(lambda line: '-->' not in line, lines))
				i = 0
				while i < len(content): 	
					if content[i] == '[':
						el = ''
						i += 1
						while i < len(content) and content[i] != ']':
							el += content[i]
							i += 1
						assert i < len(content)
						els += [el]		
					i += 1	
				for line in filter(lambda line: '-->' in line, lines):
					news += [int(line.split('-->')[0], 16)]
			else:
				raise ValueError('Unkwnon operation : '+op)
			steps += [dict(
				op=op, 
				elements=els, 
				instantiations=news, 
				rule=rule,
				order=idx,
				)]
		root = Node(
			parent = None,
			properties = {
				'type': 'inst',
				'text': '[0] '+elements[list(elements)[0]],
				},
			index = 0,
			)
		noded_steps = [(root, )]
		reverse = {}
		curr = root
		idx = 1
		for i, step in enumerate(steps):
			if step['op'] == 'refute':
				head = step['op']
			elif type(step.get('rule')) == str:
				head = step['op'] + step['rule']
			main_node = Node(
				parent = curr,
				properties = {
					'type': 'action',
					'text': head + ': ' + str(' ').join(map(type(self).represent_element_key, step['elements'])), 
					},
				index = idx,
				auto_affect_children = True,
				)  
			idx += 1
			reverse[main_node] = step
			curr = main_node
			if step['instantiations'] and step['op'] != 'unwind':
				inst_node = Node(
					parent = curr,
					properties = {
						'type': 'inst',
						'text': str('\n').join(
							unpackingmap(
								type(self).represent_element, 
								map(
									lambda key: (key, elements[key]), 
									filter(
										lambda key: key in elements,
										step['instantiations'],
										),
									),
								),
							),
						},
					index = idx,
					auto_affect_children = True,
					)
				idx += 1
				curr = inst_node
				noded_steps += [(main_node, inst_node)]
			else:
				noded_steps += [(main_node, )]
			if step['op'] == 'unwind':
				main_node.properties['erase_children'] = True
				main_node.properties['unwinding'] = True
				curr = curr.parent
				while True: 
					#if curr is None or (reverse[curr]['rule'] == step['rule'] and set(reverse[curr]['elements']) == set(step['elements'])):
					if curr.parent is None or (curr in reverse and reverse[curr]['rule'] == step['rule'] and set(reverse[curr]['elements']) == set(step['elements'])):
						#print(check)
						break	
					curr = curr.parent
				main_node.properties['target'] = curr
		for noded_step in noded_steps:
			for node in noded_step:
				if node.properties.get('erase_children') is True:
					node.children.clear()
	except:
		import traceback; traceback.print_exc()
		from mylib import idle
		idle(globals(), locals())
	self.steps = steps
	self.noded_steps = list(filter(lambda t: len(t)>0, noded_steps))
	#assert noded_steps and noded_steps[0]
	#root = noded_steps[0][0]
	#assert root.parent is None
	self.root = root
	self.elements = elements
	self.nodes = [root] + self.root.apply(list, list.__add__)