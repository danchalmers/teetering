import unittest

from teetering.main import run_program


class StandardLibraryTestCase(unittest.TestCase):
    def test_no_op(self):
        program = """
        1
        noop
        2
        """
        stack, outputs = run_program(program)
        self.assertEqual(2, stack.size())
        self.assertEqual(0, len(outputs.errors))
        self.assertEqual([], outputs.outputs)

    def test_no_op_call(self):
        program = """
        noop
        :fn true
        "yes"
        .
        1 2 =
        \\true \\noop if
        """
        stack, outputs = run_program(program)
        self.assertEqual(0, stack.size())
        self.assertEqual(0, len(outputs.errors))

    def test_is_zero_true(self):
        program = """
        0
        is_zero
        """
        stack, outputs = run_program(program)
        self.assertEqual(1, stack.size())
        self.assertEqual(0, len(outputs.errors))
        self.assertEqual([], outputs.outputs)
        self.assertEqual(True, stack.pop())

    def test_is_zero_false(self):
        program = """
        111
        is_zero
        """
        stack, outputs = run_program(program)
        self.assertEqual(1, stack.size())
        self.assertEqual(0, len(outputs.errors))
        self.assertEqual([], outputs.outputs)
        self.assertEqual(False, stack.pop())

    def test_sum_none(self):
        program = """
        sum
        """
        stack, outputs = run_program(program)
        # self.assertEqual(1, stack.size())
        self.assertEqual(0, len(outputs.errors))
        self.assertEqual(0, stack.pop())

    def test_sum_one(self):
        program = """
        10
        sum
        """
        stack, outputs = run_program(program)
        self.assertEqual(1, stack.size())
        self.assertEqual(0, len(outputs.errors))
        self.assertEqual(10, stack.pop())

    def test_sum_several(self):
        program = """
        1 2 3 4 5
        sum
        """
        stack, outputs = run_program(program)
        self.assertEqual(1, stack.size())
        self.assertEqual(0, len(outputs.errors))
        self.assertEqual(15, stack.pop())


if __name__ == '__main__':
    unittest.main()
