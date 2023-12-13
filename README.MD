# Integration Log File Annotation Tool

## Get Started

Ensure you have the following Python packages installed:
```
pip install numpy
pip install scikit-learn
pip install python-Levenshtein
pip install py_stringmatching
pip install jaro-winkler
pip install seaborn
```

## Creating Annotated Pairs of Lines Dataset

This tool provides functionality to generate a dataset in CSV format with the following structure:
```
path, index_line, line1, line2, annotation
```
The 'annotation' column comprises numbers 1, 2, 3 indicating 'same', 'modified', and 'strictly different', respectively.

Usage:
```bash
python3 annotate_log_lines.py <data_folder> <csv_file>
```
Where `<data_folder>` should contain 'failure.log' and 'success.log' files. Subfolders can exist before these files as long as they conclude with 'failure.log' and 'success.log'.

⚠️ Be cautious with folder names containing commas, as this might affect the CSV output. Use the 'rename_folders.py' script to recursively remove commas from folder names:
```bash
python3 rename_folders.py <data_folder>
```
Keep a backup of your folders.

*Note*: Different characters will be highlighted in blue when printed in your terminal.

Post-annotation, you might want to remove timestamps from your dataset using:
```bash
python3 remove_stamp.py <csv_file.py>
```

## Evaluating Annotation Quality

This project includes a tool to assess your annotations. If you annotated a 'csv_file', another person can redo these annotations using:
```bash
python3 annotate_from_csv.py <csv_file>
```
This will generate another 'csv_file'.

Compare them using Cohen's Kappa method:
```bash
python3 interrater_reliability.py <csv_file1> <csv_file2>
```
The output is a number between 0 and 1, where 1 signifies the best score.