from flask import Blueprint, request, jsonify

from backend.utils.calculations import (
    calculate_nutrition_summary
)


nutrition_bp = Blueprint(
    "nutrition",
    __name__,
    url_prefix="/api/nutrition"
)


@nutrition_bp.route("/calculate", methods=["POST"])
def calculate_nutrition():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    weight_kg = data.get("weight_kg")
    height_cm = data.get("height_cm")
    activity_level = data.get("activity_level")

    if weight_kg is None or height_cm is None or not activity_level:
        return jsonify({
            "error": "weight_kg, height_cm and activity_level are required"
        }), 400

    try:
        weight_kg = float(weight_kg)
        height_cm = float(height_cm)

    except (TypeError, ValueError):
        return jsonify({
            "error": "weight_kg and height_cm must be numbers"
        }), 400

    if weight_kg <= 0 or height_cm <= 0:
        return jsonify({
            "error": "weight_kg and height_cm must be greater than 0"
        }), 400

    result = calculate_nutrition_summary(
        weight_kg=weight_kg,
        height_cm=height_cm,
        activity_level=activity_level
    )

    return jsonify({
        "message": "Nutrition calculated successfully",
        "nutrition": result
    })
from database.database import SessionLocal
from backend.services.health_service import get_health
from backend.utils.calculations import (
    calculate_daily_protein_target
)


@nutrition_bp.route("/<int:user_id>", methods=["GET"])
def get_user_nutrition(user_id):

    db = SessionLocal()

    try:
        health = get_health(db, user_id)

        if health is None:
            return jsonify({
                "error": "Health information not found"
            }), 404

        protein_target = calculate_daily_protein_target(
            health.weight_kg,
            health.activity_level
        )

        return jsonify({
            "user_id": user_id,
            "nutrition": {
                "bmi": health.bmi,
                "daily_calorie_target": health.daily_calorie_target,
                "daily_protein_target": protein_target
            }
        })

    finally:
        db.close()