import openai
import os
import re

def authenticate_openai(api_key):
    openai.api_key = api_key

def list_openai_engines():
    # Ensure the user is authenticated
    if not openai.api_key:
        raise ValueError("OpenAI API key not set. Please authenticate using 'authenticate_openai(api_key)' function.")

    try:
        response = openai.Engine.list()
        engines = response['data']
        return engines
    except openai.error.APIError as api_error:
        print(f"API error: {api_error}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def extract_code_blocks(text):
    code_blocks = re.findall(r'```([\s\S]*?)```', text)
    code_blocks = [code_block.strip() for code_block in code_blocks]
    return code_blocks

def get_code_block_openai(prompt, model='gpt-3.5-turbo'):
    # Ensure the user is authenticated
    if not openai.api_key:
        raise ValueError("OpenAI API key not set. Please authenticate using 'authenticate_openai(api_key)' function.")

    # Set up the API request
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 150,
        "n": 1,
        "stop": None,
        "temperature": 1.0
    }

    try:
        print(f"Sending request to OpenAI API with the following parameters:")
        print(f"  Model: {model}")
        print(f"  Prompt: {prompt}")

        # Make the API request
        response = openai.ChatCompletion.create(**data)

        # Check if there are choices in the response
        if not response.choices:
            print("Error: The API response does not contain any generated text.")
            return None

        # Extract the generated text
#        import ipdb
#        ipdb.set_trace()
        print(response)
        print(response.choices[0].message.content)
        generated_text = response.choices[0].message.content.strip()
        print("Generated text successfully received.")

        code_blocks = extract_code_blocks(generated_text)
        if len(code_blocks) > 0:
            return code_blocks[0]
        else:
            return generated_text

    except openai.error.APIError as api_error:
        print(f"API error: {api_error}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


if __name__ == '__main__':
    authenticate_openai(os.environ['OPENAI_API_TOKEN'])
    # print(list_openai_engines())
    print(get_code_block_openai('Generate a sample python code that adds two numbers'))
