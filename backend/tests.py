import unittest
from code123 import add, subtract, multiply, divide, calculator


class TestCalculator(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(3, 5), 8)

    def test_subtract(self):
        self.assertEqual(subtract(5, 3), 2)

    def test_multiply(self):
        self.assertEqual(multiply(3, 5), 15)

    def test_divide(self):
        self.assertEqual(divide(10, 2), 5)

    def test_calculator(self):
        self.assertEqual(calculator(), None)

if __name__ == "__main__":
    unittest.main()
