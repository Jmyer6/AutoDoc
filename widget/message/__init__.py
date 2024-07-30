from PySide6.QtCore import QObject,Signal,QPoint
from PySide6.QtWidgets import QHBoxLayout,QVBoxLayout,QFrame,QSizePolicy,QWidget
from PySide6.QtGui import QColor, QShowEvent

from typing import Union

from ..label import LabelNormal
from ..button import ButtonNormal,ButtonTheme
from ..showway import PopupMessage

from qss import Color_,ColorStyle,FontSize,FontWeight,Font_,QssPlusClass,BorderStyle
from lib import ShadowEffect

class TitleLabel(LabelNormal):
    def __init__(self, *args, **kwargs):
        super(TitleLabel, self).__init__(*args, **kwargs)

    def Setqss(self):
        self.qss.SetColor(Color_(ColorStyle.FullColor,100))
        self.font_=Font_(FontSize=FontSize(Shift=0,Min=10,Max=16),FontWeight=FontWeight.bold)
        self.qss.SetFont(self.font_)
        self.qss.SetPadding(3,4,4,3)
   
class NormalLabel(LabelNormal):
    def __init__(self, *args, **kwargs):
        super(NormalLabel, self).__init__(*args, **kwargs)
        self.SetMaxWidth(400)
    
    def Setqss(self):
        self.qss.SetColor(Color_(ColorStyle.FullColor,100))
        self.font_=Font_(FontSize=FontSize(Shift=0,Min=10,Max=16))
        self.qss.SetFont(self.font_)
        self.qss.SetPadding(3,4,4,3)

class ButtonFrame(QFrame,QssPlusClass):
    clicked=Signal(str)
    def __init__(self, *args, **kwargs):
        super(ButtonFrame,self).__init__(*args, **kwargs) 
        self._ok=None
        self._cancel=None

        self.setFixedHeight(70)
        self.__SetLayout()
        self.QssApply(self,"ButtonFrame",True,False)
        
    def Setqss(self):
        self.qss.SetBackgroundColor(Color_(ColorStyle.FullColor,3,Rshift=-7,Bshift=3))
        self.qss.SetBorderWidth(WidthTop=1)
        self.qss.SetBorderStyle(StyleTop=BorderStyle.solid)
        self.qss.SetBorderRadius(0,0,5,5)
        self.qss.SetBorderColor(ColorTop=Color_(ColorStyle.FullColor,10))

    def __SetLayout(self): 
        self.layouts=QHBoxLayout()
        self.layouts.setSpacing(5)
        self.layouts.setContentsMargins(20,0,20,0)
        self.layouts.addStretch(1)
        self.setLayout(self.layouts)

    def LoadButton(self,OkText:str="确定",CancelText:str=None,OkClickTime:int=0,CancelClickTime:int=0):
        '''
        OkText:确定按钮文字
        CancelText:取消按钮文字
        OkClickTime:确定按钮倒计时
        CancelClickTime:取消按钮倒计时
        '''
        if OkText!=None and OkText!="":
            self._ok=ButtonTheme(OkText)
            self._ok.SetShadow(True)
            self._ok.setMinimumSize(60,30)
            self._ok.clicked.connect(lambda: self.clicked.emit(OkText))
            self._ok.CountDownStart(OkClickTime)
            self.layouts.addWidget(self._ok)
        
        if CancelText!=None and CancelText!="":
            self._cancel=ButtonNormal(CancelText)
            self._cancel.SetShadow(True)
            self._cancel.setMinimumSize(60,30)
            self._cancel.clicked.connect(lambda: self.clicked.emit(CancelText))
            self._cancel.CountDownStart(CancelClickTime)
            self.layouts.addWidget(self._cancel)

    def showEvent(self, event: QShowEvent) -> None:
        if self._ok!=None:
            self._ok.adjustSize()
            self._ok.setFixedSize(self._ok.size())
        if self._cancel!=None:
            self._cancel.adjustSize()
            self._cancel.setFixedSize(self._cancel.size())
        return super().showEvent(event)

class Message(PopupMessage):
    buttonpress=Signal(str)#用来丰富按钮事件
    def __init__(self,Title:str,Content:Union[str,QWidget],OkText:str="确定",CancelText:str=None,OkClickTime:int=0,CancelClickTime:int=0,parent=None):
        super(Message,self).__init__(parent=parent)
        #返回参数
        self._pressText=None

        self._showframe.setMinimumSize(400,200)
        self._showframe.layouts.setContentsMargins(0,0,0,0)
        self._showframe.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        #标签布局
        self._contentLayout=QVBoxLayout()
        self._contentLayout.setSpacing(15)
        self._contentLayout.setContentsMargins(20,15,20,50)

        self._titleLabel=TitleLabel()
        self._titleLabel.setText(Title)
        self._contentLayout.addWidget(self._titleLabel)

        if isinstance(Content,str):
            self._contentLabel=NormalLabel()
            self._contentLabel.setText(Content)
            self._contentLayout.addWidget(self._contentLabel)
        elif isinstance(Content,QWidget):
            self._contentLayout.addWidget(Content)

        self._showframe.layouts.addLayout(self._contentLayout)

        # 按钮布局
        self._buttonFrame=ButtonFrame()
        self._buttonFrame.LoadButton(OkText,CancelText,OkClickTime,CancelClickTime)
        self._buttonFrame.clicked.connect(self.__ButtonClick)
        self._showframe.layouts.addWidget(self._buttonFrame)

        self._showframe.qss.SetBackgroundColor(Color_(ColorStyle.FullColor,0))
        self._showframe.qss.SetBorderRadius(Radius=5)
        self._showframe._qssplus.ApplyQss()

        #阴影
        self._shadow=ShadowEffect(Color_(ColorStyle.FullColor,30),15,QPoint(0,0))
        self._showframe.setGraphicsEffect(self._shadow)

    def Show(self,Widget:QWidget=None,Mask:QObject = None):
        '''
        Widget:定位窗口或控件,None为桌面
        Mask:遮罩窗口
        '''
        self.Exec(Widget=Widget,Duration=300,MoveMultiple=0.1,Mask=Mask)
        return self._pressText

    def __ButtonClick(self,Text:str):
        self._pressText=Text
        self.Close(HideEvent_=lambda: self.close())

