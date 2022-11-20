from PyQt5.QtWidgets import QMainWindow
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas)

from UI.PlotWindowUI import Ui_PlotWindow

class PlotWindow(QMainWindow, Ui_PlotWindow):
    def __init__(self):
        super(PlotWindow, self).__init__()
        Ui_PlotWindow().setupUi(self)
    def show(self) -> None:
        self.canvas = FigureCanvas(plt.gcf())
        # 将绘制好的图像设置为中心 Widget
        # self.window.addToolBar(NavigationToolbar(self.window.canvas, self.window))
        # self.window.vlayout = QVBoxLayout()
        # self.window.vlayout.addWidget(self.window.canvas)  # 画布添加到窗口布局中
        # self.window.setLayout(self.window.vlayout)
        self.setCentralWidget(self.canvas)
        # 创建figure对象
        super().show()