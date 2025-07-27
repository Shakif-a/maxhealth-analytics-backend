from fastapi import APIRouter, Query, Body
from ..services import fetch_cognito_data, CARE_UNIT_ID, TIMEZONE, process_cognito_reports, save_shift_times, get_shift_times
from ..models import CareUnitIdRequest, CareUnitListResponse, ShiftTimesRequest, ShiftTimesResponse
from ..controller import add_care_unit_id, get_all_care_unit_ids
from fastapi import HTTPException, status

router = APIRouter()

@router.post("/fetch")
async def fetch_cognito(
    reportNo: str = Query(..., description="Report number"),
    stTime: str = Query(..., description="Start time in YYYY-MM-DD format"),
    endTime: str = Query(..., description="End time in YYYY-MM-DD format")
):
    await fetch_cognito_data(reportNo, CARE_UNIT_ID, stTime, endTime, TIMEZONE)
    return {"status": "Cognito data fetch triggered", "reportNo": reportNo, "careUnitId": CARE_UNIT_ID, "stTime": stTime, "endTime": endTime, "timezone": TIMEZONE}

@router.post("/careunit")
async def add_careunit_endpoint(request: CareUnitIdRequest):
    result = await add_care_unit_id(request.careUnitId)
    return result

@router.get("/careunit", response_model=CareUnitListResponse)
async def get_careunit_endpoint():
    care_unit_ids = await get_all_care_unit_ids()
    return {"careUnitIds": care_unit_ids}

@router.post("/process_reports")
async def process_cognito_reports_endpoint():
    """
    Scan the csvs directory for r1 and r2 files, import r1 files into db.cognito.response_time, and r2 files into db.cognito.events. Tracks imported files to avoid duplicates.
    """
    result = await process_cognito_reports()
    return result

@router.post("/api/shift-times", response_model=None)
async def store_shift_times(request: ShiftTimesRequest):
    """
    Saves shift times for a given care unit.
    """
    try:
        return await save_shift_times(request)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Server/database failure.")

@router.get("/api/shift-times/{care_unit_id}", response_model=ShiftTimesResponse)
async def get_shift_times_endpoint(care_unit_id: str):
    """
    Fetches existing shift times for the selected care unit.
    """
    try:
        result = await get_shift_times(care_unit_id)
        return result
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Database read failure.")
