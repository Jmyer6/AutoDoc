from PySide6.QtCore import QEvent, QObject, QPoint,QTimer,QEasingCurve
from PySide6.QtGui import  QCursor
from PySide6.QtWidgets import QWidget

from ..label  import LabelNormal
from ..showway import Popup_

from lib import Position,ShadowEffect
from qss import Color_,ColorStyle

class ToolTip(Popup_):
    def __init__(self, text_:str='', parent=None):
        super(ToolTip, self).__init__(parent=parent)
        #设置窗口属性
        self.SetWindowTool()
        #文本
        self._text=LabelNormal(text_)
        self._showframe.layouts.addWidget(self._text)
        #设置阴影
        self._shadoweffect=ShadowEffect(Color_(ColorStyle.FullColor,70,FixAlpha=70),15,QPoint(0,2))
        self._showframe.setGraphicsEffect(self._shadoweffect)
      
    def setText(self,text_:str):
        self._text.setText(text_)

class ToolTipFilter(QObject):
    """
        创建ToolTipFilter

        Widget:tooltip应用的控件
        PointShift:位置偏移量
        ShowDelay:延迟显示tooltip
        ShowPosition:弹出位置
        ShowType:显示关闭位置
        EasingCurve:显示关闭动画曲线
        Duration:显示关闭动画持续时间
        Opacity:显示关闭透明效果
        MoveMultiple:弹出位置偏移
        PositionAdjuest:是否自动调整位置
        FollowMouse:跟随鼠标
        WindowIn:显示在窗口内
    """
    def __init__(self,
                 Widget:QWidget,
                 PointShift:QPoint=QPoint(8,13),
                 ShowDelay:int=600,
                 ShowPosition:Position=Position.BOTTOM_RIGHT,
                 ShowType: Position = Position.TOP,
                 EasingCurve: QEasingCurve = QEasingCurve.OutQuad,
                 Duration: int = 500,
                 Opacity: bool = False,
                 MoveMultiple: float = 0.5,
                 PositionAdjuest: bool = True,
                 FollowMouse: bool = True,
                 WindowIn:bool=False):
        super().__init__(parent=Widget)
        self._isEnter = False  #判断是否进入控件
        self._tooltip = None   #tooltip对象缓存
        self._widget = Widget  #控件对象
        self._point_shift=PointShift  #位置偏移量
        self._tooltipDelay = ShowDelay  #延迟显示时间
        self._position = ShowPosition  #弹出位置
        self._show_type = ShowType  #显示关闭位置
        self._easingCurves = EasingCurve  #动画曲线
        self._duration = Duration  #动画持续时间
        self._opacity = Opacity  #透明效果
        self._movemultiple = MoveMultiple  #弹出位置偏移
        self._position_adjuest = PositionAdjuest  #是否自动调整位置
        self._follow_mouse = FollowMouse  #跟随鼠标
        self.windows_in_=WindowIn  #是否显示在窗口内

        #创建延迟器
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.__ShowToolTip)
        
    def eventFilter(self, obj: QObject, e: QEvent) -> bool:
        if e.type() == QEvent.ToolTip:
            return True
        
        elif e.type() in [QEvent.Hide, QEvent.Leave, QEvent.Wheel]:
            self._isEnter = False
            self.__HideToolTip()

        elif e.type() == QEvent.Enter:
            self._isEnter = True
    
            if self.__CanShowToolTip():
                if self._tooltip is None:
                    if self.windows_in_:
                        self._tooltip = ToolTip(self._widget.toolTip(),self._widget.window())
                    else:
                        self._tooltip = ToolTip(self._widget.toolTip())
                self.timer.start(self._tooltipDelay)

        elif e.type() == QEvent.MouseButtonPress:
            self.__HideToolTip()
        return super().eventFilter(obj, e)

    def __HideToolTip(self):#隐藏事件
        self.timer.stop()
        if self._tooltip:
            self._tooltip.Close(self._show_type,self._easingCurves,self._duration,self._opacity,self._movemultiple)
            self._tooltip=None

    def __ShowToolTip(self):#显示事件
        if not self._isEnter:
            return

        self._tooltip.setText(self._widget.toolTip())

        if self._follow_mouse:
            self._tooltip.ExecPos(QCursor.pos()+self._point_shift,
                                   self._position,
                                   self._show_type,
                                   self._easingCurves,
                                   self._duration,
                                   self._opacity,
                                   self._movemultiple,
                                   self._position_adjuest,
                                   True)
        else:
            self._tooltip.ExecWindowOut(self._widget,
                                          self._point_shift,
                                          self._position,
                                          self._show_type,
                                          self._easingCurves,
                                          self._duration,
                                          self._opacity,
                                          self._movemultiple,
                                          self._position_adjuest,
                                          True)

    def __CanShowToolTip(self) -> bool: #判断是否可以显示tooltip
        return self._widget.isWidgetType() and self._widget.toolTip() and self._widget.isEnabled()
