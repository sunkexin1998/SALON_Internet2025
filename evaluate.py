import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score

senti_labels = [-1, 0, 1]


def evaluate(human_labeled_file, pred_file):
    human_labeled_data = pd.read_csv(human_labeled_file)
    human_labeled_senti = list(human_labeled_data['sentiment'])
    pred_data = pd.read_csv(pred_file)
    pred_senti = list(pred_data['sentiment'])
    result = []
    accuracy = accuracy_score(human_labeled_senti, pred_senti)
    macro_f1 = f1_score(human_labeled_senti,
                        pred_senti,
                        labels=senti_labels,
                        average='macro')
    micro_f1 = f1_score(human_labeled_senti,
                        pred_senti,
                        labels=senti_labels,
                        average='micro')
    # Output overall accuracy, Macro-F1, Micro-F1
    print(f"accuracy_score: {accuracy}")
    print(f"macro: {macro_f1}")
    print(f"micro: {micro_f1}")
    result.extend([accuracy, macro_f1, micro_f1])
    # Calculate the precision, recall, and F1 score for each category.
    precision = precision_score(human_labeled_senti,
                                pred_senti,
                                labels=senti_labels,
                                average=None)
    recall = recall_score(human_labeled_senti,
                          pred_senti,
                          labels=senti_labels,
                          average=None)
    f1 = f1_score(human_labeled_senti,
                  pred_senti,
                  labels=senti_labels,
                  average=None)
    for sentiment in (1, 0, -1):
        index = sentiment + 1
        print(f'{precision[index]}\t{recall[index]}\t{f1[index]}')
        result.extend([precision[index], recall[index], f1[index]])
    print("\t".join([str(item) for item in result]))
    return result


#Plot the confusion matrix.
def draw_confusion_matrix(human_labeled_file, pred_file):
    human_labeled_data = pd.read_csv(human_labeled_file)
    human_labeled_senti = list(human_labeled_data['sentiment'])
    pred_data = pd.read_csv(pred_file)
    pred_senti = list(pred_data['sentiment'])
    # Generate the confusion matrix.
    cm = confusion_matrix(human_labeled_senti, pred_senti)
    # Calculate the percentage.
    cm_percentage = cm.astype('float') / len(pred_senti)
    sns.set(font_scale=2.2)
    plt.figure(figsize=(8, 7))
    # Plot the confusion matrix using a heatmap.
    sns.heatmap(cm_percentage,
                annot=True,
                fmt=".1%",
                cmap="Blues",
                xticklabels=senti_labels,
                yticklabels=senti_labels,
                annot_kws={"size": 33})
    plt.xlabel("Predicted labels", fontsize=23)
    plt.ylabel("True labels", fontsize=23)
    plt.show()


#4.8(2): 考虑insight底部的空格

#4.10: 不考虑insight底部的空格
#4.10(2): 考虑了insight底部的空格
#4.10(3): 考虑了insight底部的空格
#4.10(4): 不考虑insight底部的空格
if __name__ == '__main__':

    target = "SOF-1"

    human_labeled_file = f'human_labeled/{target}_test.csv'
    pred_file = f'ChatGPT/outputs(basic_prompt_2)/{target}_formated_p3.8.csv'

    evaluate(human_labeled_file, pred_file)
    # draw_confusion_matrix(human_labeled_file, pred_file)
