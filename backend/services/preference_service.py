from sqlalchemy.orm import Session

from database.models import UserPreference


def create_preference(
    db: Session,
    user_id: int,
    diet_type=None,
    allergies=None,
    disliked_foods=None,
    budget_level=None
):
    # Check whether preferences already exist
    existing = (
        db.query(UserPreference)
        .filter(UserPreference.user_id == user_id)
        .first()
    )

    if existing:
        return None

    preference = UserPreference(
        user_id=user_id,
        diet_type=diet_type,
        allergies=allergies,
        disliked_foods=disliked_foods,
        budget_level=budget_level
    )

    db.add(preference)
    db.commit()
    db.refresh(preference)

    return preference


def get_preference(db: Session, user_id: int):
    return (
        db.query(UserPreference)
        .filter(UserPreference.user_id == user_id)
        .first()
    )


def update_preference(
    db: Session,
    user_id: int,
    diet_type=None,
    allergies=None,
    disliked_foods=None,
    budget_level=None
):
    preference = get_preference(db, user_id)

    if not preference:
        return None

    if diet_type is not None:
        preference.diet_type = diet_type

    if allergies is not None:
        preference.allergies = allergies

    if disliked_foods is not None:
        preference.disliked_foods = disliked_foods

    if budget_level is not None:
        preference.budget_level = budget_level

    db.commit()
    db.refresh(preference)

    return preference


def delete_preference(db: Session, user_id: int):
    preference = get_preference(db, user_id)

    if not preference:
        return False

    db.delete(preference)
    db.commit()

    return True