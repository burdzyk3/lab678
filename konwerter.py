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

def load_yaml(file_path):
    with open(file_path, 'r') as file:
        try:
            data = yaml.safe_load(file)
        except yaml.YAMLError:
            print(f"Error decoding YAML from {file_path}")
            sys.exit(1)
    return data

def save_yaml(data, file_path):
    with open(file_path, 'w') as file:
        yaml.dump(data, file)

def load_xml(file_path):
    try:
        tree = etree.parse(file_path)
        root = tree.getroot()
        return xml_to_dict(root)
    except etree.XMLSyntaxError:
        print(f"Error decoding XML from {file_path}")
        sys.exit(1)

def save_xml(data, file_path):
    root = dict_to_xml('root', data)
    tree = etree.ElementTree(root)
    tree.write(file_path, pretty_print=True, xml_declaration=True, encoding='UTF-8')


if __name__ == '__main__':
    input_file, output_file = parse_args()
    if input_file.endswith('.json'):
        data = load_json(input_file)
    elif input_file.endswith('.yml') or input_file.endswith('.yaml'):
        data = load_yaml(input_file)
    elif input_file.endswith('.xml'):
        data = load_xml(input_file)

    if output_file.endswith('.json'):
        save_json(data, output_file)
    elif output_file.endswith('.yml') or output_file.endswith('.yaml'):
        save_yaml(data, output_file)
    elif output_file.endswith('.xml'):
        save_xml(data, output_file)
