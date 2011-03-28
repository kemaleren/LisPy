"""
Functions used for parsing input to the interpreter.

The basic approach used by the parser was suggested by Neelam Soundarajan.

"""

from regexes import ATOM_regex, INT_regex, WHITESPACE_regex
from sexp import SExp
import error

def lex(myinput):
    """A generator for yielding tokens in myinput"""
    my_atom = ""
    for char in myinput:
        if not my_atom == "":
            if ATOM_regex.match(char):
                my_atom += char
                continue
            else:
                yield my_atom
                my_atom = ""
        if WHITESPACE_regex.match(char):
            continue
        elif char in "().'": yield char
        elif ATOM_regex.match(char):
            my_atom += char
        else:
            raise error.LispException("bad token: {0}".format(char))
    if not my_atom == "":
        yield my_atom


def get_tokens(myinput):
    """Returns all tokens in myinput"""
    return [i for i in lex(myinput)]


def balanced(tokens):
    """Returns true if parentheses in a list of tokens are balanced"""

    count = 0
    for token in tokens:
        if token == "(": count += 1
        if token == ")": count -= 1
        if count < 0: raise error.LispException("imbalanced parens")
    return count == 0


def process_list_tokens(tokens):
    """
    Parses tokens in a partial list form into an s-expression

    The tokens should have the form ')' 's1)' 's1 s2)' etc
    
    """
    if len(tokens) == 0: raise error.LispException("parse error: missing tokens")
    if tokens[0] == ")":
        tokens.pop(0)
        return SExp("NIL")
    first = process_tokens(tokens)
    if len(tokens) == 0: raise error.LispException("parse error: missing tokens")
    if tokens[0] == ".": raise error.LispException("mixed notation not supported")
    second = process_list_tokens(tokens)
    return SExp(first, second)


def process_tokens(tokens):
    """
    Destructively parses tokens into an s-expression
    Stops after one s-expression and returns it, leaving any remaining tokens untouched
    
    """
    if len(tokens) == 0: raise error.LispException("parse error: missing tokens")
    if ATOM_regex.match(tokens[0]):
        sexp = SExp(tokens.pop(0))
        return sexp
    if tokens[0] == "(" and tokens[1] == ")":
        tokens.pop(0)
        tokens.pop(0)
        return SExp("NIL")
    #recursively continue
    if not tokens.pop(0) == "(": raise error.LispException("missing open parentheses")
    first = process_tokens(tokens)
    if len(tokens) == 0: raise error.LispException("parse error: missing tokens")
    second = []
    if tokens[0] == ".":
        tokens.pop(0)
        second = process_tokens(tokens)
        if len(tokens) == 0: raise error.LispException("parse error: missing tokens")
        if not tokens.pop(0) == ")": raise error.LispException("missing close parentheses")
    else:
        second = process_list_tokens(tokens)
    sexp  = SExp(first, second)
    return sexp


def parse(tokens):
    """Parses tokens and returns an s-expression"""
    sexp = process_tokens(tokens)
    return sexp


def parse_gen(tokens):
    """A generator that parses tokens and returns as many s-expressions as possible"""
    while (len(tokens) > 0):
        yield process_tokens(tokens)

