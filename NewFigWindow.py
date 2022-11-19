from PyQt5.QtWidgets import QMainWindow, QMessageBox

import NewFigWindowUI
from m_plot import new_plot


class NewFigWindow(QMainWindow, NewFigWindowUI.Ui_NewFigWindow):
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
        new_plot(self.xlaLlineEdit.text(), self.ylaLineEdit.text(), self.titLineEdit.text())
        QMessageBox.information(self, '新建图片', '新建图片成功', QMessageBox.Yes, QMessageBox.Yes)
        self.close()
