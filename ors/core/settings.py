import os
import tomllib
from pathlib import Path


def _load_config() -> dict:
    """Load config.toml if present, otherwise return an empty dict."""
    try:
        with open("config.toml", "rb") as f:
            return tomllib.load(f)
    except FileNotFoundError:
        return {}


def get_base_dir() -> Path:
    return Path(
        os.path.expanduser(os.getenv("ORESHIC_RECORD_DIR"))
    )


def get_records_dir() -> Path:
    return get_base_dir() / "records"


def get_command_dir() -> Path:
    return get_records_dir() / "commands"


def get_track_dir() -> Path:
    return get_records_dir() / "tracks"


def get_track_name_file() -> Path:
    return "/tmp/oreshic_records_track_name"


def get_writeups_dir() -> Path:
    return get_records_dir() / "writeups"


def get_auto_interactive() -> []:
    conf = _load_config()
    return conf.get("auto_interactive", [])
