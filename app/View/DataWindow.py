from itertools import product

import pandas as pd
from PyQt5.QtCore import Qt, QStringListModel
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import (
    QMainWindow, QMessageBox, QApplication, QAbstractItemView, QTableWidgetItem, QMenu)

from app.Controller.DataController import DataController
from app.Model.MainModel import MainModel
from app.View.DataWindowUI import Ui_DataWindow



class DataWindow(QMainWindow, Ui_DataWindow):  # 继承自 QWidget类
    def __init__(self, model:MainModel, controller:DataController):
        super().__init__()
        self.setupUi(self)
        self.data = None
        self._m = model
        self._c = controller

        self.clipboard = QApplication.clipboard()
        self.tableWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)

        #管理表格邮件菜单
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.contextMenu = QMenu(self.tableWidget)
        self.cpactionMenu = self.contextMenu.addAction('复制内容')
        self.importColMenu = self.contextMenu.addAction('导入为列向量')
        self.cpactionMenu.triggered.connect(self.table_copy)
        self.importColMenu.triggered.connect(self.get_col_var)

        # 实例化列表模型，添加数据
        self.colVarModel = QStringListModel()
        self.setColVarTabelView()
        self.colVarTableView.clicked.connect(self.onColVarTabelViewClicked)

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

    def onColVarTabelViewClicked(self, index):
        pass


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
        self.colVarModel.setStringList(self._m.col_var)
        self.colVarTableView.setModel(self.colVarModel)



