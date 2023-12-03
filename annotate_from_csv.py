import os
import sys
import csv
from annotate_log_lines import highlight_diff
from annotate_log_lines import get_annotation

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage : python annotate_from_csv.py <csv_file>")
        sys.exit(1)
    csv_file = sys.argv[1]
    if not os.path.exists(csv_file):
        print(f"Error : {csv_file} does not exist.")
        sys.exit(1)

    #open csv file and create another csv file with the same name but with different annotations

    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        with open(csv_file[:-4] + "ver2.csv", mode='w') as new_file:
            writer = csv.writer(new_file)
            writer.writerow(["path", "line", "line1", "annotation"])
            for row in reader:
                f_line, s_line = highlight_diff(row[1], row[2])
                print("1st line:", f_line)
                print("2nd line:", s_line)
                annotation = get_annotation()
                writer.writerow([row[0], row[1], row[2], annotation])
                print("Annotation saved :", annotation)
                print("------")
        print("New csv file created :", csv_file[:-4] + "_annotated.csv")

