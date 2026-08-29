from sqlalchemy.orm import Session

from database.models import FoodCategory


def create_category(db: Session, category_name: str):
    existing_category = (
        db.query(FoodCategory)
        .filter(FoodCategory.category_name == category_name)
        .first()
    )

    if existing_category:
        return None

    category = FoodCategory(
        category_name=category_name
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


def get_category(db: Session, category_id: int):
    return (
        db.query(FoodCategory)
        .filter(FoodCategory.category_id == category_id)
        .first()
    )


def get_all_categories(db: Session):
    return db.query(FoodCategory).all()


def update_category(
    db: Session,
    category_id: int,
    category_name: str
):
    category = get_category(db, category_id)

    if not category:
        return None

    category.category_name = category_name

    db.commit()
    db.refresh(category)

    return category


def delete_category(db: Session, category_id: int):
    category = get_category(db, category_id)

    if not category:
        return False

    db.delete(category)
    db.commit()

    return True