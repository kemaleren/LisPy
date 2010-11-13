"""Contains the primitives S-Expressions that come with the interpreter."""

from sexp import SExp

#TODO: This way of instantiating primitives (and s-expressions in general) is way too hacky.
#      First, they are created multiple times, manually.
#      Second, each special form and built-in function needs to know the explicty name of the S-expression anways.
#      Refactor to make more natural, and to encapsulate S-expression logic, especially for special forms.

PRIMITIVES_STRING = "T NIL CAR CDR CONS ATOM EQ NULL INT PLUS MINUS TIMES QUOTIENT REMAINDER LESS GREATER COND QUOTE DEFUN HELP QUIT + - % * / = < >"
PRIMITIVES = [i for i in PRIMITIVES_STRING.split()]

help_string = "Available primitives:\n{0}\n\nFurther help not currently available.".format(PRIMITIVES_STRING)

#BASIC S-EXPRESSIONS
#TODO: don't do this manually
T = (SExp("T"),)
NIL = (SExp("NIL"),)

CAR = (SExp("CAR"),)
CDR = (SExp("CDR"),)
CONS = (SExp("CONS"),)
ATOM = (SExp("ATOM"),)
NULL = (SExp("NULL"),)
EQ = (SExp("EQ"), SExp("="),)
INT = (SExp("INT"),)
PLUS = (SExp("PLUS"), SExp("+"),)
MINUS = (SExp("MINUS"), SExp("-"),)
TIMES = (SExp("TIMES"), SExp("*"),)
QUOTIENT = (SExp("QUOTIENT"), SExp("/"),)
REMAINDER = (SExp("REMAINDER"), SExp("%"),)
LESS = (SExp("LESS"), SExp("<"),)
GREATER = (SExp("GREATER"), SExp(">"),)
QUIT = (SExp("QUIT"),)
HELP = (SExp("HELP"),)
QUOTE = (SExp("QUOTE"),)
COND = (SExp("COND"),)
DEFUN = (SExp("DEFUN"),)

#a list of all primitive s-expressions
PRIMITIVE_SEXPS = [SExp(i) for i in PRIMITIVES]
