from typing import List

from teetering.standard_library import STANDARD_LIBRARY

CodeStr = str
LineNum = int
Name = str


class Stack:
    def __init__(self, verbose: bool=False):
        self.items = []
        self.verbose = verbose

    def size(self):
        return len(self.items)

    def push(self, value):
        self.items.append(value)
        if self.verbose:
            print(f'pushing {value} giving {self.items}')

    def pop(self):
        if not self.items:
            return None
        value = self.items[-1]
        self.items = self.items[:-1]
        if self.verbose:
            print(f'popping {value} leaving {self.items}')
        return value

    def dup(self):
        self.push(self.items[-1])

    def swap(self):
        x = self.pop()
        y = self.pop()
        self.push(x)
        self.push(y)


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
