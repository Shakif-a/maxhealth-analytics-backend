from .database import get_cognito_db

CAREUNIT_DOC_ID = "careunitlist"

async def add_care_unit_id(care_unit_id: str):
    db = get_cognito_db()
    collection = db.settings
    doc = await collection.find_one({"_id": CAREUNIT_DOC_ID})
    if doc:
        if care_unit_id in doc.get("careUnitIds", []):
            return {"message": "careUnitId already exists."}
        await collection.update_one({"_id": CAREUNIT_DOC_ID}, {"$push": {"careUnitIds": care_unit_id}})
        return {"message": "careUnitId added."}
    else:
        await collection.insert_one({"_id": CAREUNIT_DOC_ID, "careUnitIds": [care_unit_id]})
        return {"message": "careUnitId added as first entry."}

async def get_all_care_unit_ids():
    db = get_cognito_db()
    collection = db.settings
    doc = await collection.find_one({"_id": CAREUNIT_DOC_ID})
    if doc:
        return doc.get("careUnitIds", [])
    return []
