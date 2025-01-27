from flask import Blueprint, jsonify, request

api = Blueprint('api', __name__)

# Test Route
@api.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Server is running!"}), 200

# Example POST route
@api.route('/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Echo the received data
    return jsonify({"received": data}), 200
