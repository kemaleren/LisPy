from error import LispException
from regexes import ATOM_regex, INT_regex, WHITESPACE_regex

class SExp(object):
    """
    The S-Expression class. Each s-expression can be atomic, or it has two s-expression children, CAR and CDR.

    Member functions implement most of the basic primitive functions that are not special forms, such as
    addition, subtraction, checking whether an integer, etc.

    Boolean member functions return Python's True and False. However, if the optional 'sexp' argument evaluates to
    True, they instead return the primitive s-expressions T and NIL.

    """

    def __init__(self, left, right=None):
        """Create an S-expression (left . right). If 'right' is not provided,
        'left' should be atomic.

        """
        if right is None:
            if not isinstance(left, str):
                raise LispException("trying to create an S-expression from {0}".format(str(left)))
            if ATOM_regex.match(left) is None:
                raise LispException("not a valid atomic S-expression: {0}".format(left))
            self.val = left.upper()
        else:
            if not isinstance(left, SExp) or not isinstance(right, SExp):
                raise LispException("not an S-expression")
            self.val = (left, right)
        self.bool_sexps = {True: "T", False: "NIL"}


    def atom(self, sexp=False):
        result = type(self.val) == type("")
        if sexp: return SExp(self.bool_sexps[result])
        return result

    def __eq__(self, other):
        if not self.atom(): raise LispException("not an atomic S-expression: {0}".format(self))
        if not other.atom(): raise LispException("not an atomic S-expression: {0}".format(other))
        return self.val == other.val

    def __ne__(self, other):
        return not self.__eq__(other)

    def eq(self, other, sexp=False):
        result = False
        if self.__eq__(other): result = True
        if sexp: return SExp(self.bool_sexps[result])
        return result

    def null(self, sexp=False):
        result = False
        if self.atom():
            if self.val == "NIL": result = True
        if sexp: return SExp(self.bool_sexps[result])
        return result

    def int(self, sexp=False):
        result = False
        if self.atom():
            if INT_regex.match(self.val) is not None:
                result = True
        if sexp: return SExp(self.bool_sexps[result])
        return result

    def car(self):
        if self.atom(): raise LispException("cannot call CAR on atomic s-expression: {0}".format(self))
        return self.val[0]

    def cdr(self):
        if self.atom():
            raise LispException("cannot call CDR on atomic s-expression: {0}".format(self))
        return self.val[1]

    def _arithmetic(self, other, op):
        if not self.int(): raise LispException("not an int: {0}".format(self))
        if not other.int(): raise LispException("not an int: {0}".format(other))
        return SExp(str(op(int(self.val),
                           int(other.val))))

    def plus(self, other):
        return self._arithmetic(other, lambda a, b: a+b)

    def minus(self, other):
        return self._arithmetic(other, lambda a, b: a-b)

    def times(self, other):
        return self._arithmetic(other, lambda a, b: a*b)

    def quotient(self, other):
        return self._arithmetic(other, lambda a, b: a/b)

    def remainder(self, other):
        return self._arithmetic(other, lambda a, b: a%b)

    def _compare(self, other, op):
        if not self.int(): raise LispException("not an int: {0}".format(self))
        if not other.int(): raise LispException("not an int: {0}".format(other))
        if op(int(self.val), int(other.val)): return SExp("T")
        return SExp("NIL")

    def greater(self, other):
        return self._compare(other, lambda a, b: a>b)

    def less(self, other):
        return self._compare(other, lambda a, b: a<b)

    def is_list(self):
        if self.null(): return True
        if self.atom(): return False
        if self.val[1].is_list(): return True
        return False

    def length(self):
        if not self.is_list():
            raise LispException("calling length on non-list {0}".format(self))
        if self.null(): return 0
        return 1+self.val[1].length()

    def non_int_atom(self):
        """Checks if this is an atom, but not an integer"""
        if not self.atom(): return False
        if INT_regex.match(self.val) is not None: return False
        return True

    def _repr_helper(self):
        if self.null():
            return ""
        return " {0}{1}".format(self.val[0], self.val[1]._repr_helper())

    def __repr__(self):
        """
        Creates the string representation of the S-expression. Uses list notation
        whenever possible.

        """
        if self.atom():
            return self.val
        else:
            if self.is_list():
                return "({0}{1})".format(self.val[0], self.val[1]._repr_helper())
            return "({0} . {1})".format(self.val[0], self.val[1])

    def copy(self, other):
        self.val = other.val
