from enum import IntEnum, unique

@unique
class ExpressionType(IntEnum):
    ASSIGN_EXPRESSION = 0
    BINARY_EXPRESSION = 1
    IDENTIFIER = 2
    NUMBER = 3

class Expression:
    def __init__(self, ttype: ExpressionType, arg1, arg2=None, arg3=None):
        self.type = ttype
        if ttype == ASSIGN_EXPRESSION:
            self.const = arg3
            self.left = arg1
            self.right = arg2
        elif type == BINARY_EXPRESSION:
            self.op = arg3
            self.left = arg1
            self.right = arg2
        elif type == IDENTIFIER:
            self.iden = arg1
        elif type == NUMBER:
            self.num = arg1
