import os
import sys
import csv

def remove_stamp(line):
    return line[29:]

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage : python remove_stamp.py <csv_file>")
        sys.exit(1)
    csv_file = sys.argv[1]
    if not os.path.exists(csv_file):
        print(f"Error : {csv_file} does not exist.")
        sys.exit(1)

    #open csv file and create another csv file with the same name but with no time stamp
    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        with open(csv_file[:-4] + "_no_stamp.csv", mode='w') as new_file:
            writer = csv.writer(new_file)
            writer.writerow(["path", "line", "line1", "annotation"])
            for row in reader:
                writer.writerow([row[0],row[1], remove_stamp(row[2]), remove_stamp(row[3]), row[4]])