import os

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# configuration
DEBUG = True

postgres_name = os.environ.get('POSTGRES_NAME')
postgres_password = os.environ.get('POSTGRES_PASSWORD')
postgres_user = os.environ.get('POSTGRES_USER')


# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{postgres_user}:{postgres_password}@db/{postgres_name}'

CORS(app)

db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    distance = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __init__(self, name, amount, distance, date):
        self.name = name
        self.amount = amount
        self.distance = distance
        self.date = date

    def as_dict(self):
        return {"id": self.id, "name": self.name, "amount": self.amount, "distance": self.distance,
                "date": self.date}


db.create_all()


@app.route('/', methods=['GET'])
def get_all():
    # page = int(request.args.get('page', 1))
    # per_page = int(request.args.get('per_page', 5))
    # sort_key = request.args.get('sort_key', 'name')
    # filter_column = request.args.get('filter_column')
    # filter_condition = request.args.get('filter_condition')
    # filter_value = request.args.get('filter_value')

    query = [i.as_dict() for i in Item.query.all()]
    return jsonify(query)


@app.route('/add/', methods=['POST'])
def add_item():
    data = request.get_json()
    name = data['name']
    amount = data['amount']
    distance = data['distance']
    date = data['date']

    db.session.add(Item(name, amount, distance, date))
    db.session.commit()
    return jsonify({'status': 'success'})


@app.route('/remove/<item_id>', methods=['DELETE'])
def remove_item(item_id):
    item = Item.query.get(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'status': 'success'})
