LisPy README
============
Author: Kemal Eren (kemal@kemaleren.com)

ABOUT
-----

LisPy is an implementation of a subset of the features of LISP 1.5, as
outlined in John McCarthy's [LISP 1.5 Programmer's
Manual](http://www.softwarepreservation.org/projects/LISP/book/LISP%201.5%20Programmers%20Manual.pdf).

The following primitives are defined:

* T
* NIL
* CAR
* CDR
* CONS
* ATOM
* EQ
* NULL
* INT
* PLUS
* MINUS
* TIMES
* QUOTIENT
* REMAINDER
* LESS
* GREATER
* COND
* QUOTE
* DEFUN
* HELP
* QUIT

and various math symbols: + - % * / = < >

LisPy supports both interactive and batch modes.


REQUIREMENTS
------------

* Python (tested with 2.6 and 2.7)


USAGE
-----

NB: LisPy is case-insensitive, and allows both dot and list notation
(though they may not be mixed).

See 'demo.lsp' for some simple examples.


### Interactive mode:

In interactive mode, individual LISP commands may be entered
into the REPL (read-eval-print loop).

Simply run './interpreter.py' to start an interactive
toplevel. LISP commands may be entered over multiple lines;
a command will not be evaluated until the parentheses
match.

Pressing "Control+c" abandons the current expression
and starts a new line. Calling (help) gives some minimal
help.

When finished, type (quit) or press "Control+d" to exit.


### Batch mode

Run './interpreter.py <input file>'. All expressions in the
file will be read, evaluated, and printed in order to
standard output.
