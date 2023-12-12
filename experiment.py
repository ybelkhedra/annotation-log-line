import sys
import os
import csv
from sklearn.metrics import confusion_matrix
import seaborn as sn
import matplotlib.pyplot as plt


from metrics import python_diff_str, cosine_similarity_str, levenshtein_distance_str, SmithWaterman_str, MongeElkan_str, jarowinkler_str, jaccard_str, ngram_str

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
    metrics = [python_diff_str, cosine_similarity_str, levenshtein_distance_str, SmithWaterman_str, MongeElkan_str, jarowinkler_str, jaccard_str, ngram_str]
    csv_file = "annotations.csv"
    if len(sys.argv) == 2:
        csv_file = sys.argv[1]
    elif len(sys.argv) > 2:
        print("Usage: python3 annotate_log_lines.py [csv_file]. Default is 'annotations.csv'")
        exit(1)
    
    if not os.path.exists(csv_file):
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
        axs.set_ticklabels(['Negative', 'Positive'])
    plt.show()
