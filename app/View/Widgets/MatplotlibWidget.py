import numpy
import matplotlib as mpl
from PyQt5 import QtCore, sip
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas)
from matplotlib.backends.backend_qt import NavigationToolbar2QT
from matplotlib.axes import Axes


class MatplotlibWidget(QWidget):
    mouseMove = QtCore.pyqtSignal(numpy.float64, mpl.lines.Line2D)  # 自定义触发信号，用于与UI交互
    figChanged = pyqtSignal()
    axesChanged = pyqtSignal(Axes)

    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)

    def setplot(self, fig):

        self.canvas = FigureCanvas(fig)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvas.draw()
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        if self.layout() is None:
            self.setLayout(QVBoxLayout(self))
            self.layout().addWidget(self.toolbar)
            self.layout().addWidget(self.canvas)
        else:
            self.layout().replaceWidget(self.layout().itemAt(0).widget(), self.toolbar)
            self.layout().replaceWidget(self.layout().itemAt(1).widget(), self.canvas)

        super(MatplotlibWidget, self).update()

    def update(self) -> None:
        self.canvas.resize()
        super(MatplotlibWidget, self).update()
