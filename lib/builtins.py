builtins = {
	'___dab': [['__pydab']],
	'___dip': [['__pydip']],
	'___dot': [['__pydot']],
}

intrinsics = {
	'__pydab': [
		'temp = temp[1:]',
	],
	'__pydwn': [
		'subt = sum(temp[:1])',
		'temp = tuple(max(arg - subt, arg - subt & 1) for arg in temp)',
	],
	'__pydip': [
		'temp = tuple(abs(arg - 1) for arg in temp)',
	],
	'__pydis': [
		'temp = ()',
	],
	'__pydot': [
		'temp = sum(temp),',
	],
}
