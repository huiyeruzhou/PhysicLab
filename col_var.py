col_var = {"X":[1,2,3,4], "Y":[1,1,1,1]}

def critical(parent, e):
    QMessageBox.critical(parent, '错误', print(e), QMessageBox.Yes, QMessageBox.Yes)