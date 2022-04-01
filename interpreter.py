from lib2to3.pgen2.token import GREATER
from tree import *

class Environment:
  def __init__(self):
    # store variables as a dictionary
    self.variables = {}
    self.const = {}
  
  def execute_stmt(self, smt: Statement):
    if smt.type == StatementType.LET_STATEMENT:
      if smt.left in self.variables or smt.left in self.const:
        raise Exception("Cannot create a variable when one with the same name already exists")
      self.variables[smt.left] = self.execute_expr(smt.right)
    
    elif smt.type == StatementType.CONST_STATEMENT:
      if smt.left in self.const:
        raise Exception("Cannot reassign a const value")
      if smt.left in self.variables:
        raise Exception("Cannot create a variable when one with the same name already exists")
      self.const[smt.left] = self.execute_expr(smt.right)
    
    elif smt.type == StatementType.WHILE_STATEMENT:
      while self.execute_expr(smt.cond) == 1: 
        for smt_in_while in smt.body:
          self.execute_stmt(smt_in_while)
    
    elif smt.type == StatementType.EXPRESSION_STATEMENT:
      self.execute_expr(smt.expr)

    elif smt.type == StatementType.PRINT_STATEMENT:
      print(self.execute_expr(smt.expr))
  
  def execute_expr(self, expr: Expression):
    if expr.type == ExpressionType.ASSIGN_EXPRESSION:
      if expr.left not in self.variables:
        if expr.left in self.const:
          raise Exception("Cannot reassign to a constant value")
        raise Exception("Assigning to variable that has not been declared")
      self.variables[expr.left] = self.execute_expr(expr.right)
    
    elif expr.type == ExpressionType.BINARY_EXPRESSION:
      # find which op to do
      if expr.op == OperationType.ADD:
        left = self.execute_expr(expr.left)
        right = self.execute_expr(expr.right)
        return left + right
      elif expr.op == OperationType.SUB:
        left = self.execute_expr(expr.left)
        right = self.execute_expr(expr.right)
        return left - right
      elif expr.op == OperationType.MUL:
        left = self.execute_expr(expr.left)
        right = self.execute_expr(expr.right)
        return left * right
      elif expr.op == OperationType.DIV:
        left = self.execute_expr(expr.left)
        right = self.execute_expr(expr.right)
        return left / right
      elif expr.op == OperationType.EQUALITY:
        left = self.execute_expr(expr.left)
        right = self.execute_expr(expr.right)
        return 1 if left == right else 0
      elif expr.op == OperationType.LESS:
        left = self.execute_expr(expr.left)
        right = self.execute_expr(expr.right)
        return 1 if left < right else 0
      elif expr.op == OperationType.GREATER:
        left = self.execute_expr(expr.left)
        right = self.execute_expr(expr.right)
        return 1 if left > right else 0
    
    elif expr.type == ExpressionType.IDENTIFIER_EXPRESSION:
      if expr.iden in self.variables:
        return self.variables[expr.iden]
      elif expr.iden in self.const:
        return self.const[expr.iden]
      else:
        raise Exception("Variable does not exist")
    
    elif expr.type == ExpressionType.NUMBER_EXPRESSION:
      return expr.num