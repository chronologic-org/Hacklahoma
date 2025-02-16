from flask import Flask, request, jsonify

app = Flask(__name__)

# Define the operations
operations = {
    'add': lambda a, b: a + b,
    'subtract': lambda a, b: a - b,
    'multiply': lambda a, b: a * b,
    'divide': lambda a, b: a / b if b != 0 else None
}

@app.route('/calculate', methods=['POST'])
def calculate():
    # Get the request data
    data = request.get_json()
    
    # Check for missing parameters
    required_params = ['number1', 'number2', 'operation']
    if not all(param in data for param in required_params):
        return jsonify({"error": "Missing input parameter(s)."}), 400
    
    number1 = data['number1']
    number2 = data['number2']
    operation = data['operation']
    
    # Validate numeric inputs
    if not isinstance(number1, (int, float)) or not isinstance(number2, (int, float)):
        return jsonify({"error": "Non-numeric input parameter(s)."}), 400
    
    # Validate operation
    if operation not in operations:
        return jsonify({"error": f"Unsupported operation: {operation}."}), 400
    
    # Perform the operation
    if operation == 'divide':
        if number2 == 0:
            return jsonify({"error": "Division by zero is not allowed."}), 400
        result = operations[operation](number1, number2)
    else:
        result = operations[operation](number1, number2)
    
    return jsonify({"result": result}), 200

if __name__ == "__main__":
    app.run(debug=True)
