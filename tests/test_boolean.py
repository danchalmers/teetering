import unittest

from teetering.main import run_program


class BooleanTestCase(unittest.TestCase):
    def test_and_true(self):
        program = """
        1 1 &
        2 2 =
        2 2 =
        &
        """
        stack, outputs = run_program(program)
        self.assertEqual(0, len(outputs.errors))
        self.assertEqual(True, stack.pop())
        self.assertEqual(True, stack.pop())

    def test_and_false(self):
        program = """
        0 -1 &
        0 1 &
        2 2 =
        1 2 =
        &
        """
        stack, outputs = run_program(program)
        self.assertEqual(0, len(outputs.errors))
        self.assertEqual(False, stack.pop())
        self.assertEqual(False, stack.pop())
        self.assertEqual(False, stack.pop())

    def test_or_true(self):
        program = """
        1 1 |
        2 2 =
        1 2 =
        |
        3 4 =
        5 5 =
        |        
        """
        stack, outputs = run_program(program)
        self.assertEqual(0, len(outputs.errors))
        self.assertEqual(True, stack.pop())
        self.assertEqual(True, stack.pop())
        self.assertEqual(True, stack.pop())

    def test_or_false(self):
        program = """
        0 0 |

        """
        stack, outputs = run_program(program)
        self.assertEqual(0, len(outputs.errors))
        self.assertEqual(False, stack.pop())

if __name__ == '__main__':
    unittest.main()
