from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, field_validator, computed_field, ConfigDict, model_validator
from typing_extensions import Self

MIN_AGE = 18   # app gives diet/weight tips: adults only (legal + medical reasons)
MAX_AGE = 120  # oldest realistic living person; above that it's a typo

class Measurement(BaseModel):
    measurement_date: date = Field(description="The date of the measurement") #renamed to measurement_date because we use date dataType :)
    weight_kg: float = Field(description="The weight in kilograms")
    height_cm: float = Field(description="The height in centimeters")
    note: Optional[str] = Field(description="Any additional notes or comments about the measurement",max_length=200,default=None)
    model_config = ConfigDict(extra="forbid")

    @field_validator('weight_kg')
    @classmethod
    def check_between_valid_weight(cls, value: float) -> float:
        if not 20 <= value <= 300:
            raise ValueError('Weight must be between 20 and 300 kg.')
        return value

    @field_validator('height_cm')
    @classmethod
    def check_between_valid_height(cls, value: float) -> float:
        if not 50 <= value <= 250:
            raise ValueError('Height must be between 50 and 250 cm.')
        return value

    @field_validator('measurement_date')
    @classmethod
    def check_date_not_in_future(cls, value: date) -> date:
        if value > date.today():
            raise ValueError('date must not be in the future')
        return value

    @computed_field
    @property
    def bmi(self) -> float:
        height_meters = self.height_cm / 100
        return round(self.weight_kg / (height_meters ** 2),1)



class DailyNutrition(BaseModel):
    nutrition_date: date = Field(description="The date of the nutrition",) #renamed to nutrition_date because we use date dataType :)
    calories: int = Field(description="The calories consumed",ge=0)
    protein_g: float = Field(description="The protein consumed in grams",ge=0)
    carbs_g: float = Field(description="The carbs consumed in grams",ge=0)
    fat_g: float = Field(description="The fat consumed in grams",ge=0)
    model_config = ConfigDict(extra="forbid")


    @model_validator(mode='after') #crossfield validation !!!! loc tuple is empty
    def check_calories(self) -> Self:
        value = self.calories
        implied_calories = (self.protein_g * 4) + (self.carbs_g * 4 + self.fat_g * 9)
        plus_10_percent = value + (value * 0.1)
        minus_10_percent = value - (value * 0.1)
        if not minus_10_percent <= implied_calories <= plus_10_percent:
            raise ValueError(f'Implied calories must be within 10% of the calories, implied: {implied_calories} , actual: {value}')
        return self


class User(BaseModel):
    name: str = Field(description="The name of the user",max_length=100,min_length=1)
    birth_year: int = Field(description="The birth year of the user")
    measurements: list[Measurement] = Field(description="The measurements of the user")
    nutrition: list[DailyNutrition] = Field(description="The nutrition of the user")
    model_config = ConfigDict(extra="forbid")

    @field_validator("name",mode='after')
    @classmethod
    def check_name_length(cls, value: str) -> str:
        value = value.strip()
        if len(value) > 100 or len(value) < 1:
            raise ValueError(f'Name must be between 1 and 100 characters, actual: {len(value)}')
        return value

    @field_validator("measurements",mode='after')
    @classmethod
    def check_measurements_date(cls, value: list[Measurement]) -> list[Measurement]:

        already_seen_dates = set()
        for measurement in value:
            current_date = measurement.measurement_date
            if current_date in already_seen_dates:
                raise ValueError(f'Measurement date must be unique, actual: {current_date}')
            else:
                already_seen_dates.add(current_date)

        return value

    @field_validator("nutrition", mode='after')
    @classmethod
    def check_nutrition_date(cls, value: list[DailyNutrition]) -> list[DailyNutrition]:

        already_seen_dates = set()
        for nutrition in value:
            current_date = nutrition.nutrition_date
            if current_date in already_seen_dates:
                raise ValueError(f'Nutrition date must be unique, actual: {current_date}')
            else:
                already_seen_dates.add(current_date)

        return value

    @field_validator("birth_year", mode='after')
    @classmethod
    def check_birth_year(cls, value: int) -> int:

        current_year = date.today().year
        oldest_allowed = current_year - MAX_AGE
        youngest_allowed = current_year - MIN_AGE

        if not oldest_allowed <= value <= youngest_allowed:
            raise ValueError(
                f"Birth year must be between {oldest_allowed} and {youngest_allowed} "
                f"(age {MIN_AGE}-{MAX_AGE}), got {value}"
            )
        return value