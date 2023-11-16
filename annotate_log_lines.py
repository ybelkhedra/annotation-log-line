import os
import random
import csv

# Function to get random line pairs
def get_random_line_pairs(root_folder, n_pairs):
    line_pairs = []

    # Exploring folders and files
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if n_pairs == 0:
                return line_pairs
            if file == "failure.log" or file == "success.log":
                file_path_success = os.path.join(root, "success.log")
                file_path_failure = os.path.join(root, "failure.log")
                with open(file_path_failure, 'r') as f_failure:
                    with open(file_path_success, 'r') as f_success:
                        lines_success = f_success.readlines()
                        lines_failure = f_failure.readlines()
                        # Getting random line pairs
                        if len(lines_success) > 0 and len(lines_failure) > 0:
                            i = random.randint(0, min(len(lines_success), len(lines_failure)))
                            #try to get ith line of success and failure log and if fails do nothing
                            try:
                                line_success = lines_success[i]
                                line_failure = lines_failure[i]
                                line_pairs.append([line_success, line_failure])
                                n_pairs -= 1
                            except:
                                pass

    return line_pairs 

# Function to get user annotation
def get_annotation():
    print("Choose the annotation for this paired lines :")
    print("1. Same")
    print("2. Strictly different")
    print("3. Modified")
    while True:
        choice = input("Your choice (1/2/3) : ")
        if choice in ['1', '2', '3']:
            return choice
        else:
            print("Please enter 1, 2 or 3.")


if __name__ == "__main__":

    data_folder = "dataset"
    n_pairs = 5
    pairs = get_random_line_pairs(data_folder, n_pairs)

    print(len(pairs), "pairs of lines randomly selected.")

    # Creation of a CSV file to save the annotations
    csv_file = "annotations.csv"

    #Writing line pairs and annotations in the CSV file
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['line', 'line2', 'annotation'])
        for pair in pairs:
            print("First line:", pair[0])
            print("Second line:", pair[1])
            annotation = get_annotation()
            writer.writerow([pair[0], pair[1], annotation])
            print("Annotation saved :", annotation)
            print("------")

    print(f"Annotations saved in file {csv_file}.")
