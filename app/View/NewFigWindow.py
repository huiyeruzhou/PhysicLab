from PyQt5.QtWidgets import QMainWindow, QMessageBox

from app.Controller import MainController

from app.View.NewFigWindowUI import Ui_NewFigWindow


class NewFigWindow(QMainWindow, Ui_NewFigWindow):
    def __init__(self, model, controller: MainController):
        super(NewFigWindow, self).__init__()
        self._m = None
        self._c: MainController = controller
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
            self._c.new_fig(self.xlaLlineEdit.text(),
                           self.ylaLineEdit.text(),
                           self.titLineEdit.text())

        except ValueError as e:
            QMessageBox.critical(self, '非法输入', '请检查输入的内容是否符合latex语法: ' + str(e), QMessageBox.Yes,
                                 QMessageBox.Yes)
        else:
            QMessageBox.information(self, '新建图片', '新建图片成功', QMessageBox.Yes, QMessageBox.Yes)
            self.close()
