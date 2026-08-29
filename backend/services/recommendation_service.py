from sqlalchemy.orm import Session

from database.models import Food


def get_food_recommendations(
    db: Session,
    calorie_target: float,
    protein_target: float,
    limit: int = 10
):
    """
    Return foods that are useful for meeting
    the user's daily calorie and protein targets.
    """

    foods = (
        db.query(Food)
        .filter(
            Food.calories.isnot(None),
            Food.protein.isnot(None)
        )
        .order_by(Food.protein.desc())
        .limit(limit)
        .all()
    )

    recommendations = []

    for food in foods:
        recommendations.append({
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
        })

    return recommendations