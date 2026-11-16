from datetime import date

from health.models import User, Measurement, DailyNutrition


def save_user(user_object:User, working_path:str) -> None:
    json_str = user_object.model_dump_json(indent=4,exclude={"measurements": {"__all__": {"bmi"}}}) # we dont save bmi because it is calculated automatically
    with open(working_path, "w",encoding="utf-8") as f:
        f.write(json_str)

def load_user(working_path:str) -> User:
    with open(working_path, "r") as f:
        data = f.read()
        user_l = User.model_validate_json(data)
    return user_l


if __name__ == "__main__":

    measurement = Measurement(
        measurement_date = date.today(),
        weight_kg = 60,
        height_cm = 170
    )

    daily_nutrition = DailyNutrition(
        nutrition_date = date.today(),
        calories = 2200,
        protein_g = 150,
        carbs_g = 250,
        fat_g = 70
    )

    user = User(
        name="John Doe",
        birth_year=1999,
        measurements = [measurement],
        nutrition = [daily_nutrition],
    )

    save_user(user, "user.json")
    print(user)
    print(load_user("user.json"))
