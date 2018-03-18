from .builtins import builtins, intrinsics
from .generate import emit_define, emit_header, emit_monad, emit_return
from .optimizer import funcdeps, recognize_intrinsics
from .parser import parse

def dodosc(filename):
	code = []
	emit_header(code.append)

	with open(filename, 'rb') as lines:
		funcs = parse(lines)

	inline_intrinsics(funcs)
	recognize_intrinsics(funcs)
	inline_intrinsics(funcs)
	deps = funcdeps(funcs)

	for name, body in funcs.items():
		recursive = name in deps[name]
		emit_define(code.append, name, recursive)
		for monad in body: emit_monad(code.append, monad, recursive)
		emit_return(code.append, recursive)

	py_source = ''.join(code)
	namespace = {}
	exec(py_source, namespace)

	return namespace['___main']

def inline_intrinsics(funcs):
	while True:
		macros = {}

		for name, body in funcs.items():
			if name == '___main':
				continue

			if len(body) == 1 and len(body[0]) == 1 and body[0][0] in intrinsics:
				macros[name] = body[0][0]

		if not macros: break
		for name in macros: del funcs[name]

		for body in funcs.values():
			for monad in body:
				for index, name in enumerate(monad):
					if name in macros:
						monad[index] = macros[name]
