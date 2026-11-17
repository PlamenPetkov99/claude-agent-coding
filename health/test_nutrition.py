from datetime import date, timedelta

from pydantic import ValidationError

from health.models import DailyNutrition


def print_raw_data(raw):
    print(raw)
    for key,value in raw.items():
        print(f"Parameter: {key} with type: {type(value)} , Value: {value}")

def run_tests(cases, is_strict:bool=False):
    if is_strict:
        print("With Strict Mode: ")
    for key, data in cases.items():
        print_raw_data(data.copy())
        try:
            daily_nutrition = DailyNutrition.model_validate({**data}, strict=is_strict)
            print(f"Pass , Name of the test: {key} Object: {daily_nutrition.model_dump_json()}")
        except ValidationError as e:
            print(f"Fail, Name of the test: {key}:")
            for error in e.errors():
                if not error['loc']:
                    print(f"Field: entire model , Reason: {error['msg']}")
                else:
                    print(f"Field: {error['loc'][0]} , Reason: {error['msg']}")

if __name__ == "__main__":

    data_dict = {
        'data_valid' : {
            "nutrition_date": date.today(),
            "protein_g": 150,
            "carbs_g": 250,
            "fat_g": 70,
            "calories": 2200,
        },
        'data_invalid': {
            "nutrition_date": date.today(),
            "protein_g": 150,
            "carbs_g": 250,
            "fat_g": 70,
            "calories": 2000,
        },
        'data_exatcly_plus_10_percent': {
            "nutrition_date": date.today(),
            "protein_g": 160,
            "carbs_g": 300,
            "fat_g": 40,
            "calories": 2000,
        },
        'data_exatcly_minus_10_percent': {
            "nutrition_date": date.today(),
            "protein_g": 100,
            "carbs_g": 260,
            "fat_g": 40,
            "calories": 2000,
        },
        'data_just_outside': {
            "nutrition_date": date.today(),
            "protein_g": 161,
            "carbs_g": 300,
            "fat_g": 40,
            "calories": 2000,
        },
        'data_all_zero': {
            "nutrition_date": date.today(),
            "protein_g": 0,
            "carbs_g": 0,
            "fat_g": 0,
            "calories": 0,
        },
        'data_zero_calories': {
            "nutrition_date": date.today(),
            "protein_g": 10,
            "carbs_g": 0,
            "fat_g": 0,
            "calories": 0,
        },
        'data_negative_value': {
            "nutrition_date": date.today(),
            "protein_g": 150,
            "carbs_g": 250,
            "fat_g": -5,
            "calories": 2200,
        },
        'data_calories_with_decimals': {
            "nutrition_date": date.today(),
            "protein_g": 150,
            "carbs_g": 250,
            "fat_g": 70,
            "calories": 2200.5,
        },
        'data_calories_as_2200_0': {
            "nutrition_date": date.today(),
            "protein_g": 150,
            "carbs_g": 250,
            "fat_g": 70,
            "calories": 2200.0,
        },
        'data_extra_field': {
            "nutrition_date": date.today(),
            "protein_g": 161,
            "carbs_g": 300,
            "fat_g": 40,
            "calories": 2000,
            "water": 2
        },
        'data_two_errors': {
            "nutrition_date": date.today(),
            "protein_g": -161,
            "carbs_g": 300,
            "fat_g": -40,
            "calories": 2000,
        },
    }

    run_tests(data_dict,True)
