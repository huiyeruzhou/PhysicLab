# from PyQt5.QtCore import QObject
# from PyQt5.QtGui import QCursor
#
# from app.View.Widgets.MatplotlibWidget import MatplotlibWidget
#
#
# class PlotWidgetView(QObject):
#     def __init__(self, view:MatplotlibWidget,model:MainModel, controller:PlotController):
#         self.v = view
#         self._m = model
#         self._c = controller
#
#         self.v.setplot(self._m.fig)
#         self.figure = self.v.canvas.figure
#         # # matplotlib事件绑定
#         # self.__cid = self.v.canvas.mpl_connect("scroll_event", self.do_scrollZoom)  # 支持鼠标滚轮缩放
#         # self.__cid1 = self.v.canvas.mpl_connect("pick_event", self.do_series_pick)  # 支持曲线抓取
#         # # self.__cid2 = self.v.canvas.mpl_connect("button_press_event",self.do_pressMouse)#支持鼠标按下
#         # self.__cid3 = self.v.canvas.mpl_connect("button_release_event", self.do_releaseMouse)  # 支持鼠标释放
#         # self.__cid4 = self.v.canvas.mpl_connect("motion_notify_event", self.do_moveMouse)  # 支持鼠标移动
#         # self.mouseIsPress = False
#         # self.pickStatus = False


        # 公共函数接口

    # def setToolbarVisible(self, isVisible=True):  # 是否显示工具栏
    #     self.__showToolbar = isVisible
    #     self.naviBar.setVisible(isVisible)
    #
    # def setDataHintVisible(self, isVisible=True):  # 是否显示坐标提示
    #     self.__showHint = isVisible
    #     self.__lastActtionHint.setVisible(isVisible)





    # def do_scrollZoom(self, event):  # 通过鼠标滚轮缩放
    #     ax = event.inaxes  # 产生事件axes对象
    #     if ax is None:
    #         return
    #     self.toolbar.push_current()
    #     xmin, xmax = ax.get_xbound()
    #     xlen = xmax - xmin
    #     ymin, ymax = ax.get_ybound()
    #     ylen = ymax - ymin
    #
    #     xchg = event.step * xlen / 20
    #     xmin = xmin + xchg
    #     xmax = xmax - xchg
    #     ychg = event.step * ylen / 20
    #     ymin = ymin + ychg
    #     ymax = ymax - ychg
    #     ax.set_xbound(xmin, xmax)
    #     ax.set_ybound(ymin, ymax)
    #     event.canvas.draw()
    #
    # def do_series_pick(self, event):  # picker事件获取抓取曲线
    #     self.series = event.artist
    #     # index = event.ind[0]
    #     # print("series",event.ind)
    #     if isinstance(self.series, mpl.lines.Line2D):
    #         self.pickStatus = True
    #     if isinstance(event.artist, mpl.axis.Axis):
    #         String = event.artist.get_label_text()
    #         while True:
    #             String, ok = QInputDialog.getText(self, "更改{}轴标注".format(type(event.artist).__name__[0]),
    #                                               "请输入新的标注",
    #                                               text=String)
    #             ##type(event.artist).__name__为"XAxis"或"YAxis"
    #             if ok is True:
    #                 try:
    #                     test_latex(String)
    #                 except Utils as e:
    #                     exception_handler(self, e, tit='非法输入', txt='请检查输入内容是否符合latex语法')
    #                 else:
    #                     event.artist.set_label_text(String)
    #                     self.figChanged.emit()
    #                     return
    #             else:
    #                 return
    #
    #     # if isinstance(event.artist, mpl.axis.XTick):
    #     #     String, ok = QInputDialog.getText(self, "更改标注", "请输入新的标注", text=event.artist.get_label_text())
    #     #     if ok is True:
    #     #         event.artist.axes.get_xaxis().set_label_text(String)
    #     #         self.figChanged.emit()
    #     # if isinstance(event.artist, mpl.axis.YTick):
    #     #     String, ok = QInputDialog.getText(self, "更改标注", "请输入新的标注", text=event.artist.get_label_text())
    #     #     if ok is True:
    #     #         event.artist.axes.get_yaxis().set_label_text(String)
    #     #         self.figChanged.emit()
    #
    # def do_releaseMouse(self, event):  # 鼠标释放，释放抓取曲线
    #     if event.inaxes is None:
    #         return
    #     if self.pickStatus:
    #         self.series.set_color(color="black")
    #         self.figure.canvas.draw()
    #         self.pickStatus = False
    #     # self.mouseRelease.emit(event.xdata,event.ydata)
    #
    # def do_moveMouse(self, event):  # 鼠标移动，重绘抓取曲线
    #     if event.inaxes is None:
    #         return
    #     if self.pickStatus:
    #         self.series.set_xdata([event.xdata, event.xdata])
    #         self.series.set_color(color="red")
    #         self.figure.canvas.draw()
    #         self.mouseMove.emit(event.xdata, self.series)  # 自定义触发信号，用于与UI交互

    