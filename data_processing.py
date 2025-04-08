import sys
from enum import Enum
from PyQt6.QtWidgets import QWidget, QRadioButton, QVBoxLayout, QPushButton, QButtonGroup, QFileDialog
from PyQt6.QtCore import pyqtSignal


class DataProcessing(QWidget):
    data_loaded = pyqtSignal() #to setup time slider
    def __init__(self):
        super().__init__()
        self.data_choice = None

        self.times = []
        self.spins = []
        self.x_values = []
        self.num_nodes = 0

        self.modelDataButtons = QButtonGroup(self)
        self.read_button = QPushButton('Read .dat File', self)

        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout()

        self.read_button.clicked.connect(self.choose_model_file)

        layout.addWidget(self.read_button)

        self.setLayout(layout)

    def choose_model_file(self):
        # TODO: a proper file choice dialog with an optional CL argument
        self.data_file_name = QFileDialog.getOpenFileName(self, "Select Data File", "", "Text Files (*.dat)")
        file_path = self.data_file_name[0]
        if file_path:
            try:
                self.read_from_file(file_path)

                # with open(self.data_file_name, 'r') as file:
                self.data_loaded.emit()
                # TODO: Multiple exceptions
                # File not found, wrong format, ...
            except FileNotFoundError:
                print(f"ERROR: File {self.data_file_name} not found!")
        else:
            print("ERROR: No file selected or data type is not set.")

    
    def read_from_file(self, file_path):
        self.times.clear()
        self.spins.clear()
        self.x_values.clear()
        with open(file_path, 'r') as file:
            for line_number, line in enumerate(file):
                # Expected format:
                # instance spin-1 X-1 spin-2 X-2 ...
                values = line.strip().split()

                if not values:
                    continue  

                self.times.append(float(values[0]))

                data_pairs = values[1:]
                if line_number == 0:
                    self.num_nodes = len(data_pairs) // 2

                for i in range(0, len(data_pairs), 2):
                    # TODO: Data validation
                    self.spins.append(int(data_pairs[i])) 
                    self.x_values.append(float(data_pairs[i+1]))

    def __repr__(self):
        return (f"SimulationData(num_nodes={self.num_nodes},\n"
                f"  times={self.times},\n"
                f"  spins={self.spins},\n"
                f"  x_values={self.x_values})")
