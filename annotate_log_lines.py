import os
import random
import csv
import sys
import argparse
from remove_stamp import remove_stamp

# Function to get random line pairs
def get_random_line_pairs(root_folder, n_pairs, remove_stamp_bool=False):
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
                                line_success = remove_backslash_n_and_coma(lines_success[i])
                                line_failure = remove_backslash_n_and_coma(lines_failure[i])
                                if remove_stamp_bool:
                                    line_success = remove_stamp(line_success)
                                    line_failure = remove_stamp(line_failure)
                                line_pairs.append([root, i, line_success, line_failure])
                                n_pairs -= 1
                            except:
                                pass
    
    return random.shuffle(line_pairs)

def remove_backslash_n_and_coma(line):
    return line.replace("\n", "").replace(",", "")


def highlight_diff(str1, str2):
    if str1 == str2:
        return str1, str2
    
    highlighted_str1 = ''
    highlighted_str2 = ''
    
    for char1, char2 in zip(str1, str2):
        if char1 == char2:
            highlighted_str1 += char1
            highlighted_str2 += char2
        else:
            highlighted_str1 += f"\033[94m{char1}\033[0m"
            highlighted_str2 += f"\033[94m{char2}\033[0m"
    
    if len(str1) > len(str2):
        highlighted_str1 += f"\033[94m{str1[len(str2):]}\033[0m"
    elif len(str2) > len(str1):
        highlighted_str2 += f"\033[94m{str2[len(str1):]}\033[0m"
    
    
    return highlighted_str1, highlighted_str2


# Function to get user annotation
def get_annotation():
    print("Choose the annotation for this paired lines :")
    print("1. Same")
    print("2. Modified")
    print("3. Strictly different")
    print("4. I don't know")
    print("5. Pass")
    print("6. Save and Exit")
    while True:
        choice = input("Your choice (1/2/3/4/5/6):")
        if choice in ['1', '2', '3', '4', '5', '6']:
            return choice
        else:
            print("Please choose a valid answer.")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--n_pairs", type=int, default=100, help="number of pairs of line to sample on")
    parser.add_argument("-d", "--data_dir", type=str, default="./dataset", help="path of the directory containing the dataset")
    parser.add_argument("-f", "--csv_file", type=str, default="annotations.csv", help="path of the csv file to save the annotations")
    args = parser.parse_args()
    data_folder = args.data_dir
    csv_file = args.csv_file
    n_pairs = args.n_pairs

    n_equals, n_different, n_modified = -1, -1, -1
    
    #ask the user for n_equals, n_different and n_modified
    print("How many pairs of lines should be labeled equal ?")
    n_equals = int(input())
    print("How many pairs of lines should be labeled different ?")
    n_different = int(input())
    print("How many pairs of lines should be labeled modified ?")
    n_modified = int(input())

    assert n_equals + n_different + n_modified <= n_pairs, "The sum of n_equals, n_different and n_modified should be less than n_pairs."
    
    print("Collecting pairs of lines...")
    
    #ask if user wants to remove time stamp
    print("Do you want to remove time stamp ? (y/n)")
    remove_stamp_bool = input()
    if remove_stamp_bool == 'y':
        remove_stamp_bool = True
    else:
        remove_stamp_bool = False
    
    pairs = get_random_line_pairs(data_folder, n_pairs, remove_stamp_bool=remove_stamp_bool)

    print(len(pairs), "pairs of lines randomly selected.")

    #Writing line pairs and annotations in the CSV file
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['path', 'index_line','line1', 'line2', 'annotation'])
        i = 0
        #for pair in pairs:
        while (n_equals > 0 or n_different > 0 or n_modified > 0) and i < len(pairs):
            f_line, s_line = highlight_diff(pairs[i][2], pairs[i][3])
            print("1st line:", f_line)
            print("2nd line:", s_line)
            annotation = get_annotation()
            if annotation == '1' and n_equals > 0:
                writer.writerow([pairs[i][0], pairs[i][1], pairs[i][2], pairs[i][3], annotation])
                print("Annotation saved :", annotation)
                print("------")
                n_equals -= 1
            elif annotation == '2' and n_different > 0:
                writer.writerow([pairs[i][0], pairs[i][1], pairs[i][2], pairs[i][3], annotation])
                print("Annotation saved :", annotation)
                print("------")
                n_different -= 1
            elif annotation == '3' and n_modified > 0:
                writer.writerow([pairs[i][0], pairs[i][1], pairs[i][2], pairs[i][3], annotation])
                print("Annotation saved :", annotation)
                print("------")
                n_modified -= 1
            elif annotation == '4':
                writer.writerow([pairs[i][0], pairs[i][1], pairs[i][2], pairs[i][3], annotation])
                print("Annotation saved :", annotation)
                print("------")
            elif annotation == '5':
                print("------")
            elif annotation == '6':
                break
            i += 1

    print(f"Annotations saved in file {csv_file}.")
