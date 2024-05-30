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


def xml_to_dict(element):
    if len(element) == 0:
        return element.text
    return {element.tag: {child.tag: xml_to_dict(child) for child in element}}

def dict_to_xml(tag, d):
    elem = etree.Element(tag)
    for key, val in d.items():
        child = etree.SubElement(elem, key)
        if isinstance(val, dict):
            child.extend(dict_to_xml(key, val).getchildren())
        else:
            child.text = str(val)
    return elem

class ConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 400, 200)  # Ustawienie rozmiaru okna na 700x700 pikseli

        self.layout = QVBoxLayout()

        self.label = QLabel("Wybierz plik do konwersji", self)
        self.layout.addWidget(self.label)

        self.btn_open = QPushButton('Plik', self)
        self.btn_open.clicked.connect(self.open_file)
        self.layout.addWidget(self.btn_open)

        self.label_format = QLabel("Wybierz format:", self)
        self.layout.addWidget(self.label_format)

        self.btn_json = QPushButton('Zapisz jako JSON', self)
        self.btn_json.clicked.connect(lambda: self.save_file('json'))
        self.layout.addWidget(self.btn_json)

        self.btn_yaml = QPushButton('Zapisz jako YAML', self)
        self.btn_yaml.clicked.connect(lambda: self.save_file('yaml'))
        self.layout.addWidget(self.btn_yaml)

        self.btn_xml = QPushButton('Zapisz jako XML', self)
        self.btn_xml.clicked.connect(lambda: self.save_file('xml'))
        self.layout.addWidget(self.btn_xml)

        self.setLayout(self.layout)
        self.setWindowTitle('Konwerter')
        self.show()

    def open_file(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;JSON Files (*.json);;XML Files (*.xml);;YAML Files (*.yaml)", options=options)
        if file:
            self.label.setText(f"Opened file: {file}")
            self.input_file = file

    def save_file(self, format):
        options = QFileDialog.Options()
        default_extension = f"*.{format}"
        file, _ = QFileDialog.getSaveFileName(self, "Save File", f"output.{format}", f"All Files (*);;{format.upper()} Files (*.{format})", options=options)
        if file:
            self.label.setText(f"Saved file: {file}")
            self.output_file = file
            self.convert_file(format)

    def convert_file(self, format):
        input_ext = os.path.splitext(self.input_file)[1].lower()
        output_ext = f".{format}"

        load_thread = threading.Thread(target=self.load_and_convert, args=(input_ext, output_ext))
        load_thread.start()

    def load_and_convert(self, input_ext, output_ext):
        if input_ext == '.json':
            data = load_json(self.input_file)
        elif input_ext == '.yaml' or input_ext == '.yml':
            data = load_yaml(self.input_file)
        elif input_ext == '.xml':
            data = load_xml(self.input_file)
        else:
            print("Unsupported input format")
            return

        if output_ext == '.json':
            save_json(data, self.output_file)
        elif output_ext == '.yaml' or output_ext == '.yml':
            save_yaml(data, self.output_file)
        elif output_ext == '.xml':
            save_xml(data, self.output_file)
        else:
            print("Unsupported output format")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        input_file, output_file = parse_args()
        input_ext = os.path.splitext(input_file)[1].lower()
        output_ext = os.path.splitext(output_file)[1].lower()

        if input_ext == '.json':
            data = load_json(input_file)
        elif input_ext == '.yaml' or input_ext == '.yml':
            data = load_yaml(input_file)
        elif input_ext == '.xml':
            data = load_xml(input_file)
        else:
            print("Unsupported input format")
            sys.exit(1)

        if output_ext == '.json':
            save_json(data, output_file)
        elif output_ext == '.yaml' or output_ext == '.yml':
            save_yaml(data, output_file)
        elif output_ext == '.xml':
            save_xml(data, output_file)
        else:
            print("Unsupported output format")
            sys.exit(1)
    else:
        app = QApplication(sys.argv)
        ex = ConverterApp()
        sys.exit(app.exec_())

