import sys
import getopt
from sly import Lexer, Parser

class Operation:
    pass

class Parameter:
    pass

class Variable:
    pass

class Basicblock: 
    variables = {}
    operations = {}

    def __init__(self):
        pass

    def isValid(self):
        pass

class CompilerLexer(Lexer):
    # tokens = {NAME, NUMBER, PLUS, TIMES, MINUS, DIVIDE, ASSIGN, LPAREN, RPAREN}
    # ignore = ' \t'

    # # Tokens
    # NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    # NUMBER = r'\d+'

    # # Special symbols
    # PLUS = r'\+'
    # MINUS = r'-'
    # TIMES = r'\*'
    # DIVIDE = r'/'
    # ASSIGN = r'='
    # LPAREN = r'\('
    # RPAREN = r'\)'

    # # Ignored pattern
    # ignore_newline = r'\n+'

    # # Extra action for newlines
    # def ignore_newline(self, t):
    #     self.lineno += t.value.count('\n')

    # def error(self, t):
    #     print("Illegal character '%s'" % t.value[0])
    #     self.index += 1


class CompilerParser(Parser):
    pass

if __name__ == "__main__":
    params = getopt.getopt(sys.argv[1:], "i:o:", ["in", "out"])
    params = {i[1]: i[2] for i in params}
    inFile = sys.stdin
    outFile = sys.stdout
    if '-i' in params:
        inFile = open("")
    
    