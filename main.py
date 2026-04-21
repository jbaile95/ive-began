from calculator import Calculator


def get_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")


def get_operation():
    operations = {
        "1":  ("Add",         Calculator.add,      2),
        "2":  ("Subtract",    Calculator.subtract, 2),
        "3":  ("Multiply",    Calculator.multiply, 2),
        "4":  ("Divide",      Calculator.divide,   2),
        "5":  ("Power",       Calculator.power,    2),
        "6":  ("Modulo",      Calculator.modulo,   2),
        "7":  ("Square Root", Calculator.sqrt,     1),
        "8":  ("Log10",       Calculator.log10,    1),
        "9":  ("Quit",        None,                0),
    }

    print("\nSimple Python Calculator")
    for key, (name, _, _args) in operations.items():
        print(f"{key}. {name}")

    while True:
        choice = input("Choose an operation: ").strip()
        if choice in operations:
            return operations[choice]
        print("Please choose a number from the menu.")


def main():
    while True:
        operation_name, operation, arg_count = get_operation()
        if operation is None:
            print("Goodbye!")
            break

        a = get_number("Enter the first number: ")

        try:
            if arg_count == 1:
                result = operation(a)
            else:
                b = get_number("Enter the second number: ")
                result = operation(a, b)
        except (ZeroDivisionError, ValueError) as exc:
            print("Error:", exc)
        else:
            print(f"Result: {result}")


if __name__ == "__main__":
    main()
