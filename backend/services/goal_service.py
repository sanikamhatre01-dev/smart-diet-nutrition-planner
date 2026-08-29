from sqlalchemy.orm import Session
from database.models import UserGoal


def create_goal(
    db: Session,
    user_id: int,
    goal_type: str,
    target_weight=None,
    target_date=None
):
    existing_goal = (
        db.query(UserGoal)
        .filter(UserGoal.user_id == user_id)
        .first()
    )

    if existing_goal:
        return None

    goal = UserGoal(
        user_id=user_id,
        goal_type=goal_type,
        target_weight=target_weight,
        target_date=target_date
    )

    db.add(goal)
    db.commit()
    db.refresh(goal)

    return goal


def get_goal(db: Session, user_id: int):
    return (
        db.query(UserGoal)
        .filter(UserGoal.user_id == user_id)
        .first()
    )


def update_goal(
    db: Session,
    user_id: int,
    goal_type=None,
    target_weight=None,
    target_date=None
):
    goal = get_goal(db, user_id)

    if not goal:
        return None

    if goal_type is not None:
        goal.goal_type = goal_type

    if target_weight is not None:
        goal.target_weight = target_weight

    if target_date is not None:
        goal.target_date = target_date

    db.commit()
    db.refresh(goal)

    return goal


def delete_goal(db: Session, user_id: int):
    goal = get_goal(db, user_id)

    if not goal:
        return False

    db.delete(goal)
    db.commit()

    return True