from enum import Enum
from typing import List, Optional
from memory_manager import Value
from abc import ABC, abstractmethod


class IOType(Enum):
    READ = 1,
    WRITE = 2


class TreeNode(ABC):
    @staticmethod
    def printBlock(commands: list, position: int):
        result = ""
        offset = 0
        for comm in commands:
            result += comm.print(position+offset)
            offset = len(result.splitlines())
        return result

class Action(TreeNode):
    @abstractmethod
    def print(self, pos: int):
        pass


class IOAction(Action):
    _type: IOType
    parameter: Value

    def __init__(self, _type: IOType, parameter: Value):
        self._type = _type
        self.parameter = parameter

    def print(self, pos: int):
        if self._type == IOType.READ:
            return "GET\n" + self.parameter.store()
        else:
            return self.parameter.getValue(pos) + "PUT\n"


class AssignAction(Action):
    dest: Value
    src = None

    def __init__(self, dest: Value, src):
        self.dest = dest
        self.src = src

    def print(self, pos):
        return self.src.getValue(pos) + self.dest.store()


class ProgramAST:
    commands: List[TreeNode]
    # variables = None

    def __init__(self, commands: list):
        self.commands = commands
        # self.variables = variables #TODO CLEAR

# class Parameter:
#     pass


class BoolOperator(Enum):
    EQ = 1,
    NEQ = 2,
    LE = 3,
    GE = 4,
    LEQ = 5,
    GEQ = 6


class BoolExpression:
    _type: BoolOperator
    paramA: Value
    paramB: Value

    def __init__(self, _type: BoolOperator, paramA: Value, paramB: Value):
        self._type = _type
        self.paramA = paramA
        self.paramB = paramB

    def getValue(self, position: int):
        result = self.paramB.getValue(position) + "STORE 3\n"
        shift = len(result.splitlines())
        result += self.paramA.getValue(position+shift)
        result += "SUB 3\n"
        shift = len(result.splitlines())

        pos = 10  # TODO normalize basic values, move from userspace
        zero = 11
        neg = 12

        if len(self._type.name) == 3:
            bool1pos = pos
            bool2pos = zero
        else:
            bool1pos = zero
            bool2pos = pos

        if self._type == BoolOperator.EQ or self._type == BoolOperator.NEQ:
            jump = "JZERO"
        elif self._type == BoolOperator.GE or self._type == BoolOperator.LEQ:
            jump = "JPOS"
        else:
            jump = "JNEG"

        result += f"""{jump} {position+shift+2}
JUMP {position+shift+4}
LOAD {bool1pos}
JUMP {position+shift+5}
LOAD {bool2pos}
"""
        return result


class CalculationType(Enum):
    PLUS = 1,
    MINUS = 2,
    TIMES = 3,
    DIV = 4,
    MOD = 5


class Block(TreeNode):
    pass


class IfBlock(Block):
    condition: BoolExpression
    thenBlock: List[TreeNode]
    elseBlock: List[TreeNode]

    def __init__(self, condition: BoolExpression, thenBlock: List[TreeNode], elseBlock: Optional[List[TreeNode]] = None):
        self.condition = condition
        self.thenBlock = thenBlock
        self.elseBlock = elseBlock

    def print(self, position: int):
        result = self.condition.getValue(position)
        shift = len(result.splitlines())
        thenCode = TreeNode.printBlock(self.thenBlock, position+shift+2)
        thenLen = len(thenCode.splitlines())
        elseCode = ""
        elseLen = 0
        jumpShift = 0
        if self.elseBlock:
            elseCode = TreeNode.printBlock(self.elseBlock, position+shift+3+thenLen)
            elseLen = len(elseCode.splitlines())
            jumpShift = 1
        result += f"""JZERO {position+shift+2}
JUMP {position+shift+2+thenLen+jumpShift}
{thenCode}"""
        if self.elseBlock:
            result+=f"""JUMP {position+shift+2+thenLen+jumpShift+elseLen}
{elseCode}"""
        return result


class LoopBlock(Block):
    commands: List[TreeNode]


class WhileLoopBlock(LoopBlock):
    condition: BoolExpression
    doFirst: bool

    def __init__(self, commands: List[TreeNode], condition: BoolExpression, doFirst: bool = False):
        self.condition = condition
        self.commands = commands
        self.doFirst = doFirst

    def print(self, position: int):
        if self.doFirst:
            thenCode = TreeNode.printBlock(self.commands, position)
            thenLen = len(thenCode.splitlines())
            result = thenCode
            result += self.condition.getValue(position+thenLen)
            result += f"""JZERO {position}
"""
        else:
            result = self.condition.getValue(position)
            thenCode = TreeNode.printBlock(self.commands, position+len(result.splitlines())+2)
            thenLen = len(thenCode.splitlines())

            result += f"""JZERO {position+len(result.splitlines())+2}
JUMP {position+len(result.splitlines())+3+thenLen}
"""
            result += thenCode
            result +=f"""JUMP {position} 
"""
        return result




class ForLoopBlock(LoopBlock):
    identifier: Value
    # lowerBound: Value
    # upperBound: Value
    # isDescending: bool

    # def __init__(self, commands: List[TreeNode], identifier: Value, lowerBound: Value, upperBound: Value, reverseDirection: bool = False):
    def __init__(self, commands: List[TreeNode], iterator: Value):
        self.commands = commands
        self.identifier = iterator
        # self.lowerBound = lowerBound
        # self.upperBound = upperBound
        # self.isDescending = reverseDirection

    def print(self, position: int):
        #prep //prepLen lines
        prep = self.identifier.range[0].getValue(position) + f"""STORE {self.identifier.getPosition()}
"""
        # prep = self.identifier.range[0].getValue() + self.identifier.store() #TODO TEST it
    
        prep += self.identifier.range[1].getValue(position+len(prep.splitlines())) + f"""STORE {self.identifier.getPosition() + 1}
"""
        prepLen = len(prep.splitlines())
        #validate // 3 lines

        #execute
        code = TreeNode.printBlock(self.commands, position + prepLen + 3)
        codeLen = len(code.splitlines())

        #iterate and loop //4 lines
        iterate = f"""LOAD {self.identifier.getPosition()}
"""
        if self.identifier.range[2]:
            iterate += "DEC\n"
        else:
            iterate += "INC\n"
        iterate += self.identifier.store()
        iterate += f"""JUMP {position+prepLen}
"""
        #validate gen
        validate = f"""LOAD {self.identifier.getPosition() + 1}
SUB {self.identifier.getPosition()}
"""

        if self.identifier.range[2]:
            validate += f"""JPOS {position+prepLen+3+codeLen+4}
"""
        else:
            validate += f"""JNEG {position+prepLen+3+codeLen+4}
"""

        return prep + validate + code + iterate



class Calculation:
    _type: CalculationType
    paramA: Value
    paramB: Value

    def __init__(self, _type: CalculationType, paramA: Value, paramB: Value):
        self._type = _type
        self.paramA = paramA
        self.paramB = paramB

    def getValue(self, position: int):
        # result = ""
        # posA = self.paramA.getPosition()
        # posB = self.paramB.getPosition() #FASTER iden(iden) problem
        posA = 7
        posB = 8
        result = f"""{self.paramA.getValue(position)}STORE {posA}
"""
        result+= f"""{self.paramB.getValue(position+len(result.splitlines()))}STORE {posB}
"""
        position += len(result.splitlines())
        wA = 1
        wB = 2
        res = 3
        tmp = 4
        shift = 5
        absB = 6
        pos = 10  # TODO normalize basic values, move from userspace
        zero = 11
        neg = 12
        if self._type == CalculationType.PLUS:
            result += self.paramA.getValue(position)
            result += f"""ADD {posB}
"""
        elif self._type == CalculationType.MINUS:
            result += self.paramA.getValue(position)
            result += f"""SUB {posB}
"""
        elif self._type == CalculationType.TIMES:
            result += f"""SUB 0
STORE {res}
LOAD {posB}
JZERO {position+31}
STORE {wB}
LOAD {posA}
JPOS {position+9}
SUB 0
SUB {posA}
STORE {wA} #*a2 #+9
JZERO {position+25}
SHIFT {neg}
SHIFT {pos}
SUB {wA}
JZERO {position+18}
LOAD {res}
ADD {wB}
STORE {res}
LOAD {wB} #*sfAB
SHIFT {pos}
STORE {wB}
LOAD {wA}
SHIFT {neg}
STORE {wA}
JUMP {position+10}
LOAD {posA}
JPOS {position+30}
SUB 0
SUB {res}
JUMP {position+31}
LOAD {res}#*pre-fin
"""
        else:
            result += f"""SUB 0
STORE {res}
STORE {shift}
LOAD {posB} #norm B
JZERO {position+77}
JPOS {position+8}
SUB 0
SUB {posB}
STORE {wB} #*
STORE {absB}
LOAD {posA} #norm A
JZERO {position+77}
JPOS {position+15}
SUB 0
SUB {posA}
STORE {wA}
JZERO {position+24} #*log
SHIFT {neg}
STORE {tmp}
LOAD {shift}
INC
STORE {shift}
LOAD {tmp}
JUMP {position+16}
LOAD {wB}#*shB
SHIFT {shift}
STORE {wB} #tested
LOAD {wA} #*loop
SUB {wB}
JNEG {position+35}
STORE {wA}
LOAD {pos}
SHIFT {shift}
ADD {res}
STORE {res}
LOAD {wB} #*bshift
SHIFT {neg}
STORE {wB}
LOAD {shift}
DEC
STORE {shift}
JNEG {position+46}
LOAD {wA}
JNEG {position+46}
JZERO {position+46}
JUMP {position+27}
LOAD {posA} #probably excessive #*fin 
JPOS {position+51}  
LOAD {zero}
STORE {tmp}
JUMP {position+53}
LOAD {neg} #*else
STORE {tmp}
LOAD {posB} #*cB
JPOS {position+58}
LOAD {tmp}
INC
JUMP {position+59} #STORE {tmp} #replace with jump !!
LOAD {tmp}
JPOS {position+72} #space
JNEG {position+72} #space
SUB 0 #*cont
SUB {res}
STORE {res}
LOAD {wA}
JZERO {position+72}
LOAD {res}
DEC
STORE {res}
LOAD {absB}
SUB {wA}
STORE {wA}
LOAD {posB} #norm B #*secNeg
JPOS {position+77}
SUB 0
SUB {wA}
STORE {wA}
"""
            if self._type == CalculationType.DIV:
                result += f"LOAD {res}"
            elif self._type == CalculationType.MOD:
                result += f"LOAD {wA}"
            result += "\n"
        return result
