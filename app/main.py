import sys
from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from View.MainWindow import MainWindow
from app.Controller.MainController import MainController
from app.Model.MainModel import MainModel

if __name__ == "__main__":
    QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    path = 'qaq.png'
    app.setWindowIcon(QIcon(path))  # MAC 下 程序图标是显示在程序坞中的， 切记；
    model = MainModel()
    controller = MainController(model)
    window = MainWindow(model=model, controller=controller)
    try:
        ret = app.exec_()
    except Exception as e:
        print(e)
    finally:
        sys.exit(ret)