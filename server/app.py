# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# View to handle /earthquakes/<int:id>
@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake(id):
    earthquake = Earthquake.query.get(id)
    if earthquake:
        response = {
            'id': earthquake.id,
            'magnitude': earthquake.magnitude,
            'location': earthquake.location,
            'year': earthquake.year
        }
        return jsonify(response), 200
    else:
        error_response = {'message': f'Earthquake {id} not found.'}
        return jsonify(error_response), 404

# View to handle /earthquakes/magnitude/<float:magnitude>
@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    earthquake_list = [
        {
            'id': eq.id,
            'magnitude': eq.magnitude,
            'location': eq.location,
            'year': eq.year
        } for eq in earthquakes
    ]
    response = {
        'count': len(earthquake_list),
        'quakes': earthquake_list
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)
