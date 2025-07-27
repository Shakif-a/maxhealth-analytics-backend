# app/services.py
# This file contains the functions for fetching data from the external APIs

import httpx
import logging
from .utils import save_joke_to_csv, save_cognito_csv
import os
from dotenv import load_dotenv
import glob
from .database import get_cognito_db
import pandas as pd

EXTERNAL_API = "https://official-joke-api.appspot.com/random_joke"
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

COGNITO_URL = os.getenv("COGNITO_URL")

# Parameters for Cognito API
REPORT_NO = "r1"
CARE_UNIT_ID = "cram33B"
ST_TIME = "2024-11-01"
END_TIME = "2025-01-31"
TIMEZONE = "10"

async def fetch_joke() -> dict:
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(EXTERNAL_API)
            response.raise_for_status()
            return response.json()
    except (httpx.HTTPError, httpx.TimeoutException) as e:
        logger.error(f"API fetch error: {e}")
        return {}

async def fetch_and_store_joke() -> str:
    joke = await fetch_joke()
    if joke:
        filename = save_joke_to_csv(joke)
        return filename
    return ""

async def fetch_cognito_data(reportNo, careUnitId, stTime, endTime, timezone):
    url = f"{COGNITO_URL}/{reportNo}/{careUnitId}/{stTime}/{endTime}/{timezone}"
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url)
        if response.status_code == 200 and response.text.strip():
            print("Data successfully fetched from Cognito API.")
            filename = save_cognito_csv(response.text, reportNo, careUnitId, stTime, endTime)
            print(f"Saved Cognito data to {filename}")
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
        print(f"Status code: {response.status_code}")

async def process_cognito_reports():
    db = get_cognito_db()
    settings_collection = db.settings
    response_time_collection = db.response_time

    # Get list of already imported files from settings
    settings_doc = await settings_collection.find_one({"_id": "imported_cognito_files"})
    imported_files = set(settings_doc.get("files", [])) if settings_doc else set()

    # Find all r1 and r2 files in csvs directory
    r1_files = glob.glob("csvs/r1*.csv")
    r2_files = glob.glob("csvs/r2*.csv")
    files_to_import = [f for f in r1_files + r2_files if os.path.basename(f) not in imported_files]

    imported_r1 = []
    imported_r2 = []
    imported_now = []
    for file_path in files_to_import:
        filename = os.path.basename(file_path)
        if filename.startswith("r1"):
            df = pd.read_csv(file_path)
            records = df.to_dict(orient='records')
            total = len(records)
            print(f"Importing {filename} with {total} rows...")
            BATCH_SIZE = 10000
            for i in range(0, total, BATCH_SIZE):
                batch = records[i:i+BATCH_SIZE]
                if batch:
                    await response_time_collection.insert_many(batch)
                if (i // BATCH_SIZE) % 1 == 0 and i > 0:
                    print(f"Imported {i}/{total} rows from {filename}...")
            print(f"Finished importing {filename} ({total} rows).")
            imported_r1.append(filename)
        elif filename.startswith("r2"):
            events_collection = db.events
            df = pd.read_csv(file_path)
            records = df.to_dict(orient='records')
            total = len(records)
            print(f"Importing {filename} with {total} rows...")
            BATCH_SIZE = 10000
            for i in range(0, total, BATCH_SIZE):
                batch = records[i:i+BATCH_SIZE]
                if batch:
                    await events_collection.insert_many(batch)
                if (i // BATCH_SIZE) % 1 == 0 and i > 0:
                    print(f"Imported {i}/{total} rows from {filename}...")
            print(f"Finished importing {filename} ({total} rows).")
            imported_r2.append(filename)
        imported_now.append(filename)
    # Update settings with newly imported files
    if imported_now:
        if settings_doc:
            await settings_collection.update_one({"_id": "imported_cognito_files"}, {"$addToSet": {"files": {"$each": imported_now}}})
        else:
            await settings_collection.insert_one({"_id": "imported_cognito_files", "files": imported_now})
    return {"imported_r1": imported_r1, "imported_r2": imported_r2, "skipped": list(imported_files)}