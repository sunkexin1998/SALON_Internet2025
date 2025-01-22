from openai import OpenAI
import time
import concurrent.futures
import functools
from openai import AzureOpenAI

# openai_api_key = 'sk-onKl1M8665QV0A3yxZisOwSDX9Vs14Sevmbiyms6I7C15tiv' # 世杰项目里的
# openai_base_url = 'https://api.bianxie.ai/v1'

openai_api_key = ''
openai_base_url = 'https://api.openai.com/v1'
openai_client = OpenAI(api_key=openai_api_key, base_url=openai_base_url)


AZURE_OPENAI_ENDPOINT = 'https://subcription-openai.openai.azure.com/'
AZURE_OPENAI_API_KEY = ''
azure_client = AzureOpenAI(
  azure_endpoint = AZURE_OPENAI_ENDPOINT,
  api_key = AZURE_OPENAI_API_KEY,
  api_version = "2024-09-01-preview"
)

client = openai_client


turbo_name = "gpt-4o-mini"
big_turbo_name = "gpt-4o"


def timeout(seconds):

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(func, *args, **kwargs)
                try:
                    return future.result(timeout=seconds)
                except concurrent.futures.TimeoutError:
                    raise TimeoutError(
                        f'The function "{func.__name__}" timed out after {seconds} seconds'
                    )

        return wrapper

    return decorator


def get_completion_by_loop(get_completion, prompt):
    while True:
        try:
            response = get_completion(prompt)
            # Check if the response has a value
            if response is not None:
                break  # If the response has a value, jump out of the loop
        except TimeoutError as e:
            print(f"Timeout exception: {e}, Retrying currently...")
        except Exception as e:
            sec = 30
            print(
                f"An exception has occurred: {e}, Retrying in {sec} seconds..."
            )
            time.sleep(sec)  # Wait and rerun the code

    return response


@timeout(90)
def get_turbo_completion_with_prompt(prompt, model=turbo_name):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return dict(response.choices[0].message)["content"]


@timeout(90)
def get_turbo_completion_with_messages(messages, model=turbo_name):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return dict(response.choices[0].message)["content"]


@timeout(90)
def get_big_turbo_completion_with_prompt(prompt, model=big_turbo_name):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return dict(response.choices[0].message)["content"]


@timeout(90)
def get_big_turbo_completion_with_messages(messages, model=big_turbo_name):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return dict(response.choices[0].message)["content"]


def get_completion_from_pmt_with_turbo(prompt):
    response = get_completion_by_loop(get_turbo_completion_with_prompt, prompt)
    return response


def get_completion_from_msg_with_turbo(messages):
    response = get_completion_by_loop(get_turbo_completion_with_messages,
                                      messages)
    return response


def get_completion_from_pmt_with_big_turbo(prompt):
    response = get_completion_by_loop(get_big_turbo_completion_with_prompt,
                                      prompt)
    return response


def get_completion_from_msg_with_big_turbo(messages):
    response = get_completion_by_loop(get_big_turbo_completion_with_messages,
                                      messages)
    return response
