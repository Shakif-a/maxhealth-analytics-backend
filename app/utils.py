import pandas as pd
import os
from datetime import datetime
import csv

CSV_DIR = "csvs"

def save_joke_to_csv(joke: dict):
    os.makedirs(CSV_DIR, exist_ok=True)
    today = datetime.today().strftime("%Y-%m-%d")
    filename = f"{today}.csv"
    filepath = f"{CSV_DIR}/{filename}"
    
    # Create new CSV or append to existing
    if not os.path.exists(filepath):
        pd.DataFrame([joke]).to_csv(filepath, index=False)
    else:
        df = pd.read_csv(filepath)
        new_df = pd.DataFrame([joke])
        updated_df = pd.concat([df, new_df], ignore_index=True)
        updated_df.to_csv(filepath, index=False)
    
    return filename

def save_cognito_csv(data, report_no, care_unit_id, st_time, end_time):
    """
    Save Cognito API CSV data to a file with a specific naming convention.
    data: CSV string or list of dicts
    """
    os.makedirs(CSV_DIR, exist_ok=True)
    filename = f"{report_no}_{care_unit_id}_{st_time}_{end_time}.csv"
    filepath = f"{CSV_DIR}/{filename}"
    if isinstance(data, str):
        # Assume CSV string
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            f.write(data)
    elif isinstance(data, list):
        # Assume list of dicts
        if data:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
    return filename

def get_cognito_csv_files():
    """
    Returns a list of all r1 and r2 CSV filenames in the csvs directory.
    """
    r1_files = [f for f in os.listdir(CSV_DIR) if f.startswith("r1") and f.endswith(".csv")]
    r2_files = [f for f in os.listdir(CSV_DIR) if f.startswith("r2") and f.endswith(".csv")]
    return r1_files + r2_files

def get_r2_csv_header():
    """
    Returns the expected header for r2 CSV files as a list of column names.
    """
    return [
        "CareUnitId","CareUnit","PatientSn","MaskId","BedNo","BoxId","EventCode","Event","EventTime","EventUnixMilli"
    ]