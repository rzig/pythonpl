from typing import List
from tree import Expression, ExpressionType, Statement, StatementType, OperationType
from lexer import TokenType,Token

def optional(*args):
    for item in args:
        res = item()
        if res:
            return res
    return None

def sequence(*args):
    res = []
    for f in args:
        callres = f()
        res.append(callres)
        if callres == None:
            return [None]*len(args)
    return res
    
class Parser:
    def __init__(self, program: List[Token]):
        self.program = program 
        self.cur_index = 0