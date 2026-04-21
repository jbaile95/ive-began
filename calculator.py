import math


class Calculator:
    """A simple calculator with basic arithmetic operations."""

    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def subtract(a, b):
        return a - b

    @staticmethod
    def multiply(a, b):
        return a * b

    @staticmethod
    def divide(a, b):
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return a / b

    @staticmethod
    def power(a, b):
        return a ** b

    @staticmethod
    def sqrt(a):
        if a < 0:
            raise ValueError("Cannot take square root of a negative number.")
        return math.sqrt(a)

    @staticmethod
    def log10(a):
        if a <= 0:
            raise ValueError("Logarithm requires a positive number.")
        return math.log10(a)

    @staticmethod
    def modulo(a, b):
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return a % b
