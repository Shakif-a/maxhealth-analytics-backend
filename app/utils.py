import pandas as pd
import os
from datetime import datetime

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