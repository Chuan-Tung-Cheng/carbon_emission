import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
CSV_DIR = os.getenv("CSV_DIR")

def find_csv_file_dir():
    """return generator of csv file path"""
    parent_dir = Path(CSV_DIR)
    try:
        csv_file_list = parent_dir.glob("*.csv")
        return csv_file_list
    except FileNotFoundError as e:
        print(f"{parent_dir} does not have any csv files")

if __name__ == "__main__":
    csv = find_csv_file_dir()
    for csv_file in csv:
        print(csv_file)