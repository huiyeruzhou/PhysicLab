

col_var = {"X": [1, 2, 3, 4], "Y": [1, 1, 1, 1]}


def critical(parent, e: Exception, tit='错误', txt: str = ''):
    from PyQt5.QtWidgets import QMessageBox
    QMessageBox.critical(parent, tit, txt + str(e), QMessageBox.Yes, QMessageBox.Yes)

def test_latex(s):
    from matplotlib.font_manager import FontProperties
    from matplotlib.mathtext import  MathTextParser
    prop = FontProperties()
    parser = MathTextParser('path')
    width, height, depth, _, _ = parser.parse(s, dpi=72, prop=prop)