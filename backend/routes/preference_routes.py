from flask import Blueprint, request, jsonify

from database.database import SessionLocal

from backend.services.preference_service import (
    create_preference,
    get_preference,
    update_preference,
    delete_preference
)


preference_bp = Blueprint(
    "preference",
    __name__,
    url_prefix="/api/preferences"
)


def preference_to_dict(preference):
    return {
        "preference_id": preference.preference_id,
        "user_id": preference.user_id,
        "diet_type": preference.diet_type,
        "allergies": preference.allergies,
        "disliked_foods": preference.disliked_foods,
        "budget_level": preference.budget_level
    }


# CREATE PREFERENCE
@preference_bp.route("/<int:user_id>", methods=["POST"])
def create_user_preference(user_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    db = SessionLocal()

    try:

        preference = create_preference(
            db=db,
            user_id=user_id,
            diet_type=data.get("diet_type"),
            allergies=data.get("allergies"),
            disliked_foods=data.get("disliked_foods"),
            budget_level=data.get("budget_level")
        )

        if preference is None:
            return jsonify({
                "error": "Preferences already exist for this user"
            }), 409

        return jsonify({
            "message": "User preferences created successfully",
            "preference": preference_to_dict(preference)
        }), 201

    finally:
        db.close()


# GET PREFERENCE
@preference_bp.route("/<int:user_id>", methods=["GET"])
def get_user_preference(user_id):

    db = SessionLocal()

    try:

        preference = get_preference(
            db,
            user_id
        )

        if preference is None:
            return jsonify({
                "error": "Preferences not found"
            }), 404

        return jsonify(
            preference_to_dict(preference)
        )

    finally:
        db.close()


# UPDATE PREFERENCE
@preference_bp.route("/<int:user_id>", methods=["PUT"])
def update_user_preference(user_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    db = SessionLocal()

    try:

        preference = update_preference(
            db=db,
            user_id=user_id,
            diet_type=data.get("diet_type"),
            allergies=data.get("allergies"),
            disliked_foods=data.get("disliked_foods"),
            budget_level=data.get("budget_level")
        )

        if preference is None:
            return jsonify({
                "error": "Preferences not found"
            }), 404

        return jsonify({
            "message": "User preferences updated successfully",
            "preference": preference_to_dict(preference)
        })

    finally:
        db.close()


# DELETE PREFERENCE
@preference_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user_preference(user_id):

    db = SessionLocal()

    try:

        deleted = delete_preference(
            db,
            user_id
        )

        if not deleted:
            return jsonify({
                "error": "Preferences not found"
            }), 404

        return jsonify({
            "message": "User preferences deleted successfully"
        })

    finally:
        db.close()