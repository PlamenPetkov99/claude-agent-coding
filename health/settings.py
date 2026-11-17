from pathlib import Path

from pydantic import (
    Field,
    field_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_name: str = Field(default="claude-haiku-5-5", description="The name of the model to use")
    max_tokens: int = Field(default=500, description="The maximum number of tokens to generate")
    data_file: Path = Field(description="The path to the data file")
    model_config = SettingsConfigDict(env_prefix='MY_HEALTH_', extra='forbid', env_file='.env',
                                      env_file_encoding='utf-8')

    @field_validator('max_tokens')
    @classmethod
    def check_max_tokens_in_range(cls, value: int) -> int:
        if not 1 <= value <= 4096:
            raise ValueError('max_tokens must be between 1 and 4096')
        return value
