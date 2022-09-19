#!/usr/bin/python3
"""new view for Amenities"""
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import jsonify, abort, request


@app_views.route("/amenities", strict_slashes=False, methods=['GET'])
def get_amenities():
    """Get amenities"""
    amenities = storage.all(Amenity)
    mylist = []
    for instance in amenities.values():
        mylist.append(instance.to_dict())
    return jsonify(mylist)


@app_views.route(
    "/amenities/<amenity_id>", strict_slashes=False, methods=['GET'])
def get_amenities_id(amenity_id):
    """Get object amenities"""
    amenities = storage.all(Amenity)
    for instance in amenities.values():
        if instance.id == amenity_id:
            return jsonify(instance.to_dict())
    abort(404)


@app_views.route(
    "/amenities/<amenity_id>", strict_slashes=False, methods=['DELETE'])
def delete_state(amenity_id):
    """delete an amenities"""
    amenities = storage.get(Amenity, amenity_id)
    if amenities is None:
        abort(404)
    else:
        storage.delete(amenities)
        storage.save()
        return jsonify({}), 200


@app_views.route("/amenities", strict_slashes=False, methods=['POST'])
def post_amenities():
    if not request.get_json():
        abort(400, "Not a JSON")
    if 'name' not in request.get_json():
        abort(400, "Missing name")
    amenities = Amenity(**request.get_json())
    amenities.save()
    return jsonify(amenities.to_dict()), 201


@app_views.route(
    "/amenities/<amenity_id>", strict_slashes=False, methods=['PUT'])
def put_state(amenity_id):
    amenities = storage.get(Amenity, amenity_id)
    if amenities is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    for key, value in request.get_json().items():
        if key != "id" or key != "created_at" or key != "updated_at":
            setattr(amenities, key, value)
    amenities.save()
    return jsonify(amenities.to_dict()), 200
