from PySide6.QtCore import QSize,QPoint,Qt
from PySide6.QtWidgets import QFrame,QLineEdit,QSpinBox,QApplication,QTextEdit

from typing import Union
from lib import Position,ShadowEffect
from qss import QssPlusClass,GradientColor,GradientStyle,GradientSpread,GradientColorList,ColorStyle,Color_,BorderStyle

from ..button import ButtonTransparent
from ..icon import Icon
from ..showway import Popup_


class MenuSeparate(QFrame,QssPlusClass):#分割线
    def __init__(self, *args, **kwargs):
        super(MenuSeparate, self).__init__(*args, **kwargs)
        self.setFixedHeight(3)
        self.QssApply(self,"MenuSeparate",True,False) 

    def Setqss(self):
        self.qss.SetBorderStyle(BorderStyle.solid)
        self.qss.SetBorderWidth(Width=1)
        self.qss.SetBorderColor(Color_(ColorStyle.FullColor,20))
        self.qss.SetMargin(1,7,0,7)
    
class MenuButton(ButtonTransparent):#菜单按钮
    def __init__(self,Text:str,Icon:Union[Icon|str]=None,ShortCut:str=None,IconSize:QSize=QSize(14,14),parent=None):
        super(MenuButton, self).__init__(Text=Text,parent=parent)
        #设置可聚焦
        self.SetFocusType(2)
        #设置鼠标move事件跟随
        self.setMouseTracking(True)
        self.SetIcon_(Icon,IconSize,IconSize+QSize(10,0),Position.LEFT,5)
        self.SetShortCut(ShortCut)
        self.SetTextAlignment(Qt.AlignLeft|Qt.AlignVCenter)

        self.setFixedHeight(30)
        
    def leaveEvent(self, event) -> None:
        self.clearFocus()
        return super().leaveEvent(event)

    def focusOutEvent(self, arg__1) -> None:
        if self._mouse or self._fouce:
            self._mouse=False
            self._fouce=False
            self._Colorout()
        return super().focusOutEvent(arg__1)
    
    def mouseMoveEvent(self, arg__1) -> None:
        if self._mouse==False or self._fouce==False:
            self.setFocus()
        return super().mouseMoveEvent(arg__1)

class LineEditMenu(Popup_):
    def __init__(self,LineEdit,parent=None):
        super(LineEditMenu, self).__init__(parent=parent)
        self.lineedit_=LineEdit
        self.SetWindowPopup()

        self.additems(self.CalMenu())

        self._showframe.setFixedWidth(180)
        self._showframe.layouts.setContentsMargins(2,2,2,2)
        self._showframe.layouts.setSpacing(1)

        #设置阴影
        self._shadoweffect=ShadowEffect(Color_(ColorStyle.FullColor,70,FixAlpha=100),15,QPoint(0,1))
        self._showframe.setGraphicsEffect(self._shadoweffect)

        self.setFocus()

    def __MenuClick(self,Type:int):
        if isinstance(self.lineedit_,QLineEdit):
            _widget=self.lineedit_
        elif isinstance(self.lineedit_,QSpinBox): 
            _widget=self.lineedit_.lineEdit()
        elif isinstance(self.lineedit_,QTextEdit):
            _widget=self.lineedit_
        else:
            return()
        
        if Type==1:
            _widget.undo()
        elif Type==2:
            _widget.redo()
        elif Type==3:
            _widget.copy()
        elif Type==4:
            _widget.cut()
        elif Type==5:
            _widget.paste()
        elif Type==6:
            _widget.del_()
        elif Type==7:
            _widget.selectAll()
        

        self.Close()
    
    def additem(self,item):
        self._showframe.layouts.addWidget(item)

    def additems(self,items:list):
        for item in items:
            self.additem(item)
        return len(items)

    def __parentText(self):
        if isinstance(self.lineedit_,QLineEdit):
            return self.lineedit_.text()
        elif isinstance(self.lineedit_,QSpinBox):
            return self.lineedit_.lineEdit().text()
        elif isinstance(self.lineedit_,QTextEdit):
            return self.lineedit_.toPlainText()

    def __parentSelectedText(self):
        if isinstance(self.lineedit_,QLineEdit):
            return self.lineedit_.selectedText()
        elif isinstance(self.lineedit_,QSpinBox):
            return self.lineedit_.lineEdit().selectedText()
        elif isinstance(self.lineedit_,QTextEdit):
            return self.lineedit_.textCursor().selectedText()

    def __parentUndoAvailable(self):
        if isinstance(self.lineedit_,QLineEdit):
            return self.lineedit_.isUndoAvailable()
        elif isinstance(self.lineedit_,QSpinBox):
            return self.lineedit_.lineEdit().isUndoAvailable()
        elif isinstance(self.lineedit_,QTextEdit):
            return self.lineedit_.document().isUndoAvailable()

    def __parentRedoAvailable(self):
        if isinstance(self.lineedit_,QLineEdit):
            return self.lineedit_.isRedoAvailable()
        elif isinstance(self.lineedit_,QSpinBox):
            return self.lineedit_.lineEdit().isRedoAvailable()
        elif isinstance(self.lineedit_,QTextEdit):
            return self.lineedit_.document().isRedoAvailable()

    def CalMenu(self):
        R=self.lineedit_.isReadOnly()
        C=QApplication.clipboard().mimeData().hasText()
        T=self.__parentText()
        S=self.__parentSelectedText()
        UN=self.__parentUndoAvailable()
        RE=self.__parentRedoAvailable()
        l=[]

        if R:
            if T:
                if S:
                    _copy=MenuButton("复制",Icon.copy,"Ctrl+C")
                    _copy.clicked.connect(lambda: self.__MenuClick(3))
                    _selectall=MenuButton("全选",Icon.selectall,"Ctrl+A")
                    _selectall.clicked.connect(lambda: self.__MenuClick(7))
                    l.append(_copy)
                    l.append(_selectall)
                else:  
                    _selectall=MenuButton("全选",Icon.selectall,"Ctrl+A")
                    _selectall.clicked.connect(lambda: self.__MenuClick(7))
                    l.append(_selectall)    
            else:
                return l
        else:
            if UN:
                _undo=MenuButton("撤销",Icon.undo,"Ctrl+Z")
                _undo.clicked.connect(lambda: self.__MenuClick(1))
                l.append(_undo)
            if RE:
                _redo=MenuButton("重做",Icon.redo,"Ctrl+Y")
                _redo.clicked.connect(lambda: self.__MenuClick(2))
                l.append(_redo)
            if C:
                if T:
                    if S:
                        if len(l)!=0:
                            l.append(MenuSeparate())

                        _copy=MenuButton("复制",Icon.copy,"Ctrl+C")
                        _copy.clicked.connect(lambda: self.__MenuClick(3))
                        _cut=MenuButton("剪切",Icon.cut,"Ctrl+X",)
                        _cut.clicked.connect(lambda: self.__MenuClick(4))
                        _paste=MenuButton("粘贴",Icon.paste,"Ctrl+V")
                        _paste.clicked.connect(lambda: self.__MenuClick(5))
                        _delete=MenuButton("删除",Icon.delete,"Delete")
                        _delete.clicked.connect(lambda: self.__MenuClick(6))
                        _selectall=MenuButton("全选",Icon.selectall,"Ctrl+A")
                        _selectall.clicked.connect(lambda: self.__MenuClick(7))

                        l.append(_copy)
                        l.append(_cut)
                        l.append(_paste)
                        l.append(_delete)
                        l.append(MenuSeparate())
                        l.append(_selectall)
                    else:

                        if len(l)!=0:
                            l.append(MenuSeparate())
                        _paste=MenuButton("粘贴",Icon.paste,"Ctrl+V")
                        _paste.clicked.connect(lambda: self.__MenuClick(5))
                        _selectall=MenuButton("全选",Icon.selectall,"Ctrl+A")
                        _selectall.clicked.connect(lambda: self.__MenuClick(7))

                        l.append(_paste)
                        l.append(_selectall)
                else:
                    if len(l)!=0:
                        l.append(MenuSeparate())

                    _paste=MenuButton("粘贴",Icon.paste,"Ctrl+V")
                    _paste.clicked.connect(lambda: self.__MenuClick(5))
                    l.append(_paste)

            else:
                if T:
                    if S:
                        if len(l)!=0:
                            l.append(MenuSeparate())

                        _copy=MenuButton("复制",Icon.copy,"Ctrl+C")
                        _copy.clicked.connect(lambda: self.__MenuClick(3))
                        _cut=MenuButton("剪切",Icon.cut,"Ctrl+X",)
                        _cut.clicked.connect(lambda: self.__MenuClick(4))
                        _delete=MenuButton("删除",Icon.delete,"Delete")
                        _delete.clicked.connect(lambda: self.__MenuClick(6))
                        _selectall=MenuButton("全选",Icon.selectall,"Ctrl+A")
                        _selectall.clicked.connect(lambda: self.__MenuClick(7))

                        l.append(_copy)
                        l.append(_cut)
                        l.append(_delete)
                        l.append(MenuSeparate())
                        l.append(_selectall)

                    else:
                        if len(l)!=0:
                            l.append(MenuSeparate())

                        _selectall=MenuButton("全选",Icon.selectall,"Ctrl+A")
                        _selectall.clicked.connect(lambda: self.__MenuClick(7))
                        l.append(_selectall)
                else:
                    return l
        return l

