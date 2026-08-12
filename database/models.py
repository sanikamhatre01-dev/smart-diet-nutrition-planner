from sqlalchemy import Column, Integer, String, Float, Date
from database.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    age = Column(Integer)
    gender = Column(String(20))


class UserHealth(Base):
    __tablename__ = "user_health"

    health_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    height_cm = Column(Float)
    weight_kg = Column(Float)
    activity_level = Column(String(50))
    bmi = Column(Float)
    daily_calorie_target = Column(Integer)


class UserGoal(Base):
    __tablename__ = "user_goals"

    goal_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    goal_type = Column(String(50))
    target_weight = Column(Float)
    target_date = Column(Date)


class UserPreference(Base):
    __tablename__ = "user_preferences"

    preference_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    diet_type = Column(String(50))
    allergies = Column(String(255))
    disliked_foods = Column(String(255))
    budget_level = Column(String(30))


class FoodCategory(Base):
    __tablename__ = "food_categories"

    category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(100), nullable=False)


class Food(Base):
    __tablename__ = "foods"

    food_id = Column(Integer, primary_key=True, index=True)
    food_name = Column(String(150), nullable=False)
    category_id = Column(Integer)
    food_type = Column(String(30))
    serving_size = Column(String(50))
    calories = Column(Float)
    protein = Column(Float)
    carbohydrates = Column(Float)
    fat = Column(Float)
    fiber = Column(Float)
    cost = Column(Float)


class MealPlan(Base):
    __tablename__ = "meal_plans"

    plan_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    plan_date = Column(Date)
    total_calories = Column(Integer)
    total_protein = Column(Float)


class MealItem(Base):
    __tablename__ = "meal_items"

    meal_item_id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, nullable=False)
    food_id = Column(Integer, nullable=False)
    meal_type = Column(String(30))
    quantity = Column(Float)


class NutritionTracking(Base):
    __tablename__ = "nutrition_tracking"

    tracking_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    tracking_date = Column(Date)
    calories_consumed = Column(Integer)
    protein_consumed = Column(Float)
    water_liters = Column(Float)
    steps = Column(Integer)
