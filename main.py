import sys
import circle_model
import data_processing
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                            QSlider, QLabel, QPushButton)
from PyQt6.QtCore import Qt, QTimer
#from PyQt6.QtGui import QColor, QPalette


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spin Reader")
        self.setGeometry(100, 100, 1300, 700)

        if len(sys.argv) < 2:
            print("Ising machine GUI\n")
            print("Usage: python main.py data_file.dat")
            sys.exit(1)

        self.main_layout = QVBoxLayout()
        self.top_bar_layout = QHBoxLayout()

        # Circle Model & Data
        self.circle_model = circle_model.CircleModel(self)
        self.data_processing = data_processing.DataProcessing()

        # Slider for time control
        self.time_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.data_processing.data_loaded.connect(self.setup_time_slider)
        self.time_label = QLabel("Time: 0.000", self)

        self.ProgressButton = QPushButton("Increase Time", self)
        self.ProgressButton.clicked.connect(self.Progress)
        self.RegressButton = QPushButton("Decrease Time", self)
        self.RegressButton.clicked.connect(self.Regress)
        self.PlayPauseButton = QPushButton("Play", self)
        self.PlayPauseButton.clicked.connect(self.PlayPauseControl)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.Progress)

        self.setLayout(self.main_layout)
        self.initUI()

        self.setup_time_slider()

    def initUI(self):
        # palette = self.palette()
        # palette.setColor(QPalette.ColorRole.Window, QColor(0, 0, 50))
        # self.setPalette(palette)
        self.top_bar_layout.addWidget(QLabel("Time Control:"))
        self.top_bar_layout.addWidget(self.time_slider)
        self.top_bar_layout.addWidget(self.time_label)
        self.main_layout.addLayout(self.top_bar_layout)
        self.main_layout.addWidget(self.circle_model)
        self.main_layout.addWidget(self.data_processing)
        self.top_bar_layout.addWidget(self.RegressButton)
        self.top_bar_layout.addWidget(self.PlayPauseButton)
        self.top_bar_layout.addWidget(self.ProgressButton)
        self.time_slider.setMinimum(0)  
        self.time_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.time_slider.valueChanged.connect(self.update_time)

    def Progress(self):
        if self.time_slider.value() < self.time_slider.maximum():
            self.time_slider.setValue(self.time_slider.value() + 1)

    def Regress(self):
        if self.time_slider.value() > self.time_slider.minimum():
            self.time_slider.setValue(self.time_slider.value() - 1)

    def setup_time_slider(self):
        if self.data_processing.times:
            self.time_slider.setEnabled(True)
            self.time_slider.setTracking(True)
            max_time_index = len(self.data_processing.times) - 1
            self.time_slider.setMaximum(max_time_index)
            self.update_time(0)

        else:
            self.time_slider.setEnabled(False)

    def update_time(self, timeIndex):
        if self.data_processing.times:
            current_time = self.data_processing.times[timeIndex]
            self.time_label.setText(f"Time: {current_time:.3f}")
            self.circle_model.fullModelUpdate(self.data_processing, timeIndex)

    def PlayPauseControl(self):
        if self.PlayPauseButton.text() == "Play":
            self.PlayPauseButton.setText("Pause")
            self.timer.start(100) #Make choosable
        else:
            self.PlayPauseButton.setText("Play")
            self.timer.stop()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
