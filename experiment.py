import sys
import os
import csv
import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix
import seaborn as sn
import matplotlib.pyplot as plt
from metrics import python_diff_str, cosine_similarity_str, levenshtein_distance_str, SmithWaterman_str, MongeElkan_str, jarowinkler_str, jaccard_str, ngram_str, cidiff_str
from scores import get_scores

def apply_metric(s1, s2, metric=python_diff_str):
    return metric(s1, s2)


def choose_class_from_score(score):
    if score == 1:
        return 1
    elif score < 0.5:
        return 2
    else: #score between 0.5 and 1
        return 3


if __name__ == "__main__":
    # metrics = [python_diff_str, cosine_similarity_str, levenshtein_distance_str, SmithWaterman_str, MongeElkan_str, jarowinkler_str, jaccard_str, ngram_str]
    metrics = [python_diff_str, levenshtein_distance_str, SmithWaterman_str, MongeElkan_str, jarowinkler_str, jaccard_str, ngram_str, cidiff_str]
    csv_file = "annotations.csv"
    if len(sys.argv) == 2:
        csv_file = sys.argv[1]
    
    if not os.path.exists(csv_file):
        print(f"Usage: python3 annotate_log_lines.py [csv_file]. Default is 'annotations.csv'")
        print(f"Error: {csv_file} does not exist.")
        exit(1)

    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        y_annot = []
        y_metric = [[] for _ in range(len(metrics))]
        for row in reader:
            line1 = row[2]
            line2 = row[3]
            y_annot.append(int(row[4]))
            for i, metric in enumerate(metrics):
                score = apply_metric(line1, line2, metric)
                y_metric[i].append(choose_class_from_score(score))    


    metrics_confusion_matrix = []
    for i, metric in enumerate(metrics):
        cm = confusion_matrix(y_annot, y_metric[i])
        # cm = cm / cm.astype(float).sum(axis=1) * 100
        metrics_confusion_matrix.append(cm)
    
    #plot the confusion matrix with seaborn
    fig, axs = plt.subplots(2, 4, figsize=(20, 10))
    for i, metric in enumerate(metrics):
        sn.heatmap(metrics_confusion_matrix[i], annot=True, ax=axs[i//4, i%4], fmt='g', square=True, cmap='Blues', cbar=False)
        axs[i//4, i%4].set_title(metric.__name__)
        axs[i//4, i%4].set_xlabel('Predicted')
        axs[i//4, i%4].set_ylabel('Annotation')
        axs[i//4, i%4].set_xticklabels(['Same', 'Modified', 'Different'])
        axs[i//4, i%4].set_yticklabels(['Same', 'Modified', 'Different'])
    plt.savefig('fig/confusion_matrix.png')
    plt.show()

    scores = []
    for i, metric in enumerate(metrics):
        accuracy, precision, recall, f1 = get_scores(y_annot, y_metric[i])
        scores.append([metric.__name__, np.round(accuracy,2), np.round(precision, 2), np.round(recall, 2), np.round(f1, 2)])
    scores = pd.DataFrame(scores, columns=['Metric', 'Accuracy', 'Precision', 'Recall', 'F1'])
    scores.to_csv('fig/scores.csv', index=False)
    print(scores)
    print("Higest F1 score: ", scores.loc[scores['F1'].idxmax()]["Metric"], scores.loc[scores['F1'].idxmax()]["F1"])
    print("Higest Recall score: ", scores.loc[scores['Recall'].idxmax()]["Metric"], scores.loc[scores['Recall'].idxmax()]["Recall"])
    print("Higest Precision score: ", scores.loc[scores['Precision'].idxmax()]["Metric"], scores.loc[scores['Precision'].idxmax()]["Precision"])
    print("Higest Accuracy score: ", scores.loc[scores['Accuracy'].idxmax()]["Metric"], scores.loc[scores['Accuracy'].idxmax()]["Accuracy"])
    
