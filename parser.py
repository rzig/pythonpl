from typing import List
from tree import *
from lexer import TokenType,Token

class Chain:
    def __init__(self, failure=None):
        self.fail = failure
    def __or__(self, x):
        if x != None:
            return x
        else:
            return Chain(self.fail)

def optional(expr):
    return expr if type(expr) != Chain else expr.fail
    
class Parser:
    def __init__(self, program: List[Token]):
        self.program = program 
        self.cur_index = 0
    
    def match(self, ttype: TokenType) -> Token:
        if tokens[self.cur_index].type == ttype:
            self.cur_index += 1
            return tokens[self.cur_index-1]
        else:
            return None
            
    def match(self,*args) -> bool:
        return 

    def parse_program(self) -> List[Statement]:
        program = []
        stmt = parse_statement()
        while stmt:
            program.append(stmt)
            stmt = parse_statement()
        return program
            
    def parse_statement(self) -> Statement:
        return Chain(None) | parse_let_statement() | parse_const_statement() | parse_while_statement() | parse_if_statement() | Statement(EXPRESSION_STATEMENT, parse_expression())
                
    def parse_let_statement(self) -> Statement:
        start = self.cur_index
        if not match(LET):
            return None
        iden = match(IDENTIFIER)
        if iden is None:
            self.cur_index = start
            return None
        if not match(EQUALS):
            self.cur_index = start
            return None
        expr = parse_expression()
        if not expr:
            self.cur_index = start
            return None
        if not match(SEMI):
            self.cur_index = start
            return None
        return Statement(LET_STATEMENT, iden.lexed, expr)
        
    def parse_const_statement(self) -> Statement:
        start = self.cur_index
        if not match(CONST):
            return None
        iden = match(IDENTIFIER)
        if not iden:
            self.cur_index = start
            return None
        if not match(EQUALS):
            self.cur_index = start
            return None
        expr = parse_expression()
        if not expr:
            self.cur_index = start
            return None
        if not match(SEMI):
            self.cur_index = start
            return None
        return Statement(CONST_STATEMENT, iden.lexed, expr)
        
    def parse_while_statement(self) -> Statement:
        start = self.cur_index
        if not match(WHILE):
            return None
        cond = parse_expression()
        if not expr:
            self.cur_index = start
            return None
        if not match(LEFT_BRACE):
            self.cur_index = start
            return None
        stmts = []
        stmt = parse_statement()
        while stmt:
            stmts.append(stmt)
            stmt = parse_statement()
        if not match(RIGHT_BRACE):
            self.cur_index = start
            return None
        return Statement(WHILE_STATEMENT, cond, stmts)
        
    def parse_if_statement(self) -> Statement:
        start = self.cur_index
        if not match(IF):
            return None
        cond = parse_expression()
        if not expr:
            self.cur_index = start
            return None
        if not match(LEFT_BRACE):
            self.cur_index = start
            return None
        stmts = []
        stmt = parse_statement()
        while stmt:
            stmts.append(stmt)
            stmt = parse_statement()
        if not match(RIGHT_BRACE):
            self.cur_index = start
            return None
        return Statement(IF_STATEMENT, cond, stmts)
