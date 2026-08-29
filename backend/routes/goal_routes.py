from flask import Blueprint, request, jsonify
from datetime import datetime

from database.database import SessionLocal

from backend.services.goal_service import (
    create_goal,
    get_goal,
    update_goal,
    delete_goal
)


goal_bp = Blueprint(
    "goal",
    __name__,
    url_prefix="/api/goals"
)


@goal_bp.route("/<int:user_id>", methods=["POST"])
def add_goal(user_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    goal_type = data.get("goal_type")

    if not goal_type:
        return jsonify({
            "error": "Goal type is required"
        }), 400

    target_date = data.get("target_date")

    if target_date:
        try:
            target_date = datetime.strptime(
                target_date, "%Y-%m-%d"
            ).date()
        except ValueError:
            return jsonify({
                "error": "target_date must be in YYYY-MM-DD format"
            }), 400

    db = SessionLocal()

    try:
        goal = create_goal(
            db=db,
            user_id=user_id,
            goal_type=goal_type,
            target_weight=data.get("target_weight"),
            target_date=target_date
        )

        if goal is None:
            return jsonify({
                "error": "Goal already exists for this user"
            }), 409

        return jsonify({
            "message": "Goal created successfully",
            "goal": {
                "goal_id": goal.goal_id,
                "user_id": goal.user_id,
                "goal_type": goal.goal_type,
                "target_weight": goal.target_weight,
                "target_date": (
                    goal.target_date.isoformat()
                    if goal.target_date else None
                )
            }
        }), 201

    finally:
        db.close()


@goal_bp.route("/<int:user_id>", methods=["GET"])
def get_user_goal(user_id):

    db = SessionLocal()

    try:
        goal = get_goal(db, user_id)

        if goal is None:
            return jsonify({
                "error": "Goal not found"
            }), 404

        return jsonify({
            "goal_id": goal.goal_id,
            "user_id": goal.user_id,
            "goal_type": goal.goal_type,
            "target_weight": goal.target_weight,
            "target_date": (
                goal.target_date.isoformat()
                if goal.target_date else None
            )
        })

    finally:
        db.close()


@goal_bp.route("/<int:user_id>", methods=["PUT"])
def update_user_goal(user_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    target_date = data.get("target_date")

    if target_date:
        try:
            target_date = datetime.strptime(
                target_date, "%Y-%m-%d"
            ).date()
        except ValueError:
            return jsonify({
                "error": "target_date must be in YYYY-MM-DD format"
            }), 400

    db = SessionLocal()

    try:
        goal = update_goal(
            db=db,
            user_id=user_id,
            goal_type=data.get("goal_type"),
            target_weight=data.get("target_weight"),
            target_date=target_date
        )

        if goal is None:
            return jsonify({
                "error": "Goal not found"
            }), 404

        return jsonify({
            "message": "Goal updated successfully",
            "goal": {
                "goal_id": goal.goal_id,
                "user_id": goal.user_id,
                "goal_type": goal.goal_type,
                "target_weight": goal.target_weight,
                "target_date": (
                    goal.target_date.isoformat()
                    if goal.target_date else None
                )
            }
        })

    finally:
        db.close()


@goal_bp.route("/<int:user_id>", methods=["DELETE"])
def remove_user_goal(user_id):

    db = SessionLocal()

    try:
        deleted = delete_goal(db, user_id)

        if not deleted:
            return jsonify({
                "error": "Goal not found"
            }), 404

        return jsonify({
            "message": "Goal deleted successfully"
        })

    finally:
        db.close()