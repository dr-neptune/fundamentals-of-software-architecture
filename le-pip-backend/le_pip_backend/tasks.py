import time
import numpy as np
import pandas as pd
from celery import group
from celery_app import celery
from sklearn.datasets import fetch_california_housing
from sklearn.datasets import fetch_openml
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


@celery.task(name='process_fast_task')
def process_fast_task(dataset):
    match dataset:
        case 'california_housing':
            data = fetch_california_housing(as_frame=True)
            result = data.frame.describe().to_dict()
        case 'ames_housing':
            data = fetch_openml(name="house_prices", as_frame=True)
            result = data.frame.describe().to_dict()
        case _:
            result = {'error': 'Invalid dataset selected'}
    return result

@celery.task(name='process_slow_task')
def process_slow_task(dataset):
    match dataset:
        case 'california_housing':
            data = fetch_california_housing(as_frame=True)
            time.sleep(5)  # Simulating a slow task by sleeping for 5 seconds
            result = data.frame.describe().to_dict()
        case 'ames_housing':
            data = fetch_openml(name="house_prices", as_frame=True)
            time.sleep(5)  # Simulating a slow task by sleeping for 5 seconds
            result = data.frame.describe().to_dict()
        case _:
            result = {'error': 'Invalid dataset selected'}
    return result


@celery.task(name='get_dataset_columns')
def get_dataset_columns(dataset):
    match dataset:
        case 'california_housing':
            data = fetch_california_housing(as_frame=True)
            columns = data.frame.columns.tolist()
        case 'ames_housing':
            data = fetch_openml(name="house_prices", as_frame=True)
            columns = data.frame.columns.tolist()
        case _:
            columns = []
    return columns


@celery.task(name='fit_linear_regression_task')
def fit_linear_regression_task(dataset, target_column):
    match dataset:
        case 'california_housing':
            data = fetch_california_housing(as_frame=True)
        case 'ames_housing':
            data = fetch_openml(name="house_prices", as_frame=True)
        case _:
            return {'error': 'Invalid dataset selected'}

    if target_column not in data.frame.columns:
        return {'error': 'Invalid target column selected'}

    if not pd.api.types.is_numeric_dtype(data.frame[target_column]):
        return {'error': 'Target column must be numeric'}

    X = data.frame.drop(columns=[target_column])
    y = data.frame[target_column]

    numeric_columns = X.select_dtypes(include=[np.number]).columns
    X = X[numeric_columns]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)

    # Create a dictionary of column names and their corresponding coefficients
    coefficients = dict(zip(X.columns, model.coef_))
    intercept = model.intercept_

    result = {
        'train_score': train_score,
        'test_score': test_score,
        'coefficients': coefficients,
        'intercept': intercept
    }
    return result

@celery.task(name='parallel_processing_task')
def parallel_processing_task(dataset):
    # Define the number of parallel tasks to run
    num_tasks = 5

    # Create a group of tasks to be executed in parallel
    task_group = group([process_data_task.s(dataset) for _ in range(num_tasks)])

    # Execute the tasks in parallel and return the async result
    async_result = task_group.apply_async()

    return async_result.id  # Return the async result ID

@celery.task(name='process_data_task')
def process_data_task(dataset):
    match dataset:
        case 'california_housing':
            data = fetch_california_housing(as_frame=True)
            time.sleep(2)  # Simulating processing time
            result = data.frame.describe().to_dict()
        case 'ames_housing':
            data = fetch_openml(name="house_prices", as_frame=True)
            time.sleep(2)  # Simulating processing time
            result = data.frame.describe().to_dict()
        case _:
            result = {'error': 'Invalid dataset selected'}
    return result
