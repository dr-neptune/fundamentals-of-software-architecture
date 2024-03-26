from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from celery import Celery

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

celery = Celery('tasks', broker='redis://localhost:6379', backend='redis://localhost:6379')

@app.post('/process')
async def process_data():
    result = celery.send_task('process_task')
    processed_data = result.get()  # Wait for the task to complete and retrieve the result
    return processed_data
