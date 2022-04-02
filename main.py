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

tokens = lexer.lex(myProgram)

p = Parser(tokens)

res = p.parse_program()

env = Environment()
for stmt in res:
    env.execute_stmt(stmt)
