"""
ConfigLoader — single place for settings (config.json + Env/.env).

Why this exists:
- Tests and pages should not hard-code URLs, timeouts, or secrets.
- One load at session start = faster and consistent behaviour in Jenkins/local.

Step-by-step:
1) Resolve project root from this file's location (works even if pytest is started
   from another working directory — a common Jenkins mistake).
2) Load Env/.env into os.environ (for secrets).
3) Parse Config/config.json for URLs, timeouts, paths.
4) Read ORANGEHRM_USERNAME / ORANGEHRM_PASSWORD from the environment.

Important (Windows): Never use the variable name USERNAME in .env for the app user.
Windows already sets USERNAME to your OS login, so python-dotenv would not override it
and your tests would log in with the wrong "username".
"""
import json
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


class ConfigError(Exception):
    """Raised when config.json or .env is missing required values."""


class ConfigLoader:
    """
    Loads `Config/config.json` once and exposes simple getters for tests/pages.
    """

    def __init__(self, config_file: Optional[str] = None):
        # Project root = parent of the Core/ package (…/opensource-demo.orangehrmlive.com).
        self._root = Path(__file__).resolve().parent.parent

        env_path = self._root / "Env" / ".env"
        # load_dotenv: reads KEY=value lines into os.environ for this process.
        load_dotenv(env_path)

        cfg_path = (
            Path(config_file)
            if config_file
            else self._root / "Config" / "config.json"
        )
        if not cfg_path.is_absolute():
            cfg_path = self._root / cfg_path

        self.config = self._load_config_file(cfg_path)
        self._validate_required_keys()

        # Demo app credentials — use names that do not clash with Windows USERNAME.
        self.username = os.getenv("ORANGEHRM_USERNAME")
        self.password = os.getenv("ORANGEHRM_PASSWORD")

        if not self.username or not self.password:
            raise ConfigError(
                "Missing ORANGEHRM_USERNAME or ORANGEHRM_PASSWORD in Env/.env. "
                "On Windows, do not use USERNAME — it is reserved by the OS."
            )

    def _load_config_file(self, path: Path) -> dict:
        """
        Why: Central JSON load with clear errors if the file is missing or invalid.

        What happens: read UTF-8 text → json.load → Python dict.
        """
        if not path.is_file():
            raise ConfigError(f"Config file not found: {path}")

        try:
            with path.open(encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError as exc:
            raise ConfigError(
                f"Invalid JSON in config file: {exc.msg} (line {exc.lineno}, column {exc.colno})"
            ) from exc

    def _validate_required_keys(self):
        """
        Why: Fail fast at startup instead of mid-test with a vague KeyError.

        What happens: ensure top-level sections and important timeout keys exist.
        """
        required_sections = ["base_url", "browser", "timeouts", "paths"]
        for key in required_sections:
            if key not in self.config:
                raise ConfigError(f"Missing '{key}' in config.json")

        timeouts = self.config["timeouts"]
        for tkey in ("implicit_wait", "explicit_wait", "page_load_timeout"):
            if tkey not in timeouts:
                raise ConfigError(f"Missing 'timeouts.{tkey}' in config.json")

        if "screenshots" not in self.config["paths"]:
            raise ConfigError("Missing 'paths.screenshots' in config.json")

    def get(self, key: str):
        """Return a value from config.json (top-level key)."""
        return self.config.get(key)

    def get_timeout(self, key: str):
        """Return a numeric timeout from the `timeouts` section (or None if absent)."""
        return self.config["timeouts"].get(key)

    def get_path(self, key: str):
        """Return a folder path string from `paths` (e.g. screenshots, logs)."""
        return self.config["paths"].get(key)
