import openai
import re

def authenticate_openai(api_key):
    openai.api_key = api_key

def extract_code_blocks(text):
    code_blocks = re.findall(r'```([\s\S]*?)```', text)
    code_blocks = [code_block.strip() for code_block in code_blocks]
    return code_blocks

def get_code_block_openai(prompt, model='gpt-4'):
    # Ensure the user is authenticated
    if not openai.api_key:
        raise ValueError("OpenAI API key not set. Please authenticate using 'authenticate_openai(api_key)' function.")

    # Set up the API request
    data = {
        'engine': model,
        'prompt': prompt,
        'max_tokens': 100,
        'n': 1,
        'stop': None,
        'temperature': 1,
    }

    try:
        print(f"Sending request to OpenAI API with the following parameters:")
        print(f"  Model: {model}")
        print(f"  Prompt: {prompt}")

        # Make the API request
        response = openai.Completion.create(**data)

        # Check if there are choices in the response
        if not response.choices:
            print("Error: The API response does not contain any generated text.")
            return None

        # Extract the generated text
        generated_text = response.choices[0].text.strip()
        print("Generated text successfully received.")
        return extract_code_blocks(generated_text)

    except openai.error.APIError as api_error:
        print(f"API error: {api_error}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

