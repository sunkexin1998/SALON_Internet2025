import pandas as pd
import matplotlib.pyplot as plt
from evaluate import evaluate

indexs = []
datas = [[] for _ in range(12)]

field_list = [
    'accuracy', 'macro', 'micro', 'positize_P', 'positize_R', 'positize_F',
    'neutral_P', 'neutral_R', 'neutral_F', 'negative_P', 'negative_R',
    'negative_F'
]

target = 'SOF-1'
output_dir = 'ChatGPT/outputs(basic_prompt_1)/'


def add2csv(def_index, prompt_index):
    human_labeled_file = f'human_labeled/{target}_test.csv'
    if def_index == 0:
        pred_file = f'ChatGPT/outputs(deepseek)/{target}_formated_p{def_index}.{prompt_index}.csv'
    else:
        pred_file = f'ChatGPT/outputs(basic_prompt_2)(deepseek)/{target}_formated_p{def_index}.{prompt_index}.csv'
    result = evaluate(human_labeled_file, pred_file)
    for index, data in enumerate(result):
        datas[index].append(data)
    indexs.append(f'{def_index}.{prompt_index}')


def generate():
    dic = {'index': indexs}
    for index, data in enumerate(datas):
        dic[field_list[index]] = data

    data_formated = pd.DataFrame(dic)
    data_formated.to_csv('data(deepseek).csv', index=False)


if __name__ == '__main__':

    def_index_arr = [i for i in range(0, 3+1)]
    for def_index in def_index_arr:
        if def_index == 0:
            prompt_index_arr = [1,2,3]
        else:
            prompt_index_arr = ['1', '2' ,'3', '4', '5',
                                '6', '7' ,'8', '9', '10',
                                '11', '12' ,'13']

        for prompt_index in prompt_index_arr:
            add2csv(def_index, prompt_index)

    generate()
