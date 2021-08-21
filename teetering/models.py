from typing import List

from teetering.standard_library import STANDARD_LIBRARY

CodeStr = str
LineNum = int
Name = str


class Stack:
    def __init__(self):
        self.items = []

    def size(self):
        return len(self.items)

    def push(self, value):
        self.items.append(value)

    def pop(self):
        if not self.items:
            return None
        value = self.items[-1]
        self.items = self.items[:-1]
        return value

    def dup(self):
        self.push(self.items[-1])


class Definitions:
    def __init__(self):
        self.functions = STANDARD_LIBRARY

    def add_function(self, fn_name: Name, fn_lines: List[CodeStr]):
        self.functions[fn_name] = fn_lines

    def get_function(self, fn_name: Name) -> List[CodeStr]:
        return self.functions[fn_name]

    def is_a_function(self, fn_name: Name) -> bool:
        return fn_name in self.functions


class Outputs:
    def __init__(self):
        self.outputs = []
        self.errors = []

    def output(self, line: str):
        self.outputs.append(line)
        print(line)

    def error(self, info: str):
        self.errors.append(info)
        print(info)
