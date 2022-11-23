import matplotlib
import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from scipy.interpolate import make_interp_spline
from app.Utils.Exception import BusinessException, LatexSyntaxError
from app.Utils.LatexTest import test_latex

"""
在matplotlib中使用中文,注意,$$内不能有中文
"""
matplotlib.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

zorder_map = {
    'grid': 10,
    'line': 20,
    'scatter': 30,
}


class MainModel(QObject):

    @property
    def x(self):
        return self._x

    xchanged = pyqtSignal(str)

    @x.setter
    def x(self, x: str):
        self._x = x
        self.xchanged.emit(x)

    @property
    def y(self):
        return self._y

    y_changed = pyqtSignal(str)

    @y.setter
    def y(self, y: str):
        self._y = y
        self.y_changed.emit(y)

    @property
    def fig(self):
        return self._fig

    fig_changed = pyqtSignal(Figure)
    fig_updated = pyqtSignal()

    @fig.setter
    def fig(self, fig: Figure):
        self._fig = fig
        self.active_axes = fig.gca()
        self.fig_changed.emit(fig)
        self.fig_updated.emit()

    @property
    def col_var(self):
        return self._col_var

    col_var_changed = pyqtSignal(dict)

    @col_var.setter
    def col_var(self, col_var: dict):
        self._col_var = col_var
        self.col_var_changed.emit(col_var)

    @property
    def legend(self):
        return self._legend

    legend_changed = pyqtSignal(str)

    @legend.setter
    def legend(self, legend: str):
        try:
            test_latex(legend)
        except ValueError as e:
            raise LatexSyntaxError(str(e))
        else:
            self._legend = legend
            self.legend_changed.emit(legend)

    @property
    def marker(self):
        return self._marker

    marker_changed = pyqtSignal(str)

    @marker.setter
    def marker(self, marker: str):
        self._marker = marker
        self.marker_changed.emit(marker)

    @property
    def active_axes(self):
        return self._active_axes

    active_axes_changed = pyqtSignal(Axes)

    @active_axes.setter
    def active_axes(self, axes: Axes):
        # self.fig.sca(Axes)
        self._active_axes = axes
        self.active_axes_changed.emit(axes)

    def __init__(self):
        super(MainModel, self).__init__()

    def init(self):
        self.x = ""
        self.y = ""
        self.legend = ""
        self.fig: Figure = self.default_figure()
        self.active_axes: Axes = self.fig.gca()
        # self.active_axes.set_xlabel(xla)
        # self.active_axes.set_ylabel(yla)
        # self.active_axes.set_title(tit)
        # if (grid_on):
        #     self.fig.minorticks_on()
        #     self.fig.grid(which='minor', linestyle=(0, (1, 2)), color='#DFDFDF', zorder=zorder_map['grid'])
        #     self.fig.grid(which='major', color='#DFDFDF', zorder=zorder_map['grid'])
        # self.active_axes.set_prop_cycle(color=list(mcolors.TABLEAU_COLORS.keys()))
        self.active_axes.xaxis.set_picker(True)
        self.active_axes.yaxis.set_picker(True)
        self.active_axes.xaxis.set_pickradius(200)
        self.active_axes.yaxis.set_pickradius(200)
        self.col_var = {"X": [1, 2, 3, 4], "Y": [1, 1, 1, 1]}
        self.marker = '圆圈（默认）'

    def addline(self):
        if self.fig is None:
            raise BusinessException('无法添加线条', "请先新建图片")

        elif self.x == "":
            raise BusinessException('无法添加线条', "请先选择x轴数据")

        elif self.y == "":
            raise BusinessException('无法添加线条', "请先选择y轴数据")

        elif self.x not in self.col_var:
            raise BusinessException('无法添加线条', "x轴数据数据不在已经导入的列向量中")

        elif self.y not in self.col_var:
            raise BusinessException('无法添加线条', "y轴数据数据不在已经导入的列向量中")

        x = self.col_var[self.x]
        y = self.col_var[self.y]
        x = np.array(x)
        y = np.array(y)
        if len(x) != len(y):
            raise BusinessException('无法添加线条', "xy轴数据长度不相同")
        elif np.any(x[1:] < x[:-1]):
            line_data = np.array([x, y]).T
            line_data = line_data[np.argsort(line_data[:, 0])]
            x = line_data[:, 0]
            y = line_data[:, 1]
        leg = self.legend

        marker_dict = {"圆圈（默认）": "o", "X型": "x", "朝上的三角": "^", "不加散点": ""}
        try:
            self.m_plot(x, y, leg, marker=marker_dict[self.marker])
        except ValueError as e:
            if str(e).startswith('The number of derivatives'):
                raise BusinessException('无法绘图', "插值绘图需要至少四个数据点, 请重新选择列向量")
            elif str(e) == 'Array must not contain infs or nans.':
                raise BusinessException('无法绘图', "数据中不应含有nan或inf, 请重新选择列向量")
            else:
                raise BusinessException('无法绘图', str(e))
        self.active_axes.legend()
        self.fig_updated.emit()

    def m_plot(self, a, b, leg, marker="o", scatter=True):
        # 在输入区间内均匀选取100个点为插值x轴
        x = np.linspace(a[0], a[-1], 100)
        # 用自带的线条插值法计算y轴值
        y = make_interp_spline(a, b)(x)
        # 绘制平滑曲线,设置图例
        self.active_axes.plot(x, y, label=leg, zorder=zorder_map['line'])
        # 绘制数据点,注意去掉图例
        if scatter:
            self.active_axes.scatter(a, b, 20, marker=marker, label='', zorder=zorder_map['scatter'])

    def m_plot2(self, a, b, leg, c=1, marker="o", scatter=True, curve=True):
        """
        用拟合法绘图, 默认绘出一条平滑曲线, 以散点标注数据点,
        并添加图例, 图例内容使用latex格式

        a: x轴数据
        b: y轴数据
        c: 拟合多项式次数
        leg: 图例
        scatter: 是否绘制散点,默认True
        curve: 是否插入更多x值以生成平滑曲线,默认True
        """

        # 以ab为输入数据进行c次拟合
        n = np.polyfit(a, b, c)
        # 输出拟合结果
        print(c)

        # 绘制拟合之后的曲线
        if curve:
            # 选取100个点为x轴
            x = np.linspace(a[0], a[-1], 100)
            # 确保数据点也在这些x中,防止丢失关键的峰值等
            x = np.append(a, x)
            # 重新排序
            x.sort()
        # 绘制拟合之后的折线
        else:
            x = a

        # 带入拟合多项式,计算y值
        y = np.polyval(n, x)
        # 绘制曲线
        self.active_axes.plot(x, y, label=leg, zorder=zorder_map['line'])
        # 绘制散点
        if scatter:
            self.active_axes.scatter(a, b, 100, marker=marker, label='', zorder=zorder_map['scatter'])

    def save_plot(self, filename):
        """
        保存图片
        这个函数充分自注释.
        """
        self.fig.savefig(filename, bbox_inches='tight', dpi=400)

    def addTwinsAxes(self):
        self.active_axes = self.active_axes.twinx()

    def new_fig(self, xla, yla, tit):
        try:
            test_latex(xla)
            test_latex(yla)
            test_latex(tit)
        except ValueError as e:
            raise LatexSyntaxError(str(e))
        else:
            self.fig: Figure = self.default_figure()
            self.active_axes.set_xlabel(xla)
            self.active_axes.set_ylabel(yla)
            self.active_axes.set_title(tit)

    def default_figure(self):
        return Figure((6.4, 4.8), 75, linewidth=0.5)
