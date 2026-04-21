import ast

from flask import Flask, render_template, request, jsonify
from calculator import Calculator

app = Flask(__name__)

BINARY_OPERATIONS = {
    "add": Calculator.add,
    "subtract": Calculator.subtract,
    "multiply": Calculator.multiply,
    "divide": Calculator.divide,
    "power": Calculator.power,
    "modulo": Calculator.modulo,
}

UNARY_OPERATIONS = {
    "sqrt": Calculator.sqrt,
    "log10": Calculator.log10,
}

_AST_BINARY_OPS = {
    ast.Add: Calculator.add,
    ast.Sub: Calculator.subtract,
    ast.Mult: Calculator.multiply,
    ast.Div: Calculator.divide,
    ast.Pow: Calculator.power,
    ast.Mod: Calculator.modulo,
}

_AST_FUNCTIONS = {
    "sqrt": Calculator.sqrt,
    "log": Calculator.log10,
}


def _eval_node(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return float(node.value)
        raise ValueError("Invalid literal.")
    if isinstance(node, ast.BinOp):
        op_func = _AST_BINARY_OPS.get(type(node.op))
        if op_func is None:
            raise ValueError("Unsupported operator.")
        return op_func(_eval_node(node.left), _eval_node(node.right))
    if isinstance(node, ast.UnaryOp):
        if isinstance(node.op, ast.USub):
            return -_eval_node(node.operand)
        if isinstance(node.op, ast.UAdd):
            return _eval_node(node.operand)
        raise ValueError("Unsupported unary operator.")
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Invalid function call.")
        fn = _AST_FUNCTIONS.get(node.func.id)
        if fn is None:
            raise ValueError(f"Unknown function: {node.func.id}")
        return fn(*[_eval_node(a) for a in node.args])
    raise ValueError(f"Unsupported expression: {type(node).__name__}")


def safe_evaluate(expression):
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError:
        raise ValueError("Invalid expression syntax.")
    return _eval_node(tree.body)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/advanced")
def advanced():
    return render_template("advanced.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()

    try:
        a = float(data["a"])
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Invalid numbers provided."}), 400

    operation = data.get("operation")

    if operation in UNARY_OPERATIONS:
        try:
            result = UNARY_OPERATIONS[operation](a)
        except (ValueError, ZeroDivisionError) as exc:
            return jsonify({"error": str(exc)}), 400
        return jsonify({"result": result})

    if operation not in BINARY_OPERATIONS:
        return jsonify({"error": f"Unknown operation: {operation}"}), 400

    try:
        b = float(data["b"])
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Invalid numbers provided."}), 400

    try:
        result = BINARY_OPERATIONS[operation](a, b)
    except (ZeroDivisionError, ValueError) as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify({"result": result})


@app.route("/evaluate", methods=["POST"])
def evaluate():
    data = request.get_json()
    expression = data.get("expression", "").strip()
    if not expression:
        return jsonify({"error": "No expression provided."}), 400

    try:
        result = safe_evaluate(expression)
    except (ValueError, ZeroDivisionError) as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(debug=True)
