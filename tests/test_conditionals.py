import unittest

from teetering.main import run_program


class ConditionalsTestCase(unittest.TestCase):
    def test_if_true_branch(self):
        program = """
        :fn true
        "are equal"
        .
        :fn false
        "not equal"
        .
        1 1 =
        \\true \\false if
        """
        stack, outputs = run_program(program)
        self.assertEqual(1, stack.size())
        self.assertEqual(0, len(outputs.errors))
        self.assertEqual("are equal", stack.pop())

    def test_if_false_branch(self):
        program = """
        :fn true
        "are equal"
        .
        :fn false
        "not equal"
        .
        1 2 =
        \\true \\false if
        """
        stack, outputs = run_program(program)
        self.assertEqual(1, stack.size())
        self.assertEqual(0, len(outputs.errors))
        self.assertEqual("not equal", stack.pop())

    def test_while(self):
        program = """
        :fn loopy
        1 +
        .

        :fn end_while
        dup
        10 <
        .

        1  
        \loopy \end_while while
        """
        stack, outputs = run_program(program)
        self.assertEqual(1, stack.size())
        self.assertEqual(0, len(outputs.errors))
        self.assertEqual(10, stack.pop())

    def test_while_never(self):
        program = """
        :fn loopy
        1 +
        .

        :fn end_while
        dup
        1 <
        .

        1  
        \loopy \end_while while
        """
        stack, outputs = run_program(program)
        self.assertEqual(1, stack.size())
        self.assertEqual(0, len(outputs.errors))
        self.assertEqual(1, stack.pop())


if __name__ == '__main__':
    unittest.main()
