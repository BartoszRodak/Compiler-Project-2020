from block_manager import Basicblock, Terminator
from memory_manager import MemoryManager
from block_manager import BlockManager


class Printer():
    blocks: list
    memory: MemoryManager

    def __init__(self, block: BlockManager, memory: MemoryManager):
        self.memory = memory
        self.blocks = block.blocks

    def print(self) -> str:
        result: str = self.memory.allocate()
        position = len(result.splitlines())
        for block in self.blocks:
            segment = block.print(position)
            result += segment
            position += len(segment.splitlines())
        return result