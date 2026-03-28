import json
import os
from pathlib import Path
from dotenv import load_dotenv

class ConfigError(Exception):
    """
    Custom error.
    We raise this when config.json or .env has missing or bad values.
    This helps us quickly understand what went wrong
    """

class ConfigLoader:
    """
    This class loads the config.json file and .env file.
    It Loads everything only ONE time when the projects starts.
    All test will use the same config.
    """

    def __init__(self, config_file: str = "Config/config.json"):
        #load environment variables first (.env)
        load_dotenv("Env/.env")

        # load the config.json
        self.config = self._load_config_file(config_file)

        #Validate important keys
        self._validate_required_keys()

        #load username/password form .env
        self.username = os.getenv("USERNAME")
        self.password = os.getenv("PASSWORD")

        if not self.username or not self.password:
            raise ConfigError("USERNAME or PASSWORD missing in .env file")

    # ---------------------------------------------------------
    # STEP 1: READ CONFIG.JSON FILE
    # ---------------------------------------------------------
    def _load_config_file(self, config_file: str) -> dict:
        """
            Why this step:
            - We must read config.json so the project knows:
              browser type, headless mode, waits, paths, reports, etc.

            What will happen:
            - Try to open config.json.
            - If file not found → ConfigError.
            - If JSON is broken → ConfigError.
            - If everything is good → return Python dictionary.
        """
        path = Path(config_file)
        if not path.is_file():
            raise ConfigError(f"Config file not found at : {path}")

        try:
            with path.open(encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError as exc:
            raise ConfigError(
                f"Invalid JSON format in config file: {exc.msg}"
                f"(line {exc.lineno}, column {exc.colno})"
            )

    # ---------------------------------------------------------
    # STEP 2: VALIDATE IMPORTANT KEYS IN CONFIG.JSON
    # ---------------------------------------------------------

    def _validate_required_keys(self):
        """
        Why this step:
        - We must make sure important keys exist in config.json.
        - If any important key is missing, the project will break later.
        - So, we fail fast and show a clear error message.

        What will happen:
        - Check if all keys exist.
        - If anything is missing → throw ConfigError.
        """

        required_sections = ["base_url", "browser", "timeouts", "paths"]

        for key in required_sections:
            if key not in self.config:
                raise ConfigError(f"Missing '{key}' in config.json")

        # Validate subkeys
        if "explicit_wait" not in self.config["timeouts"]:
            raise ConfigError("Missing 'explicit_wait' under timeouts section")

        if "screenshots" not in self.config["paths"]:
            raise ConfigError("Missing 'screenshots' under paths section")

    # ---------------------------------------------------------
    # STEP 3: GETTERS TO ACCESS CONFIG VALUES EASILY
    # ---------------------------------------------------------

    def get(self, key: str):
        """Simple helper to get any value from config.json."""
        return self.config.get(key)

    def get_timeout(self, key: str):
        """Get timeout values like explicit_wait, page_load_timeout."""
        return self.config["timeouts"].get(key)

    def get_path(self, key: str):
        """Get folder paths like screenshots, reports, logs."""
        return self.config["paths"].get(key)

