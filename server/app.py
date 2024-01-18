#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Home(Resource):
    def get(self):
        response_dict = {
            "message": "Welcome to Plantsy."
        }
        response = make_response(response_dict, 200)
        return response
api.add_resource(Home, '/')

class Plants(Resource):
    def get(self):
        response_dict_list = [n.to_dict() for n in Plant.query.all()]
        response = make_response(response_dict_list, 200)
        return response

    def post(self):
        data = request.get_json()

        if "name" not in data or "image" not in data or "price" not in data:
            response_dict = {"error": "Missing required fields"}
            response = make_response(response_dict, 400)
            return response

        new_plant = Plant(
            name=data["name"],
            image=data["image"],
            price=data["price"]
        )

        db.session.add(new_plant)
        db.session.commit()

        response_dict = {"message": "Plant created successfully"}
        response = make_response(response_dict, 201)
        return response
api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.get(id)
        if plant:
            response_dict = plant.to_dict()
            response = make_response(response_dict, 200)
        else:
            response_dict = {"error": "Plant not found"}
            response = make_response(response_dict, 404)
        return response

    def put(self, id):
        plant = Plant.query.get(id)
        if plant:
            data = request.get_json()
            plant.name = data.get('name', plant.name)
            plant.image = data.get('image', plant.image)
            plant.price = data.get('price', plant.price)
            db.session.commit()
            response_dict = plant.to_dict()
            response = make_response(response_dict, 200)
        else:
            response_dict = {"error": "Plant not found"}
            response = make_response(response_dict, 404)
        return response

    def delete(self, id):
        plant = Plant.query.get(id)
        if plant:
            db.session.delete(plant)
            db.session.commit()
            response_dict = {"message": "Plant deleted successfully"}
            response = make_response(response_dict, 200)
        else:
            response_dict = {"error": "Plant not found"}
            response = make_response(response_dict, 404)
        return response

api.add_resource(PlantByID, '/plants/<int:id>')      


if __name__ == '__main__':
    app.run(port=5555, debug=True)
