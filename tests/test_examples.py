import unittest

from teetering.main import run_program


class TestExamples(unittest.TestCase):
    def test_factorial(self):
        program = """
        :fn fac_again
        dup
        1 - factorial_ *
        .
        
        :fn factorial_
        dup 
        1 =
        1 \\fac_again if
        .
        
        :fn factorial
        factorial_ * 
        .
        
        6
        factorial 
        """
        stack, outputs = run_program(program)
        self.assertEqual(1, stack.size())
        self.assertEqual(0, len(outputs.errors))
        self.assertEqual(720, stack.pop())


if __name__ == '__main__':
    unittest.main()
