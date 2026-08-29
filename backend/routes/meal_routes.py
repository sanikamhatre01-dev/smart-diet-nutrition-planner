from flask import Blueprint, request, jsonify
from datetime import datetime

from database.database import SessionLocal

from backend.services.meal_service import (
    create_meal_plan,
    get_meal_plan,
    get_user_meal_plans,
    add_meal_item,
    get_meal_items,
    get_meal_item,
    update_meal_item,
    delete_meal_item
)


meal_bp = Blueprint(
    "meal",
    __name__,
    url_prefix="/api/meals"
)


def plan_to_dict(plan):
    return {
        "plan_id": plan.plan_id,
        "user_id": plan.user_id,
        "plan_date": (
            plan.plan_date.isoformat()
            if plan.plan_date else None
        ),
        "total_calories": plan.total_calories,
        "total_protein": plan.total_protein
    }


# --------------------------------------------------
# CREATE MEAL PLAN
# --------------------------------------------------

@meal_bp.route("/<int:user_id>", methods=["POST"])
def add_meal_plan(user_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    plan_date = data.get("plan_date")

    if not plan_date:
        return jsonify({
            "error": "plan_date is required"
        }), 400

    try:
        plan_date = datetime.strptime(
            plan_date,
            "%Y-%m-%d"
        ).date()

    except ValueError:
        return jsonify({
            "error": "plan_date must be in YYYY-MM-DD format"
        }), 400

    db = SessionLocal()

    try:

        plan = create_meal_plan(
            db=db,
            user_id=user_id,
            plan_date=plan_date
        )

        return jsonify({
            "message": "Meal plan created successfully",
            "meal_plan": plan_to_dict(plan)
        }), 201

    finally:
        db.close()


# --------------------------------------------------
# GET USER MEAL PLANS
# --------------------------------------------------

@meal_bp.route("/<int:user_id>", methods=["GET"])
def get_user_meal_plans_route(user_id):

    db = SessionLocal()

    try:

        plans = get_user_meal_plans(
            db,
            user_id
        )

        return jsonify({
            "meal_plans": [
                plan_to_dict(plan)
                for plan in plans
            ]
        })

    finally:
        db.close()


# --------------------------------------------------
# GET SINGLE MEAL PLAN
# --------------------------------------------------

@meal_bp.route("/plan/<int:plan_id>", methods=["GET"])
def get_plan(plan_id):

    db = SessionLocal()

    try:

        plan = get_meal_plan(
            db,
            plan_id
        )

        if plan is None:
            return jsonify({
                "error": "Meal plan not found"
            }), 404

        return jsonify(
            plan_to_dict(plan)
        )

    finally:
        db.close()


# --------------------------------------------------
# ADD FOOD TO MEAL PLAN
# --------------------------------------------------

@meal_bp.route(
    "/plan/<int:plan_id>/items",
    methods=["POST"]
)
def add_item_to_plan(plan_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    food_id = data.get("food_id")
    meal_type = data.get("meal_type")
    quantity = data.get("quantity")

    if not food_id or not meal_type or quantity is None:
        return jsonify({
            "error": "food_id, meal_type and quantity are required"
        }), 400

    db = SessionLocal()

    try:

        item = add_meal_item(
            db=db,
            plan_id=plan_id,
            food_id=food_id,
            meal_type=meal_type,
            quantity=quantity
        )

        if item is None:
            return jsonify({
                "error": "Meal plan or food not found"
            }), 404

        return jsonify({
            "message": "Food added to meal plan successfully",
            "meal_item": {
                "meal_item_id": item.meal_item_id,
                "plan_id": item.plan_id,
                "food_id": item.food_id,
                "meal_type": item.meal_type,
                "quantity": item.quantity
            }
        }), 201

    finally:
        db.close()


# --------------------------------------------------
# GET MEAL ITEMS
# --------------------------------------------------

@meal_bp.route(
    "/plan/<int:plan_id>/items",
    methods=["GET"]
)
def get_plan_items(plan_id):

    db = SessionLocal()

    try:

        plan = get_meal_plan(
            db,
            plan_id
        )

        if plan is None:
            return jsonify({
                "error": "Meal plan not found"
            }), 404

        items = get_meal_items(
            db,
            plan_id
        )

        return jsonify({
            "meal_items": [
                {
                    "meal_item_id": item.meal_item_id,
                    "plan_id": item.plan_id,
                    "food_id": item.food_id,
                    "meal_type": item.meal_type,
                    "quantity": item.quantity
                }
                for item in items
            ]
        })

    finally:
        db.close()


# --------------------------------------------------
# UPDATE MEAL ITEM
# --------------------------------------------------

@meal_bp.route(
    "/item/<int:meal_item_id>",
    methods=["PUT"]
)
def update_item(meal_item_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    quantity = data.get("quantity")
    meal_type = data.get("meal_type")

    if quantity is None and meal_type is None:
        return jsonify({
            "error": "Quantity or meal_type is required"
        }), 400

    if quantity is not None:

        try:
            quantity = float(quantity)

        except (TypeError, ValueError):
            return jsonify({
                "error": "Quantity must be a number"
            }), 400

        if quantity <= 0:
            return jsonify({
                "error": "Quantity must be greater than 0"
            }), 400

    db = SessionLocal()

    try:

        item = update_meal_item(
            db=db,
            meal_item_id=meal_item_id,
            quantity=quantity,
            meal_type=meal_type
        )

        if item is None:
            return jsonify({
                "error": "Meal item not found"
            }), 404

        return jsonify({
            "message": "Meal item updated successfully",
            "meal_item": {
                "meal_item_id": item.meal_item_id,
                "plan_id": item.plan_id,
                "food_id": item.food_id,
                "meal_type": item.meal_type,
                "quantity": item.quantity
            }
        })

    finally:
        db.close()


# --------------------------------------------------
# DELETE MEAL ITEM
# --------------------------------------------------

@meal_bp.route(
    "/item/<int:meal_item_id>",
    methods=["DELETE"]
)
def remove_meal_item(meal_item_id):

    db = SessionLocal()

    try:

        deleted = delete_meal_item(
            db,
            meal_item_id
        )

        if not deleted:
            return jsonify({
                "error": "Meal item not found"
            }), 404

        return jsonify({
            "message": "Meal item deleted successfully"
        })

    finally:
        db.close()