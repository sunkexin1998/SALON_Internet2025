from ChatGPT import gpt_completion as llm
from pathlib import Path
import PyPDF2
import re

essays_dir_path = Path('./essays')
questions_dir_path = Path('./questions')
# essays_name = [f.name for f in essays_dir_path.iterdir() if f.is_file()]
questions_list = [f.name for f in questions_dir_path.iterdir() if f.is_file()]

essays_path = './essays/'
insights_path = 'insights(deepseek)/'

# 自定义序号字典
essays_name = [
    "SentiStrength-SE- Exploiting domain specificity for improved sentiment analysis in software engineering text.pdf",
    "Exploiting the Unique Expression for Improved Sentiment Analysis in Software Engineering Text.pdf",
    "SentiCR- A Customized Sentiment Analysis Tool for Code Review Interactions.pdf",
    "Entity-Level Sentiment Analysis of Issue Comments.pdf",
    "SEntiMoji-An Emoji-Powered Learning Approach for Sentiment Analysis in Software Engineering.pdf",
    "Sentiment Polarity Detection for Software Development.pdf",

    "Assessment of off-the-shelf SE-specific sentiment analysis tools: An extended replication study .pdf",
    "Can We Use SE-specific Sentiment Analysis Tools in a Cross-Platform Setting?.pdf",
    "Development and Application of Sentiment Analysis Tools in Software Engineering: A Systematic Literature Review.pdf",
    "Incorporating Pre-trained Transformer Models into TextCNN for Sentiment Analysis on Software Engineering Texts.pdf",
    "Opinion Mining for Software Development: A Systematic Literature Review.pdf",
    "Revisiting Sentiment Analysis for Software Engineering in the Era of Large Language Models.pdf",
    "“Looks Good To Me ;-)\": Assessing Sentiment Analysis Tools for Pull Request Discussions.pdf"
]

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


get_completion_from_msg = llm.get_completion_from_msg_with_deepseek_V3
def extract_insight_from_paper_with_questions(paper, questions):
    insight_list = []
    first_question = questions[0]
    user_question_1 = paper + "\n\n" + first_question
    messages = []
    messages.append({"role": "user", "content": user_question_1})
    first_insight = get_completion_from_msg(messages)
    messages.append({"role": "assistant", "content": first_insight})
    insight_list.append(first_insight)
    for next_q in questions[1:]:
        messages.append({"role": "user", "content": next_q})
        next_insight = get_completion_from_msg(messages)
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

    for question_name in ['Q1.txt','Q2.txt','Q3.txt']:
        for index, essay_name in enumerate(essays_name):
            extractor(question_name, essay_name, index + 1)
