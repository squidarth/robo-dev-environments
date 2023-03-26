import os
from celery import Celery
from celery.utils.log import get_task_logger
from gh_client_clean import create_codespace_with_files, docker_file, devcontainer_json, sample_script


from gpt import authenticate_openai, get_code_block_openai

app = Celery('tasks', broker=os.getenv("CELERY_BROKER_URL"))
logger = get_task_logger(__name__)

authenticate_openai(os.environ['OPENAI_API_KEY'])

postmark_api_key = os.environ["POSTMARK_API_KEY"]
#client = postmark.Client(api_token=postmark_api_key)

#def send_postmark_email(email, github_url):
#    message = postmark.Message(
#        sender='sender@example.com',
#        to=email,
#        subject='Your development environment is ready!',
#        text_body=f"Your codespace is ready! You can access it here: {github_url}"
#    )
#
#    client.send(message)

@app.task
def create_development_environment(github_repo_url, github_access_token, user_email):
    logger.info('Creating development environment')

    # Get dockerfile
#    prompt_dockerfile = f'''
#        Here is the repo url: {github_repo_url}.
#        Based on contents of its README, generate a docker file with the library in that repo installed
#        '''
#    dockerfile_string = get_code_block_openai(prompt_dockerfile)
#
#    # Get devcontainer.json
#    prompt_devcontainer = f'''
#        Based on what you know about dev containers, here are some reference pages
#        https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/introduction-to-dev-containers
#        https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/setting-up-your-python-project-for-codespaces.
#        Generate a devcontainer.json that uses the dockerfile you just generated
#        '''
#    devcontainer_string = get_code_block_openai(prompt_devcontainer)
#
#    # Get sample script
#    prompt_sample_script = f'''
#        Using the repo you are working with, generate a cool python script that can be run inside the docker container you first generated using files accessible on the internet. 
#        '''
#    sample_script_string = get_code_block_openai(prompt_sample_script)

    # Folk a repo and create codespace on top of that
    import ipdb
    ipdb.set_trace()

#    print(sample_script_string)

    # Add a function to send an email
    create_codespace_with_files("squidarth", github_access_token, github_repo_url, docker_file, devcontainer_json, sample_script)
    return 'Development environment created'


@app.task
def add(x, y):
    logger.info(f'Adding {x} + {y}')
    return x + y