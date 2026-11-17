from pathlib import Path
import pytest
from pydantic import ValidationError
from health.settings import Settings


def test_valid_settings_with_only_data_file_set(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MY_HEALTH_DATA_FILE", "user.json")
    monkeypatch.delenv("MY_HEALTH_MAX_TOKENS", raising=False)
    monkeypatch.delenv("MY_HEALTH_MODEL_NAME", raising=False)

    settings = Settings(_env_file=None)
    assert settings.data_file == Path("user.json")
    assert settings.model_name == "claude-haiku-5-5"
    assert settings.max_tokens == 500

def test_valid_settings_with_all_set(monkeypatch: pytest.MonkeyPatch) -> None:

    monkeypatch.setenv("MY_HEALTH_MODEL_NAME", "gpt-3.5-turbo")
    monkeypatch.setenv("MY_HEALTH_MAX_TOKENS", "300")
    monkeypatch.setenv("MY_HEALTH_DATA_FILE", "user.json")

    settings = Settings(_env_file=None)
    assert settings.data_file == Path("user.json")
    assert settings.model_name == "gpt-3.5-turbo"
    assert settings.max_tokens == 300


def test_max_tokens_zero(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MY_HEALTH_MODEL_NAME", "gpt-3.5-turbo")
    monkeypatch.setenv("MY_HEALTH_MAX_TOKENS", "0")
    monkeypatch.setenv("MY_HEALTH_DATA_FILE", "user.json")

    with pytest.raises(ValidationError) as exc_info:
        Settings(_env_file=None)

    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0]["loc"] == ("max_tokens",)


def test_max_tokens_too_big_number(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MY_HEALTH_MODEL_NAME", "gpt-3.5-turbo")
    monkeypatch.setenv("MY_HEALTH_MAX_TOKENS", "5000")
    monkeypatch.setenv("MY_HEALTH_DATA_FILE", "user.json")

    with pytest.raises(ValidationError) as exc_info:
        Settings(_env_file=None)

    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0]["loc"] == ("max_tokens",)

def test_settings_without_data_file(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MY_HEALTH_MODEL_NAME", "gpt-3.5-turbo")
    monkeypatch.setenv("MY_HEALTH_MAX_TOKENS", "400")
    monkeypatch.delenv("MY_HEALTH_DATA_FILE", raising=False)

    with pytest.raises(ValidationError) as exc_info:
        Settings(_env_file=None)

    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0]["loc"] == ("data_file",)