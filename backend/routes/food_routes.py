from flask import Blueprint, request, jsonify

from database.database import SessionLocal

from backend.services.food_service import (
    create_food,
    get_food,
    get_all_foods,
    update_food,
    delete_food,
    search_foods
)


food_bp = Blueprint(
    "food",
    __name__,
    url_prefix="/api/foods"
)


def food_to_dict(food):
    return {
        "food_id": food.food_id,
        "food_name": food.food_name,
        "category_id": food.category_id,
        "food_type": food.food_type,
        "serving_size": food.serving_size,
        "calories": food.calories,
        "protein": food.protein,
        "carbohydrates": food.carbohydrates,
        "fat": food.fat,
        "fiber": food.fiber,
        "cost": food.cost
    }


@food_bp.route("", methods=["POST"])
def add_food():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    food_name = data.get("food_name")

    if not food_name:
        return jsonify({
            "error": "Food name is required"
        }), 400

    db = SessionLocal()

    try:
        food = create_food(
            db=db,
            food_name=food_name,
            category_id=data.get("category_id"),
            food_type=data.get("food_type"),
            serving_size=data.get("serving_size"),
            calories=data.get("calories"),
            protein=data.get("protein"),
            carbohydrates=data.get("carbohydrates"),
            fat=data.get("fat"),
            fiber=data.get("fiber"),
            cost=data.get("cost")
        )

        if food is None:
            return jsonify({
                "error": "Food already exists"
            }), 409

        return jsonify({
            "message": "Food created successfully",
            "food": food_to_dict(food)
        }), 201

    finally:
        db.close()


@food_bp.route("", methods=["GET"])
def get_foods():

    db = SessionLocal()

    try:
        foods = get_all_foods(db)

        return jsonify({
            "foods": [
                food_to_dict(food)
                for food in foods
            ]
        })

    finally:
        db.close()


@food_bp.route("/search", methods=["GET"])
def search_food():

    keyword = request.args.get("keyword")

    if not keyword:
        return jsonify({
            "error": "Search keyword is required"
        }), 400

    db = SessionLocal()

    try:
        foods = search_foods(db, keyword)

        return jsonify({
            "foods": [
                food_to_dict(food)
                for food in foods
            ]
        })

    finally:
        db.close()


@food_bp.route("/<int:food_id>", methods=["GET"])
def get_food_details(food_id):

    db = SessionLocal()

    try:
        food = get_food(db, food_id)

        if food is None:
            return jsonify({
                "error": "Food not found"
            }), 404

        return jsonify(food_to_dict(food))

    finally:
        db.close()


@food_bp.route("/<int:food_id>", methods=["PUT"])
def update_food_details(food_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    db = SessionLocal()

    try:
        food = update_food(
            db=db,
            food_id=food_id,
            food_name=data.get("food_name"),
            category_id=data.get("category_id"),
            food_type=data.get("food_type"),
            serving_size=data.get("serving_size"),
            calories=data.get("calories"),
            protein=data.get("protein"),
            carbohydrates=data.get("carbohydrates"),
            fat=data.get("fat"),
            fiber=data.get("fiber"),
            cost=data.get("cost")
        )

        if food is None:
            return jsonify({
                "error": "Food not found"
            }), 404

        return jsonify({
            "message": "Food updated successfully",
            "food": food_to_dict(food)
        })

    finally:
        db.close()


@food_bp.route("/<int:food_id>", methods=["DELETE"])
def remove_food(food_id):

    db = SessionLocal()

    try:
        deleted = delete_food(db, food_id)

        if not deleted:
            return jsonify({
                "error": "Food not found"
            }), 404

        return jsonify({
            "message": "Food deleted successfully"
        })

    finally:
        db.close()