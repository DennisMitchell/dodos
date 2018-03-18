from .builtins import intrinsics

def funcdeps(funcs):
	all_deps = {}

	for name, body in funcs.items():
		all_deps[name] = {
			dep
			for monad in body
			for dep in monad
			if not dep in intrinsics
		}

	while True:
		old_deps = all_deps.copy()

		for name, deps in all_deps.items():
			all_deps[name] = all_deps[name].copy()
			for func in deps: all_deps[name] |= all_deps[func]

		if all_deps == old_deps: break

	for name, deps in all_deps.items():
		all_deps[name] = {dep for dep in all_deps[name] if name in all_deps[dep]}

	return all_deps

def recognize_intrinsics(funcs):
	for name, body in funcs.items():
		if len(body) == 1:
			if body[0][:1] == [name]:
				if set(body[0][1:]) == {'__pydab'}:
					body[0][:] = ['__pydis']
					continue
				if body[0][1:] == ['__pydip']:
					body[0][:] = ['__pydwn']
					continue
