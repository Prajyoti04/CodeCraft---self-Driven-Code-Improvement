def generate_flask_crud():
    code = """
from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory database (for demonstration purposes)
items = []

# Route to get all items
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items), 200

# Route to create a new item
@app.route('/items', methods=['POST'])
def create_item():
    if not request.json or 'name' not in request.json:
        return jsonify({'error': 'Bad Request', 'message': 'Name is required'}), 400

    new_item = {
        'id': len(items) + 1,
        'name': request.json['name']
    }
    items.append(new_item)
    return jsonify(new_item), 201

# Route to update an item
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = next((item for item in items if item['id'] == item_id), None)
    if item is None:
        return jsonify({'error': 'Not Found', 'message': 'Item not found'}), 404

    if 'name' in request.json:
        item['name'] = request.json['name']
    
    return jsonify(item), 200

# Route to delete an item
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global items
    items = [item for item in items if item['id'] != item_id]
    return jsonify({'message': 'Item deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True)
"""
    return code

# Generate and print the CRUD application code
print(generate_flask_crud())