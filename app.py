from flask import Flask, render_template, request, jsonify
from calculator import Calculator

app = Flask(__name__)

OPERATIONS = {
    "add": Calculator.add,
    "subtract": Calculator.subtract,
    "multiply": Calculator.multiply,
    "divide": Calculator.divide,
    "power": Calculator.power,
}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()

    try:
        a = float(data["a"])
        b = float(data["b"])
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Invalid numbers provided."}), 400

    operation = data.get("operation")
    if operation not in OPERATIONS:
        return jsonify({"error": f"Unknown operation: {operation}"}), 400

    try:
        result = OPERATIONS[operation](a, b)
    except ZeroDivisionError as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(debug=True)
