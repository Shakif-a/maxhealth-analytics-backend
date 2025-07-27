from pydantic import BaseModel

class Joke(BaseModel):
    id: int
    type: str
    setup: str
    punchline: str

class ProcessedJoke(Joke):
    processed_value: str