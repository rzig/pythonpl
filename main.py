import lexer
from parser import Parser
from lexer import Token, TokenType
from interpreter import Environment

myProgram = """
let a = 2;
while a < 5 {
    print a;
    a = a + 2;
}
if a > 10 {
    print 0 - 10000000;
}
print a - 10;
const b = a;
print b;
b = 10;
"""

# myProgram = "let a_b = 3;"
tokens = lexer.lex(myProgram)

# for token in tokens:
#     print(str(token))

# t1 = Token("hello", 1, 1, TokenType.LET)
# t2 = Token("hello", 1, 1, TokenType.IDENTIFIER)
# t3 = Token("", 1, 1, TokenType.EQUALS)
# t4 = Token("", 1, 1, TokenType.IDENTIFIER)
# t5 = Token("", 1, 1, TokenType.SEMI)

p = Parser(tokens)

res = p.parse_program()

env = Environment()
for stmt in res:
    env.execute_stmt(stmt)

# class Chain:
#     def __init__(self, failure=None):
#         self.fail = failure
#     def __or__(self, x):
#         if x != None:
#             return x
#         else:
#             return Chain(self.fail)
# def mf(a):
#     print("in mf")
#     return "b"

# print(Chain(None) | "a" | mf("a"))

# def optional(*args):
#     items = args
#     for item in items:
#         res = item()
#         if res:
#             return res
#     return None