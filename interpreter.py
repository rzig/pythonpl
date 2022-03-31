from tree import *

class Environment:
  def __init__(self):
    # store variables as a dictionary
    self.variables = {}
    self.const = {}
  
  def execute_stmt(self, smt: Statement):
    if smt.type is StatementType.LET_STATEMENT:
      if smt.left in self.variables or smt.left in self.const:
        raise Exception("Cannot create a variable when one with the same name already exists")
      self.variables[smt.left] = smt.right 
    
    elif smt.type is StatementType.CONST_STATEMENT:
      if smt.left in self.const:
        raise Exception("Cannot reassign a const value")
      if smt.left in self.variables:
        raise Exception("Cannot create a variable when one with the same name already exists")
      self.const[smt.left] = smt.right
    
    elif smt.type is StatementType.WHILE_STATEMENT:
      # could be necessary for checking 
      # if not isinstance(smt.cond, bool):
      #   raise Exception("While statement expected boolean condition")
      while smt.cond is 1:
        for smt_in_while in smt.body:
          self.execute_stmt(smt_in_while)
    
    elif smt.type is StatementType.EXPRESSION_STATEMENT:
      self.execute_expr(smt.arg1)
  
  def execute_expr(self, expr: Expression):
    if expr.type is ExpressionType.ASSIGN_EXPRESSION:
      if self.variables[expr.left] not in self.variables:
        raise Exception("Assigning to variable that has not been declared")
      self.variables[expr.left] = expr.right
    
    elif expr.type is ExpressionType.BINARY_EXPRESSION:
      # find which op to do
      if expr.op is OperationType.ADD:
        left = self.execute_expr(expr.left)
        right = self.execute_expr(expr.right)
        return left + right
      elif expr.op is OperationType.SUB:
        left = self.execute_expr(expr.left)
        right = self.execute_expr(expr.right)
        return left - right
      elif expr.op is OperationType.MUL:
        left = self.execute_expr(expr.left)
        right = self.execute_expr(expr.right)
        return left * right
      elif expr.op is OperationType.DIV:
        left = self.execute_expr(expr.left)
        right = self.execute_expr(expr.right)
        return left / right

    elif expr.type is ExpressionType.IDENTIFIER_EXPRESSION:
      if expr.iden in self.variables:
        return self.variables[expr.iden]
      elif expr.iden in self.const:
        return self.const[expr.iden]
      else:
        raise Exception("Variable does not exist")
    
    elif expr.type is ExpressionType.NUMBER_EXPRESSION:
      return expr.num