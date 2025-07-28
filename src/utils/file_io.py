# import json, os, pandas as pd

# def write_json(obj, path):
#     os.makedirs(os.path.dirname(path), exist_ok=True)
#     with open(path, "w", encoding="utf-8") as f:
#         json.dump(obj, f, ensure_ascii=False, indent=2)

# def read_annotations(path="data/annotations.csv"):
#     return pd.read_csv(path)


import json
import os
import pandas as pd

def read_annotations():
    """
    Reads the annotations.csv file and returns a Pandas DataFrame.
    This file is expected to contain the manually labeled text spans.
    """
    annotations_path = "data/annotations.csv"
    if not os.path.exists(annotations_path):
        print(f"Error: {annotations_path} not found.")
        print("Please ensure you have generated the template using scripts/export_spans.py")
        print("and then manually labeled it and saved as data/annotations.csv.")
        exit(1) # Exit if the annotation file is missing

    try:
        df = pd.read_csv(annotations_path)
        # Ensure 'label' column is integer type for consistency
        # This will raise an error if non-integer labels are present,
        # which is good for catching labeling mistakes.
        df['label'] = df['label'].astype(int)
        return df
    except Exception as e:
        print(f"Error reading or processing {annotations_path}: {e}")
        print("Please check the CSV format and ensure 'label' column contains valid integers.")
        exit(1)

def write_json(data, output_path):
    """
    Writes a dictionary to a JSON file.
    Ensures the output directory exists before writing.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)