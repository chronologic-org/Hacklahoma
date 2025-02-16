def add(num1: float, num2: float) -> float:
    """Perform addition operation."""
    return num1 + num2

def subtract(num1: float, num2: float) -> float:
    """Perform subtraction operation."""
    return num1 - num2

def multiply(num1: float, num2: float) -> float:
    """Perform multiplication operation."""
    return num1 * num2

def divide(num1: float, num2: float) -> float:
    """Perform division operation, handling division by zero."""
    if num2 == 0:
        raise ZeroDivisionError("Division by zero is undefined.")
    return num1 / num2

def calculate(num1: float, num2: float, operation: str) -> float:
    """Perform the specified arithmetic operation."""
    operations = {
        '+': add,
        '-': subtract,
        '*': multiply,
        '/': divide
    }
    
    if operation not in operations:
        raise ValueError(f"Invalid operation: '{operation}'. Please use one of: +, -, *, /.")
    
    return operations[operation](num1, num2)

def calculator(input_args=None):
    """Main calculator function that processes input."""
    if input_args is None:
        user_input = input("Enter two numbers and an operation (+, -, *, /), "
                           "e.g., '5 3 +': ")
        parts = user_input.split()
    else:
        parts = input_args

    if len(parts) != 3:
        raise ValueError("Invalid input format. Please use 'num1 num2 operation'.")

    try:
        num1 = float(parts[0])
        num2 = float(parts[1])
    except ValueError:
        print("Invalid input: please enter numerical values.")
        return

    operation = parts[2]
    if operation not in ['+', '-', '*', '/']:
        print(f"Invalid operation: '{operation}'. Please select one of: +, -, *, /.")
        return

    try:
        result = calculate(num1, num2, operation)
    except ZeroDivisionError as e:
        print(str(e))
        return
    except ValueError as e:
        print(f"Invalid input: {str(e)}")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return

    if isinstance(result, float) and result.is_integer():
        print(int(result))
    else:
        print(result)

import unittest

class TestCalculator(unittest.TestCase):
    def test_add(self):
        self.assertEqual(calculate(5, 3, '+'), 8.0)
        self.assertEqual(calculate(-5, 3, '+'), -2.0)

    def test_subtract(self):
        self.assertEqual(calculate(5, 3, '-'), 2.0)
        self.assertEqual(calculate(3, 5, '-'), -2.0)

    def test_multiply(self):
        self.assertEqual(calculate(5, 3, '*'), 15.0)
        self.assertEqual(calculate(-5, 3, '*'), -15.0)

    def test_divide(self):
        self.assertEqual(calculate(6, 3, '/'), 2.0)
        self.assertEqual(calculate(-6, 3, '/'), -2.0)

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            calculate(5, 0, '/')

    def test_invalid_operation(self):
        with self.assertRaises(ValueError):
            calculate(5, 3, '%')

    def test_negative_numbers(self):
        self.assertEqual(calculate(-5, -3, '+'), -2.0)
        self.assertEqual(calculate(-5, 3, '+'), -2.0)
        self.assertEqual(calculate(-5, -3, '*'), 15.0)
        self.assertEqual(calculate(-5, 3, '*'), -15.0)

    def test_zero_inputs(self):
        self.assertEqual(calculate(0, 0, '+'), 0.0)
        self.assertEqual(calculate(0, 0, '-'), 0.0)
        self.assertEqual(calculate(0, 0, '*'), 0.0)
        with self.assertRaises(ZeroDivisionError):
            calculate(1, 0, '/')

    def test_large_numbers(self):
        self.assertEqual(calculate(1e300, 2, '+'), 1e300 + 2)
        self.assertEqual(calculate(1e300, 2, '-'), 1e300 - 2)
        self.assertEqual(calculate(1e300, 2, '*'), 2e300)
        self.assertEqual(calculate(1e300, 2, '/'), 5e299)

if __name__ == "__main__":
    print("Simple Calculator App")
    print("Valid operations: +, -, *, /")
    print("Example usage: '5 3 +'\n")

    # Run calculator with example inputs
    calculator(['5', '3', '+'])
    calculator(['5', '3', '-'])
    calculator(['5', '3', '*'])
    calculator(['6', '3', '/'])
    try:
        calculator(['5', '0', '/'])
    except ZeroDivisionError:
        print("Division by zero error caught.")
    try:
        calculator(['5', '3', '%'])
    except ValueError:
        print("Invalid operation error caught.")

    # Run unit tests
    print("\nRunning unit tests...")
    unittest.main(argv=[''], verbosity=2, exit=False)
