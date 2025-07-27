from pydantic import BaseModel

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