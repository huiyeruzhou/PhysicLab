import os
import sys
from itertools import product

from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QStringListModel

import window2
import window3
from m_plot import *
from qaqui import *

class NewFigWindow(QMainWindow, window3.Ui_NewFigWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def doNewFigButtonOnClicked(self):
        if self.xlaLlineEdit.text() == "":
            ret = QMessageBox.warning(self, '确认新建图片', "确认新建图片吗? 还没有填写x轴单位", buttons=QMessageBox.Yes |QMessageBox.No,
                                defaultButton=QMessageBox.No)
        elif self.ylaLineEdit.text() == "":
            ret = QMessageBox.warning(self, '确认新建图片', "确认新建图片吗? 还没有填写y轴单位", buttons=QMessageBox.Yes |QMessageBox.No,
                                defaultButton=QMessageBox.No)
        elif self.titLineEdit.text() == "":
            ret = QMessageBox.warning(self, '确认新建图片', "确认新建图片吗? 还没有填写图片标题", buttons=QMessageBox.Yes |QMessageBox.No,
                                defaultButton=QMessageBox.No)
        else:
            ret = QMessageBox.Yes
        if ret != QMessageBox.Yes:
            return
        new_plot(self.xlaLlineEdit.text(), self.ylaLineEdit.text(), self.titLineEdit.text())
        QMessageBox.information(self, '新建图片', '新建图片成功', QMessageBox.Yes, QMessageBox.Yes)


class MainWindow(QMainWindow, Ui_MainWindow):  # 继承自 QWidget类
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.data = None
        self.col_var = {}
        self.initUI()  # 创建窗口

        self.cpactionMenu.triggered.connect(self.table_copy)
        self.importColMenu.triggered.connect(self.get_col_var)

        self.colVarTableView.clicked.connect(self.colVarTabelViewOnClicked)

    # def saveFigButtonOnClicked(self):
    #     if len(plt.get_fignums()) == 0:
    #         QMessageBox.warning(self, '无法保存图片', "请先新建图片", buttons=QMessageBox.Ok,
    #                             defaultButton=QMessageBox.Ok)
    #         return
    #     save_plot()

    def LoadExcelButtonOnClicked(self):
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(self, "选取文件", os.getcwd(),
                                                                   "Excel Files(*.xls;*.xlsx;*.xlsm;*.xlsb;*.odf);;All Files(*)")
        self.read_excel(fileName)
        pass

    def read_excel(self, path):
        # 打开文件
        # 由于这里会触发信号槽，所以我们先阻断信号
        self.tableWidget.blockSignals(True)
        self.data: pd.DataFrame = pd.read_excel(path)
        # 获取所有sheet
        # sheet2_name = workbook.sheet_names()[0]
        # 根据sheet索引或者名称获取sheet内容
        xlsx_row_nums, xlsx_col_nums = self.data.shape
        # 设置表头
        for i in range(xlsx_row_nums):
            # 在tablewidget中添加行
            self.tableWidget.insertRow(i)
        for i in range(xlsx_col_nums):
            # 在tablewidget中添加行
            self.tableWidget.insertColumn(i)

        head = [str(i) for i in self.data.columns]
        self.tableWidget.setHorizontalHeaderLabels(head)
        # 获取整行和整列的值（数组）
        for i in range(xlsx_row_nums):
            rowslist = self.data.iloc[i, :]  # 获取excel每行内容

            for j in range(xlsx_col_nums):
                # 把数据写入tablewidget中
                newItem = QTableWidgetItem(str(rowslist[j]))
                self.tableWidget.setItem(i, j, newItem)
        self.tableWidget.blockSignals(False)

    def initUI(self):
        self.clipboard = QApplication.clipboard()
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.contextMenu = QMenu(self.tableWidget)
        self.cpactionMenu = self.contextMenu.addAction('复制内容')
        self.importColMenu = self.contextMenu.addAction('导入为列向量')
        self.tableWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)

        # 实例化列表模型，添加数据
        self.colVarModel = QStringListModel()
        self.setColVarTabelView()
        self.show()
        self.showFigWindow: QMainWindow = QMainWindow()
        self.showFigWindowUi = window2.Ui_MainWindow()
        self.showFigWindowUi.setupUi(self.showFigWindow)

        self.newFigWindow = NewFigWindow()

    # def getInt(self):
    #     num, ok = QInputDialog.getInt(self, 'Integer input dialog', '输入数字')
    #     if ok and num:
    #         self.GetIntlineEdit.setText(str(num))
    #
    # def getStr(self):
    #     text, ok = QInputDialog.getText(self, 'Text Input Dialog', '输入姓名：')
    #     if ok and text:
    #         self.GetstrlineEdit.setText(str(text))

    def newFigButtonOnClicked(self):
        # QInputDialog.accept()
        self.newFigWindow.show()


    def addLineButtonOnClicked(self):
        if len(plt.get_fignums()) == 0:
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
        elif self.getXLineEdit.text() not in self.col_var:
            QMessageBox.warning(self, '无法添加线条', "x轴数据数据不在已经导入的列向量中", buttons=QMessageBox.Ok,
                                defaultButton=QMessageBox.Ok)
            return
        elif self.getYLineEdit.text() not in self.col_var:
            QMessageBox.warning(self, '无法添加线条', "y轴数据数据不在已经导入的列向量中", buttons=QMessageBox.Ok,
                                defaultButton=QMessageBox.Ok)
            return

        x = self.col_var[self.getXLineEdit.text()]
        y = self.col_var[self.getYLineEdit.text()]
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
        try:
            m_plot(x, y, leg)
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

        plt.legend()
        plt.gcf().set_size_inches(6.4, 4.8)
        plt.gcf().dpi = 100
        self.showFigWindow.canvas = FigureCanvas(plt.gcf())
        # 将绘制好的图像设置为中心 Widget
        # self.window.addToolBar(NavigationToolbar(self.window.canvas, self.window))
        # self.window.vlayout = QVBoxLayout()
        # self.window.vlayout.addWidget(self.window.canvas)  # 画布添加到窗口布局中
        # self.window.setLayout(self.window.vlayout)
        self.showFigWindow.setCentralWidget(self.showFigWindow.canvas)
        # 创建figure对象
        self.showFigWindow.show()

    def colVarTabelViewOnClicked(self):
        pass

    def getXButtonOnClicked(self):
        items = self.col_var.keys()
        if len(items) is 0:
            QMessageBox.warning(self, '无法选择数据', "已导入的向量为空,请先导入向量", buttons=QMessageBox.Ok,
                                defaultButton=QMessageBox.Ok)
            return
        else:
            item, ok = QInputDialog.getItem(self, "select input dialog", '列向量', items, 0, False)
            if ok and item:
                self.getXLineEdit.setText(str(item))

    def getYButtonOnClicked(self):
        items = self.col_var.keys()
        if len(items) is 0:
            QMessageBox.warning(self, '无法选择数据', "已导入的向量为空,请先导入向量", buttons=QMessageBox.Ok,
                                defaultButton=QMessageBox.Ok)
            return
        item, ok = QInputDialog.getItem(self, "select input dialog", '列向量', items, 0, False)
        if ok and item:
            self.getYLineEdit.setText(str(item))

    def saveFigButtonOnClicked(self):
        if len(plt.get_fignums()) == 0:
            QMessageBox.warning(self, '无法保存图片', "请先生成图片", buttons=QMessageBox.Ok,
                                defaultButton=QMessageBox.Ok)
            return
        filename,filetype = QFileDialog.getSaveFileName(self, "保存文件", os.getcwd(),
                                                 "png files (*.png);;all files(*.*)")
        save_plot(filename)

    def showMenu(self):  # 右键展示菜单，pos 为鼠标位置
        # 菜单显示前，将它移动到鼠标点击的位置
        if self.data is None:
            QMessageBox.warning(self, '无法操作表格', "没有打开excel文件,请先导入excel数据", buttons=QMessageBox.Ok,
                                defaultButton=QMessageBox.Ok)
            return
        self.contextMenu.exec_(QCursor.pos())  # 在鼠标位置显示

    def get_col_var(self):
        selectRect = self.tableWidget.selectedRanges()
        if selectRect is None:
            QMessageBox.warning(self, '无法导入向量数据', "没有选择任何区域", buttons=QMessageBox.Ok,
                                defaultButton=QMessageBox.Ok)
            return
        for r in selectRect:  # 获取范围边界
            top = r.topRow()
            left = r.leftColumn()
            bottom = r.bottomRow()
            right = r.rightColumn()
            for col in range(left, right + 1):
                self.col_var[self.data.columns[col]] = self.data.iloc[top: bottom + 1, col]
        print(self.col_var)
        self.setColVarTabelView()

    def table_update(self):
        items = self.tableWidget.selectedItems()
        for i in items:  # 获取范围边界
            self.data.iloc[i.row(), i.column()] = i.text()

    def table_copy(self):
        selectRect = self.tableWidget.selectedRanges()
        self.text = str()
        for r in selectRect:  # 获取范围边界
            top = r.topRow()
            left = r.leftColumn()
            bottom = r.bottomRow()
            right = r.rightColumn()
            column_n = right - left + 1
            row_n = bottom - top + 1
            number = row_n * column_n
            c = []
            for i in range(number):
                c.append(' \t')  # 注意，是空格+\t
                if (i % column_n) == (column_n - 1):
                    c.append('\n')
                else:
                    pass
                # 这里生成了一个列表，大小是：行X（列+1），换行符占了一列。
                # 默认情况下，列表中全部是空格，
            c.pop()  # 删去最后多余的换行符

            range1 = range(top, bottom + 1)
            range2 = range(left, right + 1)
            for row, column in product(range1, range2):
                try:
                    data = self.tableWidget.item(row, column).text()
                    number2 = (row - top) * (column + 1) + (column - left)
                    c[number2] = data + '\t'
                    # 计算出单元格的位置，替换掉原来的空格。
                except:
                    pass
            for s in c:
                self.text = self.text + s
        self.clipboard.setText(self.text)
        self.text = str()  # 字符串归零

    def setColVarTabelView(self):
        self.colVarModel.setStringList(self.col_var)
        self.colVarTableView.setModel(self.colVarModel)


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    path = 'qaq.png'
    app.setWindowIcon(QIcon(path))  # MAC 下 程序图标是显示在程序坞中的， 切记；
    window = MainWindow()
    sys.exit(app.exec_())
