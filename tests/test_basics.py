import unittest

from teetering.main import run_program


class TestBasics(unittest.TestCase):
    def test_hello_world(self):
        program = """
        "Bonjour le monde!" output
        "Hello, world!" output
        "Hola Mundo!" output
        """
        stack, outputs = run_program(program)
        self.assertEqual(0, stack.size())
        self.assertEqual(0, len(outputs.errors))
        self.assertIn("Hello, world!", outputs.outputs)

    def test_hello_world_fn(self):
        program = """
        :fn hello
        "Hello, world!" output
        .
        
        hello
        """
        stack, outputs = run_program(program)
        self.assertEqual(0, stack.size())
        self.assertEqual(0, len(outputs.errors))
        self.assertIn("Hello, world!", outputs.outputs)

    def test_main_return_stack(self):
        program = """
        1 2 +
        """
        stack, outputs = run_program(program)
        self.assertEqual(1, stack.size())
        self.assertEqual(0, len(outputs.errors))
        self.assertEqual(3, stack.pop())

    def test_function_return_stack(self):
        program = """
        :fn add1
        1 +
        .
        
        2 add1 
        """
        stack, outputs = run_program(program)
        self.assertEqual(1, stack.size())
        self.assertEqual(0, len(outputs.errors))
        self.assertEqual(3, stack.pop())

    def test_function_called_twice(self):
        program = """
        :fn add1
        1 +
        .

        0 add1 add1
        """
        stack, outputs = run_program(program)
        self.assertEqual(1, stack.size())
        self.assertEqual(0, len(outputs.errors))
        self.assertEqual(2, stack.pop())

    def test_dup_output_and_stack(self):
        program = """
        1 2 +
        dup
        output
        """
        stack, outputs = run_program(program)
        self.assertEqual(1, stack.size())
        self.assertEqual(0, len(outputs.errors))
        self.assertIn(3, outputs.outputs)
        self.assertEqual(3, stack.pop())


if __name__ == '__main__':
    unittest.main()
