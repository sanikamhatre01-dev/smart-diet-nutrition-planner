from flask import Blueprint, request, jsonify

from database.database import SessionLocal
from backend.services.user_service import (
    create_user,
    get_user,
    get_all_users,
    update_user,
    delete_user
)


user_bp = Blueprint("user", __name__, url_prefix="/api/users")
@user_bp.route("", methods=["GET"])
def get_all_user_profiles():
    db = SessionLocal()

    try:
        users = get_all_users(db)

        return jsonify({
            "users": [
                {
                    "user_id": user.user_id,
                    "name": user.name,
                    "email": user.email,
                    "age": user.age,
                    "gender": user.gender
                }
                for user in users
            ]
        })

    finally:
        db.close()


@user_bp.route("", methods=["POST"])
def register_user():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({
            "error": "Name and email are required"
        }), 400

    db = SessionLocal()

    try:
        user = create_user(
            db=db,
            name=name,
            email=email,
            age=data.get("age"),
            gender=data.get("gender")
        )

        if user is None:
            return jsonify({
                "error": "Email already registered"
            }), 409

        return jsonify({
            "message": "User created successfully",
            "user": {
                "user_id": user.user_id,
                "name": user.name,
                "email": user.email,
                "age": user.age,
                "gender": user.gender
            }
        }), 201

    finally:
        db.close()


@user_bp.route("/<int:user_id>", methods=["GET"])
def get_user_profile(user_id):
    db = SessionLocal()

    try:
        user = get_user(db, user_id)

        if user is None:
            return jsonify({
                "error": "User not found"
            }), 404

        return jsonify({
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email,
            "age": user.age,
            "gender": user.gender
        })

    finally:
        db.close()


@user_bp.route("/<int:user_id>", methods=["PUT"])
def update_user_profile(user_id):
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    db = SessionLocal()

    try:
        user = update_user(
            db=db,
            user_id=user_id,
            name=data.get("name"),
            email=data.get("email"),
            age=data.get("age"),
            gender=data.get("gender")
        )

        if user is None:
            return jsonify({
                "error": "User not found"
            }), 404
        if user == "EMAIL_EXISTS":
            return jsonify({
        "error": "Email already registered"
            }), 409


        return jsonify({
            "message": "User updated successfully",
            "user": {
                "user_id": user.user_id,
                "name": user.name,
                "email": user.email,
                "age": user.age,
                "gender": user.gender
            }
        })

    finally:
        db.close()


@user_bp.route("/<int:user_id>", methods=["DELETE"])
def remove_user(user_id):
    db = SessionLocal()

    try:
        deleted = delete_user(db, user_id)

        if not deleted:
            return jsonify({
                "error": "User not found"
            }), 404

        return jsonify({
            "message": "User deleted successfully"
        })

    finally:
        db.close()