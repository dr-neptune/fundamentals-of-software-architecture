import numpy as np
import pandas as pd
from celery import Celery

celery = Celery('tasks', broker='redis://localhost:6379', backend='redis://localhost:6379')

@celery.task(name='process_task')
def process_task():
    # Generate fake data
    data = pd.DataFrame(np.random.rand(100, 3), columns=['A', 'B', 'C'])

    # Perform some simple processing
    processed_data = data.mean()

    # Return the result
    return processed_data.to_dict()
