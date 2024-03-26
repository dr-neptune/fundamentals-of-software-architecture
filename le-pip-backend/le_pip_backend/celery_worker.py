from celery_app import celery

# Import the tasks module to register the tasks
from tasks import *

if __name__ == '__main__':
    celery.worker_main()
