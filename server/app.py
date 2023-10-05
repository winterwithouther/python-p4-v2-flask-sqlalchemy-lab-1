# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
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

# Add views here
@app.route("/earthquakes/<int:id>")
def find_by_id(id):
    earthquake = Earthquake.query.filter(Earthquake.id == id).first()

    if earthquake:
        # Will return Earthquake JSON format
        status = 200
        return make_response(earthquake.to_dict(), status)
    else:
        # return message
        status = 404
        body = {
            "message" : f"Earthquake {id} not found."
        }
        return make_response(body, status)
    
@app.route("/earthquakes/magnitude/<float:magnitude>")
def min_magnitude(magnitude):
    status = 200
    earthquakes = []

    for earthquake in Earthquake.query.filter(Earthquake.magnitude >= magnitude).all():
        earthquakes.append(earthquake.to_dict())

    body = {
        "count" : len(earthquakes),
        "quakes" : earthquakes
    }

    return make_response(body, status)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
