def calculate_bmi(weight_kg, height_cm):
    """
    Calculate BMI using weight in kg and height in cm.
    """
    if not weight_kg or not height_cm or height_cm <= 0:
        return None

    height_m = height_cm / 100
    bmi = weight_kg / (height_m * height_m)

    return round(bmi, 2)


def calculate_daily_calorie_target(weight_kg, activity_level):
    """
    Basic daily calorie estimation based on weight
    and activity level.
    """

    activity_multipliers = {
        "sedentary": 30,
        "light": 33,
        "moderate": 35,
        "active": 38,
        "very_active": 40
    }

    multiplier = activity_multipliers.get(
        activity_level.lower(),
        30
    )

    return round(weight_kg * multiplier)