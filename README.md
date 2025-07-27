# MaxHealth Analytics Backend

A FastAPI backend for fetching, storing, processing, and serving jokes, with CSV and MongoDB integration.

## Features

- **Fetch Jokes:** Pulls random jokes from an external API and saves them to CSV.
- **Process Jokes:** Imports jokes from CSV files, processes them, and stores them in MongoDB.
- **REST API:** Endpoints to fetch, import, list, and retrieve jokes.
- **Asynchronous:** Fully async using FastAPI, Motor (MongoDB), and httpx.

## API Endpoints

- `POST /jokes/trigger-fetch`  
  Fetch a random joke from an external API and store it in a CSV file.

- `POST /jokes/trigger-import?date=YYYY-MM-DD`  
  Import jokes from a specific CSV (or all CSVs if no date is given) into MongoDB.

- `GET /jokes/csv-files`  
  List all available CSV files.

- `GET /jokes/`  
  Retrieve all processed jokes from MongoDB.

- `GET /jokes/{joke_id}`  
  Retrieve a specific joke by its ID.

## Data Models

- **Joke:**  
  `id`, `type`, `setup`, `punchline`
- **ProcessedJoke:**  
  Inherits from Joke, adds `processed_value`

## Tech Stack

- FastAPI
- Uvicorn
- Motor (Async MongoDB)
- Pandas
- httpx

## Setup

1. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

2. **Start MongoDB:**  
   Ensure MongoDB is running locally at `mongodb://localhost:27017`.

3. **Run the server:**
   ```
   uvicorn app.main:app --reload
   ```

4. **Access the API docs:**  
   Visit [http://localhost:8000/docs](http://localhost:8000/docs)

## Project Structure

- `app/main.py` – FastAPI app entrypoint
- `app/routers/jokes.py` – API endpoints
- `app/services.py` – Joke fetching and storage logic
- `app/tasks.py` – CSV import and processing
- `app/utils.py` – CSV utilities
- `app/database.py` – MongoDB connection 