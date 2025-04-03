import sys
from enum import Enum
from PyQt6.QtWidgets import QWidget, QRadioButton, QVBoxLayout, QPushButton, QButtonGroup
from PyQt6.QtCore import pyqtSignal

class DataChoices(Enum):
    SPINONLY = 1
    XONLY = 2
    SPINX = 3

class DataProcessing(QWidget):
    data_loaded = pyqtSignal() #to setup time slider
    def __init__(self):
        super().__init__()
        self.data_choice = None
        self.times = []
        self.spins = []
        self.x_values = []
        self.num_nodes = 0

        self.spinDataButton = QRadioButton("Spin Only (Not Implemented)", self)
        self.xDataButton = QRadioButton("X Only (Not Implemented)", self)
        self.spinXDataButton = QRadioButton("Spin & X", self)
        self.modelDataButtons = QButtonGroup(self)
        self.read_button = QPushButton('Read File', self)

        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout()

        self.spinDataButton.toggled.connect(self.update_data_type)
        self.xDataButton.toggled.connect(self.update_data_type)
        self.spinXDataButton.toggled.connect(self.update_data_type)

        self.read_button.clicked.connect(self.choose_model_file)

        layout.addWidget(self.spinDataButton)
        layout.addWidget(self.xDataButton)
        layout.addWidget(self.spinXDataButton)
        layout.addWidget(self.read_button)

        self.setLayout(layout)

    def update_data_type(self):
        if self.spinDataButton.isChecked():
            self.data_type = DataChoices.SPINONLY
        elif self.xDataButton.isChecked():
            self.data_type = DataChoices.XONLY
        elif self.spinXDataButton.isChecked():
            self.data_type = DataChoices.SPINX

    def choose_model_file(self):
        if self.data_type == DataChoices.SPINONLY:
            data_file_name = 'out_spins.dat'
        elif self.data_type == DataChoices.XONLY:
            data_file_name = 'out_x.dat'
        elif self.data_type == DataChoices.SPINX:
            data_file_name = sys.argv[1]
        else:
            data_file_name = None
            
        if data_file_name:
            try:
                with open(data_file_name, 'r') as file:
                    self.read_from_file(data_file_name)
                    self.data_loaded.emit()
            except FileNotFoundError:
                print(f"File {data_file_name} not found!")
        else:
            print("No file selected or data type is not set.")
    
    def read_from_file(self, filename):
        self.times.clear()
        self.spins.clear()
        self.x_values.clear()
        with open(filename, 'r') as file:
            for line_number, line in enumerate(file):
                values = line.strip().split()

                if not values:
                    continue  

                self.times.append(float(values[0]))

                data_pairs = values[1:]
                if line_number == 0:
                    self.num_nodes = len(data_pairs) // 2

                for i in range(0, len(data_pairs), 2):
                    self.spins.append(int(data_pairs[i])) 
                    self.x_values.append(float(data_pairs[i+1]))

    def __repr__(self):
        return (f"SimulationData(num_nodes={self.num_nodes},\n"
                f"  times={self.times},\n"
                f"  spins={self.spins},\n"
                f"  x_values={self.x_values})")
