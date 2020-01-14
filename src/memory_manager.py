from enum import Enum
from typing import Optional, List


class ValueType(Enum):
    CONSTANT = 1,
    VARIABLE = 2,
    ARRAY = 3,
    ARRAY_ACCESS = 4,
    ITERATOR = 5


class Value:
    initialized = False
    read = False
    value = 0
    _type: ValueType
    index: 'Value'
    location: int
    parent: 'Value'

    def __init__(self, _type: ValueType, value=None, index: Optional['Value'] = None, parent: 'Value' = None):
        self._type = _type
        self.value = value
        self.index = index
        self.parent = parent

    def getValue(self, pos: int):
        if self._type != ValueType.ARRAY_ACCESS:
            return f"""LOAD {self.location}
"""
        else:
            return f"""LOAD {self.parent.getPosition()}
ADD {self.index.getPosition()} 
STORE 1
LOADI 1
"""
#             return self.parent.getValue()
#             + f"""ADD {index.getPosition()}
# STORE 1
# LOADI 1
# """

    def store(self):
        if self._type != ValueType.ARRAY_ACCESS:
            return f"""STORE {self.location}
"""
        else:
            return f"""STORE 2
LOAD {self.parent.getPosition()}
ADD {self.index.getPosition()} 
STORE 1
LOAD 2
STOREI 1
"""
#             return "STORE 2\n" + self.parent.getValue() + f"""ADD {index.getPosition()}
# STORE 1
# LOAD 2
# STOREI
# """

    def getPosition(self):
        if self._type != ValueType.ARRAY_ACCESS:
            return self.location
        else:
            raise NotImplementedError()


class MemoryManager:
    variables = {}
    arrays = {}
    constants = {}
    iterators = []
    freeIndex: int

    def __init__(self, offset=10):
        self.freeIndex = offset
        self.constants[-1] = Value(ValueType.CONSTANT, value=-1)
        self.constants[0] = Value(ValueType.CONSTANT, value=0)
        self.constants[1] = Value(ValueType.CONSTANT, value=1)

    def declareVariable(self, name: str):
        # if name in self.undeclared:
        # self.constants[name] = self.undeclared[name]
        # del self.undeclared[name]
        # else:
        self.variables[name] = Value(ValueType.VARIABLE)

    def declareArray(self, name: str, firstPos: Value, lastPos: Value):
        # if firstPos.value > lastPos.value:
        #     throw ValueError()
        self.arrays[name] = Value(
            ValueType.ARRAY, index=(int(firstPos), int(lastPos)))

    def declareIterator(self, name:str): #TODO Iterator
        self.declareVariable(name)
    
    def getConstant(self, x: int) -> Value:
        x = int(x)
        if x in self.constants:
            return self.constants[x]
        else:
            self.constants[x] = Value(ValueType.VARIABLE, value=x)
            return self.constants[x]

    # def declareIterator(self, name:str):
        # self.iterators.append(self.undeclared[name])
        # del self.undeclared[name]

    def getVariable(self, name: str):
        # if name in self.variables:
        return self.variables[name]
        # elif name in self.undeclared:
        # return self.undeclared[name]
        # else:
        # self.undeclared[name] = Value(ValueType.VARIABLE)
        # return self.undeclared[x]

    def getArray(self, name: str, index: Value):
        return Value(ValueType.ARRAY_ACCESS, index=index, parent=self.arrays[name])

    def generateConstant(self, var: int, regOne: int) -> str:
        result = f"""LOAD {regOne}
"""
        for bit in bin(abs(var))[3:]:
            result += f"""SHIFT {regOne}
"""
            if bit == "1":
                result += "INC\n"

        if var < 0:
            result += """STORE 1
SUB 0
SUB 1
"""
        return result

    def allocate(self) -> str:
        # constants
        result = f"""SUB 0
INC
STORE {self.freeIndex}
DEC
STORE {self.freeIndex+1}
DEC
STORE {self.freeIndex+2}
"""
        regOne = self.freeIndex
        self.constants[1].location = self.freeIndex
        self.constants[0].location = self.freeIndex + 1
        self.constants[-1].location = self.freeIndex + 2
        self.freeIndex += 3
        for var, value in self.constants.items():
            if var <= 1 and var >= -1:
                continue
#             result += f"""LOAD {regOne}
# """
#             for bit in bin(abs(var))[3:]:
#                 result += f"""SHIFT {regOne}
# """
#                 if bit == "1":
#                     result += "INC\n"

#             if var < 0:
#                 result += """STORE 1
# SUB 0
# SUB 1
# """
            result += self.generateConstant(var, regOne)

            value.location = self.freeIndex
            result += f"""STORE {self.freeIndex}
"""
            self.freeIndex += 1
        # vars
        for value in self.variables.values():
            value.location = self.freeIndex
            self.freeIndex += 1

        # arrays
        for value in self.arrays.values():
            size = value.index[1] - value.index[0] + 1
            imaginaryZero = self.freeIndex + 1 - value.index[0]
            value.location = self.freeIndex
            result += self.generateConstant(imaginaryZero, regOne)
            result += f"STORE {self.freeIndex}"
            result += "\n"
            self.freeIndex += 1
        return result

# TODO Better error messages
