from .builtins import intrinsics

def emit_header(emit):
	emit('class Surrender(Exception): pass\n')

def emit_define(emit, name, recursive):
	if recursive:
		emit('\ndef {}(argv, call_stack = []):\n'.format(name))
		emit('\targcv = (len(argv), argv)\n')
		emit('\tif call_stack and not argcv < call_stack[-1]: raise Surrender\n')
		emit('\tcall_stack.append(argcv)\n\n')
		emit('\ttry:\n')
		emit('\t\tretval = []\n')
	else:
		emit('\ndef {}(argv):\n'.format(name))
		emit('\tretval = []\n')

def emit_monad(emit, monad, recursive):
	indent = '\t' * (1 + recursive)
	emit(indent + 'temp = argv\n')

	for reference in reversed(monad):
		try:
			for line in intrinsics[reference]:
				emit('{}{}\n'.format(indent, line))
		except KeyError:
			emit(indent + 'temp = {}(temp)\n'.format(reference))

	emit(indent + 'retval.extend(temp)\n')

def emit_return(emit, recursive):
	if recursive:
		emit('\texcept Surrender:\n\t\tretval = argv\n\n')
		emit('\tcall_stack.pop()\n')

	emit('\treturn tuple(retval)\n')
