# Dodos Only Divide Or Surrender

*Dodos* is a programming language based on the *Divide Or Surrender* paradigm.

Given any problem, a Dodos program tries to recursively break it down into smaller subproblems. If and when that is no longer possible, it surrenders (backs out).

As a consequence, Dodos will find a solution to *any* problem, although it might not be *the* solution.

### Quickstart

Getting started with Dodos is easy and only requires Python 3.5+.

```sh
$ git clone --quiet https://github.com/DennisMitchell/dodos.git
$ cd dodos
$ ./dodos examples/cat.dodos 109 101 111 119 10
109
101
111
119
10
```

For more information, run `./dodos -h`.

Alternatively, you can use the [Dodos interpreter on Try It Online](https://tio.run/#dodos).

### Syntax

Dodos source code consists entirely of function definitions. Each function takes a tuple of natural numbers (integers strictly grater than zero) as its sole argument and, likewise, returns a tuple of natural numbers.

Function definitions consist of a single line containing one or more names for the function, followed by the function body. Each line of the function body must begin with a tabulator or a space.

```
F f
	g h
	φ ψ
```

This defines two functions **F** and **f** that can be described by the following pseudo-code.

```
F(x) = f(x) = (g(h(x)), φ(ψ(x)))
```

While they perform the same calls, the functions **F** and **f** are different. The importance of this distinction will become clear later.

The output tuple is flattened, if necessary. If the function body is empty, the function will discard its input and return an empty tuple.

The function with name `main` is special, as its input and output are the input and output of the program. Programs start with an implicit `main` line.

While empty lines are ignored, lines containing only whitespace are considered part of the corresponding function body. An empty statement does nothing; it returns its argument vector unchanged. Thus, a program consisting of a single tabulator (remember: the `main` is implicit) is a "cat" program.

Functions can be defined multiple times, but all definitions are effective before the `main` function is called. This means that only the last definition of any given function "counts". Calls to undefined functions are ignored.

Valid function names consist of one or more bytes in the range **\[33, 256)**. With the exception of tabulators, newlines, and spaces, all other bytes that occur in the source code are ignored.

### Builtins

Dodos only has three builtin functions:

* `dab` removes the first element of its argument vector.
* `dip` maps each coordinate **x** in its argument vector to **|x - 1|**.
* `dot` computes the sum of the coordinates of its argument vector.

The simplest Dodos program that computes the sum of its input arguments looks like this.

```
	dot
```

[Try it online!](https://tio.run/##S8lPyS/@/58zJb/k////hib/jSwA "Dodos – Try It Online")

### Divide Or Surrender

Most programming languages allow function definitions such as `f(x) = f(x)` or `f(x) = f(x + 1)` and actually try to compute **f(x)** by computing **f(x)** or even **f(x + 1)**. The result is an infinite loop that will never return any output.

The *Divide Or Surrender* paradigm doesn't such nonsense. If, while trying to compute **f(x)**, we find ourselves in need of computing **f(y)**, the following happens.

* If **y < x**, the function call proceeds as usual.
* If **y ≥ x**, a *Surrender* exception is raised, the function call attempting to compute **f(y)** is interrupted, and its argument is returned unchanged.

Argument vectors are compared first by their lengths, then lexicographically. For example, **(1, 0, 8) < (1, 2, 3) < (0, 0, 0, 0)**. It is easy to verify that this comparison induces a well-ordering on the set of all argument vectors. As a consequence, all Dodos programs halt eventually.

For example, let us consider the following function.

```
f
	f dip
```

**f** is defined as **f(x) = f(|x - 1|)**. Trying to compute **f(3)** proceeds as follows.

* **|3 - 1| = 2 < 3**, so **f(3) = f(2)**.
* **|2 - 1| = 1 < 2**, so **f(2) = f(1)**.
* **|1 - 1| = 0 < 1**, so **f(1) = f(0)**.
* **|0 - 1| = 1 ≥ 0**, so trying to compute **f(1)** will raise an exception, and **f(0)** returns its argument (**0**).

Thus, **f(3) = f(2) = f(1) = f(0) = 0**.

[Try it online!](https://tio.run/##S8lPyS/@/58zjSuNizNNISWz4P///8YA "Dodos – Try It Online")

When given a 2-tuple argument **(x, y)**, the function from the last example lets us compute **y - x**. After **x** calls to **f**, we arrive at **(0, y - x)** and the attempted call **f(1, |y - x - 1|)** fails.

If we use `dab` to discard the first coordinates of **(0, y - x)**, we obtain the desired result. [Try it online!](https://tio.run/##S8lPyS/@/58zJTFJIY0rjYszTSEls@D///9Gpv8NDQwA "Dodos – Try It Online")
