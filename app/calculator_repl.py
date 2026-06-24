########################
# Calculator REPL       #
########################

from decimal import Decimal
import logging

from app.calculator import Calculator
from app.exceptions import OperationError, ValidationError
from app.history import AutoSaveObserver, LoggingObserver
from app.operations import OperationFactory


def calculator_repl():
    """
    Command-line interface for the calculator.

    Implements a Read-Eval-Print Loop (REPL) that continuously prompts the user
    for commands, processes arithmetic operations, and manages calculation history.
    """
    try:
        # Initialize the Calculator instance
        calc_class = Calculator()

        # Register observers for logging and auto-saving history
        calc_class.add_observer(LoggingObserver())
        calc_class.add_observer(AutoSaveObserver(calc_class))

        print("Calculator started. Type 'help' for commands.")

        while True:
            try:

                user_input = input("Enter an operation type: ").lower().strip()

                # Help input
                if user_input == 'help':
                    print("Available commands:\n- add: Add two numbers\n- subtract: Subtract two numbers\n- multiply: Multiply two numbers\n- divide: Divide two numbers\n- history: Show calculation history\n- quit: Exit the calculator")
                    print("-save: Save calculation history to file\n- load: Load calculation history from file\n- clear: Clear calculation history\n- undo: Undo last calculation\n- redo: Redo last undone calculation")
                    continue
                
                # Quit input
                if user_input == "quit":
                    print("Exiting calculator.")
                    break

                # History Input
                if user_input == "history":
                    if not calc_class.history:
                        print("No calculations in history.")
                    else:
                        print("Calculation History:")
                        for entry in calc_class.history:
                            print(f"  {entry}")
                    continue

                # Clear Input
                if user_input == 'clear':
                    calc_class.clear_history()
                    print("History cleared.")
                    continue
                
                # Undo/Redo Input
                if user_input == 'undo':
                    try:
                        calc_class.undo_last()
                        print("Last calculation undone.")
                    except IndexError:
                        print("No calculations to undo.")
                    continue

                if user_input == 'redo':
                    try:
                        calc_class.redo_last()
                        print("Last undone calculation redone.")
                    except IndexError:
                        print("No calculations to redo.")
                    continue
                
                # SAVE input
                if user_input == 'save':
                    try:
                        calc_class.save_history()
                        print("History saved.")
                    except Exception as e:
                        print(f"Error saving history: {e}")
                    continue

                if user_input == 'load':
                    try:
                        calc_class.load_history()
                        print("History loaded.")
                    except Exception as e:
                        print(f"Error loading history: {e}")
                    continue

                # Operation Input
                valid_commands = ['add', 'subtract', 'multiply', 'divide', 'power', 'root']
                if user_input in valid_commands:
                    try:
                        operand1 = Decimal(input("Enter first number: "))
                        operand2 = Decimal(input("Enter second number: "))

                        operation = OperationFactory.create_operation(user_input)
                        calc_class.set_operation(operation)
                        
                        result = calc_class.perform_operation(operand1, operand2)
            
                        print(f"Result: {result}")

                    except Exception as e:
                        print(f"Invalid input: {e}")
                        continue
                    except (OperationError, ValidationError) as e:
                        print(f"Error: {e}")
                    except Exception as e:
                        print(f"Unexpected error: {e}")
                    continue

                print(f"Unknown command: {user_input}. Type 'help' for a list of commands.")

            except KeyboardInterrupt:
                print("\nExiting calculator.")
                break
            except EOFError:
                # Handle end-of-file (e.g., Ctrl+D) gracefully
                print("\nInput terminated. Exiting...")
                break
            except Exception as e:
                # Handle any other unexpected exceptions
                print(f"Error: {e}")
                continue

    except Exception as e:
        logging.error(f"Unexpected error in REPL: {e}")
        print(f"An unexpected error occurred: {e}")
        raise


            