import json

def o(obj) :

	print(json.dumps(obj, indent = 3))

def args (**kwargs) :

	obj = {}

	for arg in kwargs :

		obj[arg] = kwargs.get(arg)

	o(obj)