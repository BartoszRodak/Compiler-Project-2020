import sys
import argparse
from pars_lex import CompilerLexer, CompilerParser
from block_manager import BlockManager
from printer import Printer

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
        print(
            f"Cannot access {params['input']}. Standard input will be used insted.")
    try:
        if params['output'] is not None:
            outFile = open(params['output'], 'w', newline='\n')
    except:
        print(
            f"Cannot open {params['output']}. Standard output will be used insted.")

    lexer = CompilerLexer()
    parser = CompilerParser()
    tokens = lexer.tokenize(inFile.read())
    (tree, memory) = parser.parse(tokens)

    bm = BlockManager(tree)
    printer = Printer(bm, memory)
    outFile.write(printer.print())
    inFile.close()
    outFile.close()
