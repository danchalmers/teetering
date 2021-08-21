import unittest

from teetering.main import run_program


class TestErrorHandling(unittest.TestCase):
    def test_bad_fn_definition_no_ending(self):
        program = """
        :fn sub1
        1 -
        .
        :fn add1
        1 +
        """
        stack, outputs = run_program(program)
        self.assertTrue(len(outputs.errors) > 0)

    def test_not_enough_arguments_in_main(self):
        program = """
        1 +
        """
        stack, outputs = run_program(program)
        self.assertTrue(len(outputs.errors) > 0)

    def test_not_enough_arguments_in_fn(self):
        program = """
        :fn sub1
        1 -
        .
        :fn add1
        1 +
        .
        add1
        """
        stack, outputs = run_program(program)
        self.assertTrue(len(outputs.errors) > 0)

if __name__ == '__main__':
    unittest.main()
