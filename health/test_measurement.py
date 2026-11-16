from datetime import date, timedelta

from pydantic import ValidationError

from health.models import Measurement


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
            measurement = Measurement.model_validate({**data}, strict=is_strict)
            print(f"Pass , Name of the test: {key} Object: {measurement.model_dump_json()}")
        except ValidationError as e:
            print(f"Fail, Name of the test: {key}:")
            for error in e.errors():
                print(f"Field: {error['loc'][0]} , Reason: {error['msg']}")

if __name__ == "__main__":

    data_dict = {
        'data_valid' : {
            "weight_kg":70,
            "height_cm":170,
            "measurement_date":date.today()
        },
        'data_negative_weight':{
            "weight_kg":-10,
            "height_cm":170,
            "measurement_date":date.today()
        },
        'data_weight_as_string':{
            "weight_kg":"72.5",
            "height_cm":170,
            "measurement_date":date.fromisoformat("2026-11-16")
        },
        'data_weight_as_abc':{
            "weight_kg":"abc",
            "height_cm":170,
            "measurement_date":date.today()
        },
        'data_date_in_future':{
            "weight_kg":70,
            "height_cm":170,
            "measurement_date":date.today() + timedelta(days=1)
        },
        'data_height_missing':{
            "weight_kg":70,
            "measurement_date":date.today()
        },
        'data_extra_fields':{
            "weight_kg": 70,
            "height_cm": 170,
            "measurement_date": date.today(),
            "mood": "happy"
        },
        'data_date_as_str':{
            "weight_kg":70,
            "height_cm":170,
            "measurement_date":"16.11.2026"
        },
        'data_date_as_real_str':{
            "weight_kg":70,
            "height_cm":170,
            "measurement_date": "2026-11-16",
        },
        'data_two_errors':{
            "weight_kg":-70,
            "height_cm":170,
            "measurement_date":"16.11.2026"
        }
    }

    run_tests(data_dict)
