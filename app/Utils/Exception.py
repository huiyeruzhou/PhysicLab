from PyQt5.QtWidgets import QMessageBox


class BusinessException(Exception):
    def __init__(self, name="", disc=""):
        self.name = name
        self.disc = disc

    def __str__(self):
        return f'{self.name}:{self.disc}'


class LatexSyntaxError(BusinessException):
    def __init__(self, str):
        super(LatexSyntaxError, self).__init__(
            name="无法渲染的Latex公式",
            disc="请检查内容是否符合latex格式,"
                 "如果您不想使用latex,请在'$'符号前加\\" + str
        )


def exception_handler(window, e, tit='错误', txt=''):
    if txt == '':
        txt = str(e)
    QMessageBox.critical(window, tit, txt, buttons=QMessageBox.Ok,
                         defaultButton=QMessageBox.Ok)
