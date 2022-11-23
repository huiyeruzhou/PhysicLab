from PyQt5.QtCore import QObject


from app.Utils.Exception import BusinessException
from app.Model.MainModel import MainModel


class MainController(QObject):

    def __init__(self, mainModel):
        super(MainController, self).__init__()
        self._model: MainModel = mainModel

    def set_legend(self, legend):
        self._model.legend = legend

    def set_x(self, x: str):
        self._model.x = x

    def set_y(self, y: str):
        self._model.y = y

    def get_items_for_choice(self) -> dict:
        item = self._model.col_var
        if len(item) is 0:
            raise BusinessException('无法选择列向量', '当前没有列向量,请先从excel数据中导入列向量')
        else:
            return item

    def onAddLineButtonClicked(self):
        try:
            self._model.addline()
        except BusinessException as e:
            raise e

    def save_plot(self, filename: str):
        self._model.save_plot(filename)

    def addTwinsAxes(self):
        self._model.addTwinsAxes()

    def resize_fig(self):
        self._model.fig.set_size_inches(6.4, 4.8)
        self._model.fig.dpi = 150

    def set_axes(self, axes):
        self._model.active_axes = axes

    def set_fig(self, fig):
        self._model.fig = fig

    def new_fig(self, xla, yla, tit):
        self._model.new_fig(xla,yla,tit)

