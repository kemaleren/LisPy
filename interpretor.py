import re

primitives = (NULL, TRUE) + (i for i in "CAR CDR CONS ATOM EQ NULL INT PLUS MINUS TIMES QUOTIENT REMAINDER LESS GREATER, COND, QUOTE, DEFUN".split())


LIST = re.compile()
DOT = re.compile()

#write lexer & parser classes:
#steps:
#1. lexer: get tokens
#2. parser: arrange tokens into tree
#3. analysis: link references, ensure well-defined
#4. output as s-expression


#write eval, apply, defun, cond, quote

#experiment with my own tail-recursion stack, to avoid recursion depth of python
    
class sexp:
    #some useful regexes:
    NULL = ("NIL")
    TRUE = ("T")
    ATOM = re.compile("^\w+$")
    INT = re.compile("^[0-9]+$")

    def init(self, left, right=None):
        """Create an S-expression (left . right). If 'right' is not provided,
        'left' should be atomic.

        """
        if right is None:
            if not isinstance(left, str):
                raise Exception("Not an atomic S-expression")
            val = left
        else:
            if not isinstance(left, sexp) or not isinstance(right, sexp):
                raise Exception("Not an S-expression")
            val = (left, right)

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

        
