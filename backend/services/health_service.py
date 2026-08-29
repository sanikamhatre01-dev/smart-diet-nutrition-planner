from sqlalchemy.orm import Session

from database.models import UserHealth
from backend.utils.calculations import (
    calculate_bmi,
    calculate_daily_calorie_target
)


def create_health(
    db: Session,
    user_id: int,
    height_cm: float,
    weight_kg: float,
    activity_level: str
):
    # Check whether user exists in health table
    existing_health = (
        db.query(UserHealth)
        .filter(UserHealth.user_id == user_id)
        .first()
    )

    if existing_health:
        return None

    bmi = calculate_bmi(weight_kg, height_cm)

    daily_calorie_target = calculate_daily_calorie_target(
        weight_kg,
        activity_level
    )

    health = UserHealth(
        user_id=user_id,
        height_cm=height_cm,
        weight_kg=weight_kg,
        activity_level=activity_level,
        bmi=bmi,
        daily_calorie_target=daily_calorie_target
    )

    db.add(health)
    db.commit()
    db.refresh(health)

    return health


def get_health(db: Session, user_id: int):
    return (
        db.query(UserHealth)
        .filter(UserHealth.user_id == user_id)
        .first()
    )


def update_health(
    db: Session,
    user_id: int,
    height_cm=None,
    weight_kg=None,
    activity_level=None
):
    health = get_health(db, user_id)

    if not health:
        return None

    if height_cm is not None:
        health.height_cm = height_cm

    if weight_kg is not None:
        health.weight_kg = weight_kg

    if activity_level is not None:
        health.activity_level = activity_level

    # Recalculate BMI and calories
    health.bmi = calculate_bmi(
        health.weight_kg,
        health.height_cm
    )

    health.daily_calorie_target = calculate_daily_calorie_target(
        health.weight_kg,
        health.activity_level
    )

    db.commit()
    db.refresh(health)

    return health