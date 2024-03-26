from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from celery.result import AsyncResult
from celery_app import celery
from sklearn.datasets import fetch_openml

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:5173",  # Update with your React app's URL if different
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/get_columns')
async def get_columns(request: Request):
    data = await request.json()
    dataset = data.get('dataset')

    match dataset:
        case 'california_housing':
            result = celery.send_task('get_dataset_columns', args=[dataset])
            columns = result.get()
        case 'ames_housing':
            data = fetch_openml(name="house_prices", as_frame=True)
            columns = data.frame.columns.tolist()
        case _:
            columns = []

    return columns

@app.post('/process/fast')
async def process_fast_data(request: Request):
    data = await request.json()
    dataset = data.get('dataset', 'california_housing')
    result = celery.send_task('process_fast_task', args=[dataset])
    processed_data = result.get()
    return processed_data

@app.post('/process/slow')
async def process_slow_data(request: Request):
    data = await request.json()
    dataset = data.get('dataset', 'california_housing')
    result = celery.send_task('process_slow_task', args=[dataset])
    processed_data = result.get()
    return processed_data


@app.post('/process/parallel')
async def process_parallel_data(request: Request):
    data = await request.json()
    dataset = data.get('dataset', 'california_housing')
    result = celery.send_task('parallel_processing_task', args=[dataset])
    return {'task_id': result.id}

@app.get('/process/parallel/{task_id}')
async def get_parallel_result(task_id: str):
    async_result = AsyncResult(task_id)
    if async_result.ready():
        return async_result.get()
    else:
        return {'status': 'PENDING'}


@app.post('/fit_models/parallel')
async def fit_models_parallel(request: Request):
    data = await request.json()
    dataset = data.get('dataset', 'california_housing')
    target_column = data.get('target_column', '')
    num_models = data.get('num_models', 5)
    result = celery.send_task('parallel_fit_models_task', args=[dataset, target_column, num_models])
    model_results = result.get()
    return model_results


@app.get('/fit_models/parallel/{task_id}')
async def get_parallel_fit_result(task_id: str):
    async_result = AsyncResult(task_id)
    if async_result.ready():
        return async_result.get()
    else:
        return {'status': 'PENDING'}
