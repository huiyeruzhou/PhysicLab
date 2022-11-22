import os
import sys

import numpy as np
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, pyqtSlot, QCoreApplication, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QInputDialog, QWidget, QFileDialog, QApplication

from DataWindow import DataWindow
from MatplotlibPlot import MatplotlibPlot
from NewFigWindow import NewFigWindow
from UI.MainWindowUI import Ui_MainWindow
from col_var import col_var, critical


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.plot = MatplotlibPlot(fig=self.canvas.canvas.figure)
        self.show()
        self.canvas.figChanged.emit()
        self.dataWindow = DataWindow()
        self.newFigWindow = NewFigWindow()
        self.newFigWindow.newFigCreated.connect(self.onNewFigCreated)
        self.newFigWindow.setWindowModality(Qt.ApplicationModal)


    def onGetXButtonClicked(self):
        items = col_var.keys()
        if len(items) is 0:
            QMessageBox.warning(self, '无法选择数据', "已导入的向量为空,请先导入向量", buttons=QMessageBox.Ok,
                                defaultButton=QMessageBox.Ok)
            return
        else:
            item, ok = QInputDialog.getItem(self, "select input dialog", '列向量', items, 0, False)
            if ok and item:
                self.getXLineEdit.setText(str(item))

    def onGetYButtonClicked(self):
        items = col_var.keys()
        if len(items) is 0:
            QMessageBox.warning(self, '无法选择数据', "已导入的向量为空,请先导入向量", buttons=QMessageBox.Ok,
                                defaultButton=QMessageBox.Ok)
            return
        item, ok = QInputDialog.getItem(self, "select input dialog", '列向量', items, 0, False)
        if ok and item:
            self.getYLineEdit.setText(str(item))

    def onAddLineButtonClicked(self):
        if self.plot == None:
            QMessageBox.warning(self, '无法添加线条', "请先新建图片", buttons=QMessageBox.Ok,
                                defaultButton=QMessageBox.Ok)
            return
        elif self.getXLineEdit.text() == "":
            QMessageBox.warning(self, '无法添加线条', "请先选择x轴数据", buttons=QMessageBox.Ok,
                                defaultButton=QMessageBox.Ok)
            return
        elif self.getYLineEdit.text() == "":
            QMessageBox.warning(self, '无法添加线条', "请先选择y轴数据", buttons=QMessageBox.Ok,
                                defaultButton=QMessageBox.Ok)
            return
        elif self.getXLineEdit.text() not in col_var:
            QMessageBox.warning(self, '无法添加线条', "x轴数据数据不在已经导入的列向量中", buttons=QMessageBox.Ok,
                                defaultButton=QMessageBox.Ok)
            return
        elif self.getYLineEdit.text() not in col_var:
            QMessageBox.warning(self, '无法添加线条', "y轴数据数据不在已经导入的列向量中", buttons=QMessageBox.Ok,
                                defaultButton=QMessageBox.Ok)
            return

        x = col_var[self.getXLineEdit.text()]
        y = col_var[self.getYLineEdit.text()]
        x = np.array(x)
        y = np.array(y)
        if len(x) != len(y):
            QMessageBox.critical(self, '无法绘图', "用于绘图的数据应当长度相等, 请重新选择xy轴数据",
                                 buttons=QMessageBox.Ok,
                                 defaultButton=QMessageBox.Ok)
            return
        elif np.any(x[1:] < x[:-1]):
            line_data = np.array([x, y]).T
            line_data = line_data[np.argsort(line_data[:, 0])]
            x = line_data[:, 0]
            y = line_data[:, 1]
        leg = self.LegendEdit.text()

        marker_dict = {"圆圈（默认）": "o", "X型": "x", "朝上的三角": "^", "不加散点": ""}
        try:
            self.plot.m_plot(x, y, leg, marker=marker_dict[self.markerComboBox.currentText()])
        except ValueError as e:
            if str(e).startswith('The number of derivatives'):
                QMessageBox.critical(self, '无法绘图', "插值绘图需要至少四个数据点, 请重新选择列向量",
                                     buttons=QMessageBox.Ok,
                                     defaultButton=QMessageBox.Ok)
            elif str(e) == 'Array must not contain infs or nans.':
                QMessageBox.critical(self, '无法绘图', "数据中不应含有nan或inf, 请重新选择列向量",
                                     buttons=QMessageBox.Ok,
                                     defaultButton=QMessageBox.Ok)
            else:
                QMessageBox.critical(self, '无法绘图', str(e), buttons=QMessageBox.Ok,
                                     defaultButton=QMessageBox.Ok)
            return

        self.plot.axes.legend()
        self.canvas.figChanged.emit()

    def onSaveFigButtonClicked(self):
        if self.plot is None:
            QMessageBox.warning(self, '无法保存图片', "请先生成图片", buttons=QMessageBox.Ok,
                                defaultButton=QMessageBox.Ok)
            return
        filename, filetype = QFileDialog.getSaveFileName(self, "保存文件", os.getcwd(),
                                                         "png files (*.png);;all files(*.*)")
        self.plot.save_plot(filename)
    def onNewFigButtonClicked(self):
        # QInputDialog.accept()
        self.newFigWindow.show()

    def onFigChanged(self):
        self.plot.fig.set_size_inches(6.4, 4.8)
        self.plot.fig.dpi = 150
        self.canvas.canvas.resize(self.canvas.canvas.size() + QSize(1, 1))
        self.canvas.canvas.resize(self.canvas.canvas.size() - QSize(1, 1))

    def onNewFigCreated(self, plot):
        self.plot: MatplotlibPlot = plot
        self.findChild(QWidget, "canvas").setplot(plot.fig)

    def onLoadExcelButtonClicked(self):
        fileName, fileType = QFileDialog.getOpenFileName(self, "选取文件", os.getcwd(),
                                                         "Excel Files(*.xls;*.xlsx;*.xlsm;*.xlsb;*.odf);;All Files(*)")
        if fileName is "":
            return
        try:
            self.dataWindow.read_excel(fileName)
        except Exception as e:
            critical(self, e)
        self.dataWindow.show()


if __name__ == "__main__":
    QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    path = 'qaq.png'
    app.setWindowIcon(QIcon(path))  # MAC 下 程序图标是显示在程序坞中的， 切记；
    window = MainWindow()
    try:
        ret = app.exec_()
    except Exception as e:
        print(e)
    finally:
        sys.exit(ret)
