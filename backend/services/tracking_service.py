from sqlalchemy.orm import Session

from database.models import NutritionTracking


def create_tracking(
    db: Session,
    user_id: int,
    tracking_date,
    calories_consumed=0,
    protein_consumed=0,
    water_liters=0,
    steps=0
):
    tracking = NutritionTracking(
        user_id=user_id,
        tracking_date=tracking_date,
        calories_consumed=calories_consumed,
        protein_consumed=protein_consumed,
        water_liters=water_liters,
        steps=steps
    )

    db.add(tracking)
    db.commit()
    db.refresh(tracking)

    return tracking


def get_tracking(db: Session, tracking_id: int):
    return (
        db.query(NutritionTracking)
        .filter(
            NutritionTracking.tracking_id == tracking_id
        )
        .first()
    )


def get_user_tracking(db: Session, user_id: int):
    return (
        db.query(NutritionTracking)
        .filter(
            NutritionTracking.user_id == user_id
        )
        .all()
    )


def update_tracking(
    db: Session,
    tracking_id: int,
    calories_consumed=None,
    protein_consumed=None,
    water_liters=None,
    steps=None
):
    tracking = get_tracking(db, tracking_id)

    if not tracking:
        return None

    if calories_consumed is not None:
        tracking.calories_consumed = calories_consumed

    if protein_consumed is not None:
        tracking.protein_consumed = protein_consumed

    if water_liters is not None:
        tracking.water_liters = water_liters

    if steps is not None:
        tracking.steps = steps

    db.commit()
    db.refresh(tracking)

    return tracking


def delete_tracking(db: Session, tracking_id: int):
    tracking = get_tracking(db, tracking_id)

    if not tracking:
        return False

    db.delete(tracking)
    db.commit()

    return True