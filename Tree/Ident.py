# Ident -- Parse tree node class for representing identifiers

from Tree import *
from Print import Printer

class Ident(Node):
    def __init__(self, n):
        self.name = n

    def print(self, n, p=False):
        Printer.printIdent(n, self.name)

    def getName(self):
        return self.name

    def isSymbol(self):
        return True

    def eval(self, node, env):
        a = Cons( Ident(node.getName()), Nil())
        args = eval_list(a, env)
        if(not args.isNull()):
            if(args.getCar().isPair()):
                pass #TODO
            elif (args.getCar().isNumber()):
                return IntLit(args.getCar().getVal())
            elif (args.getCar().isString()):
                return StrLit(args.getCar().getStrVal())
            elif (args.getCar().isBool()):
                return BoolLit(args.getCar().getBoolean())
            else:
                return Nil()
        else:
            return None

        #return new StrLit("")


    def eval_list(self, node, env):
        if ((node is None) or (node.isNull())):
            lst = Cons(Nil(), Nil())
            return lst
        else:
            arg1 = node.getCar()
            rest = node.getCdr()

            if(arg1.isSymbol()):
                arg1 = env.lookup(arg1)
            if ((arg1 is None) or (arg1.isNull())):
                return Nil()
            lst = Cons(arg1.eval(env), eval_list(rest, env))
            return lst


if __name__ == "__main__":
    id = Ident("foo")
    id.print(0)
