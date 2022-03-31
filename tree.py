from enum import IntEnum, unique

@unique
class ExpressionType(IntEnum):
    ASSIGN_EXPRESSION = 0
    BINARY_EXPRESSION = 1
    IDENTIFIER_EXPRESSION = 2
    NUMBER_EXPRESSION = 3

class Expression:
    def __init__(self, ttype: ExpressionType, arg1, arg2=None, arg3=None):
        self.type = ttype
        if ttype == ASSIGN_EXPRESSION:
            self.const = arg3
            self.left = arg1
            self.right = arg2
        elif ttype == BINARY_EXPRESSION:
            self.op = arg3
            self.left = arg1
            self.right = arg2
        elif ttype == IDENTIFIER_EXPRESSION:
            self.iden = arg1
        elif ttype == NUMBER_EXPRESSION:
            self.num = arg1

@unique
class StatementType(IntEnum):
    LET_STATEMENT = 0
    CONST_STATEMENT = 1
    WHILE_STATEMENT = 2
    IF_STATEMENT = 3
    EXPRESSION_STATEMENT = 4

class Statement:
    def __init__(self, ttype: StatementType, arg1, arg2=None):
        self.type = ttype
        if ttype == LET_STATEMENT:
            self.left = arg1
            self.right = arg2
        elif ttype == CONST_STATEMENT:
            self.left = arg1
            self.right = arg2
        elif ttype == WHILE_STATEMENT:
            self.cond = arg1
            self.body = arg2
        elif ttype == IF_STATEMENT:
            self.cond = arg1
            self.body = arg2
        elif ttype == EXPRESSION_STATEMENT:
            self.expr = arg1
