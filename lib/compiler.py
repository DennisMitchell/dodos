builtins = \
           \
'''
class Surrender(Exception): pass

def ___dab(*argv):
	return argv[1:]

def ___dip(*argv):
	return tuple(abs(arg - 1) for arg in argv)

def ___dot(*argv):
	return sum(argv),
'''

def dodosc(filename):
	code = [builtins]
	header = []
	defined = {'___dab', '___dip', '___dot'}
	emit_define(code.append, [b'main'], defined)

	with open(filename, 'rb') as lines:
		for line in lines:
			tokens = bytes(filter((32).__le__, line.replace(b'\t', b' '))).split()
			if not tokens: continue

			if line[:1].isspace():
				emit_monad(code.append, tokens, defined, header)
			else:
				emit_return(code.append)
				emit_define(code.append, tokens, defined)

	emit_return(code.append)
	py_source = ''.join(header + code)
	namespace = {}
	exec(py_source, namespace)

	return namespace['___main']

def funcname(bytestring):
	try:
		string = '___{}'.format(bytestring.decode('ascii'))
		if not string.isidentifier(): raise ValueError
		return string
	except (UnicodeDecodeError, ValueError):
		return '__{:x}'.format(int.from_bytes(bytestring, 'big'))

def emit_define(emit, tokens, defined):
	first_name = funcname(tokens[0])
	defined.add(first_name)

	for token in tokens[1:]:
		name = funcname(token)
		emit('\ndef {}(*argv, call_stack = []):\n'.format(name))
		emit('\treturn {}(*argv, call_stack =  call_stack)\n'.format(first_name))

	emit('\ndef {}(*argv, call_stack = []):\n'.format(first_name))
	emit('\targcv = (len(argv), *argv)\n')
	emit('\tif call_stack and not argcv < call_stack[-1]: raise Surrender\n')
	emit('\tcall_stack.append(argcv)\n')
	emit('\tretval = []\n')
	emit('\n\ttry:\n')

def emit_monad(emit, tokens, defined, header):
	emit('\t\ttemp = argv\n')

	for token in reversed(tokens):
		name = funcname(token)
		emit('\t\ttemp = {}(*temp)\n'.format(name))

		if name not in defined:
			header.append('def {}(*argv):\n\treturn argv\n'.format(funcname(token)))
			defined.add(name)

	emit('\t\tretval.extend(temp)\n')

def emit_return(emit):
	emit('\t\tpass\n')
	emit('\texcept Surrender:\n\t\tretval[:] = argv\n\n')
	emit('\tcall_stack.pop()\n')
	emit('\treturn retval\n')
