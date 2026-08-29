from sqlalchemy.orm import Session

from database.models import Food


def create_food(
    db: Session,
    food_name: str,
    category_id=None,
    food_type=None,
    serving_size=None,
    calories=None,
    protein=None,
    carbohydrates=None,
    fat=None,
    fiber=None,
    cost=None
):
    # Check if food already exists
    existing_food = (
        db.query(Food)
        .filter(Food.food_name == food_name)
        .first()
    )

    if existing_food:
        return None

    food = Food(
        food_name=food_name,
        category_id=category_id,
        food_type=food_type,
        serving_size=serving_size,
        calories=calories,
        protein=protein,
        carbohydrates=carbohydrates,
        fat=fat,
        fiber=fiber,
        cost=cost
    )

    db.add(food)
    db.commit()
    db.refresh(food)

    return food


def get_food(db: Session, food_id: int):
    return (
        db.query(Food)
        .filter(Food.food_id == food_id)
        .first()
    )


def get_all_foods(db: Session):
    return db.query(Food).all()


def update_food(
    db: Session,
    food_id: int,
    food_name=None,
    category_id=None,
    food_type=None,
    serving_size=None,
    calories=None,
    protein=None,
    carbohydrates=None,
    fat=None,
    fiber=None,
    cost=None
):
    food = get_food(db, food_id)

    if not food:
        return None

    if food_name is not None:
        food.food_name = food_name

    if category_id is not None:
        food.category_id = category_id

    if food_type is not None:
        food.food_type = food_type

    if serving_size is not None:
        food.serving_size = serving_size

    if calories is not None:
        food.calories = calories

    if protein is not None:
        food.protein = protein

    if carbohydrates is not None:
        food.carbohydrates = carbohydrates

    if fat is not None:
        food.fat = fat

    if fiber is not None:
        food.fiber = fiber

    if cost is not None:
        food.cost = cost

    db.commit()
    db.refresh(food)

    return food


def delete_food(db: Session, food_id: int):
    food = get_food(db, food_id)

    if not food:
        return False

    db.delete(food)
    db.commit()

    return True


def search_foods(db: Session, keyword: str):
    return (
        db.query(Food)
        .filter(Food.food_name.ilike(f"%{keyword}%"))
        .all()
    )