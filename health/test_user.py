import json
from datetime import date
from pathlib import Path

import pytest
from pydantic import ValidationError

from health.models import User, Measurement, DailyNutrition
from health.storage import save_user, load_user


@pytest.fixture
def valid_user() -> User:
    return User(
        name="John Doe",
        birth_year=1999,
        measurements=[
            Measurement(measurement_date=date.fromisoformat("2026-11-14"), weight_kg=70, height_cm=180),
            Measurement(measurement_date=date.fromisoformat("2026-11-15"), weight_kg=69.5, height_cm=180),
            Measurement(measurement_date=date.fromisoformat("2026-11-16"), weight_kg=69.8, height_cm=180),
        ],
        nutrition=[
            DailyNutrition(nutrition_date=date.fromisoformat("2026-11-15"), calories=2200,
                           protein_g=150, carbs_g=250, fat_g=70),
            DailyNutrition(nutrition_date=date.fromisoformat("2026-11-16"), calories=2000,
                           protein_g=140, carbs_g=220, fat_g=65),
        ],
    )


@pytest.fixture
def invalid_user_data() -> dict:
    return {
        "name": "John Doe",
        "birth_year": 1999,
        "measurements": [
            {"measurement_date": "2026-11-14", "weight_kg": -70, "height_cm": 180},
            {"measurement_date": "2026-11-15", "weight_kg": -500, "height_cm": 180},  # invalid
        ],
        "nutrition": [],
    }


def test_save_and_load_returns_the_same_user(valid_user: User, tmp_path) -> None:
    # Arrange - Prepare the data for the test step 1/3 of pytest documentation
    path = tmp_path / "user.json"

    # Act - Perform the action of the test step 2/3 of pytest documentation
    save_user(valid_user, path)
    loaded = load_user(path)

    # Assert - Verify the result of the test step 3/3 of pytest documentation
    assert loaded == valid_user


def test_validate_invalid_user(invalid_user_data: dict) -> None:
    with pytest.raises(ValidationError) as exc_info:
        User.model_validate(invalid_user_data)

    errors = exc_info.value.errors()
    assert len(errors) == 2
    assert errors[0]['loc'] == ('measurements', 0, 'weight_kg')
    assert errors[1]['loc'] == ('measurements', 1, 'weight_kg')


def test_load_user_rejects_invalid_value_in_file(valid_user: User, tmp_path: Path) -> None:
    path = tmp_path / "user.json"
    data = valid_user.model_dump(
        mode="json",
        exclude={"measurements": {"__all__": {"bmi"}}},
    )
    data["birth_year"] = 3000
    path.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(ValidationError) as exc_info:
        loaded = load_user(path)

    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0]['loc'] == ('birth_year',)


@pytest.fixture
def valid_user_dict() -> dict:
    return {
        "name": "John Doe",
        "birth_year": 1999,
        "measurements": [],
        "nutrition": [],
    }


def test_user_with_empty_lists_is_valid(valid_user_dict: dict)-> None:
    user = User.model_validate(valid_user_dict)
    assert len(user.measurements) == 0
    assert len(user.nutrition) == 0


@pytest.mark.parametrize("data,expected", [
    ({"name": "John Doe", "birth_year": date.today().year + 1, "measurements": [], "nutrition": [], }, ('birth_year',)),
    ({"name": "John Doe", "birth_year": 1850, "measurements": [], "nutrition": [], }, ('birth_year',)),
    ({"name": "", "birth_year": 2005, "measurements": [], "nutrition": [], }, ('name',)),
    ({"name": "   ", "birth_year": 2005, "measurements": [], "nutrition": [], }, ('name',)),
    ({"name": "John Doe", "birth_year": 2005,
      "measurements": [{"measurement_date":date.fromisoformat("2026-11-14"), "weight_kg":40, "height_cm":170},
                       {"measurement_date": date.fromisoformat("2026-11-14"), "weight_kg": 70,
                        "height_cm": 180}, ], "nutrition": [], }, ('measurements',)),
    ({"name": "John Doe", "birth_year": 2005, "measurements": [],
      "nutrition": [{"nutrition_date":date.fromisoformat("2026-11-15"), "calories":2200,
                                   "protein_g":150, "carbs_g":250, "fat_g":70},
                    {"nutrition_date":date.fromisoformat("2026-11-15"), "calories":2000,
                                   "protein_g":140, "carbs_g":220, "fat_g":65}, ], }, ('nutrition',)),

],ids=["invalid_birth_year_next_year","invalid_birth_year_before_1900","invalid_name","invalid_name_whitespace","invalid_measurements_same_date","invalid_nutrition_same_date"])
def test_user_with_invalid_parameters(data, expected)->None :

    with pytest.raises(ValidationError) as exc_info:
        User.model_validate(data)

    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0]['loc'] == expected
