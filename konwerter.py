import sys
import os
import json
import yaml
from lxml import etree
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
import threading

def parse_args():
    if len(sys.argv) != 3:
        print("Usage: program.exe pathFile1.x pathFile2.y")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    if not os.path.isfile(input_path):
        print(f"Input file {input_path} does not exist.")
        sys.exit(1)

    return input_path, output_path

def load_json(file_path):
    with open(file_path, 'r') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {file_path}")
            sys.exit(1)
    return data

def save_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

if __name__ == '__main__':
    input_file, output_file = parse_args()
    if input_file.endswith('.json'):
        data = load_json(input_file)
        if output_file.endswith('.json'):
            save_json(data, output_file)