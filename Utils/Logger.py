"""
Logging setup for the whole framework.

Why logging instead of only print():
- Pytest and Jenkins capture stdout, but files like Logs/automation.log survive after the run.
- You can set levels (DEBUG in file, INFO on console) without changing test code.

What happens when this module is imported:
1) Ensure Logs/ exists (mkdir once).
2) Create one named logger "OrangeHRM_Automation".
3) Attach three handlers: console (INFO+), automation.log (DEBUG+), error.log (ERROR+).
4) Other modules do `from Utils.Logger import logger` and call logger.info(...).
"""
import logging
from pathlib import Path


# -------------------------------------------------------------
# CREATE LOG DIRECTORY IF NOT EXISTS
# -------------------------------------------------------------
log_folder = Path("Logs")
log_folder.mkdir(exist_ok=True)


# -------------------------------------------------------------
# LOG FILE PATHS
# -------------------------------------------------------------
automation_log_file = log_folder / "automation.log"
error_log_file = log_folder / "error.log"


# -------------------------------------------------------------
# CREATE LOGGER
# -------------------------------------------------------------
logger = logging.getLogger("OrangeHRM_Automation")
logger.setLevel(logging.DEBUG)   # You selected DEBUG


# -------------------------------------------------------------
# FORMATTER
# -------------------------------------------------------------
# Why this:
# It creates a clean log format like:
# 2026-03-27 12:30:10 - INFO - Clicking login button
#
log_format = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


# -------------------------------------------------------------
# 1) CONSOLE HANDLER (prints logs to terminal)
# -------------------------------------------------------------
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # console: show only INFO+
console_handler.setFormatter(log_format)


# -------------------------------------------------------------
# 2) FILE HANDLER (automation.log - ALL logs)
# -------------------------------------------------------------
file_handler = logging.FileHandler(automation_log_file, mode="a")
file_handler.setLevel(logging.DEBUG)  # log EVERYTHING to file
file_handler.setFormatter(log_format)


# -------------------------------------------------------------
# 3) ERROR FILE HANDLER (error.log - ONLY ERRORS)
# -------------------------------------------------------------
error_handler = logging.FileHandler(error_log_file, mode="a")
error_handler.setLevel(logging.ERROR)  # only errors go here
error_handler.setFormatter(log_format)


# -------------------------------------------------------------
# ADD HANDLERS TO LOGGER
# -------------------------------------------------------------
logger.addHandler(console_handler)
logger.addHandler(file_handler)
logger.addHandler(error_handler)