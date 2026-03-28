import json
import csv
import pandas as pd
from pathlib import Path
from Utils.Logger import logger


class DataReader:
    """
    DataReader:
    This class reads test data from JSON, CSV, and Excel files.
    It returns the data in a clean list-of-dictionaries format.

    Example output:
    [
        {"username": "Admin", "password": "admin123"},
        {"username": "User1", "password": "pass1"}
    ]
    """

    def __init__(self, file_path: str):
        """
        Why:
        - Store file path for reading later.

        What happens:
        - Convert given string path into Path object.
        """
        self.file_path = Path(file_path)

        if not self.file_path.exists():
            raise FileNotFoundError(f"Test data file not found: {self.file_path}")

        logger.info(f"DataReader initialized for file: {self.file_path}")

    @classmethod
    def merge_data_files(cls, *relative_paths: str) -> list:
        """
        Why:
        - Many tests want JSON + CSV + (optionally) Excel in one list.
        - Excel files are often omitted from Git/Jenkins; missing .xlsx must not crash collection.

        What happens:
        - For each path: if the file exists, read it with DataReader and extend a combined list.
        - If missing, log a warning and skip (so pytest --collect-only works everywhere).
        """
        combined: list = []
        for rel in relative_paths:
            path = Path(rel)
            if not path.is_file():
                logger.warning("Optional test data file missing, skipping: %s", path)
                continue
            combined.extend(cls(str(path)).get_data())
        return combined

    # -------------------------------------------------------
    # MAIN FUNCTION: AUTO-DETECT FILE TYPE
    # -------------------------------------------------------
    def get_data(self) -> list:
        """
        Why:
        - Decide which function to call based on file extension.

        What happens:
        - If .json → read JSON
        - If .csv → read CSV
        - If .xlsx → read Excel
        """
        ext = self.file_path.suffix.lower()

        if ext == ".json":
            return self._read_json()
        elif ext == ".csv":
            return self._read_csv()
        elif ext in [".xls", ".xlsx"]:
            return self._read_excel()
        else:
            raise ValueError(f"Unsupported file format: {ext}")

    # -------------------------------------------------------
    # READ JSON FILE
    # -------------------------------------------------------
    def _read_json(self) -> list:
        """
        Why:
        - JSON is commonly used for test data.

        What happens:
        - Open JSON
        - Convert to Python list
        - Return list
        """
        logger.info(f"Reading JSON test data: {self.file_path}")

        with self.file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("JSON test data must be a list of dictionaries")

        return data

    # -------------------------------------------------------
    # READ CSV FILE
    # -------------------------------------------------------
    def _read_csv(self) -> list:
        """
        Why:
        - CSV files are small and easy to handle.

        What happens:
        - Read CSV using csv.DictReader
        - Convert rows into dictionaries
        """
        logger.info(f"Reading CSV test data: {self.file_path}")

        rows = []

        with self.file_path.open("r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                rows.append(row)

        return rows

    # -------------------------------------------------------
    # READ EXCEL FILE (XLSX)
    # -------------------------------------------------------
    def _read_excel(self) -> list:
        """
        Why:
        - Excel is widely used in companies.
        - Pandas makes Excel reading very easy.

        What happens:
        - Read Excel into DataFrame
        - Convert DataFrame into list of dictionaries
        """
        logger.info(f"Reading Excel test data: {self.file_path}")

        df = pd.read_excel(self.file_path)

        # Convert DataFrame → List of dicts
        return df.to_dict(orient="records")

    # -------------------------------------------------------
    # GET DATA AS DATAFRAME (USEFUL FOR ADVANCED USERS)
    # -------------------------------------------------------
    def get_dataframe(self) -> pd.DataFrame:
        """
        Why:
        - Sometimes we want raw DataFrame for filtering or advanced logic.

        What happens:
        - Read file based on extension
        - Always return pandas DataFrame
        """
        ext = self.file_path.suffix.lower()
        logger.info(f"Reading test data as DataFrame: {self.file_path}")

        if ext == ".json":
            return pd.DataFrame(self._read_json())
        elif ext == ".csv":
            return pd.read_csv(self.file_path)
        elif ext in [".xls", ".xlsx"]:
            return pd.read_excel(self.file_path)
        else:
            raise ValueError(f"Unsupported file format for DataFrame: {ext}")