import pandas as pd
import os
import asyncio
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging

logger = logging.getLogger(__name__)

async def import_csv_to_mongodb(db: AsyncIOMotorDatabase, filename: str):
    try:
        filepath = f"csvs/{filename}"
        if not os.path.exists(filepath):
            logger.error(f"File not found: {filepath}")
            return 0
        
        df = pd.read_csv(filepath)
        records = df.to_dict(orient='records')
        
        # Add processing to each record
        processed_records = []
        for record in records:
            # Add your custom processing here
            record["processed_value"] = f"PROCESSED: {record['setup']} -> {record['punchline']}"
            record["import_timestamp"] = datetime.utcnow().isoformat()
            processed_records.append(record)
        
        # Insert into MongoDB
        if processed_records:
            result = await db.processed_jokes.insert_many(processed_records)
            return len(result.inserted_ids)
        
        return 0
    except Exception as e:
        logger.error(f"Import error: {e}")
        return 0