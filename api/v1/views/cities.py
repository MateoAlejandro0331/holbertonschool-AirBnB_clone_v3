#!/usr/bin/python3
"""new view for State"""
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from flask import jsonify, abort, request


@app_views.route(
    "/states/<state_id>/cities", strict_slashes=False, methods=['GET'])
def retrive_cities(state_id):
    """retrive cities"""
    state = storage.get(State, state_id)
    if state is not None:
        mylist = []
        cities = storage.all(City)
        for instance in cities.values():
            if instance.state_id == state_id:
                mylist.append(instance.to_dict())
        return jsonify(mylist)
    abort(404)


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=['GET'])
def get_city(city_id):
    """get cities"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=['DELETE'])
def delete_city(city_id):
    """delete cities"""
    city = storage.all(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    "/states/<state_id>/cities", strict_slashes=False, methods=['POST'])
def city_post(state_id):
    """create a city object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    if 'name' not in request.get_json():
        abort(400, "Missing name")
    request.get_json()['state_id'] = state_id
    city = City(**request.get_json())
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=['PUT'])
def put_city(city_id):
    """Update a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    for key, value in request.get_json().items():
        if key != "id" or key != "created_at" or key != "updated_at":
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200