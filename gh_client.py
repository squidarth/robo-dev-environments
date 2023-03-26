from github import Github
import os
import base64

access_token = os.environ.get('GH_TOKEN')
# First create a Github instance:

# using an access token
def create_gh_client():
    return Github(access_token)

# Github Enterprise with custom hostname
#g = Github(base_url="https://{hostname}/api/v3", login_or_token="access_token")


# Then play with your Github objects:
def print_all_repos():
    for repo in g.get_user().get_repos():
        print(repo.name)


import requests

# Set your personal access token and the repository to fork
#access_token = 'YOUR_GITHUB_ACCESS_TOKEN'
#repo_owner = 'kkroening'


def fork_repo(repo_owner, repo_name):
    headers = {
        'Authorization': f'token {access_token}',
        'Accept': 'application/vnd.github+json'
    }

    api_base_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/forks'

    # Fork the repository
    response = requests.post(api_base_url, headers=headers)

    if response.status_code == 202:
        print("Repository forked successfully.")
        print(f"Forked repository URL: {response.json()['html_url']}")
    else:
        print("Error forking the repository.")
        print(f"Status code: {response.status_code}")
        print(f"Error message: {response.json()}")


repo_owner = 'sdk21'
repo_name = 'ffmpeg-python'

def create_branch_add_dev_container(repo_owner, repo_name, new_branch_name):
    import requests
    import json
    import base64

    # Set your personal access token, repository information, and new branch name

    headers = {
        'Authorization': f'token {access_token}',
        'Accept': 'application/vnd.github+json'
    }

    api_base_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}'

    # Get default branch and its commit SHA
    repo_info = requests.get(api_base_url, headers=headers).json()
    default_branch = repo_info['default_branch']
    default_branch_sha = requests.get(f'{api_base_url}/git/ref/heads/{default_branch}', headers=headers).json()['object']['sha']

    '''
    # Create new branch
    new_branch_ref = f'refs/heads/{new_branch_name}'
    requests.post(f'{api_base_url}/git/refs', headers=headers, json={
        'ref': new_branch_ref,
        'sha': default_branch_sha
    })
    '''
    # Create blobs for devcontainer.json and Dockerfile
    devcontainer_json_content = '''{
    "name": "ffmpeg-python-dev-container",
    "dockerFile": "Dockerfile",
    "settings": {
        "terminal.integrated.shell.linux": "/bin/bash"
    },
    "extensions": [
        "ms-python.python"
    ],
    "forwardPorts": [],
    "postCreateCommand": "echo 'Welcome to your ffmpeg-python dev container!'"
    }
    '''
    dockerfile_content = '''# Use the official Python base image
    FROM python:3.9-slim

    # Set the working directory
    WORKDIR /app

    # Install FFmpeg
    RUN apt-get update && \
        apt-get install -y --no-install-recommends ffmpeg && \
        rm -rf /var/lib/apt/lists/*

    # Clone the ffmpeg-python repository
    RUN apt-get update && \
        apt-get install -y --no-install-recommends git && \
        git clone https://github.com/kkroening/ffmpeg-python.git /app/ffmpeg-python && \
        rm -rf /var/lib/apt/lists/*

    # Install the required dependencies
    RUN pip install --no-cache-dir -r /app/ffmpeg-python/requirements.txt

    # Optional: Set the entrypoint for the container
    ENTRYPOINT ["python"]
    '''

    devcontainer_json_blob_sha = requests.post(f'{api_base_url}/git/blobs', headers=headers, json={
        'content': base64.b64encode(devcontainer_json_content.encode()).decode(),
        'encoding': 'base64'
    }).json()['sha']

    dockerfile_blob_sha = requests.post(f'{api_base_url}/git/blobs', headers=headers, json={
        'content': base64.b64encode(dockerfile_content.encode()).decode(),
        'encoding': 'base64'
    }).json()['sha']

    # Get latest commit tree
    latest_commit_tree_sha = requests.get(f'{api_base_url}/git/commits/{default_branch_sha}', headers=headers).json()['tree']['sha']
    print("Latest commit tree SHA:", latest_commit_tree_sha)

    # Create a new tree with the new blobs
    new_tree_response = requests.post(f'{api_base_url}/git/trees', headers=headers, json={
        'base_tree': latest_commit_tree_sha,
        'tree': [
            {
                'path': '.devcontainer/devcontainer.json',
                'mode': '100644',
                'type': 'blob',
                'sha': devcontainer_json_blob_sha
            },
            {
                'path': 'Dockerfile',
                'mode': '100644',
                'type': 'blob',
                'sha': dockerfile_blob_sha
            }
        ]
    })

    if new_tree_response.status_code == 201:
        new_tree = new_tree_response.json()
        print("New tree created successfully.")
        print("New tree SHA:", new_tree['sha'])
    else:
        print("Error creating the new tree.")
        print("Status code:", new_tree_response.status_code)
        print("Error message:", new_tree_response.json())
        exit(1)

    # Create a new commit with the new tree
    new_commit_response = requests.post(f'{api_base_url}/git/commits', headers=headers, json={
        'message': 'Add devcontainer.json and Dockerfile',
        'tree': new_tree['sha'],
        'parents': [default_branch_sha]
    })

    if new_commit_response.status_code == 201:
        new_commit = new_commit_response.json()
        print("New commit created successfully.")
        print("New commit SHA:", new_commit['sha'])
    else:
        print("Error creating the new commit.")
        print("Status code:", new_commit_response.status_code)
        print("Error message:", new_commit_response.json())
        exit(1)

    # Create new branch on the forked repository with the new commit SHA
    new_branch_ref = f'refs/heads/{new_branch_name}'
    create_branch_response = requests.post(f'{api_base_url}/git/refs', headers=headers, json={
        'ref': new_branch_ref,
        'sha': new_commit['sha']
    })

    if create_branch_response.status_code == 201:
        print(f"New branch '{new_branch_name}' created successfully on the forked repository with devcontainer.json and Dockerfile.")
    else:
        print("Error creating the new branch on the forked repository.")
        print("Status code:", create_branch_response.status_code)
        print("Error message:", create_branch_response.json())
        exit(1)
    '''
    # Update the new branch's reference to point to the new commit
    update_ref_response = requests.patch(f'{api_base_url}/git/refs/{new_branch_ref}', headers=headers, json={
        'sha': new_commit['sha']
    })

    if update_ref_response.status_code == 200:
        print(f"New branch '{new_branch_name}' updated with devcontainer.json and Dockerfile.")
    else:
        print("Error updating the new branch's reference.")
        print("Status code:", update_ref_response.status_code)
        print("Error message:", update_ref_response.json())
        exit(1)
    '''


def launch_codespace(repo_owner, repo_name, new_branch_name):
    import requests
    import time

    # Replace these variables with your own
    your_github_token = access_token

    headers = {
        'Authorization': f'token {your_github_token}',
        'Accept': 'application/vnd.github+json',
        'Content-Type': 'application/json'
    }

    api_base_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/codespaces'

    create_codespace_payload = {
        'ref': new_branch_name
    }

    create_codespace_response = requests.post(api_base_url, headers=headers, json=create_codespace_payload)

    if create_codespace_response.status_code == 201:
        print("Codespace creation request is successful. Waiting for the Codespace to be created...")
        codespace = create_codespace_response.json()

        # Poll the Codespace's status until it becomes 'available'
        codespace_id = codespace['id']
        codespace_status = codespace['status']

        while codespace_status != 'available':
            time.sleep(10)
            codespace_response = requests.get(f'{api_base_url}/{codespace_id}', headers=headers)
            codespace = codespace_response.json()
            print(codespace)
            codespace_status = codespace['status']
            print(f"Current Codespace status: {codespace_status}")

        print(f"Codespace is available! ID: {codespace_id}")
    else:
        print("Error creating the Codespace.")
        print("Status code:", create_codespace_response.status_code)
        print("Error message:", create_codespace_response.json())

#create_branch_add_dev_container('sdk21', repo_name, 'robo_dev_feature_test_e')

#launch_codespace(repo_owner, repo_name, 'robo_dev_feature_test_e')

##############################################################################
##################### ChatGPT version ########################################
##############################################################################

import requests
import time
from urllib.parse import urlparse

def create_codespace_with_files(access_token, repo_url, dockerfile_content, devcontainer_content, sample_script_content):
    headers = {
        'Authorization': f'token {access_token}',
        'Accept': 'application/vnd.github+json',
        'Content-Type': 'application/json'
    }
    
    # Parse the repo URL
    repo_path = urlparse(repo_url).path
    original_repo_owner, original_repo_name = repo_path.strip('/').split('/')

    # Fork the repo
    fork_url = f'https://api.github.com/repos/{original_repo_owner}/{original_repo_name}/forks'
    fork_response = requests.post(fork_url, headers=headers)

    if fork_response.status_code == 202:
        print("Forking the repository. This may take a few seconds...")
        forked_repo = fork_response.json()
        time.sleep(10)  # Give GitHub a few seconds to finish forking the repository
    else:
        print("Error forking the repository.")
        print("Status code:", fork_response.status_code)
        print("Error message:", fork_response.json())
        return

    forked_repo_owner = forked_repo['owner']['login']
    forked_repo_name = forked_repo['name']

    # Create new branch with the three files checked in
    new_branch_name = 'custom-dev-container'
    file_contents = {
        'Dockerfile': dockerfile_content,
        'devcontainer.json': devcontainer_content,
        'sample_script.py': sample_script_content
    }
    
    # ... (Include the code to create a new branch with the files, as discussed in the previous responses)

    # Create a new Codespace with the new branch
    api_base_url = f'https://api.github.com/repos/{forked_repo_owner}/{forked_repo_name}/codespaces'
    create_codespace_payload = {
        'ref': new_branch_name
    }
    
    create_codespace_response = requests.post(api_base_url, headers=headers, json=create_codespace_payload)
    
    if create_codespace_response.status_code == 201:
        print("Codespace creation request is successful. Waiting for the Codespace to be created...")
        codespace = create_codespace_response.json()
    
        codespace_id = codespace['id']
        codespace_status = codespace['status']
    
        while codespace_status != 'available':
            time.sleep(10)
            codespace_response = requests.get(f'{api_base_url}/{codespace_id}', headers=headers)
            codespace = codespace_response.json()
            codespace_status = codespace['status']
            print(f"Current Codespace status: {codespace_status}")
    
        print(f"Codespace is available! ID: {codespace_id}")
    else:
        print("Error creating the Codespace.")
        print("Status code:", create_codespace_response.status_code)
        print("Error message:", create_codespace_response.json())


import requests
import time

def fork_repository(username, repo_owner, repo_name, headers):
    fork_api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/forks'
    fork_response = requests.post(fork_api_url, headers=headers)

    if fork_response.status_code == 202:
        print("Repository forked successfully.")
        return fork_response.json()
    else:
        print("Error forking the repository.")
        print("Status code:", fork_response.status_code)
        print("Error message:", fork_response.json())
        return None


def create_new_branch(username, repo_name, new_branch_name, headers):
    api_base_url = f'https://api.github.com/repos/{username}/{repo_name}'
    branches_api_url = f'{api_base_url}/git/refs/heads'

    response = requests.get(branches_api_url, headers=headers)
    branches = response.json()

    main_branch_sha = None
    for branch in branches:
        if branch['ref'] == 'refs/heads/main':
            main_branch_sha = branch['object']['sha']
            break

    if not main_branch_sha:
        print("Error: Couldn't find the main branch.")
        return

    new_branch_data = {
        'ref': f'refs/heads/{new_branch_name}',
        'sha': main_branch_sha
    }

    response = requests.post(branches_api_url, headers=headers, json=new_branch_data)

    if response.status_code == 201:
        print(f"New branch '{new_branch_name}' created successfully.")
    else:
        print("Error creating the new branch.")
        print("Status code:", response.status_code)
        print("Error message:", response.json())


def commit_files_to_branch(username, repo_name, branch_name, devcontainer_json, docker_file, sample_script, headers):
    # Encode file contents as Base64
    devcontainer_json_content = base64.b64encode(devcontainer_json.encode('utf-8')).decode('utf-8')
    docker_file_content = base64.b64encode(docker_file.encode('utf-8')).decode('utf-8')
    sample_script_content = base64.b64encode(sample_script.encode('utf-8')).decode('utf-8')

    # Get the latest commit on the main branch
    api_base_url = f'https://api.github.com/repos/{username}/{repo_name}'
    latest_commit_response = requests.get(f'{api_base_url}/git/ref/heads/main', headers=headers)
    latest_commit_sha = latest_commit_response.json()['object']['sha']

    # Get the tree of the latest commit
    latest_commit_tree_response = requests.get(f'{api_base_url}/git/trees/{latest_commit_sha}', headers=headers)
    latest_commit_tree_sha = latest_commit_tree_response.json()['sha']

    # Create a new tree with the new blobs
    new_tree_data = {
        'base_tree': latest_commit_tree_sha,
        'tree': [
            {'path': '.devcontainer/devcontainer.json', 'mode': '100644', 'type': 'blob', 'content': devcontainer_json},
            {'path': 'Dockerfile', 'mode': '100644', 'type': 'blob', 'content': docker_file},
            {'path': 'sample_script.py', 'mode': '100644', 'type': 'blob', 'content': sample_script}
        ]
    }
    new_tree_response = requests.post(f'{api_base_url}/git/trees', headers=headers, json=new_tree_data)
    new_tree_sha = new_tree_response.json()['sha']

    # Create a new commit
    new_commit_data = {
        'message': 'Add devcontainer files',
        'parents': [latest_commit_sha],
        'tree': new_tree_sha
    }
    new_commit_response = requests.post(f'{api_base_url}/git/commits', headers=headers, json=new_commit_data)
    new_commit_sha = new_commit_response.json()['sha']

    # Create the new branch with the new commit
    new_branch_data = {
        'ref': f'refs/heads/{branch_name}',
        'sha': new_commit_sha
    }
    requests.post(f'{api_base_url}/git/refs', headers=headers, json=new_branch_data)


def create_codespace(username, repo_name, branch_name, headers):
    api_base_url = f'https://api.github.com'

    # Set up the Codespace creation request
    codespace_data = {
        'repository': f'{username}/{repo_name}',
        'branch': branch_name
    }

    # Send the Codespace creation request
    codespace_response = requests.post(f'{api_base_url}/user/codespaces', headers=headers, json=codespace_data)

    if codespace_response.status_code == 201:
        print("Codespace creation request is successful. Waiting for the Codespace to be created...")
        codespace_id = codespace_response.json()['id']
    else:
        raise Exception(f"Error creating Codespace: {codespace_response.status_code} - {codespace_response.json()['message']}")

    # Poll the Codespace status until it is ready
    codespace_status = 'creating'
    while codespace_status != 'ready':
        time.sleep(5)
        codespace_status_response = requests.get(f'{api_base_url}/codespaces/{codespace_id}', headers=headers)
        codespace_status = codespace_status_response.json()['state']

    print(f"Codespace is ready. ID: {codespace_id}")
    return codespace_id


def create_codespace_with_files(username, access_token, repo_url, docker_file, devcontainer_json, sample_script):
    # Extract repository owner and name from the repo URL
    repo_parts = repo_url.split('/')
    repo_owner = repo_parts[-2]
    repo_name = repo_parts[-1].replace('.git', '')

    # Configure headers for the GitHub API
    headers = {
        'Authorization': f'token {access_token}',
        'Accept': 'application/vnd.github+json',
        'Content-Type': 'application/json'
    }

    # Fork the repository
    forked_repo = fork_repository(username, repo_owner, repo_name, headers)
    print("Forked!")

    # Create a new branch in the forked repository
    new_branch_name = 'devcontainer-setup'
    #create_new_branch(username, repo_name, new_branch_name, headers)

    # Commit devcontainer.json, Dockerfile, and sample_script to the new branch
    commit_files_to_branch(username, repo_name, new_branch_name, devcontainer_json, docker_file, sample_script, headers)
    print("Branch created and committed files")

    # Create a new Codespace using the new branch
    codespace_id = create_codespace(username, repo_name, new_branch_name, headers)
    print(codespace_id)
    
    return codespace_id

username = 'sdk21'
repo_url = 'https://github.com/kkroening/ffmpeg-python'
docker_file = '''# Use the official Python base image
    FROM python:3.9-slim

    # Set the working directory
    WORKDIR /app

    # Install FFmpeg
    RUN apt-get update && \
        apt-get install -y --no-install-recommends ffmpeg && \
        rm -rf /var/lib/apt/lists/*

    # Clone the ffmpeg-python repository
    RUN apt-get update && \
        apt-get install -y --no-install-recommends git && \
        git clone https://github.com/kkroening/ffmpeg-python.git /app/ffmpeg-python && \
        rm -rf /var/lib/apt/lists/*

    # Install the required dependencies
    RUN pip install --no-cache-dir -r /app/ffmpeg-python/requirements.txt

    # Optional: Set the entrypoint for the container
    ENTRYPOINT ["python"]
    ''' 
devcontainer_json = '''{
    "name": "ffmpeg-python-dev-container",
    "dockerFile": "Dockerfile",
    "settings": {
        "terminal.integrated.shell.linux": "/bin/bash"
    },
    "extensions": [
        "ms-python.python"
    ],
    "forwardPorts": [],
    "postCreateCommand": "echo 'Welcome to your ffmpeg-python dev container!'"
    }
    '''

sample_script = '''
import requests
import ffmpeg
import tempfile

# Download a video file from the internet
video_url = 'https://download.samplelib.com/mp4/sample-5s.mp4'

response = requests.get(video_url, stream=True)
response.raise_for_status()

# Save the video to a temporary file
with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video_file:
    for chunk in response.iter_content(chunk_size=8192):
        temp_video_file.write(chunk)
    temp_video_file.flush()

    # Process the video using ffmpeg-python
    input_video = ffmpeg.input(temp_video_file.name)
    output_video = input_video.filter('scale', 320, 240).output('output_video.mp4')
    output_video.run()

print("Video processing completed. The output video is saved as output_video.mp4.")
'''

create_codespace_with_files(username, access_token, repo_url, docker_file, devcontainer_json, sample_script)
