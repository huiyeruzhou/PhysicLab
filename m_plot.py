import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import make_interp_spline
import matplotlib
import matplotlib.colors as mcolors

"""
在matplotlib中使用中文,注意,$$内不能有中文
"""
matplotlib.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

"""
zorder映射,grid最底层, 散点在线条上层
"""
zorder_map = {
    'grid': 10,
    'line': 20,
    'scatter': 30,
}

"""
color管理, 使用getcolor可以自动的选取TABLEAU_COLORS系列中的下一个颜色,
这和matlab默认颜色相同
"""
colors = list(mcolors.TABLEAU_COLORS.keys())
color_index = 0

"""
获得TABLEAU_COLORS颜色系列中未使用的下一个颜色
"""


def get_color():
    global color_index
    color = mcolors.TABLEAU_COLORS[colors[color_index]]
    color_index += 1
    color_index = color_index % len(colors)
    return color


def reset_color():
    global color_index
    color_index = 0


"""
把字符串转换为latex格式
string: 输入字符串
force_add_dollor: 指示是否要对形如'$abc$'的字符串转换为'$$abc$$',默认为False
"""


def to_latex(string, force_add_dollor=False):
    if force_add_dollor is not True and string[0] == string[-1] == '$':
        print("检测到字符串以'$'开头以'$'结尾,没有再在首位添加'$'字符")
        return string
    else:
        return '$' + string + '$'


"""
用插值法绘图, 默认绘出一条平滑曲线, 以散点标注数据点,
并添加图例, 图例内容使用latex格式

a: x轴数据
b: y轴数据
leg: 图例
scatter: 是否绘制散点,默认True
"""


def m_plot(a, b, leg, scatter=True):
    # 在输入区间内均匀选取100个点为插值x轴
    x = np.linspace(a[0], a[-1], 100)
    # 用自带的线条插值法计算y轴值
    y = make_interp_spline(a, b)(x)
    # 绘制平滑曲线,设置图例
    plt.plot(x, y, label=leg, zorder=zorder_map['line'], color=get_color())
    # 绘制数据点,注意去掉图例
    if scatter:
        plt.scatter(a, b, 100, marker='.', label='', zorder=zorder_map['scatter'], color=get_color())


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


def m_plot2(a, b, leg, c=1, scatter=True, curve=True):
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
    plt.plot(x, y, label=leg, zorder=zorder_map['line'], color=get_color())
    # 绘制散点
    if scatter:
        plt.scatter(a, b, 100, marker='.', label='', zorder=zorder_map['scatter'], color=get_color())


"""
保存图片
这个函数充分自注释.
"""


def save_plot(filename):
    plt.legend(loc='upper left')
    plt.savefig(filename, bbox_inches='tight', dpi=400)


"""
新建图片
grid_on: 是否要打开网格,默认为false
"""


def new_plot(xla, yla, tit, grid_on=False):
    reset_color()
    plt.figure(linewidth=0.5)
    plt.xlabel(xla)
    plt.ylabel(yla)
    plt.title(tit)
    if (grid_on):
        plt.minorticks_on()
        plt.grid(which='minor', linestyle=(0, (1, 2)), color='#DFDFDF', zorder=zorder_map['grid'])
        plt.grid(which='major', color='#DFDFDF', zorder=zorder_map['grid'])


"""
从指定pd数据集中获取用于作图的xy数据
data: 数据集
x_col: x在数据中的列
y_col: y在数据中的列
"""


def get_line_xy(data: pd.DataFrame, x_col: int, y_col: int):
    xy: pd.DataFrame = data.iloc[:, [x_col, y_col]].dropna(axis='rows', how='all')
    x = np.array(xy.iloc[:, 0])
    y = np.array(xy.iloc[:, 1])

    # 如果x不是降序, 要对其重新排序
    if np.any(x[1:] < x[:-1]):
        line_data = np.array([x, y]).T
        line_data = line_data[np.argsort(line_data[:, 0])]
        x = line_data[:, 0]
        y = line_data[:, 1]
    return x, y


"""
来试试吧.
"""

if __name__ == "__main__":
    xlsx_filename = r'./工作簿1.xlsx'
    data: pd.DataFrame = pd.read_excel(io=xlsx_filename)

    xla = to_latex(r't/T')
    yla = to_latex(r'\theta / ^ \circ')
    tit = to_latex(r'ln\theta-T') + '图'
    filename = r'阻尼一阻尼三'

    new_plot(True)
    x, y = get_line_xy(data, 0, 1)
    m_plot(x, y, leg='阻尼1')
    save_plot(xla, yla, tit, filename)
