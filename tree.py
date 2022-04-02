from enum import IntEnum, unique

@unique
class ExpressionType(IntEnum):
    ASSIGN_EXPRESSION = 0
    BINARY_EXPRESSION = 1
    IDENTIFIER_EXPRESSION = 2
    NUMBER_EXPRESSION = 3

class Expression:
    def __init__(self, ttype: ExpressionType, arg1, arg2=None, arg3=None):
        pass

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
        pass