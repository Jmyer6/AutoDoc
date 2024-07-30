from PySide6.QtCore import QSize,QSize,Qt,QPoint,QEasingCurve,Signal,QTimer
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QLineEdit,QHBoxLayout,QFileDialog,QSpinBox,QVBoxLayout

from ..button import ButtonBase
from ..icon import Icon,IconView,IconViews
from ..menu import LineEditMenu

from qss import BorderStyle,Color_,ColorStyle,QssPlusClass,GradientColor,\
    GradientSpread,GradientStyle,GradientColorList,Font_,FontSize
from lib import Position

from typing import Union


class SpinBoxButton(ButtonBase):
    '''
    普通按钮
    '''
    def __init__(self,*args, **kwargs):
        super(SpinBoxButton, self).__init__(*args, **kwargs)
        self.SetFocusType(2)
        self.setFixedSize(13,13)
        #设置鼠标样式
        self.setCursor(Qt.ArrowCursor)
        #按下时钟事件
        self._btnclicktime=QTimer()
        self._btnclicktime.timeout.connect(self.click)
        self.mousepressed.connect(lambda: self._btnclicktime.start(100))
        self.mousereleaseed.connect(self._btnclicktime.stop)

    def SetTempLightqss(self):
        self._TempLightqss.SetBorderWidth(Width=0)
        self._TempLightqss.SetBorderStyle(Style=BorderStyle.solid)
        self._TempLightqss.SetBorderRadius(Radius=3)
        self._TempLightqss.Set_("outline","none")
        self._TempLightqss.SetBackgroundColor(Color_(ColorStyle.NullColor,10,Rshift=-10,Bshift=3))

    def SetTempDarkqss(self):
        self._TempDarkqss.SetBorderWidth(Width=0)
        self._TempDarkqss.SetBorderStyle(Style=BorderStyle.solid)
        self._TempDarkqss.SetBorderRadius(Radius=3)
        self._TempDarkqss.Set_("outline","none")
        self._TempDarkqss.SetBackgroundColor(Color_(ColorStyle.NullColor,10,Rshift=-10,Bshift=3))
        
    def SetNormalLightqss(self):
        self._NormalLightqss=self._TempLightqss.Copy()
        self._NormalLightqss.SetColor(Color_(ColorStyle.FullColor,100))

    def SetHoverLightqss(self):
        self._HoverLightqss=self._TempLightqss.Copy()
        self._HoverLightqss.SetColor(Color_(ColorStyle.ThemeColor,0))

    def SetPressLightqss(self):
        self._PressLightqss=self._TempLightqss.Copy()
        self._PressLightqss.SetColor(Color_(ColorStyle.ThemeColor,10))

    def SetNormalDarkqss(self):
        self._NormalDarkqss=self._TempDarkqss.Copy()
        self._NormalDarkqss.SetColor(Color_(ColorStyle.FullColor,100))

    def SetHoverDarkqss(self):
        self._HoverDarkqss=self._TempDarkqss.Copy()
        self._HoverDarkqss.SetColor(Color_(ColorStyle.ThemeColor,0))

    def SetPressDarkqss(self):
        self._PressDarkqss=self._TempDarkqss.Copy()
        self._PressDarkqss.SetColor(Color_(ColorStyle.ThemeColor,10))


class SpinBox(QSpinBox,QssPlusClass):
    showed = Signal(str)
    def __init__(self,*args, **kwargs):
        super(SpinBox, self).__init__(*args, **kwargs)
        self.QssApply(self,"SpinBox",True,False)


        self._defaultText="0"
        self.lineEdit().textChanged.connect(self.__TextChangeEvent)

        self.__SetLayout()
        self.MouseEventLoad(self)
        self.SetClickFunciton(False)
        #取消原生按钮
        self.setButtonSymbols(QSpinBox.NoButtons)

    def __SetLayout(self):
        self.setFixedHeight(26)

        self.layouts=QHBoxLayout()
        self.layouts.setContentsMargins(6,0,3,0)
        self.layouts.setSpacing(1)
        self.layouts.addStretch(1)
        self.setLayout(self.layouts)
       
        self._btnlayouts=QVBoxLayout()
        self._btnlayouts.setSpacing(2)
        self._btnlayouts.setContentsMargins(0,2,0,3)

        self._btnlayouts.addStretch(1)
        self._up=SpinBoxButton()
        self._up.SetIcon_(Icon.arrow2,QSize(10,10))
        self._up.SetIconClickPositon(Position.TOP)
        self._btnlayouts.addWidget(self._up)
        self._down=SpinBoxButton()
        self._down.SetIcon_(Icon.arrow2,QSize(10,10),IconAngle=180)
        self._down.SetIconClickPositon(Position.BOTTOM)
        self._btnlayouts.addWidget(self._down)
        self._btnlayouts.addStretch(1)

        self._up.clicked.connect(self.stepUp)
        self._down.clicked.connect(self.stepDown)

        self.layouts.addLayout(self._btnlayouts)

    def contextMenuEvent(self, e):
        self.SetMenu()
        LineEditMenu(self).ExecPos(e.globalPos()+QPoint(0,10),Opacity=True,MoveMultiple=0.3,Duration=300)
    
    def Setqss(self):
        self._backgroundcolor=GradientColor()
        self._backgroundcolor.SetStyle(GradientStyle.qlineargradient)
        self._backgroundcolor.SetSpread(GradientSpread.pad)
        self._backgroundcolor.Setp1(0.5,0)
        self._backgroundcolor.Setp2(0.5,1)
        _colorlist=GradientColorList()
        _colorlist.AddColor(0,Color_(ColorStyle.FullColor,2,Rshift=-10,Bshift=3))
        _colorlist.AddColor(0.94,Color_(ColorStyle.FullColor,2,Rshift=-10,Bshift=3))
        _colorlist.AddColor(0.95,Color_(ColorStyle.FullColor,2,Rshift=-10,Bshift=3))
        _colorlist.AddColor(1,Color_(ColorStyle.FullColor,2,Rshift=-10,Bshift=3))
        self._backgroundcolor.SetColorlist(_colorlist)

        self.qss.SetBackgroundColor(self._backgroundcolor)
        self.qss.SetColor(Color_(ColorStyle.FullColor,100))

        self.qss.SetFont(Font_(FontSize=FontSize(Shift=0,Min=10,Max=16)))

        self.qss.SetBorderWidth(Width=1)
        self.qss.SetBorderStyle(Style=BorderStyle.solid)
        self.qss.SetBorderRadius(Radius=5)
        self.qss.SetBorderColor(Color=Color_(ColorStyle.FullColor,10))
        self.qss.SetBorderColor(ColorBottom=Color_(ColorStyle.FullColor,20))

    def _Colorin(self,animation_:bool=True):
        _colorlist=GradientColorList()
        _colorlist.AddColor(0,Color_(ColorStyle.FullColor,2,Rshift=-10,Bshift=3))
        _colorlist.AddColor(0.94,Color_(ColorStyle.FullColor,2,Rshift=-10,Bshift=3))
        _colorlist.AddColor(0.95,Color_(ColorStyle.ThemeColorBackground,20,Rshift=-10,Bshift=3))
        _colorlist.AddColor(1,Color_(ColorStyle.ThemeColorBackground,20,Rshift=-10,Bshift=3))

        self._backgroundcolor.SetColorlist(_colorlist,True)

    def _Colorout(self,animation_:bool=True):
        _colorlist=GradientColorList()
        _colorlist.AddColor(0,Color_(ColorStyle.FullColor,2,Rshift=-10,Bshift=3))
        _colorlist.AddColor(0.94,Color_(ColorStyle.FullColor,2,Rshift=-10,Bshift=3))
        _colorlist.AddColor(0.95,Color_(ColorStyle.FullColor,2,Rshift=-10,Bshift=3))
        _colorlist.AddColor(1,Color_(ColorStyle.FullColor,2,Rshift=-10,Bshift=3))

        self._backgroundcolor.SetColorlist(_colorlist,True)

    def __TextChangeEvent(self,Text:str):
        if Text=="":
            self.lineEdit().setText(self._defaultText)
        elif len(Text)>1 and Text[0]=="0":
            self.setValue(int(Text))
