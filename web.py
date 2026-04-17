import ast
import math
import operator

from flask import Flask, jsonify, render_template, request
from calculator import Calculator

app = Flask(__name__)

OPERATION_MAP = {
    "add": Calculator.add,
    "subtract": Calculator.subtract,
    "multiply": Calculator.multiply,
    "divide": Calculator.divide,
    "power": Calculator.power,
}

_SAFE_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}

_SAFE_FUNCS = {
    "sqrt": math.sqrt,
    "log": math.log10,
    "abs": abs,
}

def _eval_node(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _SAFE_OPS:
        return _SAFE_OPS[type(node.op)](_eval_node(node.left), _eval_node(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _SAFE_OPS:
        return _SAFE_OPS[type(node.op)](_eval_node(node.operand))
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in _SAFE_FUNCS:
        args = [_eval_node(a) for a in node.args]
        return _SAFE_FUNCS[node.func.id](*args)
    raise ValueError("Unsupported expression.")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/advanced")
def advanced():
    return render_template("advanced.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json(force=True)
    try:
        a = float(data.get("a", ""))
        b = float(data.get("b", ""))
        operation = data.get("operation")
        if operation not in OPERATION_MAP:
            raise ValueError("Unknown operation")

        result = OPERATION_MAP[operation](a, b)
        return jsonify(result=result)
    except ZeroDivisionError as exc:
        return jsonify(error=str(exc)), 400
    except (TypeError, ValueError):
        return jsonify(error="Please enter two valid numbers and choose an operation."), 400

@app.route("/evaluate", methods=["POST"])
def evaluate():
    data = request.get_json(force=True)
    expression = data.get("expression", "").strip()
    if not expression:
        return jsonify(error="No expression provided."), 400
    try:
        tree = ast.parse(expression, mode="eval")
        result = _eval_node(tree.body)
        return jsonify(result=result)
    except ZeroDivisionError:
        return jsonify(error="Cannot divide by zero."), 400
    except (ValueError, TypeError) as exc:
        return jsonify(error=str(exc) or "Invalid expression."), 400
    except Exception:
        return jsonify(error="Invalid expression."), 400

if __name__ == "__main__":
    app.run(debug=True)
