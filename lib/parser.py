from .builtins import builtins, intrinsics

def parse(lines):
	funcs = builtins.copy()
	funcnames = ['___main']
	funcbody = []

	for line in lines:
		line = bytes(filter((32).__le__, line.replace(b'\t', b' ')))
		tokens = list(map(sanitize, line.split()))

		if line[:1] == b' ':
			funcbody.append(tokens)
		elif tokens:
			for funcname in funcnames:
				funcs[funcname] = funcbody
			funcnames = tokens
			funcbody = []

	for funcname in funcnames:
		funcs[funcname] = funcbody

	for func in funcs.values():
		for monad in func:
			for index, name in enumerate(monad):
				if name in funcs or name in intrinsics: continue
				del monad[index]

	return funcs

def sanitize(bytestring):
	try:
		string = '___{}'.format(bytestring.decode('ascii'))
		if not string.isidentifier(): raise ValueError
		return string
	except (UnicodeDecodeError, ValueError):
		return '__{:x}'.format(int.from_bytes(bytestring, 'big'))
