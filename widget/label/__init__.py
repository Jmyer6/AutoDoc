
from PySide6.QtWidgets import QLabel,QSizePolicy
from PySide6.QtGui import QFontMetrics,QKeySequence,QShortcut, QShowEvent,Qt
from PySide6.QtCore import QTimer,Signal

from qss import QssPlusClass,Font_,FontSize,Color_,ColorStyle


class LabelNormal(QLabel,QssPlusClass):
    def __init__(self, *args, **kwargs):
        super(LabelNormal, self).__init__(*args, **kwargs)
        self._textCache=None

        self._elidedtext=False
        self._wraptext=True

        self.QssApply(self,"LabelNormal",True,False)
        self.SetMousePenetration(True)

        if len(args)>0:
            self.setText(args[0])

    def Setqss(self):
        self.qss.SetColor(Color_(ColorStyle.FullColor,100))
        # self.qss.SetBackgroundColor(Color_(255,0,0,255))

        self.font_=Font_(FontSize=FontSize(Shift=0,Min=10,Max=16))
        self.qss.SetFont(self.font_)
        self.qss.SetPadding(3,4,4,3)

        return super().Setqss() 
    
    def SetAlwayColor(self,Color:Color_):
        self.qss.SetColor(Color)
        self._qssplus.ApplyQss()

    def setText(self, arg__1: str) -> None:
        self._textCache=arg__1

        if self._elidedtext:
            _text=self.__ElidedText(arg__1)
        elif self._wraptext:
            _text=self.__WrapText(arg__1)
        else:
            _text=arg__1

        return super().setText(_text)
    
    def text(self) -> str:
        return self._textCache
    
    def setWrapText(self,wraptext:bool):
        '''
        是否自动换行
        '''
        self._wraptext=wraptext
        self.setText(self._textCache)

    def setElidedText(self,ElidedText:bool):
        '''
        是否省略显示
        '''
        self._elidedtext=ElidedText
        self.setText(self._textCache)
    
    def __ElidedText(self,text:str):
        _metrics = QFontMetrics(self.font())
        return _metrics.elidedText(text, Qt.ElideRight, self.width())
  
    def __WrapText(self,text:str):
        """
        手动插入换行符以使文本在指定宽度内换行。
        """
        if text == "" or text is None:
            return ""
        _metrics = QFontMetrics(self.font())
        _wrappedText = ""
        line = ""

        for char in text:
            if char == "\n":
                _wrappedText += line.rstrip() + "\n"
                line = ""
            else:
                _testLine = line + char

                if _metrics.horizontalAdvance(_testLine) > self.width()-10:
                    _wrappedText += line.rstrip() + "\n"
                    line = char
                else:
                    line = _testLine

        _wrappedText += line.rstrip()  # 添加最后一行
        return _wrappedText

    def resizeEvent(self, event):
        self.setText(self.text())
        return super().resizeEvent(event)
    
    def SetMaxWidth(self,MaxWidth:int):
        self.setMaximumWidth(MaxWidth)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def GetTextWidth(self):
        _metrics = QFontMetrics(self.font())
        return _metrics.horizontalAdvance(self._textCache)

class ShortCutLabel(LabelNormal):
    shortcutpressed=Signal()
    def __init__(self,Shortcut:str=None,parent=None):
        super().__init__(parent=parent)
        self._shortcut=None
        self.setWrapText(False)
        self.SetShortcut_(Shortcut)


    def Setqss(self):
        self.qss.SetColor(Color_(ColorStyle.FullColor,100))

        self.font_=Font_(FontSize=FontSize(Shift=-2,Min=10,Max=16))
        self.qss.SetFont(self.font_)
        self.qss.SetPadding(0,0,0,0)

    def SetShortcut_(self,Shortcut:str=None):
        '''
        设置快捷键
        
        Shortcut:快捷键字符串,格式为"Ctrl+Shift+A"
        '''

        if Shortcut==None:
            if self._shortcut!=None:
                #移除快捷键
                self._shortcut.setKey(QKeySequence())
                self._shortcut=None
                #设置控件的text
                self.setText("")
                self.hide()
        else:
            _shortcut = QKeySequence(Shortcut)
            self._shortcut = QShortcut(_shortcut, self)

            #取快捷键str文本
            _shortcuttext="" if self._shortcut==None else self._shortcut.key().toString().title()
            self.setText(_shortcuttext)
            self.adjustSize()
            self.setFixedSize(self.size())

            #绑定槽函数
            self._shortcut.activated.connect(self.shortcutpressed.emit)
            self.show()

