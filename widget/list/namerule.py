from PySide6.QtCore import QSize,QEasingCurve,QPoint,Signal,Qt
from PySide6.QtGui import  QCursor
from PySide6.QtWidgets import QFrame,QVBoxLayout,QHBoxLayout,QWidget

from .draglist import DragList,DragItem
from ..lineedit import LineEditButton
from ..icon import Icon
from ..button import ButtonBase
from ..showway import Popup_
from ..message import Message
from ..radiobox import RadioBox
from ..label import LabelNormal
from ..lineedit import LineEdit
from ..spinbox import SpinBox
from ..infobar import InfoType

from qss import BorderStyle,Color_,ColorStyle

class NameRuleList(DragList):
    def __init__(self,*args, **kwargs):
        super(NameRuleList, self).__init__(*args, **kwargs)
        self._execlData=None
        self._execlDataIndex=None


        self._textInput=None
        self._numberInput=None
        self._execlInput=None

        self._index=None

        self._rulelist=[]

        self.setFixedHeight(30)
        self.SetListMode(True)
        self.draged.connect(self.__RuleListChange)

    def AddRightButton(self,Suffix:str):

        _rightframe=QFrame()

        _text=LabelNormal()
        _text.setText(Suffix)

        _rightframeLayout=QHBoxLayout()
        _rightframeLayout.setSpacing(5)
        _rightframeLayout.setContentsMargins(0,0,0,0)

        _addButton=LineEditButton()
        _addButton.SetIcon_(Icon.add,QSize(12,12))
        _addButton.setToolTip("载入规则")
        _addButton.setFixedSize(20,20)
        _addButton.clicked.connect(self.__ShowAddRule)

        _rightframeLayout.addWidget(_text)
        _rightframeLayout.addWidget(_addButton)

        _rightframe.setLayout(_rightframeLayout)

        _rightframe.adjustSize()

        self.SetRightWidget(_rightframe)

    def AddExeclData(self,ExeclDate):
        self._execlData=ExeclDate

    def AddExeclDataIndex(self,execlDataIndex:int):
        self._execlDataIndex=execlDataIndex

    def AddNameRule(self,Type:str,Date):
        '''
        Type:类型
        Date:数据
        '''
        _name=NameItem()
        if Type=="文本":
            _name.SetText("文本:"+str(Date))
        elif Type=="数字":
            _name.SetText("数字:从"+str(Date)+"开始")
        elif Type=="execl":
            _namesheet=None

            try:
                _namesheet=self._execlData[Date]
            except:
                self.window()._info.ShowInfo(InfoType.ERROR,"提示:","加载表格["+str(Date)+"]失败!")
                _name=None
                return
            
            _datasheet = self._execlData.worksheets[self._execlDataIndex]
            _maxcol=_datasheet.max_column
            _maxrow=_namesheet.max_row

            if _maxcol!=_maxrow:
                self.window()._info.ShowInfo(InfoType.ERROR,"提示:","无法添加Execl数据,Execl数据表中有"+str(_maxcol)+"行数据,Execl命名表中有"+str(_maxrow)+"个,数量不一致,请检查。")
                _name=None
                return
            
            _name.SetText("Execl表:"+str(Date))
        
        _item=DragItem(QEasingCurve.InOutCubic,300)
        _name.deleted.connect(_item.Delete)
        _name.deleted.connect(self.__DeleteRule)

        _item.AddWidget(_name)

        self._rulelist.append([_item,Type,Date])#缓存数据

        self.AddItem(_item)


    def DragPopup(self):
        self._dragPopup=Popup_()
        self._dragPopup.SetWindowTool()
        self._dragPopup.SetMousePenetration(True)

        _text=self._dragWidget._showframe.layouts.itemAt(0).widget().text()
        self._dragPopup._showframe.layouts.addWidget(NameItem(_text))
        self._dragPopup._showframe.set_shadow()

        self._dragPopup.ExecPos(QCursor.pos()+QPoint(-10,10),Duration=100)

    def __RuleFrame(self):
        from ..combobox import ComBoBox

        _frame=QFrame()
        _frame.setFixedSize(400,100)

        _frameLayout=QVBoxLayout()
        _frameLayout.setSpacing(15)
        _frameLayout.setContentsMargins(0,10,0,0)
        _frame.setLayout(_frameLayout)

        _typeLayout=QHBoxLayout()
        _typeLayout.setSpacing(5)
        _typeLayout.setContentsMargins(0,0,0,0)
        _frameLayout.addLayout(_typeLayout)

        _text=RadioBox("纯文本")
        _number=RadioBox("纯数字")
        _execl=RadioBox("Execl数据")

        _typeLayout.addWidget(_text)
        _typeLayout.addWidget(_number)
        _typeLayout.addWidget(_execl)

        _textInputLayout=QHBoxLayout()
        _textInputLayout.setSpacing(5)
        _textInputLayout.setContentsMargins(0,0,0,0)

        self._text1=LabelNormal("文本:")
        self._text1.setFixedSize(40,30)
        self._textInput=LineEdit()
        self._textInput.setPlaceholderText("请输入文本")

        _textInputLayout.addWidget(self._text1)
        _textInputLayout.addWidget(self._textInput)
        _frameLayout.addLayout(_textInputLayout)

        _numberInputLayout=QHBoxLayout()
        _numberInputLayout.setSpacing(5)
        _numberInputLayout.setContentsMargins(0,0,0,0)

        self._text2=LabelNormal("数字:")
        self._text2.setFixedSize(40,30)
        self._numberInput=SpinBox()
        self._numberInput.setMaximum(9999999)
        self._numberInput.lineEdit().setPlaceholderText("请输入文本")

        _numberInputLayout.addWidget(self._text2)
        _numberInputLayout.addWidget(self._numberInput)
        _frameLayout.addLayout(_numberInputLayout)

        _execlInputLayout=QHBoxLayout()
        _execlInputLayout.setSpacing(5)
        _execlInputLayout.setContentsMargins(0,0,0,0)

        self._text3=LabelNormal("Execl数据:")
        self._text3.setFixedSize(70,30)
        self._execlInput=ComBoBox()
        self._execlInput.setFixedHeight(28)
  
        _execlInputLayout.addWidget(self._text3)
        _execlInputLayout.addWidget(self._execlInput)
        _frameLayout.addLayout(_execlInputLayout)

        _text.toggled.connect(lambda: self.__TypeChange(1))
        _number.toggled.connect(lambda: self.__TypeChange(2))
        _execl.toggled.connect(lambda: self.__TypeChange(3))

        if self._execlData is not None:
            self._execlInput.Addtexts(self._execlData.sheetnames)
            self._execlInput.SetCheck(0)

        _text.toggle()

        return _frame

    def __DeleteRule(self,Item:QWidget):
        for _rule in self._rulelist:
            if Item == _rule[0]:
                self._rulelist.remove(_rule)
                break

    def __ShowAddRule(self):
        _msg=Message("添加命名规则",self.__RuleFrame(),"确定","取消",parent=self.window())

        _str=_msg.Show(self.window(),self.window().userFrame)

        if _str=="确定":
            if self._index is None:
                self.window()._info.ShowInfo(InfoType.ERROR,"提示:","未知错误,请重试!")
            elif self._index == 1:
                self.AddNameRule("文本",self._textInput.text())
            elif self._index == 2:
                self.AddNameRule("数字",self._numberInput.value())
            elif self._index == 3:
                self.AddNameRule("execl",self._execlInput.text())

    def __TypeChange(self,Index:int):
        self._text1.hide()
        self._textInput.hide()
        self._text2.hide()
        self._numberInput.hide()
        self._text3.hide()
        self._execlInput.hide()

        if Index==1:
            self._text1.show()
            self._textInput.show()
        elif Index==2:
            self._text2.show()
            self._numberInput.show()
        elif Index==3:
            self._text3.show()
            self._execlInput.show()
        else:
            self._index=None
            return
        
        self._index=Index

    def __RuleListChange(self):
        _list=[]

        for item in self._list:
            for rule in self._rulelist:
                if rule[0]==item:
                    _list.append(rule)
                    break
            
        self._rulelist= _list
       
class ItemCloseButton(ButtonBase):
    '''
    普通按钮
    '''
    def __init__(self,*args, **kwargs):
        super(ItemCloseButton, self).__init__(*args, **kwargs)
        self.SetFocusType(2)
        self.setFixedSize(16,16)
        #设置鼠标样式
        self.setCursor(Qt.ArrowCursor)

    def SetTempLightqss(self):
        self._TempLightqss.SetBorderWidth(Width=0)
        self._TempLightqss.SetBorderStyle(Style=BorderStyle.solid)
        self._TempLightqss.SetBorderRadius(Radius=3)
        self._TempLightqss.Set_("outline","none")

    def SetTempDarkqss(self):
        self._TempDarkqss.SetBorderWidth(Width=0)
        self._TempDarkqss.SetBorderStyle(Style=BorderStyle.solid)
        self._TempDarkqss.SetBorderRadius(Radius=3)
        self._TempDarkqss.Set_("outline","none")

    def SetNormalLightqss(self):
        self._NormalLightqss=self._TempLightqss.Copy()

        self._NormalLightqss.SetColor(Color_(ColorStyle.Light))
        self._NormalLightqss.SetBackgroundColor(Color_(ColorStyle.FullThemeColorBackground,0))

    def SetHoverLightqss(self):
        self._HoverLightqss=self._TempLightqss.Copy()

        self._HoverLightqss.SetColor(Color_(ColorStyle.Light))
        self._HoverLightqss.SetBackgroundColor(Color_(ColorStyle.FullThemeColorBackground,20))

    def SetPressLightqss(self):
        self._PressLightqss=self._TempLightqss.Copy()

        self._PressLightqss.SetColor(Color_(ColorStyle.Light))
        self._PressLightqss.SetBackgroundColor(Color_(ColorStyle.FullThemeColorBackground,10))

    def SetNormalDarkqss(self):
        self._NormalDarkqss=self._TempDarkqss.Copy()

        self._NormalDarkqss.SetColor(Color_(ColorStyle.Light))
        self._NormalDarkqss.SetBackgroundColor(Color_(ColorStyle.FullThemeColorBackground,0))

    def SetHoverDarkqss(self):
        self._HoverDarkqss=self._TempDarkqss.Copy()

        self._HoverDarkqss.SetColor(Color_(ColorStyle.Light))
        self._HoverDarkqss.SetBackgroundColor(Color_(ColorStyle.FullThemeColorBackground,20))

    def SetPressDarkqss(self):
        self._PressDarkqss=self._TempDarkqss.Copy()

        self._PressDarkqss.SetColor(Color_(ColorStyle.Light))
        self._PressDarkqss.SetBackgroundColor(Color_(ColorStyle.FullThemeColorBackground,10))

class NameItem(ButtonBase):
    '''
    透明按钮
    '''
    deleted=Signal(QWidget)
    def __init__(self,Text:str="",parent=None):
        super(NameItem, self).__init__(Text=Text,objectName="NameItem",parent=parent)

        self._closeButton=ItemCloseButton()
        self._closeButton.SetIcon_(Icon.close,QSize(12,12))
        self._closeButton.clicked.connect(lambda: self.deleted.emit(self))
        self.SetRigthWidget(self._closeButton)

        if self._text is not None:
            self._text.SetAlwayColor(Color_(ColorStyle.Light))

    def SetTempLightqss(self):
        self._TempLightqss.SetBorderWidth(Width=1)
        self._TempLightqss.SetBorderStyle(Style=BorderStyle.solid)
        self._TempLightqss.SetBorderRadius(Radius=5)
        self._TempLightqss.SetBorderColor(Color=Color_(ColorStyle.FullThemeColor,10))
        self._TempLightqss.SetBorderColor(ColorBottom=Color_(ColorStyle.FullThemeColor,20))
        self._TempLightqss.SetPadding(Padding=5)
        self._TempLightqss.Set_("outline","none")
  
    def SetNormalLightqss(self):
        self._NormalLightqss=self._TempLightqss.Copy()

        self._NormalLightqss.SetColor(Color_(ColorStyle.Light))
        self._NormalLightqss.SetBackgroundColor(Color_(ColorStyle.FullThemeColor,0))

    def SetHoverLightqss(self):
        self._HoverLightqss=self._TempLightqss.Copy()

        self._HoverLightqss.SetColor(Color_(ColorStyle.Light))
        self._HoverLightqss.SetBackgroundColor(Color_(ColorStyle.FullThemeColor,7))

    def SetPressLightqss(self):
        self._PressLightqss=self._TempLightqss.Copy()

        self._PressLightqss.SetColor(Color_(ColorStyle.Light))
        self._PressLightqss.SetBackgroundColor(Color_(ColorStyle.FullThemeColor,10))
        self._PressLightqss.SetPadding(6,5,5,6)

    def SetDisabledLightqss(self):
        self._DisabledLightqss=self._TempLightqss.Copy()

        self._DisabledLightqss.SetColor(Color_(ColorStyle.FullColor,50))
        self._DisabledLightqss.SetBackgroundColor(Color_(ColorStyle.FullColor,20))

    def SetTempDarkqss(self):
        self._TempDarkqss.SetBorderWidth(Width=1)
        self._TempDarkqss.SetBorderStyle(Style=BorderStyle.solid)
        self._TempDarkqss.SetBorderRadius(Radius=5)
        self._TempDarkqss.SetBorderColor(Color=Color_(ColorStyle.FullThemeColor,10))
        self._TempDarkqss.SetBorderColor(ColorBottom=Color_(ColorStyle.FullThemeColor,20))
        self._TempDarkqss.SetPadding(Padding=5)
        self._TempDarkqss.Set_("outline","none")
  
    def SetNormalDarkqss(self):
        self._NormalDarkqss=self._TempDarkqss.Copy()

        self._NormalDarkqss.SetColor(Color_(ColorStyle.Light))
        self._NormalDarkqss.SetBackgroundColor(Color_(ColorStyle.FullThemeColor,0))

    def SetHoverDarkqss(self):
        self._HoverDarkqss=self._TempDarkqss.Copy()

        self._HoverDarkqss.SetColor(Color_(ColorStyle.Light))
        self._HoverDarkqss.SetBackgroundColor(Color_(ColorStyle.FullThemeColor,10))

    def SetPressDarkqss(self):
        self._PressDarkqss=self._TempDarkqss.Copy()

        self._PressDarkqss.SetColor(Color_(ColorStyle.Light))
        self._PressDarkqss.SetBackgroundColor(Color_(ColorStyle.FullThemeColor,15))
        self._PressDarkqss.SetPadding(6,5,5,6)

    def SetDisabledDarkqss(self):
        self._DisabledDarkqss=self._TempDarkqss.Copy()

        self._DisabledDarkqss.SetColor(Color_(ColorStyle.FullColor,50))
        self._DisabledDarkqss.SetBackgroundColor(Color_(ColorStyle.FullColor,20))

    def setText(self, text: str) -> None:
        super().setText(text)
        if self._text is not None:
            self.setFixedSize(QSize(self._text.GetTextWidth(),26)+QSize(21,0)+QSize(10,0))
