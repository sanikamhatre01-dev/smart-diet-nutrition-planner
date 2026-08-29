from flask import Blueprint, request, jsonify

from database.database import SessionLocal

from backend.services.category_service import (
    create_category,
    get_category,
    get_all_categories,
    update_category,
    delete_category
)


category_bp = Blueprint(
    "category",
    __name__,
    url_prefix="/api/categories"
)


def category_to_dict(category):
    return {
        "category_id": category.category_id,
        "category_name": category.category_name
    }


@category_bp.route("", methods=["POST"])
def create_category_route():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    category_name = data.get("category_name")

    if not category_name:
        return jsonify({
            "error": "category_name is required"
        }), 400

    db = SessionLocal()

    try:
        category = create_category(
            db=db,
            category_name=category_name
        )

        if category is None:
            return jsonify({
                "error": "Category already exists"
            }), 409

        return jsonify({
            "message": "Category created successfully",
            "category": category_to_dict(category)
        }), 201

    finally:
        db.close()


@category_bp.route("", methods=["GET"])
def get_categories():

    db = SessionLocal()

    try:
        categories = get_all_categories(db)

        return jsonify({
            "categories": [
                category_to_dict(category)
                for category in categories
            ]
        })

    finally:
        db.close()


@category_bp.route("/<int:category_id>", methods=["GET"])
def get_category_route(category_id):

    db = SessionLocal()

    try:
        category = get_category(db, category_id)

        if category is None:
            return jsonify({
                "error": "Category not found"
            }), 404

        return jsonify(
            category_to_dict(category)
        )

    finally:
        db.close()


@category_bp.route("/<int:category_id>", methods=["PUT"])
def update_category_route(category_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    category_name = data.get("category_name")

    if not category_name:
        return jsonify({
            "error": "category_name is required"
        }), 400

    db = SessionLocal()

    try:
        category = update_category(
            db=db,
            category_id=category_id,
            category_name=category_name
        )

        if category is None:
            return jsonify({
                "error": "Category not found"
            }), 404

        return jsonify({
            "message": "Category updated successfully",
            "category": category_to_dict(category)
        })

    finally:
        db.close()


@category_bp.route("/<int:category_id>", methods=["DELETE"])
def delete_category_route(category_id):

    db = SessionLocal()

    try:
        deleted = delete_category(
            db,
            category_id
        )

        if not deleted:
            return jsonify({
                "error": "Category not found"
            }), 404

        return jsonify({
            "message": "Category deleted successfully"
        })

    finally:
        db.close()