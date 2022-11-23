from typing import List

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QTableWidgetSelectionRange


class DataController(QObject):
    def __init__(self, model):
        super(DataController, self).__init__()
        self._m = model

    def get_col_var(self, selectRect: List[QTableWidgetSelectionRange]):
        for r in selectRect:  # 获取范围边界
            top = r.topRow()
            left = r.leftColumn()
            bottom = r.bottomRow()
            right = r.rightColumn()
            for col in range(left, right + 1):
                self._m.col_var[self._m.data.columns[col]] = self._m.data.iloc[top: bottom + 1, col]
        print(self._m.col_var)

