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

    if len(sys.argv) != 3:
        print("Usage : python interrater_reliability.py <csv_file1> <csv_file2>")
        sys.exit(1)
    
    csv_file1 = sys.argv[1]
    csv_file2 = sys.argv[2]
    if not os.path.exists(csv_file1):
        print(f"Error : {csv_file1} does not exist.")
        sys.exit(1)
    elif not os.path.exists(csv_file2):
        print(f"Error : {csv_file2} does not exist.")
        sys.exit(1)

    with open(csv_file1, mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        y_pred1 = []
        for row in reader:
            y_pred1.append(row[4])
        
    with open(csv_file2, mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        y_pred2 = []
        for row in reader:
            y_pred2.append(row[4])
    
    y_pred1 = np.array(y_pred1).astype(int)
    y_pred2 = np.array(y_pred2).astype(int)

    assert len(y_pred1) == len(y_pred2), "Error : the two csv files must have the same length."
    print("Cohen's kappa score : ", kappa_score(y_pred1, y_pred2))
