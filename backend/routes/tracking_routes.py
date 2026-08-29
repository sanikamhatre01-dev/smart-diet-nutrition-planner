from flask import Blueprint, request, jsonify
from datetime import datetime

from database.database import SessionLocal

from backend.services.tracking_service import (
    create_tracking,
    get_tracking,
    get_user_tracking,
    update_tracking,
    delete_tracking
)


tracking_bp = Blueprint(
    "tracking",
    __name__,
    url_prefix="/api/tracking"
)


def tracking_to_dict(tracking):
    return {
        "tracking_id": tracking.tracking_id,
        "user_id": tracking.user_id,
        "tracking_date": (
            tracking.tracking_date.isoformat()
            if tracking.tracking_date
            else None
        ),
        "calories_consumed": tracking.calories_consumed,
        "protein_consumed": tracking.protein_consumed,
        "water_liters": tracking.water_liters,
        "steps": tracking.steps
    }


# CREATE TRACKING
@tracking_bp.route("/<int:user_id>", methods=["POST"])
def create_tracking_record(user_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    tracking_date = data.get("tracking_date")

    if not tracking_date:
        return jsonify({
            "error": "tracking_date is required"
        }), 400

    try:
        tracking_date = datetime.strptime(
            tracking_date,
            "%Y-%m-%d"
        ).date()

    except ValueError:
        return jsonify({
            "error": "tracking_date must be in YYYY-MM-DD format"
        }), 400

    db = SessionLocal()

    try:

        tracking = create_tracking(
            db=db,
            user_id=user_id,
            tracking_date=tracking_date,
            calories_consumed=data.get(
                "calories_consumed", 0
            ),
            protein_consumed=data.get(
                "protein_consumed", 0
            ),
            water_liters=data.get(
                "water_liters", 0
            ),
            steps=data.get(
                "steps", 0
            )
        )

        return jsonify({
            "message": "Nutrition tracking created successfully",
            "tracking": tracking_to_dict(tracking)
        }), 201

    finally:
        db.close()


# GET ALL TRACKING FOR USER
@tracking_bp.route("/user/<int:user_id>", methods=["GET"])
def get_user_tracking_records(user_id):

    db = SessionLocal()

    try:

        records = get_user_tracking(
            db,
            user_id
        )

        return jsonify({
            "tracking_records": [
                tracking_to_dict(record)
                for record in records
            ]
        })

    finally:
        db.close()


# GET SINGLE TRACKING
@tracking_bp.route("/<int:tracking_id>", methods=["GET"])
def get_tracking_record(tracking_id):

    db = SessionLocal()

    try:

        tracking = get_tracking(
            db,
            tracking_id
        )

        if tracking is None:
            return jsonify({
                "error": "Tracking record not found"
            }), 404

        return jsonify(
            tracking_to_dict(tracking)
        )

    finally:
        db.close()


# UPDATE TRACKING
@tracking_bp.route("/<int:tracking_id>", methods=["PUT"])
def update_tracking_record(tracking_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    db = SessionLocal()

    try:

        tracking = update_tracking(
            db=db,
            tracking_id=tracking_id,
            calories_consumed=data.get(
                "calories_consumed"
            ),
            protein_consumed=data.get(
                "protein_consumed"
            ),
            water_liters=data.get(
                "water_liters"
            ),
            steps=data.get(
                "steps"
            )
        )

        if tracking is None:
            return jsonify({
                "error": "Tracking record not found"
            }), 404

        return jsonify({
            "message": "Nutrition tracking updated successfully",
            "tracking": tracking_to_dict(tracking)
        })

    finally:
        db.close()


# DELETE TRACKING
@tracking_bp.route(
    "/<int:tracking_id>",
    methods=["DELETE"]
)
def delete_tracking_record(tracking_id):

    db = SessionLocal()

    try:

        deleted = delete_tracking(
            db,
            tracking_id
        )

        if not deleted:
            return jsonify({
                "error": "Tracking record not found"
            }), 404

        return jsonify({
            "message": "Nutrition tracking deleted successfully"
        })

    finally:
        db.close()