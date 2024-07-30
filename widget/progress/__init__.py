from PySide6.QtCore import Qt, QRect,QPoint
from PySide6.QtGui import QPainter, QColor, QPen,QConicalGradient
from PySide6.QtWidgets import QFrame
from typing import Union

from lib import Animation,Range360
from qss import themes,Color_,ColorStyle

class CircularProgressBarBase(QFrame):
    def __init__(self):
        super().__init__()
        self._angle = 0
        
    def SetInfo(self,Color1:QColor,Color2:QColor,Percent:Union[str,int],Width:int=20,Corner:bool=True,Direction:bool=True):
        self.SetColor(Color1,Color2,False)
        self.SetPercent(Percent,False)
        self.SetWidth(Width,False)
        self.SetCorner(Corner,False)
        self.SetDirection(Direction,False)
        self.repaint()

    def SetColor(self,Color1:QColor,Color2:QColor,Repaint:bool=True):
        '''
        设置进度条颜色
        color:颜色
        Repaint:刷新显示
        '''
        self._progressColor1 = Color1
        self._progressColor2 = Color2

        if Repaint:
            self.repaint()

    def SetPercent(self,Percent:Union[str,int],Repaint:bool=True):
        '''
        设置进度条进度
        Percent:进度条进度,可以为str或int格式,str是0%-100%,int是0-360
        Repaint:刷新显示
        '''
        if isinstance(Percent,str):#判断是否str格式
            if IsPercent(Percent):#判断是否在0%-100%
                p_=GetPercentValue(Percent)#取str %前的整数
                if p_!=None:
                    self._progressPercent=p_*360/100
        elif isinstance(Percent,int):
            self._progressPercent = Percent

        if Repaint:
            self.repaint()

    def SetWidth(self,Width:int,Repaint:bool=True):
        '''
        设置进度条宽度
        Width:进度条宽度
        Repaint:刷新显示
        '''
        self._progressWidth = Width

        if Repaint:
            self.repaint()
    
    def SetCorner(self,Corner:bool,Repaint:bool=True):
        '''
        设置进度条是否圆角还是直角

        Corner:是否打开圆角
        Repaint:刷新显示
        '''
        self._progressCorner = Corner
        if Repaint:
            self.repaint()

    def SetDirection(self,Direction:bool,Repaint:bool=True):
        '''
        设置进度条顺时针还是逆时针

        Direction:true顺时针 false逆时针
        Repaint:刷新显示
        '''
        self._progressDirection = Direction

        if Repaint:
            self.repaint()

    def paintEvent(self, event):
        _painter = QPainter(self)
        _painter.setRenderHint(QPainter.Antialiasing)

        # 设置圆心和半径
        _center = self.rect().center()
        _radius = min(self.width(), self.height()) // 2 - 10

        # 旋转整个窗口
        _painter.translate(_center.x(), _center.y())
        _painter.rotate(self._angle)
        _painter.translate(-_center.x(), -_center.y())

        self.__DrawWait(_painter, _center, _radius)

    def __DrawWait(self,Painter:QPainter,Center:QPoint,Radius:int):
        _startangle =86

        Painter.setRenderHint(QPainter.Antialiasing)
        _newRect = QRect(Center.x() - Radius, Center.y() - Radius, Radius * 2, Radius * 2)

        _gradient = QConicalGradient(self.width() / 2, self.height() / 2,-270)
        _gradient.setColorAt(0, self._progressColor1)
        _gradient.setColorAt(0.7, self._progressColor1)
        _gradient.setColorAt(1, self._progressColor2)

        _pen = QPen(_gradient, self._progressWidth, Qt.SolidLine)
        if self._progressCorner:
            _pen.setCapStyle(Qt.RoundCap)
        Painter.setPen(_pen)

        if self._progressDirection:
            Painter.drawArc(_newRect, _startangle * 16, -self._progressPercent * 16)
        else:
            Painter.drawArc(_newRect, _startangle * 16, self._progressPercent * 16)

def IsPercent(Percent:str)->bool:
    '''
    判断是否在 0%-100%
    '''
    import re
    # 定义匹配 0% 到 100% 的正则表达式
    _pattern = re.compile(r'^100(\.0{1,2})?%$|^\d{1,2}(\.\d{1,2})?%$')
    # 使用正则表达式进行匹配
    _match = _pattern.match(Percent)
    # 如果匹配成功，返回 True；否则返回 False
    return bool(_match)

def GetPercentValue(Percent:str):
    '''
    获取 0%-100% 前的整数
    '''
    import re
    # 定义匹配 0% 前的整数的正则表达式
    _pattern = re.compile(r'^(\d+)%')
    # 使用正则表达式进行匹配
    _match = _pattern.match(Percent)
    # 如果匹配成功，返回提取到的整数；否则返回 None
    return int(_match.group(1)) if _match else None

class CircularProgressBar(CircularProgressBarBase):
    def __init__(self,*args, **kwargs):
        super(CircularProgressBar,self).__init__(*args, **kwargs)
        self._valueCache=0
        self._direction=True

        self._ani=Animation(0,Duration=1500)
        self._ani.Animationed.connect(self.__RunEvent)
        themes.colorchanged.connect(self.__ColorChangeEvent)

        self.__ColorChangeEvent()
        self.SetPercent(0)
        self.SetWidth(10)
        self.SetCorner(True)
        self.SetDirection(True)

    def __ColorChangeEvent(self):
        self.SetColor(Color_(ColorStyle.ThemeColor,0).GetColor(),Color_(ColorStyle.FullColor,0).GetColor())

    def __RunEvent(self,Value:int):
        if self._direction:
            if self._valueCache>Value:
                self._direction=False
                self._valueCache=0
            else:
                self._valueCache=Value
        else:
            if self._valueCache>Value:
                self._direction=True
                self._valueCache=0
            else:
                self._valueCache=Value

        _anglex=0.5 if self._direction else 1

        self._angle=Range360(Value*_anglex)

        if self._direction:
            self._progressPercent=0.44*Value
        else:
            self._progressPercent=320-0.44*Value
        
        self.repaint()

    def Start(self):
        self._ani.SetLoop(-1,720)

    def Stop(self):
        self._ani.Stop()

