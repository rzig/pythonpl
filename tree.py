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
        if ttype == ExpressionType.ASSIGN_EXPRESSION:
            self.const = arg3
            self.left = arg1
            self.right = arg2
        elif ttype == ExpressionType.BINARY_EXPRESSION:
            self.op = arg3
            self.left = arg1
            self.right = arg2
        elif ttype == ExpressionType.IDENTIFIER_EXPRESSION:
            self.iden = arg1
        elif ttype == ExpressionType.NUMBER_EXPRESSION:
            self.num = arg1

@unique
class OperationType(IntEnum):
  ADD = 0
  SUB = 1
  MUL = 2
  DIV = 3
  EQUALITY = 4
  LESS = 5
  GREATER = 6

@unique
class StatementType(IntEnum):
    LET_STATEMENT = 0
    CONST_STATEMENT = 1
    WHILE_STATEMENT = 2
    IF_STATEMENT = 3
    EXPRESSION_STATEMENT = 4
    PRINT_STATEMENT = 5

class Statement:
    def __init__(self, ttype: StatementType, arg1, arg2=None):
        self.type = ttype
        if ttype == StatementType.LET_STATEMENT:
            self.left = arg1
            self.right = arg2
        elif ttype == StatementType.CONST_STATEMENT:
            self.left = arg1
            self.right = arg2
        elif ttype == StatementType.WHILE_STATEMENT:
            self.cond = arg1
            self.body = arg2
        elif ttype == StatementType.IF_STATEMENT:
            self.cond = arg1
            self.body = arg2
        elif ttype == StatementType.EXPRESSION_STATEMENT:
            self.expr = arg1
        elif ttype == StatementType.PRINT_STATEMENT:
            self.expr = arg1