import os
from PyQt5.QtCore import QSize, pyqtSlot, Qt
from PyQt5.QtGui import QCursor

from PyQt5.QtWidgets import QMainWindow, QMessageBox, QInputDialog, QFileDialog, QMenu

from app.Controller.DataController import DataController
from app.Controller.MainController import MainController
from app.Utils.Exception import BusinessException, exception_handler
from app.View.NewFigWindow import NewFigWindow
from app.Model.MainModel import MainModel
from app.View.DataWindow import DataWindow
from app.View.MainWindowUI import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, model: MainModel, controller: MainController):
        super(MainWindow, self).__init__()
        self._m = model
        self._m.setObjectName("mainModel")
        self._c = controller
        self._c.setObjectName("mainController")
        self.setupUi(self)
        self.show()

        self._m.active_axes_changed.connect(self.on_mainModel_active_axes_changed)
        self._m.xchanged.connect(self.on_mainModel_xchanged)
        self._m.y_changed.connect(self.on_mainModel_y_changed)
        self._m.legend_changed.connect(self.on_mainModel_lagend_changed)
        self._m.fig_updated.connect(self.on_mainModel_fig_updated)
        self._m.fig_changed.connect(self.on_mainModel_fig_changed)

        self._m.init()

        self.dataWindow = DataWindow(self._m, DataController(self._m))
        self.newFigWindow = NewFigWindow(self._m, self._c)


        # canvas右键菜单
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.canvas_context_menu = QMenu(self)
        self.addTwinsAxesAction = self.canvas_context_menu.addAction('添加双y轴轴域')
        self.addTwinsAxesAction.triggered.connect(self._c.addTwinsAxes)
        self.customContextMenuRequested.connect(self.onCustomContextMenuRequested)
        # self.newFigWindow.setWindowModality(Qt.ApplicationModal)

    def business_exception_handler(self, e):
        QMessageBox.warning(self, e.name, e.disc, buttons=QMessageBox.Ok,
                            defaultButton=QMessageBox.Ok)

    def on_mainModel_xchanged(self, x):
        self.getXLineEdit.setText(x)

    def on_mainModel_y_changed(self, y):
        self.getYLineEdit.setText(y)

    def on_mainModel_lagend_changed(self, lagend):
        self.LegendEdit.setText(lagend)

    def on_mainModel_fig_updated(self):
        # # self._c.resize_fig()
        self.canvas.canvas.resize(self.canvas.canvas.size() + QSize(1, 1))
        self.canvas.canvas.resize(self.canvas.canvas.size() - QSize(1, 1))

    def on_mainModel_fig_changed(self, fig):
        self.canvas.setplot(fig)

    def on_mainModel_active_axes_changed(self):
        pass

    def onNewFigCreated(self, fig):
        self._c.set_fig(fig)



    @pyqtSlot()
    def on_getXButton_clicked(self):
        try:
            items = self._c.get_items_for_choice()
        except BusinessException as e:
            self.business_exception_handler(e)
        else:
            item, ok = QInputDialog.getItem(self, "select input dialog", '列向量', items, 0, False)
            if ok and item:
                self._c.set_x(str(item))

    @pyqtSlot()
    def on_getYButton_clicked(self):
        try:
            items = self._c.get_items_for_choice()
        except BusinessException as e:
            self.business_exception_handler(e)
        else:
            item, ok = QInputDialog.getItem(self, "select input dialog", '列向量', items, 0, False)
            if ok and item:
                self._c.set_y(str(item))

    @pyqtSlot()
    def on_addLineButton_clicked(self):
        try:
            self._c.onAddLineButtonClicked()
        except BusinessException as e:
            self.business_exception_handler(e)

    @pyqtSlot()
    def on_saveFigButton_clicked(self):
        try:
            filename, filetype = QFileDialog.getSaveFileName(self, "保存文件", os.getcwd(),
                                                             "png files (*.png);;all files(*.*)")
            self._c.save_plot(filename)
        except BusinessException as e:
            self.business_exception_handler(e)

    @pyqtSlot()
    def on_newFigButton_clicked(self):
        # QInputDialog.accept()
        self.newFigWindow.show()

    @pyqtSlot()
    def on_loadExcelButton_clicked(self):
        fileName, fileType = QFileDialog.getOpenFileName(self, "选取文件", os.getcwd(),
                                                         "Excel Files(*.xls;*.xlsx;*.xlsm;*.xlsb;*.odf);;All Files(*)")
        if fileName is "":
            return
        try:
            self.dataWindow.read_excel(fileName)
        except BusinessException as e:
            self.business_exception_handler(e)
        except Exception as e:
            exception_handler(self, e)
        self.dataWindow.show()
    @pyqtSlot(str)
    def on_markerComboBox_currentTextChanged(self,marker):
        self._m.marker = marker
    def onCustomContextMenuRequested(self):
        self.canvas_context_menu.exec_(QCursor.pos())  # 在鼠标位置显示

    @pyqtSlot(str)
    def on_LegendEdit_textChanged(self,str):
        self._c.set_legend(str)

# if __name__ == "__main__":
#     QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
#     app = QApplication(sys.argv)
#     path = 'qaq.png'
#     app.setWindowIcon(QIcon(path))  # MAC 下 程序图标是显示在程序坞中的， 切记；
#     window = MainWindow()
#     try:
#         ret = app.exec_()
#     except Utils as e:
#         print(e)
#     finally:
#         sys.exit(ret)
