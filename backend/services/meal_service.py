from sqlalchemy.orm import Session

from database.models import MealPlan, MealItem, Food


def create_meal_plan(
    db: Session,
    user_id: int,
    plan_date,
    total_calories=0,
    total_protein=0
):
    plan = MealPlan(
        user_id=user_id,
        plan_date=plan_date,
        total_calories=total_calories,
        total_protein=total_protein
    )

    db.add(plan)
    db.commit()
    db.refresh(plan)

    return plan


def get_meal_plan(db: Session, plan_id: int):
    return (
        db.query(MealPlan)
        .filter(MealPlan.plan_id == plan_id)
        .first()
    )


def get_user_meal_plans(db: Session, user_id: int):
    return (
        db.query(MealPlan)
        .filter(MealPlan.user_id == user_id)
        .all()
    )


def add_meal_item(
    db: Session,
    plan_id: int,
    food_id: int,
    meal_type: str,
    quantity: float
):
    # Check that the meal plan exists
    plan = get_meal_plan(db, plan_id)

    if not plan:
        return None

    # Check that the food exists
    food = (
        db.query(Food)
        .filter(Food.food_id == food_id)
        .first()
    )

    if not food:
        return None

    item = MealItem(
        plan_id=plan_id,
        food_id=food_id,
        meal_type=meal_type,
        quantity=quantity
    )

    db.add(item)

    # Update meal plan totals
    plan.total_calories = (
        (plan.total_calories or 0)
        + ((food.calories or 0) * quantity)
    )

    plan.total_protein = (
        (plan.total_protein or 0)
        + ((food.protein or 0) * quantity)
    )

    db.commit()
    db.refresh(item)

    return item


def get_meal_items(db: Session, plan_id: int):
    return (
        db.query(MealItem)
        .filter(MealItem.plan_id == plan_id)
        .all()
    )


def get_meal_item(db: Session, meal_item_id: int):
    return (
        db.query(MealItem)
        .filter(MealItem.meal_item_id == meal_item_id)
        .first()
    )
def update_meal_item(
    db: Session,
    meal_item_id: int,
    quantity=None,
    meal_type=None
):
    item = get_meal_item(db, meal_item_id)

    if not item:
        return None

    plan = get_meal_plan(db, item.plan_id)

    food = (
        db.query(Food)
        .filter(Food.food_id == item.food_id)
        .first()
    )

    if not plan or not food:
        return None

    # Remove old nutrition values
    plan.total_calories = (
        (plan.total_calories or 0)
        - ((food.calories or 0) * item.quantity)
    )

    plan.total_protein = (
        (plan.total_protein or 0)
        - ((food.protein or 0) * item.quantity)
    )

    # Update quantity
    if quantity is not None:
        item.quantity = quantity

    if meal_type is not None:
        item.meal_type = meal_type

    # Add new nutrition values
    plan.total_calories = (
        (plan.total_calories or 0)
        + ((food.calories or 0) * item.quantity)
    )

    plan.total_protein = (
        (plan.total_protein or 0)
        + ((food.protein or 0) * item.quantity)
    )

    db.commit()
    db.refresh(item)

    return item

def delete_meal_item(db: Session, meal_item_id: int):
    item = get_meal_item(db, meal_item_id)

    if not item:
        return False

    plan = get_meal_plan(db, item.plan_id)

    food = (
        db.query(Food)
        .filter(Food.food_id == item.food_id)
        .first()
    )

    # Remove the item's nutrition from plan totals
    if plan and food:
        plan.total_calories = max(
            0,
            (plan.total_calories or 0)
            - ((food.calories or 0) * item.quantity)
        )

        plan.total_protein = max(
            0,
            (plan.total_protein or 0)
            - ((food.protein or 0) * item.quantity)
        )

    db.delete(item)
    db.commit()

    return True