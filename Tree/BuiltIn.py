# BuiltIn -- the data structure for built-in functions

# Class BuiltIn is used for representing the value of built-in functions
# such as +.  Populate the initial environment with
# (name, BuiltIn(name)) pairs.

# The object-oriented style for implementing built-in functions would be
# to include the Python methods for implementing a Scheme built-in in the
# BuiltIn object.  This could be done by writing one subclass of class
# BuiltIn for each built-in function and implementing the method apply
# appropriately.  This requires a large number of classes, though.
# Another alternative is to program BuiltIn.apply() in a functional
# style by writing a large if-then-else chain that tests the name of
# the function symbol.

import sys
from Parse import *
from Tree import Node
from Tree import BoolLit
from Tree import IntLit
from Tree import StrLit
from Tree import Ident
from Tree import Nil
from Tree import Cons
from Tree import TreeBuilder
#from Tree import Unspecific

class BuiltIn(Node):
    env = None
    util = None

    @classmethod
    def setEnv(cls, e):
        cls.env = e

    @classmethod
    def setUtil(cls, u):
        cls.util = u

    def __init__(self, s):
        self.symbol = s                 # the Ident for the built-in function

    def getSymbol(self):
        return self.symbol

    def isProcedure(self):
        return True

    def print(self, n, p=False):
        for _ in range(n):
            sys.stdout.write(' ')
        sys.stdout.write("#{Built-In Procedure ")
        if self.symbol != None:
            self.symbol.print(-abs(n) - 1)
        sys.stdout.write('}')
        if n >= 0:
            sys.stdout.write('\n')
            sys.stdout.flush()

    # TODO: The method apply() should be defined in class Node
    # to report an error.  It should be overridden only in classes
    # BuiltIn and Closure.
    def apply(self, args):

        if args == None:
            return None
        
        symbolName = self.symbol.getName()

        arg1 = args.getCar()

        if arg1 == None or arg1.isNull():
            arg1 = Nil()

        arg2 = args.getCdr()

        if arg2 == None or arg2.isNull():
            arg2 = Nil()

        if symbolName == '+':
            if arg1.isNumber() and arg2.isNumber():
                x = arg1.getIntVal()
                y = arg2.getIntVal()
                return IntLit(x + y)
            else:
                print('bad argument for +')
                return StrLit("")
        elif symbolName == '-':
            if arg1.isNumber() and arg2.isNumber():
                x = arg1.getIntVal()
                y = arg2.getIntVal()
                return IntLit(x - y)
            else:
                print('bad argument for -')
                return StrLit("")
        elif symbolName == '*':
            if arg1.isNumber() and arg2.isNumber():
                x = arg1.getIntVal()
                y = arg2.getIntVal()
                return IntLit(x * y)
            else:
                print('bad argument for *')
                return StrLit("")
        elif symbolName == '/':
            if arg1.isNumber() and arg2.isNumber():
                x = arg1.getIntVal()
                y = arg2.getIntVal()
                return IntLit(x / y)
            else:
                print('bad argument for /')
                return StrLit("")
        elif symbolName == '=':
            if arg1.isNumber() and arg2.isNumber():
                x = arg1.getIntVal()
                y = arg2.getIntVal()
                return BoolLit(x == y)
            else:
                print('bad argument for =')
        elif symbolName == '<':
            if arg1.isNumber() and arg2.isNumber():
                x = arg1.getIntVal()
                y = arg2.getIntVal()
                return BoolLit(x < y)
            else:
                print('bad argument for <')
        elif symbolName == '>':
            if arg1.isNumber() and arg2.isNumber():
                x = arg1.getIntVal()
                y = arg2.getIntVal()
                return BoolLit(x > y)
            else:
                print('bad argument for >')
        elif symbolName == 'car':
            if arg1.isNull():
                return arg1
            return arg1.getCar()
        elif symbolName == 'cdr':
            if arg1.isNull():
                return arg1
            return arg1.getCdr()
        elif symbolName == 'cons':
            return Cons(arg1, arg2)
        elif symbolName == 'set-car!':
            arg1.setCar(arg2)
            return arg1
        elif symbolName == 'set-cdr!':
            arg1.setCdr(arg2)
            return arg1
        elif symbolName == 'symbol?':
            return BoolLit(arg1.isSymbol())
        elif symbolName == 'number?':
            return BoolLit(arg1.isNumber())
        elif symbolName == 'null?':
            return BoolLit(arg1.isNull())
        elif symbolName == 'pair?':
            return BoolLit(arg1.isPair())
        elif symbolName == 'eq?':
            if (arg1.isBool() and arg2.isBool()) or (arg1.isNumber() and arg2.isNumber()) or (arg1.isString() and arg2.isString()):
                return BoolLit(arg1 == arg2)
            elif arg1.isSymbol() and arg2.isSymbol():
                return BoolLit(arg1.getName() == arg2.getName())
            elif arg1.isNull() and arg2.isNull():
                return BoolLit(True)
            elif arg1.isPair() and arg2.isPair():
                frontArgs = Cons(arg1.getCar(), Cons(arg2.getCar(), Nil))
                backArgs = Cons(arg1.getCdr(), Cons(arg2.getCdr(), Nil))
                return BoolLit(apply(frontArgs) and apply(backArgs))
            return BoolLit(false)
        elif symbolName == 'procedure?':
            return BoolLit(arg1.isProcedure)
        elif symbolName == 'display':
            return arg1
        elif symbolName == 'newline':
            return StrLit("", false)
        elif symbolName == 'exit' or symbolName == 'quit':
            exit()
        elif symbolName == 'write':
            arg1.print(0)
        elif symbolName == 'eval':
            return arg1
        elif symbolName == 'apply':
            return arg1.apply(arg2)
        elif symbolName == 'read':
            parser = Parser()
            return parser.parseExp()
        elif symbolName == 'interaction-environment':
            self.env.print(0)
        else:
            arg1.print(0)
            return Nil()
        return StrLit('>')















        #return StrLit("Error: BuiltIn.apply not yet implemented")

        ## The easiest way to implement BuiltIn.apply is as an
        ## if-then-else chain testing for the different names of
        ## the built-in functions.  E.g., here's how load could
        ## be implemented:
 
        # if name == "load":
        #     if not arg1.isString():
        #         self._error("wrong type of argument")
        #         return Nil.getInstance()
        #     filename = arg1.getStrVal()
        #     try:
        #         scanner = Scanner(open(filename))
        #         builder = TreeBuilder()
        #         parser = Parser(scanner, builder)

        #         root = parser.parseExp()
        #         while root != None:
        #             root.eval(BuiltIn.env)
        #             root = parser.parseExp()
        #     except IOError:
        #         self._error("could not find file " + filename)
        #     return Nil.getInstance()  # or Unspecific.getInstance()
