import numpy as np
from PyQt6.QtWidgets import (QWidget, QHBoxLayout)
from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QPainter, QBrush, QColor, QPen

class CircleModel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(500)

        self.circleCenter = 0
        self.circleRadius = 0
        
        self.CircleUI()

    def CircleUI(self):

        main_layout = QHBoxLayout(self)

        main_layout.addStretch()

        self.setLayout(main_layout)



    def paintEvent(self, event):
        painter = QPainter(self)
        if not painter.isActive():
            return  

        pen = QPen(QColor(125, 125, 125))
        pen.setWidth(2)
        painter.setPen(pen)

        # Large Circle Model
        width = self.width() - 150
        height = self.height()
        # center_x_offset = 150
        self.circleRadius = int(min(width, height) // 2.25)
        self.circleCenter = QPoint(self.rect().center().x(), self.rect().center().y())
        painter.drawEllipse(self.circleCenter, self.circleRadius, self.circleRadius)

        # 0 Marker
        marker_x = self.circleCenter.x()
        marker_y = self.circleCenter.y() + self.circleRadius
        painter.drawLine(marker_x, marker_y - 10, marker_x, marker_y + 10)

        # Boundary Marker
        small_circle_center = QPoint(self.circleCenter.x(), self.circleCenter.y() - self.circleRadius)
        painter.setBrush(QBrush(QColor(125, 125, 125)))
        painter.drawEllipse(small_circle_center.x() - 3, small_circle_center.y() - 3, 6, 6)

        painter.setBrush(QBrush())  # Reset Brush Command. Should do without fill so no need to keep track of brush reset?


        if hasattr(self, 'data') and hasattr(self, 'timeIndex'):
            for i in range(self.data.num_nodes):
                spin = self.data.spins[self.timeIndex * self.data.num_nodes + i]
                x_val = self.data.x_values[self.timeIndex * self.data.num_nodes + i]
                self.NodeDisplay(painter, spin, x_val, 
                                self.circleRadius)
        painter.end()

        
    def fullModelUpdate(self, data, timeIndex):
        self.data = data  # Stores reference, NOT a copy
        self.timeIndex = timeIndex
        self.update()


    def NodeDisplay(self, painter: QPainter, spin, x_val, ModelRadius):
        if spin == 1:
            color = QColor(255, 0, 0)  # Red 
        elif spin == -1:
            color = QColor(0, 0, 255)  # Blue
        
        NodeX = self.circleCenter.x() + ModelRadius * np.cos(np.pi * x_val + np.pi/2)
        NodeY = self.circleCenter.y() + ModelRadius * np.sin(np.pi * x_val + np.pi/2)
        painter.setBrush(color)
        painter.setPen(color)
        painter.drawEllipse(int(NodeX - 15/2), int(NodeY - 15/2), 15, 15) #Node Circle Size = 15
