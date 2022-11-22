from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from matplotlib.figure import Figure
from UI.NewFigWindowUI import Ui_NewFigWindow
from MatplotlibPlot import MatplotlibPlot
from col_var import test_latex


class NewFigWindow(QMainWindow, Ui_NewFigWindow):
    newFigCreated = pyqtSignal(MatplotlibPlot)
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def doNewFigButtonOnClicked(self):
        if self.xlaLlineEdit.text() == "":
            ret = QMessageBox.warning(self, '确认新建图片', "确认新建图片吗? 还没有填写x轴单位",
                                      buttons=QMessageBox.Yes | QMessageBox.No,
                                      defaultButton=QMessageBox.No)
        elif self.ylaLineEdit.text() == "":
            ret = QMessageBox.warning(self, '确认新建图片', "确认新建图片吗? 还没有填写y轴单位",
                                      buttons=QMessageBox.Yes | QMessageBox.No,
                                      defaultButton=QMessageBox.No)
        elif self.titLineEdit.text() == "":
            ret = QMessageBox.warning(self, '确认新建图片', "确认新建图片吗? 还没有填写图片标题",
                                      buttons=QMessageBox.Yes | QMessageBox.No,
                                      defaultButton=QMessageBox.No)
        else:
            ret = QMessageBox.Yes
        if ret != QMessageBox.Yes:
            return
        try:
            test_latex(self.xlaLlineEdit.text())
            test_latex(self.ylaLineEdit.text())
            test_latex(self.titLineEdit.text())

        except ValueError as e:
            QMessageBox.critical(self, '非法输入', '请检查输入的内容是否符合latex语法: ' + str(e), QMessageBox.Yes,
                                 QMessageBox.Yes)
            return
        else:
            plot = MatplotlibPlot(xla=self.xlaLlineEdit.text(), yla=self.ylaLineEdit.text(),
                                  tit=self.titLineEdit.text())

        QMessageBox.information(self, '新建图片', '新建图片成功', QMessageBox.Yes, QMessageBox.Yes)
        self.newFigCreated.emit(plot)
        self.close()
