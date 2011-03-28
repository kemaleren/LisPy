#! /usr/bin/env python2

"""
interpreter.py
Author: Kemal Eren

A minimal implementation of a LISP 1.5 interpreter.

"""

import sys
import copy

from parse import parse, parse_gen, get_tokens, balanced
from sexp import SExp
import error
from primitives import *

#TODO: experiment with my own tail-recursion stack, to avoid recursion depth of python


def interpreter(d_list):
    """Runs the interactive toplevel"""
    print ""
    print bcolors.PROMPT + "Welcome to LISP" + bcolors.ENDC
    print "Call (help) to see available primitives"
    print "Type 'Control+c' to cancel the current input"
    print "Call (quit) or type 'Control-d' to quit"
    print ""
    try:
        import readline
    except:
        print bcolors.WARNING + "warning: " + bcolors.ENDC + "loading readline library failed. Advanced editing features will not be available"
        print ""

    while True:
        try:
            entry = raw_input(bcolors.PROMPT + "LISP: " + bcolors.ENDC)
            tokens = get_tokens(entry)

            while not balanced(tokens):
                entry = raw_input("")
                tokens += get_tokens(entry)

            #read. parse the tokens and build an S-Expression
            sexp = parse(tokens)
            if len(tokens) > 0: raise error.LispException("extra tokens found: {0}".format(" ".join(tokens)))

            #eval and print. the heart of the interpreter!
            print bcolors.OKBLUE + " OUT: " + bcolors.ENDC + str(eval_lisp(sexp, SExp("NIL"), d_list))
            print ""
        except KeyboardInterrupt:
            print ""
            print "keyboard interrupt"
            print ""
        except error.LispException as inst:
            print bcolors.FAIL + " ERR: " + bcolors.ENDC + inst.args[0]
            print ""
        except RuntimeError:
            print "error: eval failed. deep recursion not yet supported."
        except EOFError:
            entry = None
            aff = ['yes', 'y', '']
            neg = ['no', 'n']
            while not entry in aff + neg:
                print bcolors.WARNING + "\nexit? (Y/n):" + bcolors.ENDC,
                entry = raw_input("").lower()
            if entry in aff:
                sys.exit()
            print
            


def eval_lisp(exp, a_list, d_list):
    """The classic 'eval' function. Evaluates an s-expression and returns the result"""
    if exp.atom():
        if exp.int():
            return exp
        if exp in T:
            return SExp("T")
        if exp.null():
            return SExp("NIL")
        if in_pairlist(exp, a_list):
            return getval(exp, a_list)
        raise error.LispException("unbound variable: {0}".format(exp))
    if exp.car().atom():
        if not exp.car().non_int_atom:
            raise error.LispException("'{0}' is not a valid function name or special form".format(exp.car()))
        #cdar because cdr only would give (quote 5) evaluating to (5), not 5. only takes one argument.
        if exp.car() in QUOTE:
            check_args(exp.car(), exp.cdr().length(), 1)
            return exp.cdr().car() 
        if exp.car() in COND:
            return evcond(exp.cdr(), a_list, d_list)
        if exp.car() in DEFUN:
            new_func = exp.cdr().car()
            args = exp.cdr().cdr().car()
            body = exp.cdr().cdr().cdr().car()
            check_args(new_func, exp.cdr().length(), 3)
            return defun(new_func, args, body, d_list)
        return apply_lisp(exp.car(), evlis(exp.cdr(), a_list, d_list), a_list, d_list)
    raise error.LispException("eval called with invalid expression")


def evlis(targetlist, a_list, d_list):
    """calls 'eval' on all elements of 'targetlist'"""
    if targetlist.null():
        return SExp("NIL")
    return SExp(eval_lisp(targetlist.car(), a_list, d_list),
                evlis(targetlist.cdr(), a_list, d_list))


def apply_lisp(function, args, a_list, d_list):
    """
    The classic 'apply' function. Evaluates the body of a function 'f' with arguments 'x'

    function: a special form, primitive function, or a function in the dlist.
    args: a list of function arguments.
    a_list: a list of (variable . binding) pairs.
    d_list: a list of (fname . (arglist . body)) pairs.

    """
    #TODO: doing everything in one function, and handling all cases is one place, is terrible design.
    #      this refactor should go along with redoing how S-expressions are represented.

    if not function.atom(): raise error.LispException("error: cannot call non-atom {0} as a function".format(function))
    #TODO: integrate the check_args call with the other primitives definitions + help.
    if function in CAR:
        check_args(function, args.length(), 1)
        return args.car().car() #caar, because only have one argument: a list
    if function in CDR:
        check_args(function, args.length(), 1)
        return args.car().cdr() #cadr
    if function in CONS:
        check_args(function, args.length(), 2)
        return SExp(args.car(), args.cdr().car()) #two arguments. the second one is (s . nil) but we only want the s
    if function in ATOM:
        check_args(function, args.length(), 1)
        return args.car().atom(sexp=True)
    if function in NULL:
        check_args(function, args.length(), 1)
        return args.car().null(sexp=True)
    if function in EQ:
        check_args(function, args.length(), 2)
        return args.car().eq(args.cdr().car(), sexp=True)

    if function in INT:
        check_args(function, args.length(), 1)
        return args.car().int(sexp=True)
    if function in PLUS:
        check_args(function, args.length(), 2)
        return args.car().plus(args.cdr().car())
    if function in MINUS:
        check_args(function, args.length(), 2)
        return args.car().minus(args.cdr().car())
    if function in TIMES:
        check_args(function, args.length(), 2)
        return args.car().times(args.cdr().car())
    if function in QUOTIENT:
        check_args(function, args.length(), 2)
        return args.car().quotient(args.cdr().car())
    if function in REMAINDER:
        check_args(function, args.length(), 2)
        return args.car().remainder(args.cdr().car())
    if function in LESS:
        check_args(function, args.length(), 2)
        return args.car().less(args.cdr().car())
    if function in GREATER:
        check_args(function, args.length(), 2)
        return args.car().greater(args.cdr().car())
    if function in HELP:
        check_args(function, args.length(), 0)
        print help_string
        return SExp("T")
    if function in QUIT:
        check_args(function, args.length(), 0)
        exit()
    if not in_pairlist(function, d_list):
        raise error.LispException("function {0} not found".format(function))
    params = getval(function, d_list).car()
    check_args(function, args.length(), params.length())
    return eval_lisp(getval(function, d_list).cdr(), addpairs(params, args, a_list), d_list)


def defun(f, args, body, d_list):
    """Evaluates the DEFUN special form. Adds a new function to the D-list"""
    if not f.non_int_atom():
        raise error.LispException("'{0}' is not a valid function name".format(f))
    if f in PRIMITIVE_SEXPS:
        raise error.LispException("cannot redefine primitive '{0}'".format(f))
    new_d_list = SExp(SExp(f, SExp(args, body)), copy.copy(d_list))
    d_list.copy(new_d_list)
    return f


def evcond(be, a_list, d_list):
    """Evaluates the COND special form"""
    if be.null():
        raise error.LispException("boolean expression cannot be NIL")
    if not (eval_lisp(be.car().car(), a_list, d_list)).null():
        return eval_lisp(be.car().cdr().car(), a_list, d_list)
    return evcond(be.cdr(), a_list, d_list)


def in_pairlist(exp, pairlist):
    """
    Returns true if the s-expression 'exp' appears as the CAR of any of the s-expressions
    in the s-expression 'pairlist'.

    'pairlist' has the form ((a.b) (c.d) ... (e.f)) where the CAR of each element is atomic.

    Used to check for function names in the D-list, and atom bindings in the A-list.

    """
    if pairlist.null():
        return False
    if pairlist.car().atom():
        raise error.LispException("a-list or d-list in wrong format")
    if exp == pairlist.car().car():
        return True
    return in_pairlist(exp, pairlist.cdr())


def getval(exp, from_list):
    """
    If 'exp' is the CAR of any of the s-expression pairs in the pairlist, returns that
    s-expressions CDR.
    Else returns NIL.

    """
    if from_list.null():
        return SExp("NIL")
    if from_list.car().atom():
        raise error.LispException("a-list or d-list in wrong format")
    if exp == from_list.car().car():
        return from_list.car().cdr()
    return getval(exp, from_list.cdr())


def addpairs(params, cur_args, to_list):
    """
    Adds pairs formed by zipping s-expressions in 'params' and 'cur_args' to the
    pair list 'to_list'

    """
    if params.null() and cur_args.null():
        return to_list
    if params.atom() or cur_args.atom():
        raise error.LispException("pairs cannot be atoms")
    pair = SExp(params.car(), cur_args.car())
    return addpairs(params.cdr(), cur_args.cdr(), SExp(pair, to_list))


def check_args(f, got_len, exp_len):
    """Ensures that a function or special form was called with the correct number of arguments"""
    if not got_len == exp_len:
        raise error.LispException("{0} expects {1} argument; got {2}".format(f, exp_len, got_len))
    



#TODO: decouple display from the interpreter itself. Allow multiple frontends.
class bcolors:
    """Colors used in the REPL prompt."""
    PROMPT = '\033[92m'
    OKBLUE = '\033[94m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''


if __name__ == "__main__":
    d_list = copy.copy(SExp("NIL"))

    if len(sys.argv) == 1:
        try:
            interpreter(d_list)
        except EOFError:
            print ""
    elif len(sys.argv) == 2: #process a file of lisp expressions
        infile = file(sys.argv[1], "r")
        tokens = get_tokens(infile.read())
        for sexp in parse_gen(tokens):
            try:
                print str(eval_lisp(sexp, SExp("NIL"), d_list))
            except error.LispException as inst:
                print "error: " + inst.args[0]
            except RuntimeError:
                print "runtime error. deep recursion not yet supported"
        infile.close()
    else:
        print "Usage: interpreter.py [input file]"
        print ""
        print "Note that [input file] is optional. If provided, all LISP expressions in the file"
        print "will be read, eval'd and printed in order. Otherwise, the interpreter starts."""
        print ""
        print ""
