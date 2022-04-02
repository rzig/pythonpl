from tree import *

class Environment:
  def __init__(self):
    # store variables as a dictionary
    self.variables = {}
    self.const = {}
  
  def execute_stmt(self, smt: Statement):
    pass
  
  def execute_expr(self, expr: Expression):
    pass