import sys
import argparse
from pars_lex import CompilerLexer, CompilerParser
    
if __name__ == '__main__':
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-i", "--input")
    argParser.add_argument("-o", "--output")
    params = vars(argParser.parse_args())
    print(params)
    inFile = sys.stdin
    outFile = sys.stdout
    try:
        if params['input'] is not None:
            inFile = open(params['input'], 'r')
    except:
        print(f"Cannot access {params['input']}. Standard input will be used insted.")
    try:
        if  params['output'] is not None:
            outFile = open(params['output'], 'w', newline='\n')
    except:
        print(f"Cannot open {params['output']}. Standard output will be used insted.")

    lexer = CompilerLexer()
    parser = CompilerParser()
    x, mem = parser.parse(lexer.tokenize(inFile.read()))
    print(x)
    inFile.close()
    outFile.close()