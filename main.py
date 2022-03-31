import lexer

myProgram = "let x = 3; const b = c; \nwhile b < c { x = x + 1; } if a > d { y = 0; }; let a_b-4 = 3;" # BUG: lexer should not consider "a_b-4" a single identifier

tokens = lexer.lex(myProgram)

for token in tokens:
    print(str(token))
