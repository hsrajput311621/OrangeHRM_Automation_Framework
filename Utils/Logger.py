import logging
import os
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