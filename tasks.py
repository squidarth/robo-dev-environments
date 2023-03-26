import os
from celery import Celery
from celery.utils.log import get_task_logger

from gpt4 import authenticate_openai

app = Celery('tasks', broker=os.getenv("CELERY_BROKER_URL"))
logger = get_task_logger(__name__)

authenticate_openai(os.environ['OPENAI_API_KEY'])

@app.task
def create_development_environment(github_repo_url, github_access_token, user_email):
    logger.info('Creating development environment')


    # Add a function to send an email
    return 'Development environment created'


@app.task
def add(x, y):
    logger.info(f'Adding {x} + {y}')
    return x + y