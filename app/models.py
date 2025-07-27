from pydantic import BaseModel
from typing import Dict
from pydantic import Field, validator
from datetime import datetime

class Joke(BaseModel):
    id: int
    type: str
    setup: str
    punchline: str

class ProcessedJoke(Joke):
    processed_value: str

class CareUnitIdRequest(BaseModel):
    careUnitId: str

class CareUnitListResponse(BaseModel):
    careUnitIds: list[str]

class R2Event(BaseModel):
    CareUnitId: str
    CareUnit: str
    PatientSn: str
    MaskId: str
    BedNo: str
    BoxId: str
    EventCode: str
    Event: str
    EventTime: str
    EventUnixMilli: int

class ShiftTimes(BaseModel):
    day_start: str
    day_end: str
    afternoon_start: str
    afternoon_end: str
    night_start: str
    night_end: str

    @validator('*')
    def validate_datetime(cls, v):
        try:
            datetime.fromisoformat(v)
        except Exception:
            raise ValueError('All shift times must be valid ISO 8601 datetime strings')
        return v

class ShiftTimesRequest(BaseModel):
    care_unit_id: str = Field(..., description="Unique ID of the care unit or site.")
    shift_times: ShiftTimes

class ShiftTimesResponse(BaseModel):
    care_unit_id: str
    shift_times: ShiftTimes