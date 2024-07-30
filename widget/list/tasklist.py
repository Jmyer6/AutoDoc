from PySide6.QtCore import QEasingCurve,Qt,QPoint,QRect,Signal,QTimer,QEvent,QSize
from PySide6.QtGui import  QCursor, QMouseEvent,QRegion,QPainterPath,QResizeEvent,QPainter,QPixmap,QFocusEvent
from PySide6.QtWidgets import QFrame,QWidget,QVBoxLayout,QScrollArea,QApplication,QLabel,QListWidget,QListWidgetItem,QHBoxLayout

from qss import Color_,ColorStyle,QssPlusClass,themes,BorderStyle
from lib import QcolorToStr

from ..scrollbar import ScrollDelegate
from ..checkbox import CheckBox
from ..infobar import SuccessColor
from ..icon import IconView,Icon
from ..label import LabelNormal


class TaskList(QListWidget):
    def __init__(self, *args, **kwargs):
        super(TaskList, self).__init__(*args, **kwargs)
        self._sroll=ScrollDelegate(self)
        self._list=[]

        self.__SetQss()
        themes.colorchanged.connect(self.__SetQss)

    def __SetQss(self):    
        self.setStyleSheet("QListWidget{background:rgba(0,0,0,0);border-radius:5px;outline:none;"
                           "border:1px solid rgba("+QcolorToStr(Color_(ColorStyle.Color,10).GetColor())+");"
                           "border-bottom:1px solid rgba("+QcolorToStr(Color_(ColorStyle.Color,20).GetColor())+")}"
                           
                           "QListWidget::item{border:none;outline:none}"
                           "QListWidget::item:hover{border:none;outline:none}"
                           "QListWidget::item:selected{border:none;outline:none}"
                           )

    def AddText(self,Text:str):
        _item=TaskItemItem()
        _item.SetDuration(10)
        _item.SetText(Text)

        _listItem=QListWidgetItem()
        _listItem.setSizeHint(QSize(200,30))
        self.addItem(_listItem)
        self.setItemWidget(_listItem,_item)

        self._list.append(_item)

    def SelectAll(self):
        '''
        全选
        '''
        for item in self._list:
            item.setChecked(True)
            item._ColorCheckout()      

    def SelectTran(self):
        '''
        反选
        '''
        for item in self._list:
            if item.isChecked():
                item.setChecked(False)
                item._Colorout()
            else:
                item.setChecked(True)
                item._ColorCheckout()

    def Clear(self):
        for item in self._list:
            item.deleteLater()
        self._list=[]
        self.clear()

class TaskItemItem(CheckBox):
    def __init__(self,Text:str=""):
        super(TaskItemItem, self).__init__(Text=Text)
        self._tipTime=QTimer()
        self._tipTime.timeout.connect(self.__CloseTip)
        self._tipFrame=None

        self._text.setElidedText(True)

    def AddTip(self):
        if self._tipFrame!=None:
            self._tipFrame.deleteLater()
        
        self._tipFrame=QFrame()

        _tipLayout=QHBoxLayout()
        _tipLayout.setSpacing(0)
        _tipLayout.setContentsMargins(0,0,0,0)

        self._tipFrame.setLayout(_tipLayout)

        _icon=IconView(Icon.success,Color_(SuccessColor),QSize(16,16))
        _tipLayout.addWidget(_icon)

        _text=LabelNormal("运行成功")
        _tipLayout.addWidget(_text)

        _icon.show()
        _text.show()
        
        _icon.setFixedSize(16,24)
        _text.setFixedSize(70,24)
        self._tipFrame.setFixedSize(90,24)

        self.SetRigthWidget(self._tipFrame)

        self._tipTime.start(10000)

    def __CloseTip(self):
        self._tipFrame.deleteLater()
        self._tipFrame=None
        self.SetRigthWidget(None)
        self._tipTime.stop()
        pass

    def SetTempLightqss(self):
        self._TempLightqss.SetBorderWidth(Width=0)
        self._TempLightqss.SetBorderStyle(Style=BorderStyle.solid)
        self._TempLightqss.SetBackgroundColor(Color_(ColorStyle.NullColor,0))
        self._TempLightqss.Set_("outline","none")

    def SetNormalLightqss(self):
        self._NormalLightqss=self._TempLightqss.Copy()
        self._NormalLightqss.SetColor(Color_(ColorStyle.FullColor,100))

    def SetHoverLightqss(self):
        self._HoverLightqss=self._TempLightqss.Copy()
        self._HoverLightqss.SetColor(Color_(ColorStyle.ThemeColor,30))

    def SetCheckHoverLightqss(self):
        self._CheckHoverLightqss=self._TempLightqss.Copy()
        self._CheckHoverLightqss.SetColor(Color_(ColorStyle.ThemeColor,40))

    def SetCheckNormalLightqss(self):
        self._CheckNormalLightqss=self._TempLightqss.Copy()
        self._CheckNormalLightqss.SetColor(Color_(ColorStyle.ThemeColor,0))

    def SetDisabledLightqss(self):
        self._DisabledLightqss=self._TempLightqss.Copy()
        self._DisabledLightqss.SetColor(Color_(ColorStyle.FullColor,50))

    def SetTempDarkqss(self):
        self._TempDarkqss.SetBorderWidth(Width=0)
        self._TempDarkqss.SetBorderStyle(Style=BorderStyle.solid)
        self._TempDarkqss.SetBackgroundColor(Color_(ColorStyle.NullColor,0))
        self._TempDarkqss.Set_("outline","none")

    def SetNormalDarkqss(self):
        self._NormalDarkqss=self._TempDarkqss.Copy()
        self._NormalDarkqss.SetColor(Color_(ColorStyle.FullColor,100))

    def SetHoverDarkqss(self):
        self._HoverDarkqss=self._TempDarkqss.Copy()
        self._HoverDarkqss.SetColor(Color_(ColorStyle.ThemeColor,30))

    def SetCheckHoverDarkqss(self):
        self._CheckHoverDarkqss=self._TempDarkqss.Copy()
        self._CheckHoverDarkqss.SetColor(Color_(ColorStyle.ThemeColor,40))

    def SetCheckNormalDarkqss(self):
        self._CheckNormalDarkqss=self._TempDarkqss.Copy()
        self._CheckNormalDarkqss.SetColor(Color_(ColorStyle.ThemeColor,0))

    def SetDisabledDarkqss(self):
        self._DisabledDarkqss=self._TempDarkqss.Copy()
        self._DisabledDarkqss.SetColor(Color_(ColorStyle.FullColor,50))




    

    