import os
import tomllib
from pathlib import Path


def get_base_dir() -> Path:
    return Path(
        os.path.expanduser(os.getenv("ORESHIC_RECORDS_DIR") or "./records")
    )


def get_records_dir() -> Path:
    return Path(os.path.expanduser("./records"))


def get_command_dir() -> Path:
    return get_base_dir() / "commands"


def get_track_dir() -> Path:
    return get_base_dir() / "tracks"


def get_writeups_dir() -> Path:
    return get_base_dir() / "writeups"


def get_auto_interactive() -> []:
    with open("config.toml", "rb") as f:
        conf = tomllib.load(f)

    return conf.get("auto_interactive", [])
