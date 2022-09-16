#!/usr/bin/python3
"""new view for State"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort, request


@app_views.route("/states", strict_slashes=False, methods=['GET'])
def get_states():
    """get states"""
    states = storage.all(State)
    mylist = []
    for instance in states.values():
        mylist.append(instance.to_dict())
    return jsonify(mylist)


@app_views.route("/states/<state_id>", strict_slashes=False, methods=['GET'])
def get_state(state_id):
    """get state"""
    states = storage.all(State)
    for instance in states.values():
        if instance.id == state_id:
            return jsonify(instance.to_dict())
    abort(404)


@app_views.route(
    "/states/<state_id>", strict_slashes=False, methods=['DELETE'])
def delete_state(state_id):
    """delete an state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200


@app_views.route("/states", strict_slashes=False, methods=['POST'])
def state_post():
    if not request.get_json():
        abort(400, "Not a JSON")
    if 'name' not in request.get_json():
        abort(400, "Missing name")
    state = State(**request.get_json())
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>", strict_slashes=False, methods=['PUT'])
def put_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    for key, value in request.get_json().items():
        if key != "id" or key != "created_at" or key != "updated_at":
            setattr(state, key, value)
    return jsonify(state.to_dict()), 200
