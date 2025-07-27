import httpx
import logging
from .utils import save_joke_to_csv

EXTERNAL_API = "https://official-joke-api.appspot.com/random_joke"
logger = logging.getLogger(__name__)

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