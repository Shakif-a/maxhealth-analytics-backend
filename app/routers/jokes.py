from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends, Query
from motor.motor_asyncio import AsyncIOMotorDatabase
from ..services import fetch_and_store_joke
from ..tasks import import_csv_to_mongodb
from ..dependencies import get_database
import os
import glob

router = APIRouter()

@router.post("/trigger-fetch")
async def trigger_fetch(
    background_tasks: BackgroundTasks,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    filename = await fetch_and_store_joke()
    return {
        "status": "Joke fetched and stored in CSV",
        "filename": filename,
        "message": "Use /trigger-import to process CSVs"
    }

@router.post("/trigger-import")
async def trigger_import(
    background_tasks: BackgroundTasks,
    db: AsyncIOMotorDatabase = Depends(get_database),
    date: str = Query(None, description="Date in YYYY-MM-DD format")
):
    if date:
        filename = f"{date}.csv"
        background_tasks.add_task(import_csv_to_mongodb, db, filename)
        return {"status": f"Import started for {filename}"}
    
    # Import all CSVs if no date specified
    csv_files = glob.glob("csvs/*.csv")
    for filepath in csv_files:
        filename = os.path.basename(filepath)
        background_tasks.add_task(import_csv_to_mongodb, db, filename)
    
    return {"status": "Import started for all CSV files"}

@router.get("/csv-files")
async def list_csv_files():
    csv_files = glob.glob("csvs/*.csv")
    return {
        "files": [os.path.basename(f) for f in csv_files],
        "count": len(csv_files)
    }

@router.get("/")
async def get_all_jokes(db: AsyncIOMotorDatabase = Depends(get_database)):
    jokes = await db.processed_jokes.find({}, {"_id": 0}).to_list(1000)
    return jokes

@router.get("/{joke_id}")
async def get_joke(joke_id: int, db: AsyncIOMotorDatabase = Depends(get_database)):
    joke = await db.processed_jokes.find_one({"id": joke_id}, {"_id": 0})
    if not joke:
        raise HTTPException(status_code=404, detail="Joke not found")
    return joke