import math
import re
from typing import List

from teetering.models import CodeStr, Stack, Outputs, LineNum, Definitions


WHITESPACE_RE = re.compile(f'\s+')
TERM_RE = re.compile(r'("[^"]+")|[\S]+')
DEFINITION_START_RE = re.compile(r'^\s*:\w+\s+')
DEFINITION_END_RE = re.compile(r'^\s*\.')
OUTPUT_RE = re.compile(r'\boutput\b')
IF_RE = re.compile(r'\bif\b')
WHILE_RE = re.compile(r'\bwhile\b')
EMPTY_RE = re.compile(r'\bempty\b')
SIZE_RE = re.compile(r'\bsize\b')
LAMBDA_RE = re.compile(r'\\(\w+|[\+\-\/\*\^\<\>\=&\|]|[\>\<\!]\=)')
DUP_RE = re.compile(r'\bdup\b')
SWAP_RE = re.compile(r'\bswap\b')
POP_RE = re.compile(r'\bpop\b')
MATHS_2ARGS_RE = re.compile(r'[\+\-\/\*\^\<\>\=&\|]|[\>\<\!]\=')
NUMBER_RE = re.compile(r'^-?\d+(\.\d*)?')


def consume_definition(
        start_line: LineNum,
        line: CodeStr,
        following_lines: List[CodeStr],
        definitions: Definitions,
        outputs: Outputs
) -> LineNum:
    consumed_lines = 0
    definition_lines = []
    definition_name = WHITESPACE_RE.split(line)[1]
    while consumed_lines < len(following_lines) and not DEFINITION_END_RE.match(following_lines[consumed_lines]):
        definition_lines.append(following_lines[consumed_lines])
        consumed_lines += 1
    if consumed_lines == len(following_lines):
        outputs.error(f'function definition missing an ending at line {start_line}?')
    consumed_lines += 1  # for the ending .
    definitions.add_function(definition_name, definition_lines)
    return consumed_lines


def do_output(stack: Stack, outputs: Outputs):
    output = stack.pop()
    outputs.output(output)


def do_two_arg_maths(term: CodeStr, stack: Stack, outputs: Outputs, error_location: str):
    if stack.size() < 2:
        outputs.error(f'not enough values on the stack in {error_location}')
        return
    y = stack.pop()
    x = stack.pop()
    if term == '+':
        stack.push(x + y)
    elif term == '*':
        stack.push(x * y)
    elif term == '-':
        stack.push(x - y)
    elif term == '/':
        stack.push(x / y)
    elif term == '^':
        stack.push(math.pow(x, y))
    elif term == '=':
        stack.push(x == y)
    elif term == '<':
        stack.push(x < y)
    elif term == '<=':
        stack.push(x <= y)
    elif term == '>':
        stack.push(x > y)
    elif term == '>=':
        stack.push(x >= y)
    elif term == '!=':
        stack.push(x != y)
    elif term == '&':
        stack.push(x and y)
    elif term == '|':
        stack.push(x or y)

def do_if(
        definitions: Definitions,
        stack: Stack,
        outputs: Outputs,
        error_location: str
):
    if stack.size() < 3:
        outputs.error(f'not enough values on the stack for if in {error_location}')
        return
    no_fn = stack.pop()
    yes_fn = stack.pop()
    condition = stack.pop()
    if type(condition) != bool:
        outputs.error(f"conditional didn't find a boolean at {error_location}")
        return
    if condition:
        if not definitions.is_a_function(yes_fn):
            stack.push(yes_fn)
        else:
            run_lines(definitions.get_function(yes_fn), definitions, stack, outputs, yes_fn)
    else:
        if not definitions.is_a_function(no_fn):
            stack.push(no_fn)
        else:
            run_lines(definitions.get_function(no_fn), definitions, stack, outputs, no_fn)


def do_while(definitions, stack, outputs, error_location):
    if stack.size() < 3:
        outputs.error(f'not enough values on the stack for while in {error_location}')
        return
    condition_fn_name = stack.pop()
    if definitions.is_a_function(condition_fn_name):
        condition_fn = definitions.get_function(condition_fn_name)
    else:
        condition_fn = [condition_fn_name]

    loop_fn_name = stack.pop()
    if definitions.is_a_function(loop_fn_name):
        loop_fn = definitions.get_function(loop_fn_name)
    else:
        loop_fn = [loop_fn_name]

    run_lines(condition_fn, definitions, stack, outputs, condition_fn)
    condition = stack.pop()
    while condition:
        run_lines(loop_fn, definitions, stack, outputs, loop_fn_name)
        run_lines(condition_fn, definitions, stack, outputs, condition_fn_name)
        condition = stack.pop()


def do_size(stack: Stack):
    stack.push(stack.size())


def run_code_line(
        line: CodeStr,
        definitions: Definitions,
        stack: Stack,
        outputs: Outputs,
        error_location: str
):
    terms = TERM_RE.finditer(line)
    for match in terms:
        term = match.group()
        if definitions.is_a_function(term):
            run_lines(definitions.get_function(term), definitions, stack, outputs, term)
        elif DUP_RE.match(term):
            stack.dup()
        elif POP_RE.match(term):
            stack.pop()
        elif SWAP_RE.match(term):
            stack.swap()
        elif LAMBDA_RE.match(term):
            stack.push(term[1:])
        elif IF_RE.match(term):
            do_if(definitions, stack, outputs, error_location)
        elif WHILE_RE.match(term):
            do_while(definitions, stack, outputs, error_location)
        elif SIZE_RE.match(term):
            do_size(stack)
        elif OUTPUT_RE.match(term):
            do_output(stack, outputs)
        elif NUMBER_RE.match(term):
            stack.push(float(term))
        elif MATHS_2ARGS_RE.match(term):
            do_two_arg_maths(term, stack, outputs, error_location)
        else:
            if term[0] == '"':
                term = term[1:-1]
            stack.push(term)


def run_line(
        line_num: LineNum,
        line: CodeStr,
        following_lines: List[CodeStr],
        definitions: Definitions,
        stack: Stack,
        outputs: Outputs,
        error_location: str
) -> LineNum:
    consumed_lines = 1
    if DEFINITION_START_RE.match(line):
        consumed_lines += consume_definition(line_num, line, following_lines, definitions, outputs)
    else:
        run_code_line(line, definitions, stack, outputs, f'{error_location} line: {line_num}')
    return consumed_lines


def run_lines(
        lines: List[CodeStr],
        definitions: Definitions,
        stack: Stack,
        outputs: Outputs,
        error_location: str
) -> LineNum:
    line_num = 0
    while line_num < len(lines):
        consumed_lines = run_line(line_num, lines[line_num], lines[line_num+1:], definitions, stack, outputs, error_location)
        line_num += consumed_lines
    return line_num


def run_program(code: CodeStr) -> Outputs:
    definitions = Definitions()
    stack = Stack()
    outputs = Outputs()
    lines = [line.strip() for line in code.splitlines() if len(line.strip()) > 0]
    run_lines(lines, definitions, stack, outputs, "main")
    return stack, outputs
