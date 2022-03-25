import lexer

myProgram = "let x = 3; let b = c;"

tokens = lexer.lex(myProgram)

for token in tokens:
    print(str(token))