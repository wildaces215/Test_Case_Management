from flask import Flask,request,jsonify
from models import app, db, TestCase, Requirement

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/reqs/all', methods=['GET'])
def get_requirements():
    requirements = Requirement.query.all()
    requirement_list = []
    for requirement in requirements:
        requirement_data = {
            'id': requirement.id,
            'description': requirement.description
        }
        requirement_list.append(requirement_data)
    return jsonify(requirement_list)

@app.route('/api/reqs/new', methods=['POST'])
def create_requirement():
    data = request.get_json()
    description = data.get('description')

    if not description:
        return jsonify({'error': 'Description is required'}), 400

    requirement = Requirement(description=description)
    db.session.add(requirement)
    db.session.commit()

    return jsonify({'message': 'Requirement created successfully', 'requirement_id': requirement.id}), 201

@app.route('/reqs/<int:requirement_id>', methods=['GET'])
def get_requirement(requirement_id):
    requirement = Requirement.query.get(requirement_id)
    if not requirement:
        return jsonify({'error': 'Requirement not found'}), 404

    requirement_data = {
        'id': requirement.id,
        'description': requirement.description
    }

    return jsonify(requirement_data)

@app.route('/reqs/<int:requirement_id>', methods=['PUT'])
def update_requirement(requirement_id):
    requirement = Requirement.query.get(requirement_id)
    if not requirement:
        return jsonify({'error': 'Requirement not found'}), 404

    data = request.get_json()
    description = data.get('description')

    if description:
        requirement.description = description

    db.session.commit()

    return jsonify({'message': 'Requirement updated successfully'})

@app.route('/reqs/<int:requirement_id>', methods=['DELETE'])
def delete_requirement(requirement_id):
    requirement = Requirement.query.get(requirement_id)
    if not requirement:
        return jsonify({'error': 'Requirement not found'}), 404

    db.session.delete(requirement)
    db.session.commit()

    return jsonify({'message': 'Requirement deleted successfully'})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
