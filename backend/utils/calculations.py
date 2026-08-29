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
def calculate_daily_protein_target(weight_kg, activity_level):
    """
    Calculate a basic daily protein target in grams.
    """

    protein_multipliers = {
        "sedentary": 0.8,
        "light": 1.0,
        "moderate": 1.2,
        "active": 1.5,
        "very_active": 1.7
    }

    if not weight_kg or weight_kg <= 0:
        return None

    multiplier = protein_multipliers.get(
        activity_level.lower(),
        0.8
    )

    return round(weight_kg * multiplier, 2)
def calculate_nutrition_summary(
    weight_kg,
    height_cm,
    activity_level
):
    """
    Calculate BMI, daily calorie target,
    and daily protein target.
    """

    bmi = calculate_bmi(
        weight_kg,
        height_cm
    )

    calories = calculate_daily_calorie_target(
        weight_kg,
        activity_level
    )

    protein = calculate_daily_protein_target(
        weight_kg,
        activity_level
    )

    return {
        "bmi": bmi,
        "daily_calorie_target": calories,
        "daily_protein_target": protein
    }