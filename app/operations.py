########################
# Operation Classes    #
########################

from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict
from app.exceptions import ValidationError


class Operation(ABC):

    """Abstract base class for all operations. 
    The abstract decorator is used to declare a method that must be implemented by any subclass.
    Part of Python's Abstract Base Classes (ABC) module, which provides a way to define abstract classes and methods.
    """
    @abstractmethod
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        pass  

    # Regular validate method that can be overridden by specific operations for custom validation logic
    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        pass

    def __str__(self) -> str:
        """
        Return operation name for display.

        Provides a string representation of the operation, typically the class name.
    
        This will show a string rather than the memory address...for example: <__main__.Division object at 0x0000012345>

        Returns:
            str: Name of the operation.
        """
        return self.__class__.__name__


class Addition(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b) # Call the base validation method but it does nothing in this case since addition has no special validation rules
        return a + b


class Subtraction(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b) 
        return a - b


class Multiplication(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        return a * b


class Division(Operation):
    def validate_operands(self, a: Decimal, b: Decimal) -> None:

        super().validate_operands(a, b) # 'super()' calls the parent class method.
        if b == 0:
            raise ValidationError("Division by zero is not allowed")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        return a / b


class Power(Operation):
    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        super().validate_operands(a, b)
        if b < 0:
            raise ValidationError("Negative exponents not supported")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:

        self.validate_operands(a, b)
        return Decimal(pow(float(a), float(b)))


class Root(Operation):
    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        super().validate_operands(a, b)
        if a < 0:
            raise ValidationError("Cannot calculate root of negative number")
        if b == 0:
            raise ValidationError("Zero root is undefined")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        return Decimal(pow(float(a), 1 / float(b)))

"""
Factory pattern implementation for creating operation instances based on user input.
"""
class OperationFactory:
    """
    Factory class for creating operation instances.

    Implements the Factory pattern by providing a method to instantiate
    different operation classes based on a given operation type. This promotes
    scalability and decouples the creation logic from the Calculator class.
    """

    # Dictionary mapping operation identifiers to their corresponding classes
    _operations: Dict[str, type] = {
        'add': Addition,
        'subtract': Subtraction,
        'multiply': Multiplication,
        'divide': Division,
        'power': Power,
        'root': Root
    }

    @classmethod
    def register_operation(cls, name: str, operation_class: type) -> None:
        """
        Register a new operation type.

        Allows dynamic addition of new operations to the factory.

        Args:
            name (str): Operation identifier (e.g., 'modulus').
            operation_class (type): The class implementing the new operation.

        Raises:
            TypeError: If the operation_class does not inherit from Operation.
        """
        if not issubclass(operation_class, Operation):
            raise TypeError("Operation class must inherit from Operation")
        cls._operations[name.lower()] = operation_class

    @classmethod
    def create_operation(cls, operation_type: str) -> Operation:
        """
        Create an operation instance based on the operation type.

        This method retrieves the appropriate operation class from the
        _operations dictionary and instantiates it.

        Args:
            operation_type (str): The type of operation to create (e.g., 'add').

        Returns:
            Operation: An instance of the specified operation class.

        Raises:
            ValueError: If the operation type is unknown.
        """
        operation_class = cls._operations.get(operation_type.lower())
        if not operation_class:
            raise ValueError(f"Unknown operation: {operation_type}")
        return operation_class()
