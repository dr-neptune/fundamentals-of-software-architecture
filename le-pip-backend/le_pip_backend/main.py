from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from celery_app import celery

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:3000",  # Update with your React app's URL if different
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/process/fast')
async def process_fast_data():
    result = celery.send_task('process_fast_task')
    processed_data = result.get()
    return processed_data

@app.post('/process/slow')
async def process_slow_data():
    result = celery.send_task('process_slow_task')
    processed_data = result.get()
    return processed_data
