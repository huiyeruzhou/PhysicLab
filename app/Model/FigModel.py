from PyQt5.QtCore import QObject, pyqtSignal


class FigModel(QObject):
    @property
    def xlabel(self):
        return self._xlabel

    xlabel_changed = pyqtSignal(str)

    @xlabel.setter
    def xlabel(self, xlabel: str):
        self._xlabel = xlabel
        # noinspection PyUnresolvedReferences
        self.xlabel_changed.emit()

    @property
    def ylabel(self):
        return self._ylabel
    ylabel_changed = pyqtSignal(str)
    @ylabel.setter
    def ylabel(self, ylabel:str):
        self._ylabel = ylabel
        # noinspection PyUnresolvedReferences
        self.ylabel_changed.emit()

    @property
    def title(self):
        return self._title
    title_changed = pyqtSignal(str)
    @title.setter
    def title(self, title:str):
        self._title = title
        # noinspection PyUnresolvedReferences
        self.title_changed.emit()

    def __init__(self):
        super(FigModel, self).__init__()
