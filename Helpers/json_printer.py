import json

"""
	pretty pint dict as json
	@param {Dist} dict
	@return {Void}
"""
def dict (dict) :

	print(json.dumps(dict, indent = 3))

"""
	print the given args json pretty format
	@param {Mixed}
	@return {Void}
"""
def args (**kwargs) :

	obj = {}

	for arg in kwargs :

		obj[arg] = kwargs.get(arg)

	dict(obj)