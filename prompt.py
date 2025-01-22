# basic SA prompt
def basic_prompt(index, text):
    # The sentiment analysis prompt used in Andrew Ng's DeepLearning.AI course.
    # https://learn.deeplearning.ai/courses/chatgpt-prompt-eng/lesson/5/inferring
    # We mainly test the effectiveness of paper insight on this prompt
    prompt_0_1 = "What is the sentiment of the following text, which is delimited with triple backticks?\n" \
                 "Give your answer as a single word, \"positive\",\"neutral\" or \"negative\".\n\n" \
                f"Text:```{text}```"

    # From "Sentiment Analysis in the Era of Large Language Models: A Reality Check"
    prompt_0_2 = f'''Please perform Sentiment Classification task. Given the sentence, assign a sentiment label from ['positive','neutral','negative']. Return label only without any other text.\n\nSentence: {text}\nLabel: '''

    # From  "LARGE LANGUAGE MODELS ARE HUMAN-LEVEL PROMPT ENGINEERS"
    # https://github.com/keirp/automatic_prompt_engineer/blob/main/demo.py
    prompt_0_3 = f"""Instruction: write \"positive\" if the input is a positive review, \"neutral\" if the input is a neutral review, and \"negative\" if the input is a negative review.\nInput: {text}\nOutput: """

    prompts = [prompt_0_1, prompt_0_2, prompt_0_3]
    return prompts[index - 1]


# Enhanced prompt
def enhanced_basic_prompt_1(insight, text):
    prompt = insight \
             + "\n\n" + \
             "Considering that, what is the sentiment of the following text, which is delimited with triple backticks?\n" \
             "Give your answer as a single word, \"positive\",\"neutral\" or \"negative\".\n\n" \
             f"Text:```{text}```"
    return prompt


def enhanced_basic_prompt_2(insight, text):
    prompt = insight \
             + "\n\n" + \
             f"Considering that, please perform Sentiment Classification task. Given the sentence, assign a sentiment label from ['positive','neutral','negative']. Return label only without any other text.\n\nSentence: {text}\nLabel: "
    return prompt


enhanced_prompt_def_arr = [enhanced_basic_prompt_1, enhanced_basic_prompt_2]
def get_prompt(base_index, def_index, prompt_index, text):
    def_index = int(def_index)
    prompt_index = int(prompt_index)
    if def_index == 0 :
        return basic_prompt(prompt_index, text)

    insight_path = 'insights/'
    insight_name = f'Q{def_index}_{prompt_index}.txt'
    with open(insight_path + insight_name, 'r', encoding='utf-8') as file:
        insight = file.read()

    enhanced_prompt = enhanced_prompt_def_arr[base_index-1]
    return enhanced_prompt(insight, text)

def test():
    text = "test_text"

    index = 3
    prompt = basic_prompt(index,text)
    print(prompt)

    index = 2
    prompt = basic_prompt(index, text)
    print(prompt)


    def_index = 1
    prompt_index = 1
    prompt = get_prompt(def_index, prompt_index, text)
    print(prompt)

    def_index = 2
    prompt_index = 1
    prompt = get_prompt(def_index, prompt_index, text)
    print(prompt)



if __name__ == '__main__':

    test();