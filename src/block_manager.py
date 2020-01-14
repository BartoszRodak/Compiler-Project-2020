from abstract_syntax_tree import ProgramAST
from memory_manager import MemoryManager
from enum import Enum


class TerminatorType(Enum):
    HALT = 1


class Terminator:
    _type = None

    def __init__(self, _type: TerminatorType = TerminatorType.HALT):
        self._type = _type


class Basicblock:
    variables = {}
    commands: list
    terminator: Terminator

    def __init__(self):
        pass

    def print(self, line: int):
        result = ""
        shift = 0
        for command in self.commands:
            fragment: str = command.print(line+shift)
            shift += len(fragment.splitlines())
            result += fragment
        result+="HALT\n" #TODO

        return result


class BlockManager():
    blocks = []
    tree: ProgramAST

    def __init__(self, tree: ProgramAST):
        # working = {tree.commands}
        # while working:
        #     current = working.pop(0)
        #     block = Basicblock()

        #     comm =
        # self.blocks.
        block = Basicblock()
        block.commands = tree.commands
        block.terminator = Terminator()
        self.blocks.append(block)
