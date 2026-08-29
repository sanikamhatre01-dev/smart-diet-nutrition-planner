from sqlalchemy.orm import Session

from database.models import User


def create_user(db: Session, name: str, email: str, age=None, gender=None):
    # Check whether the email already exists
    existing_user = db.query(User).filter(User.email == email).first()

    if existing_user:
        return None

    # Create new user
    user = User(
        name=name,
        email=email,
        age=age,
        gender=gender
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()
def get_all_users(db: Session):
    return db.query(User).all()


def update_user(db: Session, user_id: int, name=None, email=None, age=None, gender=None):
    user = get_user(db, user_id)

    if not user:
        return None

    # Check if the new email already belongs to another user
    if email is not None and email != user.email:
        existing_user = db.query(User).filter(User.email == email).first()

        if existing_user:
            return "EMAIL_EXISTS"

        user.email = email

    if name is not None:
        user.name = name

    if age is not None:
        user.age = age

    if gender is not None:
        user.gender = gender

    db.commit()
    db.refresh(user)

    return user


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)

    if not user:
        return False

    db.delete(user)
    db.commit()

    return True