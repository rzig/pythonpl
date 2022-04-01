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
    
    def match(self, ttype: TokenType) -> Token:
        if (not self.cur_index >= len(self.program)) and self.program[self.cur_index].type == ttype:
            self.cur_index += 1
            return self.program[self.cur_index-1]
        else:
            return None

    def parse_program(self) -> List[Statement]:
        program = []
        stmt = self.parse_statement()
        while stmt:
            program.append(stmt)
            stmt = self.parse_statement()
        return program
            
    def parse_statement(self) -> Statement:
        return optional(
            self.parse_print_statement,
            self.parse_let_statement,
            self.parse_const_statement,
            self.parse_while_statement,
            self.parse_if_statement,
            self.parse_expression_statement
        )

    def parse_print_statement(self) -> Statement:
        if self.match(TokenType.PRINT):
            printed = self.parse_expression()
            if not printed:
                raise Exception("Expected expression after print statement")
            if not self.match(TokenType.SEMI):
                raise Exception("Expected semicolon")
            return Statement(StatementType.PRINT_STATEMENT, printed)
        else:
            return None
                
    def parse_expression_statement(self) -> Statement:
        expr = self.parse_expression()
        if not expr:
            return None
        if not self.match(TokenType.SEMI):
            raise Exception("Expected semicolon")
        return Statement(StatementType.EXPRESSION_STATEMENT, expr)

    def parse_let_statement(self) -> Statement:
        start = self.cur_index
        if not self.match(TokenType.LET):
            return None
        iden = self.match(TokenType.IDENTIFIER)
        if iden is None:
            self.cur_index = start
            return None
        if not self.match(TokenType.EQUALS):
            self.cur_index = start
            return None
        expr = self.parse_expression()
        if not expr:
            self.cur_index = start
            return None
        if not self.match(TokenType.SEMI):
            self.cur_index = start
            return None
        return Statement(StatementType.LET_STATEMENT, iden.lexed, expr)
        
    def parse_const_statement(self) -> Statement:
        start = self.cur_index
        if not self.match(TokenType.CONST):
            return None
        iden = self.match(TokenType.IDENTIFIER)
        if not iden:
            self.cur_index = start
            return None
        if not self.match(TokenType.EQUALS):
            self.cur_index = start
            return None
        expr = self.parse_expression()
        if not expr:
            self.cur_index = start
            return None
        if not self.match(TokenType.SEMI):
            self.cur_index = start
            return None
        return Statement(StatementType.CONST_STATEMENT, iden.lexed, expr)
        
    def parse_while_statement(self) -> Statement:
        start = self.cur_index
        if not self.match(TokenType.WHILE):
            return None
        cond = self.parse_expression()
        if not cond:
            self.cur_index = start
            return None
        if not self.match(TokenType.LEFT_BRACE):
            self.cur_index = start
            return None
        stmts = []
        stmt = self.parse_statement()
        while stmt:
            stmts.append(stmt)
            stmt = self.parse_statement()
        if not self.match(TokenType.RIGHT_BRACE):
            self.cur_index = start
            return None
        return Statement(StatementType.WHILE_STATEMENT, cond, stmts)
        
    def parse_if_statement(self) -> Statement:
        start = self.cur_index
        if not self.match(TokenType.IF):
            return None
        cond = self.parse_expression()
        if not cond:
            self.cur_index = start
            return None
        if not self.match(TokenType.LEFT_BRACE):
            self.cur_index = start
            return None
        stmts = []
        stmt = self.parse_statement()
        while stmt:
            stmts.append(stmt)
            stmt = self.parse_statement()
        if not self.match(TokenType.RIGHT_BRACE):
            self.cur_index = start
            return None
        return Statement(StatementType.IF_STATEMENT, cond, stmts)

    def parse_expression(self) -> Statement:
        return optional(
            self.parse_assignment,
            self.parse_equality
        )

    def parse_assignment(self) -> Statement:
        start = self.cur_index
        iden = self.match(TokenType.IDENTIFIER)
        if not iden:
            self.cur_index = start
            return None
        if not self.match(TokenType.EQUALS):
            self.cur_index = start
            return None
        assign = self.parse_expression()
        if not assign:
            raise Exception("Expected assignment")
        return Expression(ExpressionType.ASSIGN_EXPRESSION, iden.lexed, assign)
        
    def parse_equality(self) -> Statement:
        start = self.cur_index
        left = self.parse_comparison()
        if not left:
            return None
        if not self.match(TokenType.EQUALS_EQUALS):
            return left
        right = self.parse_equality()
        if right:
            return Expression(ExpressionType.BINARY_EXPRESSION, left, right, OperationType.EQUALITY)
        else:
            return right
            
    def parse_comparison(self) -> Statement:
        start = self.cur_index
        left = self.parse_term()
        if not left:
            return None
        op = optional(lambda: self.match(TokenType.GREATER_THAN), lambda: self.match(TokenType.LESS_THAN))
        if not op:
            return left
        right = self.parse_comparison()
        if right:
            return Expression(ExpressionType.BINARY_EXPRESSION, left, right, OperationType.GREATER if op.type == TokenType.GREATER_THAN else OperationType.LESS)
        else:
            return right
            
    def parse_term(self) -> Statement:
        start = self.cur_index
        left = self.parse_factor()
        if not left:
            return None
        op = optional(lambda: self.match(TokenType.PLUS), lambda: self.match(TokenType.MINUS))
        if not op:
            return left
        right = self.parse_term()
        if right:
            return Expression(ExpressionType.BINARY_EXPRESSION, left, right, OperationType.ADD if op.type == TokenType.PLUS else OperationType.SUB)
        else:
            return right
            
    def parse_factor(self) -> Statement:
        start = self.cur_index
        left = self.parse_primary()
        if not left:
            return None
        op = optional(lambda: self.match(TokenType.TIMES), lambda: self.match(TokenType.DIVIDE))
        if not op:
            return left
        right = self.parse_factor()
        if right:
            return Expression(ExpressionType.BINARY_EXPRESSION, left, right, OperationType.MUL if op.type == TokenType.TokenType.TIMES else OperationType.DIV)
        else:
            return right

    def parse_primary(self) -> Statement:
        return optional(
            self.parse_number,
            self.parse_identifier,
            lambda: sequence(
                lambda: self.match(TokenType.LEFT_PAREN),
                lambda: self.parse_expression(),
                lambda: self.match(TokenType.RIGHT_PAREN)
            )[1]
        )

    def parse_number(self) -> Statement:
        start = self.cur_index
        num = self.match(TokenType.NUMBER)
        if num:
            return Expression(ExpressionType.NUMBER_EXPRESSION, int(num.lexed))
        else:
            self.cur_index = start
            return None

    def parse_identifier(self) -> Statement:
        start = self.cur_index
        iden = self.match(TokenType.IDENTIFIER)
        if iden:
            return Expression(ExpressionType.IDENTIFIER_EXPRESSION, iden.lexed)
        else:
            self.cur_index = start
            return None