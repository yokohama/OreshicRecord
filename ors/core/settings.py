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


def get_github_user() -> str:
    """Return the GitHub user name for records/<user>/... paths.

    Priority:
    1. Environment variable ORESHIC_RECORD_GITHUB_USER
    2. config.toml: github_user
    3. config.toml: [user].github

    If none is configured, raise an explicit error so that the user
    notices the misconfiguration instead of silently writing to an
    unexpected location.
    """

    env_user = os.getenv("ORESHIC_RECORD_GITHUB_USER")
    if env_user:
        return env_user

    conf = _load_config()

    github_user = conf.get("github_user")
    if isinstance(github_user, str) and github_user:
        return github_user

    user_section = conf.get("user")
    if isinstance(user_section, dict):
        github = user_section.get("github")
        if isinstance(github, str) and github:
            return github

    raise RuntimeError(
        "GitHub user is not configured. Set ORESHIC_RECORD_GITHUB_USER "
        "or github_user / [user].github in config.toml."
    )


def get_base_dir() -> Path:
    return Path(
        os.path.expanduser(os.getenv("ORESHIC_RECORD_DIR"))
    )


def get_records_dir() -> Path:
    """Return records/<github-user> base directory."""
    return get_base_dir() / "records" / get_github_user()


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
