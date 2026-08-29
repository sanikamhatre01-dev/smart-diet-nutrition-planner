from flask import Blueprint, request, jsonify

from database.database import SessionLocal

from backend.services.health_service import (
    create_health,
    get_health,
    update_health
)


health_bp = Blueprint(
    "health",
    __name__,
    url_prefix="/api/health"
)


@health_bp.route("/<int:user_id>", methods=["POST"])
def add_health(user_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    height_cm = data.get("height_cm")
    weight_kg = data.get("weight_kg")
    activity_level = data.get("activity_level")

    if not height_cm or not weight_kg or not activity_level:
        return jsonify({
            "error": "Height, weight and activity level are required"
        }), 400

    db = SessionLocal()

    try:

        health = create_health(
            db=db,
            user_id=user_id,
            height_cm=height_cm,
            weight_kg=weight_kg,
            activity_level=activity_level
        )

        if health is None:
            return jsonify({
                "error": "Health information already exists for this user"
            }), 409

        return jsonify({
            "message": "Health information added successfully",
            "health": {
                "health_id": health.health_id,
                "user_id": health.user_id,
                "height_cm": health.height_cm,
                "weight_kg": health.weight_kg,
                "activity_level": health.activity_level,
                "bmi": health.bmi,
                "daily_calorie_target": health.daily_calorie_target
            }
        }), 201

    finally:
        db.close()


@health_bp.route("/<int:user_id>", methods=["GET"])
def get_health_info(user_id):

    db = SessionLocal()

    try:

        health = get_health(db, user_id)

        if health is None:
            return jsonify({
                "error": "Health information not found"
            }), 404

        return jsonify({
            "health_id": health.health_id,
            "user_id": health.user_id,
            "height_cm": health.height_cm,
            "weight_kg": health.weight_kg,
            "activity_level": health.activity_level,
            "bmi": health.bmi,
            "daily_calorie_target": health.daily_calorie_target
        })

    finally:
        db.close()


@health_bp.route("/<int:user_id>", methods=["PUT"])
def update_health_info(user_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    db = SessionLocal()

    try:

        health = update_health(
            db=db,
            user_id=user_id,
            height_cm=data.get("height_cm"),
            weight_kg=data.get("weight_kg"),
            activity_level=data.get("activity_level")
        )

        if health is None:
            return jsonify({
                "error": "Health information not found"
            }), 404

        return jsonify({
            "message": "Health information updated successfully",
            "health": {
                "health_id": health.health_id,
                "user_id": health.user_id,
                "height_cm": health.height_cm,
                "weight_kg": health.weight_kg,
                "activity_level": health.activity_level,
                "bmi": health.bmi,
                "daily_calorie_target": health.daily_calorie_target
            }
        })

    finally:
        db.close()