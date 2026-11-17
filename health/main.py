import sys

from pydantic import ValidationError

from health.settings import Settings
from health.storage import load_user

if __name__ == "__main__":
    try:
        settings = Settings()
    except ValidationError as e:
        print("Configuration error:")
        for error in e.errors():
            env_name = f"MY_HEALTH_{error['loc'][0].upper()}"
            print(f"  {env_name}: {error['msg']}")
        sys.exit(1)

    try:
        user = load_user(settings.data_file)
    except ValidationError as e:
        print(f"Invalid data in {settings.data_file}:")
        for error in e.errors():
            where = ".".join(str(part) for part in error["loc"])
            print(f"  {where}: {error['msg']}")
        sys.exit(1)

    print(f"Name: {user.name}")
    print(f"Count Measurements: {len(user.measurements)}")