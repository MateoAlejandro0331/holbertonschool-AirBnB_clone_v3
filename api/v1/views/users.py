#!/usr/bin/python3
"""new view for Users"""
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify, abort, request


@app_views.route("/users", strict_slashes=False, methods=['GET'])
def get_all_users():
    """get users"""
    users = storage.all(User)
    mylist = []
    for instance in users.values():
        mylist.append(instance.to_dict())
    return jsonify(mylist)


@app_views.route("/users/<user_id>", strict_slashes=False, methods=['GET'])
def get_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", strict_slashes=False, methods=['DELETE'])
def delete_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return {}, 200


@app_views.route("/users", strict_slashes=False, methods=['POST'])
def post_user():
    if not request.get_json():
        abort(400, "Not a JSON")
    if "email" not in request.get_json():
        abort(400, "Missing email")
    if "password" not in request.get_json():
        abort(400, "Missing password")
    user = User(**request.get_json())
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>", strict_slashes=False, methods=['PUT'])
def put_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        abort(404)
    for key, value in request.get_json().items():
        if key != "id" or key != "created_at" or key != "updated_at":
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
