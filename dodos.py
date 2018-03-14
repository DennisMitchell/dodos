#!/usr/bin/env python3

from argparse import ArgumentParser
from lib.compiler import dodosc

def dodos(*argv):
	argparser = ArgumentParser(description = 'Dodos Only Divide Or Surrender')

	try:
		argparser._actions[0].help = 'Show this help message and exit.'
	except:
		pass

	argparser.add_argument(
		'file', metavar = 'FILE',
		help = 'Read source code from FILE.'
	)

	argparser.add_argument(
		'input', metavar = 'INTEGER', type = int, nargs = '*',
		help = 'Define the input vector as the [|INTEGER| [|INTEGER| ...]].'
	)

	argparser.add_argument(
		'-b', '--inbytes', dest = 'parse_input', default = map_abs,
		action = 'store_const', const = read_stdin,
		help = 'Read raw bytes from STDIN and append their values to the input vector.'
	)

	argparser.add_argument(
		'-B', '--outbytes', dest = 'write_output', default = write_nums,
		action = 'store_const', const = write_bytes,
		help = 'Display the coordinates of the output vector (modulo 256) as raw bytes.'
	)

	args = argparser.parse_args(list(argv) or None)
	args.write_output(dodosc(args.file)(*args.parse_input(args.input)))

def map_abs(inv):
	return map(abs, inv)

def read_stdin(inv):
	from sys import stdin
	yield from map_abs(inv)
	yield from stdin.buffer.read()

def write_bytes(outv):
	from sys import stdout
	stdout.buffer.write(bytes(map((256).__rmod__, outv)))

def write_nums(outv):
	for number in outv:	print(number)

if __name__ == '__main__':
	dodos()
