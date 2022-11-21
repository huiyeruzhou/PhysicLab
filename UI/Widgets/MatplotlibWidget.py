from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas)
from matplotlib.backends.backend_qt import NavigationToolbar2QT


class MatplotlibWidget(QWidget):
    figChanged = pyqtSignal()
    def __init__(self,parent=None):
        super(MatplotlibWidget, self).__init__(parent)

    def setplot(self, fig):
        if self.layout()==None:
            self.setLayout(QVBoxLayout(self))
        else:
            for i in range(self.layout().count()):
                self.layout().itemAt(i).widget().deleteLater()

        self.canvas:QWidget= FigureCanvas(fig)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvas.draw()
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        self.layout().addWidget(self.toolbar)
        self.layout().addWidget(self.canvas)

        super(MatplotlibWidget, self).update()

    def update(self) -> None:
        self.canvas.resize()
        super(MatplotlibWidget, self).update()