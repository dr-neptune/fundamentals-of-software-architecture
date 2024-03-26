import time
import numpy as np
import pandas as pd
from celery_app import celery
from sklearn.datasets import load_iris

@celery.task(name='process_fast_task')
def process_fast_task(dataset):
    if dataset == 'penguins':
        data = pd.read_csv('https://github.com/allisonhorst/palmerpenguins/raw/5b5891f01b52ae26ad8cb9755ec93672f49328a8/data/penguins_size.csv')
        result = data.describe().to_dict()
    elif dataset == 'iris':
        data = load_iris(as_frame=True)['data']
        result = data.mean().to_dict()
    elif dataset == 'titanic':
        data = pd.read_csv('https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv')
        result = data.describe().to_dict()
    else:
        result = {'error': 'Invalid dataset selected'}
    return result

@celery.task(name='process_slow_task')
def process_slow_task(dataset):
    if dataset == 'penguins':
        data = pd.read_csv('https://github.com/allisonhorst/palmerpenguins/raw/5b5891f01b52ae26ad8cb9755ec93672f49328a8/data/penguins_size.csv')
        time.sleep(5)  # Simulating a slow task by sleeping for 5 seconds
        result = data.describe().to_dict()
    elif dataset == 'iris':
        data = load_iris(as_frame=True)['data']
        time.sleep(5)  # Simulating a slow task by sleeping for 5 seconds
        result = data.mean().to_dict()
    elif dataset == 'titanic':
        data = pd.read_csv('https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv')
        time.sleep(5)  # Simulating a slow task by sleeping for 5 seconds
        result = data.describe().to_dict()
    else:
        result = {'error': 'Invalid dataset selected'}
    return result
