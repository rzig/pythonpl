from enum import IntEnum, unique
from typing import List

@unique
class TokenType(IntEnum):
    LET = 0
    CONST = 1
    IDENTIFIER = 2
    GREATER_THAN = 3
    LESS_THAN = 4
    EQUALS = 5
    EQUALS_EQUALS = 6
    LEFT_PAREN = 7,
    RIGHT_PAREN = 8
    LEFT_BRACKET = 9
    RIGHT_BRACKET = 10
    LEFT_BRACE = 11
    RIGHT_BRACE = 12
    SEMI = 13
    NUMBER = 14
    PRINT = 15
    WHILE = 16
    IF = 17
    PLUS = 18
    MINUS = 19
    TIMES = 20
    DIVIDE = 21

class Token: 
    def __init__(self, lexed: str, line: int, col: int, ttype: TokenType):
        self.lexed = lexed
        self.line = line
        self.col = col
        self.type = ttype

    def __str__(self):
        return "<Token " + str(self.type) + "@" + str(self.line) + "," + str(self.col) + ": \"" + self.lexed + "\">"

keywords = {
    "let": TokenType.LET,
    "const": TokenType.CONST,
    "while": TokenType.WHILE,
    "if": TokenType.IF,
    "print": TokenType.PRINT
}

symbols = {
    ">": TokenType.GREATER_THAN,
    "<": TokenType.LESS_THAN,
    "=": TokenType.EQUALS,
    "==": TokenType.EQUALS_EQUALS,
    "(": TokenType.LEFT_PAREN,
    ")": TokenType.RIGHT_PAREN,
    "[": TokenType.LEFT_BRACKET,
    "]": TokenType.RIGHT_BRACKET,
    "{": TokenType.LEFT_BRACE,
    "}": TokenType.RIGHT_BRACE,
    ";": TokenType.SEMI,
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "*": TokenType.TIMES,
    "/": TokenType.DIVIDE
}

whitespace = set([" ", "\t"])
newline = set(["\n"])
terminator = set([";"])
numeric = set([str(x) for x in range(10)])

def starts_sym(letter: str):
    op_firsts = [x[0] for x in symbols.keys()]
    return letter in op_firsts

def is_sym(possible:str):
    return possible in list(symbols.keys())

def starts_kw(letter:str)->bool:
    kw_firsts = [x[0] for x in keywords.keys()]
    return letter in kw_firsts

def is_kw(possible:str)->bool:
    return possible in list(keywords.keys())

def is_whitespace(possible:str)->bool:
    return possible in whitespace

def is_newline(possible:str)->bool:
    return possible in newline

def is_terminator(possible:str)->bool:
    return possible in terminator

def is_numeric(possible:str)->bool:
    return possible in numeric

def lex(program: str) -> List[Token]:
    line = 1
    col = 1
    idx = 0
    tokens = []
    while idx < len(program):
        current_token = program[idx]
        #print(current_token, starts_sym(current_token))
        token_instance = None
        if starts_sym(current_token):
            while idx + 1 < len(program) and is_sym(current_token + program[idx+1]):
                current_token += program[idx + 1]
                idx += 1
            token_instance = Token(current_token, line, col, symbols[current_token])
        elif is_newline(current_token):
            line += 1
            col = 1
        elif is_whitespace(current_token):
            while idx + 1 < len(program) and is_whitespace(program[idx + 1]):
                current_token += program[idx + 1]
                idx += 1
        elif is_terminator(current_token):
            token_instance = Token(current_token, line, col, TokenType.SEMI)
        elif is_numeric(current_token):
            while idx + 1 < len(program) and is_numeric(program[idx+1]):
                current_token += program[idx + 1]
                idx += 1
            token_instance = Token(current_token, line, col, TokenType.NUMBER)
        else:
            # reading a string in, read until we see a space/whiteline and
            # then we will check to see if it is a keyword or not
            while idx + 1 < len(program) and not is_whitespace(program[idx+1]) and not is_terminator(program[idx+1]) and not is_sym(program[idx+1]):
                current_token += program[idx + 1]
                idx += 1
            if is_kw(current_token):
                token_instance = Token(current_token, line, col, keywords[current_token])
            else:
                token_instance = Token(current_token, line, col, TokenType.IDENTIFIER)
        idx += 1
        col += len(current_token) if not is_newline(current_token) else 0
        if token_instance:
            tokens.append(token_instance)
    return tokens
