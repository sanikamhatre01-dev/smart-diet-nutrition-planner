from flask import Blueprint, request, jsonify

from database.database import SessionLocal

from backend.services.health_service import get_health
from backend.services.recommendation_service import (
    get_food_recommendations
)
from backend.utils.calculations import (
    calculate_daily_protein_target
)


recommendation_bp = Blueprint(
    "recommendation",
    __name__,
    url_prefix="/api/recommendations"
)


@recommendation_bp.route("/<int:user_id>", methods=["GET"])
def get_recommendations(user_id):

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

        recommendations = get_food_recommendations(
            db=db,
            calorie_target=health.daily_calorie_target,
            protein_target=protein_target
        )

        return jsonify({
            "user_id": user_id,
            "targets": {
                "daily_calorie_target": health.daily_calorie_target,
                "daily_protein_target": protein_target
            },
            "recommendations": recommendations
        })

    finally:
        db.close()