import unittest

from teetering.main import run_program


class StackOpsTestCase(unittest.TestCase):
    def test_dup(self):
        program = """
        1 2 +
        dup
        """
        stack, outputs = run_program(program)
        self.assertEqual(2, stack.size())
        self.assertEqual(0, len(outputs.errors))
        self.assertEqual(3, stack.pop())

    def test_pop(self):
        program = """
        1
        dup
        pop
        """
        stack, outputs = run_program(program)
        self.assertEqual(1, stack.size())
        self.assertEqual(0, len(outputs.errors))
        self.assertEqual(1, stack.pop())

    def test_swap(self):
        program = """
        1
        2
        swap
        """
        stack, outputs = run_program(program)
        self.assertEqual(2, stack.size())
        self.assertEqual(0, len(outputs.errors))
        self.assertEqual(1, stack.pop())
        self.assertEqual(2, stack.pop())

    def test_size_empty(self):
        program = """
        1
        pop
        size
        """
        stack, outputs = run_program(program)
        self.assertEqual(1, stack.size())
        self.assertEqual(0, len(outputs.errors))
        self.assertEqual(0, stack.pop())

    def test_size_several(self):
        program = """
        1 1 1
        size
        """
        stack, outputs = run_program(program)
        self.assertEqual(4, stack.size())
        self.assertEqual(0, len(outputs.errors))
        self.assertEqual(3, stack.pop())

if __name__ == '__main__':
    unittest.main()
