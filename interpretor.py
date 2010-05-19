import re

primitives = ["NULL", "TRUE"] + [i for i in "CAR CDR CONS ATOM EQ NULL INT PLUS MINUS TIMES QUOTIENT REMAINDER LESS GREATER, COND, QUOTE, DEFUN".split()]

#some useful regexes:
NULL = ("NIL")
TRUE = ("T")
ATOM = re.compile("^\w+$")
INT = re.compile("^[0-9]+$")

WHITESPACE = re.compile("^\s+$")

#write lexer & parser classes:
#steps:
#1. lexer: get tokens
#2. parser: arrange tokens into tree
#3. analysis: link references, ensure well-defined
#4. output as s-expression


#write eval, apply, defun, cond, quote

#experiment with my own tail-recursion stack, to avoid recursion depth of python
    
class SExp:

    def __init__(self, left, right=None):
        """Create an S-expression (left . right). If 'right' is not provided,
        'left' should be atomic.

        """
        if right is None:
            if not isinstance(left, str):
                raise Exception("Not a string")
            if not self._match(left, ATOM):
                raise Exception("Not an atomic S-expression")
            self.val = left
        else:
            if not isinstance(left, SExp) or not isinstance(right, SExp):
                raise Exception("Not an S-expression")
            self.val = (left, right)

    def _match(self, val, regex):
        result = regex.match(val)
        if result is None: return False
        return True

    def atom(self):
        return self._match(val, ATOM)
        
    def eq(self, other):
        if not self.atom() or not other.atom(): raise Exception("Not an atomic S-expression")
        return self.val == other.val

    def null(self):
        if not self.atom(): return False
        return self.val == NULL

    def int(self):
        if not self.atom(): return False
        return self._match(val, INT)

    def car(self):
        if self.atom(): raise Exception("Atomic")
        return val[0]

    def cdr(self):
        if self.atom(): raise Exception("Atomic")
        return val[1]

    def _arithmetic(self, other, op):
        if not self.int() or not other.int(): raise Exception("not an int")
        return str(op(int(self.val), int(other.val)))

    def plus(self, other):
        self._arithmetic(other, lambda a,b: a+b)
        
    def minus(self, other):
        self._arithmetic(other, lambda a,b: a-b)

    def times(self, other):
        self._arithmetic(other, lambda a,b: a*b)

    def quotient(self, other):
        self._arithmetic(other, lambda a,b: a/b)

    def remainder(self, other):
        self._arithmetic(other, lambda a,b: a%b)

    def _compare(self, other, op):
        if not self.int() or not other.int(): raise Exception("not an int")
        if op(int(self.val), int(other.val)): return TRUE
        return "NIL"
        
    def greater(self, other):
        self._compare(other, lambda a,b: a>b)

    def less(self, other):
        self._compare(other, lambda a,b: a<b)


def lex_dot_notation(myinput):
    """A generator for tokens in myinput"""
    my_atom = ""
    for char in myinput:
        if not my_atom == "":
            if ATOM.match(char):
                my_atom += char
                continue
            else:
                yield my_atom
                my_atom = ""
        if WHITESPACE.match(char):
            continue
        elif char in "().": yield char
        elif ATOM.match(char):
            my_atom += char
        else:
            raise Exception("bad token: {0}".format(char))
    if not my_atom == "":
        yield my_atom


def parse_dot_notation(tokens):
    """Parses dot notation into an s-expression"""
    if ATOM.match(tokens[0]):
        return SExp(tokens.pop(0))
    #recursively continue!!!
    if not tokens.pop(0) == "(": raise Exception("mismatched parentheses")
    first = parse_dot_notation(tokens)
    if not tokens.pop(0) == ".": raise Exception("missing dot")
    second = parse_dot_notation(tokens)
    if not tokens.pop(0) == ")": raise Exception("mismatched parentheses")
    return SExp(first, second)
        
        
def parse(myinput):
    """Parses in input and returns it as an s-expression"""
    tokens = [i for i in lex_dot_notation(myinput)]
    sexp = parse_dot_notation(tokens)
    if len(tokens) > 0: raise Exception("extra tokens found")
    
