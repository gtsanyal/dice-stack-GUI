import numpy as np
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                            QRadioButton, QButtonGroup)
from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QPainter, QColor, QPen

class CircleModel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(500)
        self.show_two_circles = False

        self.circCount1 = QRadioButton("One Circle", self)
        self.circCount1.setChecked(True)
        self.circCount2 = QRadioButton("Two Circles", self)
        self.circCount = QButtonGroup(self)

        self.firstCircleCenter = 0
        self.secondCircleCenter = 0
        self.circleRadius = 0
        
        self.CircleUI()

    def CircleUI(self):
        self.circCount.addButton(self.circCount1)
        self.circCount.addButton(self.circCount2)

        self.circCount1.toggled.connect(self.toggle_circles)
        self.circCount2.toggled.connect(self.toggle_circles)

        main_layout = QHBoxLayout(self)

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.circCount1)
        button_layout.addWidget(self.circCount2)
        button_layout.addStretch()

        main_layout.addLayout(button_layout)

        main_layout.addStretch()

        self.setLayout(main_layout)

    def toggle_circles(self):
        self.show_two_circles = self.circCount2.isChecked()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        if not painter.isActive():
            return  

        #pen = QPen(QColor(255, 255, 255))
        pen = QPen(QColor(125, 125, 125))
        # pen.setWidth(4)
        pen.setWidth(2)
        painter.setPen(pen)

        width = self.width() - 150
        height = self.height()
        center_x_offset = 150

        if not self.show_two_circles:
            self.CircleRadius = int(min(width, height) // 2.5)
            self.firstCircleCenter = QPoint(self.rect().center().x() + center_x_offset // 2,
                                            self.rect().center().y())
            self.secondCircleCenter = self.firstCircleCenter

            painter.drawEllipse(self.firstCircleCenter, self.CircleRadius, self.CircleRadius)
            line_x = self.firstCircleCenter.x()
            line_y = self.firstCircleCenter.y() + self.CircleRadius
            painter.drawLine(line_x, line_y-10, line_x, line_y + 10)
        else:
            self.CircleRadius = min(width, height) // 3
            center = self.rect().center()

            self.firstCircleCenter = QPoint(width // 3 + center_x_offset - 100, center.y())
            painter.drawEllipse(self.firstCircleCenter, self.CircleRadius, self.CircleRadius)
            line_x = self.firstCircleCenter.x()
            # zero mark
            line_y = self.firstCircleCenter.y() + self.CircleRadius
            painter.drawLine(line_x, line_y - 10, line_x, line_y + 10)
            # bounary mark
            line_y = self.firstCircleCenter.y() #- self.CircleRadius
            painter.drawLine(line_x, line_y - 10, line_x, line_y + 10)

            self.secondCircleCenter = QPoint(2 * width // 3 + center_x_offset, center.y())
            painter.drawEllipse(self.secondCircleCenter, self.CircleRadius, self.CircleRadius)
            line_x = self.secondCircleCenter.x()
            # zero mark
            line_y = self.secondCircleCenter.y() + self.CircleRadius
            painter.drawLine(line_x, line_y - 10, line_x, line_y + 10)

        if hasattr(self, 'data') and hasattr(self, 'timeIndex'):
            for i in range(self.data.num_nodes):
                spin = self.data.spins[self.timeIndex * self.data.num_nodes + i]
                x_val = self.data.x_values[self.timeIndex * self.data.num_nodes + i]
                self.NodeDisplay(painter, spin, x_val, 
                                self.CircleRadius,
                                self.firstCircleCenter,
                                self.secondCircleCenter)

        painter.end()

        
    def fullModelUpdate(self, data, timeIndex):
        self.data = data  # Stores reference, NOT a copy
        self.timeIndex = timeIndex
        self.update()


    def NodeDisplay(self, painter: QPainter, spin, x_val, ModelRadius, ModelCenter1, ModelCenter0):
        if spin == 1:
            # color = QColor(255, 255, 255)  # White
            color = QColor(255, 0, 0)  # Red
            NodeX = ModelCenter1.x() + ModelRadius * np.cos(np.pi * x_val + np.pi/2)
            NodeY = ModelCenter1.y() + ModelRadius * np.sin(np.pi * x_val + np.pi/2)
        elif spin == -1:
            # color = QColor(255, 0, 0)  # Red
            color = QColor(0, 0, 255)  # Blue
            NodeX = ModelCenter0.x() + ModelRadius * np.cos(np.pi * x_val + np.pi/2)
            NodeY = ModelCenter0.y() + ModelRadius * np.sin(np.pi * x_val + np.pi/2)

        painter.setBrush(color)
        painter.setPen(color)

        circle_size = 15
        painter.drawEllipse(int(NodeX - circle_size/2), int(NodeY - circle_size/2), circle_size, circle_size)
