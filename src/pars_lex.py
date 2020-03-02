from sly import Parser, Lexer
from abstract_syntax_tree import *
from memory_manager import *
from typing import Tuple


class CompilerLexer(Lexer):
    tokens = {PLUS, MINUS, TIMES, DIV, MOD,
              EQ, NEQ, LE, GE, LEQ, GEQ,
              ASSIGN,
              FOR, FROM, TO, DOWNTO, ENDFOR,
              WHILE, DO, ENDWHILE, ENDDO,
              READ, WRITE,
              IF, THEN, ELSE, ENDIF,
              IDENTIFIER, NUMBER,
              DECLARE, BEGIN, END}

    literals = {'(', ')', ';', ',', ':'}

    ignore = ' \t'
    ignore_comment = r'\[[^\]]*\]'

    IDENTIFIER = r'[_a-z]+'
    NUMBER = r'-?\d+'  # TODO check position
    PLUS = r'PLUS'
    MINUS = r'MINUS'
    TIMES = r'TIMES'
    DIV = r'DIV'
    MOD = r'MOD'
    NEQ = r'NEQ'
    EQ = r'EQ'
    LEQ = r'LEQ'
    LE = r'LE'
    GEQ = r'GEQ'
    GE = r'GE'
    ASSIGN = r'ASSIGN'
    ENDWHILE = r'ENDWHILE'
    ENDFOR = r'ENDFOR'
    FOR = r'FOR'
    FROM = r'FROM'
    DOWNTO = r'DOWNTO'
    TO = r'TO'
    WHILE = r'WHILE'
    ENDDO = r'ENDDO'
    DO = r'DO'
    READ = r'READ'
    WRITE = r'WRITE'
    ENDIF = r'ENDIF'
    IF = r'IF'
    THEN = r'THEN'
    ELSE = r'ELSE'
    DECLARE = r'DECLARE'
    BEGIN = r'BEGIN'
    END = r'END'

    @_(r'\n+')
    def newline(self, token):
        self.lineno += token.value.count('\n')

    def error(self, token):
        raise AssertionError(f"Line {token.lineno}: Syntax error. Symbol '{token.value}'")


class CompilerParser(Parser):
    tokens = CompilerLexer.tokens
    memory = MemoryManager()

    @_('DECLARE declarations BEGIN commands END')
    def program(self, p) -> Tuple[ProgramAST, MemoryManager]:
        return ProgramAST(p.commands), self.memory

    @_('BEGIN commands END')
    def program(self, p) -> Tuple[ProgramAST, MemoryManager]:
        return ProgramAST(p.commands), self.memory

    @_('declarations "," IDENTIFIER')
    def declarations(self, p) -> None:
        self.memory.declareVariable(p.IDENTIFIER)

    @_('declarations "," IDENTIFIER "(" NUMBER ":" NUMBER ")"')
    def declarations(self, p) -> None:
        self.memory.declareArray(p.IDENTIFIER, p.NUMBER0, p.NUMBER1)

    @_('IDENTIFIER')
    def declarations(self, p) -> None:
        self.memory.declareVariable(p.IDENTIFIER)

    @_('IDENTIFIER "(" NUMBER ":" NUMBER ")"')
    def declarations(self, p) -> None:
        self.memory.declareArray(p.IDENTIFIER, p.NUMBER0, p.NUMBER1)

    @_('commands command')
    def commands(self, p) -> list:
        p.commands.append(p.command)
        return p.commands

    @_('command')
    def commands(self, p) -> list:
        return [p.command]

    @_('identifier ASSIGN expression ";"')
    def command(self, p) -> AssignAction:
        return AssignAction(p.identifier, p.expression)

    @_('IF condition THEN commands ELSE commands ENDIF')
    def command(self, p) -> IfBlock:
        return IfBlock(p.condition, p.commands0, p.commands1)

    @_('IF condition THEN commands ENDIF')
    def command(self, p) -> IfBlock:
        return IfBlock(p.condition, p.commands)

    @_('WHILE condition DO commands ENDWHILE')
    def command(self, p) -> WhileLoopBlock:
        return WhileLoopBlock(p.commands, p.condition)

    @_('DO commands WHILE condition ENDDO')
    def command(self, p) -> WhileLoopBlock:
        return WhileLoopBlock(p.commands, p.condition, True)

    @_('FOR iterator FROM value TO value DO commands ENDFOR')
    def command(self, p) -> ForLoopBlock:
        p.iterator.setRange(p.value0, p.value1)
        loop = ForLoopBlock(p.commands, p.iterator)
        self.memory.remove(p.iterator)
        return loop

    @_('FOR iterator FROM value DOWNTO value DO commands ENDFOR')
    def command(self, p) -> ForLoopBlock:
        p.iterator.setRange(p.value0, p.value1, True)
        loop = ForLoopBlock(p.commands, p.iterator)
        self.memory.remove(p.iterator)
        return loop

    @_('READ identifier ";"')
    def command(self, p) -> IOAction:
        return IOAction(IOType.READ, p.identifier)

    @_('WRITE value ";"')
    def command(self, p) -> IOAction:
        return IOAction(IOType.WRITE, p.value)

    @_('value')
    def expression(self, p) -> Value:
        return p.value #TODO perhaps enclose in other class

    @_('value PLUS value',
       'value MINUS value',
       'value TIMES value',
       'value DIV value',
       'value MOD value')
    def expression(self, p) -> Calculation:
        return Calculation(CalculationType[p[1]], p.value0, p.value1)

    @_('value EQ value',
       'value NEQ value',
       'value LE value',
       'value GE value',
       'value LEQ value',
       'value GEQ value')
    def condition(self, p) -> BoolExpression:
        return BoolExpression(BoolOperator[p[1]], p.value0, p.value1)

    @_('NUMBER')
    def value(self, p) -> Value:
        return self.memory.getConstant(p.NUMBER)

    @_('identifier')
    def value(self, p) -> Value:
        return p.identifier

    @_('IDENTIFIER')
    def iterator(self, p):
        return self.memory.getIterator(p.IDENTIFIER)

    @_('IDENTIFIER')
    def identifier(self, p):
        return self.memory.getVariable(p.IDENTIFIER)

    @_('IDENTIFIER "(" IDENTIFIER ")"')
    def identifier(self, p):
        return self.memory.getArray(p.IDENTIFIER0, self.memory.getVariable(p.IDENTIFIER1))

    @_('IDENTIFIER "(" NUMBER ")"')
    def identifier(self, p):
        return self.memory.getArray(p.IDENTIFIER, self.memory.getConstant(int(p.NUMBER)))

    def error(self, token):
        raise AssertionError(f"Line {token.lineno}: Syntax error. Token '{token.value}'")
