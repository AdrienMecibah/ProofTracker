
from .classes import method

@method
@classmethod
def represent_element_key(cls, key):
	if type(key) == str and '/' in key:
		key = key[:key.index('/')]
	return '['+str(key)+']'

@method
@classmethod
def represent_element_formula(cls, formula):
	for item in cls.formula_repr_transformation.items():
			formula = formula.replace(*item)
	return formula

@classmethod
@method
def represent_element(cls, key, formula):
	for item in cls.formula_repr_transformation.items():
			formula = formula.replace(*item)
	return cls.represent_element_key(key) + ' ' + cls.represent_element_formula(formula)