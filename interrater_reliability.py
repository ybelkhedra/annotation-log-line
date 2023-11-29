import numpy as np
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import cohen_kappa_score


def kappa_score(y_true, y_pred):
    """
    Calculates the Cohen's kappa score for two lists
    :param y_true: list of true labels
    :param y_pred: list of predicted labels
    :return: Cohen's kappa score
    """
    return cohen_kappa_score(y_true, y_pred)


if __name__ == "__main__":
    import csv
    import os
    import sys
    from difflib import SequenceMatcher

    if len(sys.argv) != 2:
        print("Usage : python interrater_reliability.py <csv_file>")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    if not os.path.exists(csv_file):
        print(f"Error : {csv_file} does not exist.")
        sys.exit(1)

    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        y_true = []
        y_pred = []
        for row in reader:
            y_pred.append(row[3])
            if SequenceMatcher(None, row[1], row[2]).ratio() == 1:
                y_true.append(1)
            elif SequenceMatcher(None, row[1], row[2]).ratio() < 0.5:
                y_true.append(2)
            else:
                y_true.append(3)
    
    y_true = np.array(y_true).astype(int)
    y_pred = np.array(y_pred).astype(int)
    print("Cohen's kappa score : ", kappa_score(y_true, y_pred))
