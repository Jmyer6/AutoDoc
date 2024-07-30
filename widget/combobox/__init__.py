from PySide6.QtCore import QSize,Signal,QPoint
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import  QCloseEvent, QHideEvent

from ..button import ButtonNormal
from ..lineedit import LineEdit
from ..icon import Icon
from ..list import TextList
from ..showway import Popup_

from qss import Color_,ColorStyle
from lib import Position,GetFontNameList,ShadowEffect

from typing import Union


class ComboboxButtonType(ButtonNormal):
    menushowed=Signal()
    def __init__(self, *args, **kwargs):
        super(ComboboxButtonType, self).__init__(*args, **kwargs)
        self.SetFocusType(3)
        self.SetClickFunciton(False)
        self.SetRightIcon(Icon.arrow2,QSize(12,12),IconAngle=180)
        self.clicked.connect(lambda: self.MenuEvent(True))

    def MenuEvent(self,open_:bool=True):
        if open_:
            self._rightIcon.RotateIcon(180,360)
            self.menushowed.emit()
        else:
            self._rightIcon.RotateIcon(0,180,False)
   
class ComboboxEditType(LineEdit):
    menushowed=Signal()
    def __init__(self, *args, **kwargs):
        super(ComboboxEditType, self).__init__(*args, **kwargs)
        self.SetRightIcon(Icon.arrow2, QSize(12, 12),180)
        self._rightIcon.clicked.connect(lambda: self.MenuEvent(True))

    def MenuEvent(self,open_:bool=True):
        if open_:
            self._rightIcon._icon.RotateIcon(180,360)
            self.menushowed.emit()
        else:
            self._rightIcon._icon.RotateIcon(0,180,False)

class ComBoBox(QWidget):
    '''   
    Type:normal普通模式/edit编辑模式/font字体模式
    '''
    def __init__(self,Type:str="normal",parent=None):
        super(ComBoBox, self).__init__(parent=parent)
        self._box=None
        self._boxtype=Type
        #弹窗
        self._menu=None

        self._listwidget=TextList(parent=self)
        self._listwidget.hided.connect(self.__PopupClose)
        self._listwidget.showed.connect(self.__PopupEvent)
        self._listwidget.checked.connect(self.ItemCheckEvent)
        self._listwidget.hide()

        self.SetItemCount()
        self.SetComboboxType()

    def Clear(self):
        self._listwidget.Clear()
        self._box.setText("")
    
    def SetItemCount(self,Count:int=7):
        self._listwidget.SetItemCount(Count)

    def SetItemHeight(self,Height:int):
        self._listwidget.SetItemHeight(Height)

    def SetComboboxType(self,ComboboxType:str=None):
        '''
        type:btn 不可编辑 edit 可编辑 font字体选择框
        '''
        #清除
        if self._box!=None:
            self._box.deleteLater()

        if ComboboxType!=None:
            self._boxtype=ComboboxType

        if self._boxtype=="normal" or self._boxtype=="font":
            self._box=ComboboxButtonType(parent=self)
        elif self._boxtype=="edit":
            self._box=ComboboxEditType(parent=self)

        self._listwidget.SetFontNameFollow(False)

        if self._boxtype=="font":
            #加载字体
            self._listwidget.SetFontNameFollow(True)
            self._listwidget.Addtexts(GetFontNameList())

        self.__SizeAdjust()
        self._box.menushowed.connect(self.__Popup)

    def setText(self,text_:str):
        self._box.setText(text_)

    def text(self):
        return self._box.text()
    
    def Addtext(self,Text:str):
        self._listwidget.Addtext(Text)

    def Addtexts(self,Texts:list[str]):
        for text in Texts:
            self.Addtext(text)

    def __SizeAdjust(self):
        self._listwidget.setFixedWidth(self.size().width())
        self._box.setFixedSize(self.size())

    def resizeEvent(self, event) -> None:
        self.__SizeAdjust()
        return super().resizeEvent(event)

    def __PopupEvent(self):
        if isinstance(self._box,ComboboxEditType):
            self.SetCheck(self._box.text())
        self._listwidget.ShowIndex()

    def hideEvent(self, event: QHideEvent) -> None:
        return super().hideEvent(event)

    def __Popup(self):   
        self._menu=Popup_()

        self._menu.SetWindowPopup()
        self._listwidget.Adjust()

        # if self._listwidget._check==None:
        #     self._listwidget._check=

        self._box.SetMenu()
        self._menu._showframe.layouts.addWidget(self._listwidget)
        self._listwidget.show()

        self._shadoweffect=ShadowEffect(Color_(ColorStyle.FullColor,70,FixAlpha=100),15,QPoint(0,1))
        self._menu._showframe.setGraphicsEffect(self._shadoweffect)

        self._menu.ExecWindowOut(self,QPoint(0,5),Position.BOTTOM_LEFT,Opacity=True,MoveMultiple=0.1,Duration=300)

        self._menu.closed.connect(self.__MenuCloseEvent)

    def __PopupClose(self):
        if self._menu!=None:
            self._menu.close()
            self._menu=None
            self._shadoweffect=None

    def SetCheck(self,Check:Union[int,str]):
        if isinstance(Check,int):
            if Check<0 or Check>=len(self._listwidget._textlist):
                self._listwidget._check=None
            else:
                self._listwidget._check=Check
        elif isinstance(Check,str):
            self._listwidget._check=None
            for i in range(0,len(self._listwidget._textlist)):
                if self._listwidget._textlist[i]==Check:
                    self._listwidget._check=i
        

        if self._listwidget._check!=None:
            if isinstance(self._box,ComboboxEditType):
                self._box.setText(self._listwidget._textlist[self._listwidget._check])
            else:
                self._box.SetText(self._listwidget._textlist[self._listwidget._check])

    def ItemCheckEvent(self,Index:int,Text:str):
        self.SetCheck(Index)
        self._box.setText(Text)
        self.__PopupClose()
    
    def __MenuCloseEvent(self):
        self._listwidget.setParent(self)
        self._listwidget.hide()
        self._box.MenuEvent(False)

    
