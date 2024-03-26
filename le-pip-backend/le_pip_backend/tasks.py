import time
import numpy as np
import pandas as pd
from celery_app import celery

@celery.task(name='process_fast_task')
def process_fast_task():
    # Generate fake data
    data = pd.DataFrame(np.random.rand(100, 3), columns=['A', 'B', 'C'])

    # Perform some simple processing
    processed_data = data.mean()

    # Return the result
    return processed_data.to_dict()

@celery.task(name='process_slow_task')
def process_slow_task():
    # Generate fake data
    data = pd.DataFrame(np.random.rand(1000, 3), columns=['A', 'B', 'C'])

    # Perform some time-consuming processing
    time.sleep(5)  # Simulating a slow task by sleeping for 5 seconds
    processed_data = data.mean()

    # Return the result
    return processed_data.to_dict()
