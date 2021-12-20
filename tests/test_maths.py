import unittest

from teetering.main import run_program


class TestMaths(unittest.TestCase):
    def test_basic_addition(self):
        program = """
        1 2 +
        """
        stack, outputs = run_program(program)
        self.assertEqual(1, stack.size())
        self.assertEqual(0, len(outputs.errors))
        self.assertEqual(3, stack.pop())

    def test_basic_subtraction(self):
        program = """
        1 2 -
        """
        stack, outputs = run_program(program)
        self.assertEqual(1, stack.size())
        self.assertEqual(0, len(outputs.errors))
        self.assertEqual(-1, stack.pop())

    def test_basic_multiplication(self):
        program = """
        1 2 *
        """
        stack, outputs = run_program(program)
        self.assertEqual(1, stack.size())
        self.assertEqual(0, len(outputs.errors))
        self.assertEqual(2, stack.pop())

    def test_basic_division(self):
        program = """
        1 2 /
        """
        stack, outputs = run_program(program)
        self.assertEqual(1, stack.size())
        self.assertEqual(0, len(outputs.errors))
        self.assertEqual(0.5, stack.pop())

    def test_basic_int_math(self):
        program = """
        1 2 + 4 * 3 / 5 -
        """
        stack, outputs = run_program(program)
        self.assertEqual(1, stack.size())
        self.assertEqual(0, len(outputs.errors))
        self.assertEqual(-1, stack.pop())

    def test_basic_negation(self):
        program = """
        -1 -2 -
        """
        stack, outputs = run_program(program)
        self.assertEqual(1, stack.size())
        self.assertEqual(0, len(outputs.errors))
        self.assertEqual(1, stack.pop())

    def test_basic_float_math(self):
        program = """
        1 1 3. + 2 * / 0.125 +
        """
        stack, outputs = run_program(program)
        self.assertEqual(1, stack.size())
        self.assertEqual(0, len(outputs.errors))
        self.assertEqual(0.25, stack.pop())

    def test_powers(self):
        program = """
        2 2 ^
        """
        stack, outputs = run_program(program)
        self.assertEqual(1, stack.size())
        self.assertEqual(0, len(outputs.errors))
        self.assertEqual(4, stack.pop())

    def test_gt(self):
        program = """
        2 2 >
        2 3 >
        3 2 >
        """
        stack, outputs = run_program(program)
        self.assertEqual(0, len(outputs.errors))
        self.assertEqual(True, stack.pop())
        self.assertEqual(False, stack.pop())
        self.assertEqual(False, stack.pop())

    def test_gteq(self):
        program = """
        2 2 >=
        2 3 >=
        3 2 >=
        """
        stack, outputs = run_program(program)
        self.assertEqual(0, len(outputs.errors))
        self.assertEqual(True, stack.pop())
        self.assertEqual(False, stack.pop())
        self.assertEqual(True, stack.pop())

    def test_eq(self):
        program = """
        2 2 =
        2 4 =
        2 2 !=
        2 4 !=
        """
        stack, outputs = run_program(program)
        self.assertEqual(0, len(outputs.errors))
        self.assertEqual(True, stack.pop())
        self.assertEqual(False, stack.pop())
        self.assertEqual(False, stack.pop())
        self.assertEqual(True, stack.pop())

    def test_quotient_1_2(self):
        program = """
        1 2 //
        """
        stack, outputs = run_program(program)
        self.assertEqual(1, stack.size())
        self.assertEqual(0, len(outputs.errors))
        self.assertEqual(0, stack.pop())

    def test_quotient_6_3(self):
        program = """
        6 3 //
        """
        stack, outputs = run_program(program)
        self.assertEqual(1, stack.size())
        self.assertEqual(0, len(outputs.errors))
        self.assertEqual(2, stack.pop())

    def test_remainder_1_2(self):
        program = """
        1 2 /%
        """
        stack, outputs = run_program(program)
        self.assertEqual(1, stack.size())
        self.assertEqual(0, len(outputs.errors))
        self.assertEqual(1, stack.pop())

    def test_remainder_6_3(self):
        program = """
        6 3 /%
        """
        stack, outputs = run_program(program)
        self.assertEqual(1, stack.size())
        self.assertEqual(0, len(outputs.errors))
        self.assertEqual(0, stack.pop())


if __name__ == '__main__':
    unittest.main()
