from openai import OpenAI
import time
import concurrent.futures
import functools
from openai import AzureOpenAI


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

gpt_client = openai_client


deepseek_V3 = "deepseek-chat"
deepseek_api_key = ''
deepseek_url = 'https://api.deepseek.com'
deepseek_client = OpenAI(api_key=deepseek_api_key, base_url=deepseek_url)





turbo_name = "gpt-4o-mini"
big_turbo_name = "gpt-4o"
deepseek_V3 = "deepseek-chat"


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

def get_completion_with_retry(model, input_data, input_type="prompt"):
    """
    通用的带重试的 GPT 请求函数。

    参数:
        model (str): 使用的模型名称。
        input_data (str or list): 输入数据，字符串表示 prompt，列表表示 messages。
        input_type (str): 输入类型，"prompt" 或 "messages"。

    返回:
        str: GPT 响应内容。
    """
    def completion_function(input_data):
        return _get_completion(model, input_data, input_type)

    return get_completion_by_loop(completion_function, input_data)


@timeout(90)
def _get_completion(model, input_data, input_type):
    """
    内部通用的 GPT 完成请求函数。

    参数:
        model (str): 使用的模型名称。
        input_data (str or list): 输入数据，字符串表示 prompt，列表表示 messages。
        input_type (str): 输入类型，"prompt" 或 "messages"。

    返回:
        str: GPT 响应内容。
    """
    if input_type == "prompt":
        messages = [{"role": "user", "content": input_data}]
    elif input_type == "messages":
        messages = input_data
    else:
        raise ValueError("input_type must be either 'prompt' or 'messages'")

    # 动态选择客户端
    if model in [turbo_name, big_turbo_name]:
        client = gpt_client
    elif model == deepseek_V3:
        client = deepseek_client
    else:
        raise ValueError(f"Unsupported model: {model}")

    # 调用 API
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return dict(response.choices[0].message)["content"]


# 简化后的具体调用函数
def get_completion_from_pmt_with_turbo(prompt):
    return get_completion_with_retry(model=turbo_name, input_data=prompt, input_type="prompt")


def get_completion_from_msg_with_turbo(messages):
    return get_completion_with_retry(model=turbo_name, input_data=messages, input_type="messages")


def get_completion_from_pmt_with_big_turbo(prompt):
    return get_completion_with_retry(model=big_turbo_name, input_data=prompt, input_type="prompt")


def get_completion_from_msg_with_big_turbo(messages):
    return get_completion_with_retry(model=big_turbo_name, input_data=messages, input_type="messages")


def get_completion_from_pmt_with_deepseek_V3(prompt):
    return get_completion_with_retry(model=deepseek_V3, input_data=prompt, input_type="prompt")


def get_completion_from_msg_with_deepseek_V3(messages):
    return get_completion_with_retry(model=deepseek_V3, input_data=messages, input_type="messages")
