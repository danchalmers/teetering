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
