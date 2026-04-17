from calculator import Calculator


def get_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")


def get_operation():
    operations = {
        "1": ("Add", Calculator.add),
        "2": ("Subtract", Calculator.subtract),
        "3": ("Multiply", Calculator.multiply),
        "4": ("Divide", Calculator.divide),
        "5": ("Power", Calculator.power),
        "6": ("Quit", None),
    }

    print("\nSimple Python Calculator")
    for key, (name, _) in operations.items():
        print(f"{key}. {name}")

    while True:
        choice = input("Choose an operation: ").strip()
        if choice in operations:
            return operations[choice]
        print("Please choose a number from the menu.")


def main():
    while True:
        operation_name, operation = get_operation()
        if operation is None:
            print("Goodbye!")
            break

        a = get_number("Enter the first number: ")
        b = get_number("Enter the second number: ")

        try:
            result = operation(a, b)
        except ZeroDivisionError as exc:
            print("Error:", exc)
        else:
            print(f"Result: {result}")


if __name__ == "__main__":
    main()
