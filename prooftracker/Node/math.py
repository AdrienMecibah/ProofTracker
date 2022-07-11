
from .classes import method

@method
def apply(self, function, operator=(lambda x, y: None)):
	result = function(self)
	for child in list(self.children):
		result = operator(result, child.apply(function, operator))
	return result