from ChatGPT import gpt_completion as gpt
from pathlib import Path
import PyPDF2
import re

essays_dir_path = Path('./essays')
questions_dir_path = Path('./questions')
essays_name = [f.name for f in essays_dir_path.iterdir() if f.is_file()]
questions_list = [f.name for f in questions_dir_path.iterdir() if f.is_file()]

essays_path = './essays/'
insights_path = 'insights(5)/'


def count_words_in_file(file_path):
    try:
        # Open the file in read mode
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        # Split the text into words using whitespace as the delimiter
        words = text.split()
        # Count the number of words
        word_count = len(words)
        return word_count
    except FileNotFoundError:
        print(f"Error: The file at '{file_path}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def extract_insight_from_paper_with_questions(paper, questions):
    insight_list = []
    first_question = questions[0]
    user_question_1 = paper + "\n\n" + first_question
    messages = []
    messages.append({"role": "user", "content": user_question_1})
    first_insight = gpt.get_completion_from_msg_with_turbo(messages)
    messages.append({"role": "assistant", "content": first_insight})
    insight_list.append(first_insight)
    for next_q in questions[1:]:
        messages.append({"role": "user", "content": next_q})
        next_insight = gpt.get_completion_from_msg_with_turbo(messages)
        insight_list.append(next_insight)
        messages.append({"role": "assistant", "content": next_insight})
    return insight_list


def extractor(question_name, essay_name, index):
    with open(essays_path + essay_name, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for pageNumber in range(len(reader.pages)):
            text += reader.pages[pageNumber].extract_text()

    basic_question_path = './questions/'
    questions = []
    with open(basic_question_path + question_name, 'r', encoding='utf-8') as qfile:
        for line in qfile:
            if not line.strip() == "":
                questions.append(line.strip())

    insight_responses = extract_insight_from_paper_with_questions(text, questions)

    insight = ''
    for response in insight_responses:
        response = re.sub(r'\n{2,}', '\n', response)
        insight +=  response + '\n\n'
    insight = insight.strip()

    question_name = question_name.replace(".txt","")
    insight_name = f'{question_name}_{index}.txt'
    with open(insights_path + insight_name, 'w', encoding='utf-8') as ofile:
        ofile.write(insight)


def create_index():
    with open(insights_path + 'index.txt', 'w', encoding='utf-8') as file:
        for index, essay_name in enumerate(essays_name):
            file.write(f'{index + 1}\t\t\t{essay_name}\n')


if __name__ == '__main__':

    # create_index()
    for question_name in ['Q1.txt','Q2.txt','Q3.txt']:
        for index, essay_name in enumerate(essays_name):
            extractor(question_name, essay_name, index + 1)
